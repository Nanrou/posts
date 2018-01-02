##为什么要用Future

普通的多进程/多线程都是传统的生产者/消费者模式，生产者并不关心消费者所产生的结果，就类似

```python
tasks = [Thread(target=task, args=a) for a in a_list]
for task in tasks:
    task.start()
for task in tasks:
    task.join()
```

这样，派生出来启动，然后阻塞至完成就完事了。

那么现在有新的需求，需要实时拿到任务的状态和返回值（不能是阻塞主进程直到全部任务完成），该怎么办呢？答案是用Future类，流畅的python这本书中将这个翻译为期物，我们可能将任务包装成期物，然后通过期物来拿到想要的东西，如任务当前的状态（是否已经完成），任务的返回值（这个操作会阻塞至任务完成）。

好了，现在知道期物的作用了，那我们现在看看怎么用起来：一般情况下

```python
pool = ProcessPoolExecutor(max_workers=3)  # 创建进程池
future = pool.submit(task, ("hello"))  # 单个添加，往进程池里面加入一个task
print(future.done())  # 判断task是否结束
print(future.result())  # 查看task返回的结果 

pool.map(task, args_list)  # 多个添加，这个map和标准的map使用方法一致
```

##源码分析

初始化部分`__init__`

```python
class ProcessPoolExecutor(_base.Executor):
   def __init__(self, max_workers=None):
       """Initializes a new ProcessPoolExecutor instance.

       Args:
           max_workers: The maximum number of processes that can be used to
               execute the given calls. If None or not given then as many
               worker processes will be created as the machine has processors.
       """
       _check_system_limits()

       if max_workers is None:
           self._max_workers = os.cpu_count() or 1
       else:
           if max_workers <= 0:
               raise ValueError("max_workers must be greater than 0")

           self._max_workers = max_workers

       # Make the call queue slightly larger than the number of processes to
       # prevent the worker processes from idling. But don't make it too big
       # because futures in the call queue cannot be cancelled.
       self._call_queue = multiprocessing.Queue(self._max_workers +
                                                EXTRA_QUEUED_CALLS)
       # Killed worker processes can produce spurious "broken pipe"
       # tracebacks in the queue's own worker thread. But we detect killed
       # processes anyway, so silence the tracebacks.
       self._call_queue._ignore_epipe = True
       self._result_queue = SimpleQueue()
       self._work_ids = queue.Queue()
       self._queue_management_thread = None
       # Map of pids to processes
       self._processes = {}

       # Shutdown is a two-step process.
       self._shutdown_thread = False
       self._shutdown_lock = threading.Lock()
       self._broken = False
       self._queue_count = 0
       self._pending_work_items = {}
```

注意`call_queue`，`result_queue`和`pending_work_items`这几个属性，后面有关任务的调度都是通过这几个结构进行的。

从入口开始看`submit`

```python
def submit(self, fn, *args, **kwargs):
   with self._shutdown_lock:
       if self._broken:
           raise BrokenProcessPool('A child process terminated '
               'abruptly, the process pool is not usable anymore')
       if self._shutdown_thread:
           raise RuntimeError('cannot schedule new futures after shutdown')
       f = _base.Future()
       w = _WorkItem(f, fn, args, kwargs)
       self._pending_work_items[self._queue_count] = w
       self._work_ids.put(self._queue_count)
       self._queue_count += 1
       # Wake up queue management thread
       self._result_queue.put(None)
       self._start_queue_management_thread()
       return f
```

先看输入和输出，输入就是要执行的函数和它的参数，输出是一个Future的实例。那submit这个方法具体做了什么呢，大概是将一个Future实例和任务包装成WorkItem，然后将这个工作件放到`pending_work_items`中去，启动`start_queue_managerment_thread`来管理这些线程。

`_start_queue_management_thread`

```python
def _start_queue_management_thread(self):
   # When the executor gets lost, the weakref callback will wake up
   # the queue management thread.
   def weakref_cb(_, q=self._result_queue):
       q.put(None)

   if self._queue_management_thread is None:
       # Start the processes so that their sentinels are known.
       self._adjust_process_count()
       self._queue_management_thread = threading.Thread(
           target=_queue_management_worker,
           args=(weakref.ref(self, weakref_cb),
                 self._processes,
                 self._pending_work_items,
                 self._work_ids,
                 self._call_queue,
                 self._result_queue))
       self._queue_management_thread.daemon = True
       self._queue_management_thread.start()
       _threads_queues[self._queue_management_thread] = self._result_queue
```

这个方法主要就是派生一个守护线程来执行`queue_management_worker`

```python
def _queue_management_worker(executor_reference,
                            processes,
                            pending_work_items,
                            work_ids_queue,
                            call_queue,
                            result_queue):
   """Manages the communication between this process and the worker processes.

   This function is run in a local thread.

       executor_reference: A weakref.ref to the ProcessPoolExecutor that owns
   Args:
       process: A list of the multiprocessing.Process instances used as
           this thread. Used to determine if the ProcessPoolExecutor has been
           garbage collected and that this function can exit.
           workers.
       pending_work_items: A dict mapping work ids to _WorkItems e.g.
           {5: <_WorkItem...>, 6: <_WorkItem...>, ...}
       work_ids_queue: A queue.Queue of work ids e.g. Queue([5, 6, ...]).
       call_queue: A multiprocessing.Queue that will be filled with _CallItems
           derived from _WorkItems for processing by the process workers.
       result_queue: A multiprocessing.Queue of _ResultItems generated by the
           process workers.
   """
   executor = None

   def shutting_down():
       return _shutdown or executor is None or executor._shutdown_thread

   def shutdown_worker():
       # This is an upper bound
       nb_children_alive = sum(p.is_alive() for p in processes.values())
       for i in range(0, nb_children_alive):
           call_queue.put_nowait(None)
       # Release the queue's resources as soon as possible.
       call_queue.close()
       # If .join() is not called on the created processes then
       # some multiprocessing.Queue methods may deadlock on Mac OS X.
       for p in processes.values():
           p.join()

   reader = result_queue._reader

   while True:
       _add_call_item_to_queue(pending_work_items,
                               work_ids_queue,
                               call_queue)

       sentinels = [p.sentinel for p in processes.values()]
       assert sentinels
       ready = wait([reader] + sentinels)
       if reader in ready:
           result_item = reader.recv()
       else:
           # Mark the process pool broken so that submits fail right now.
           executor = executor_reference()
           if executor is not None:
               executor._broken = True
               executor._shutdown_thread = True
               executor = None
           # All futures in flight must be marked failed
           for work_id, work_item in pending_work_items.items():
               work_item.future.set_exception(
                   BrokenProcessPool(
                       "A process in the process pool was "
                       "terminated abruptly while the future was "
                       "running or pending."
                   ))
               # Delete references to object. See issue16284
               del work_item
           pending_work_items.clear()
           # Terminate remaining workers forcibly: the queues or their
           # locks may be in a dirty state and block forever.
           for p in processes.values():
               p.terminate()
           shutdown_worker()
           return
       if isinstance(result_item, int):
           # Clean shutdown of a worker using its PID
           # (avoids marking the executor broken)
           assert shutting_down()
           p = processes.pop(result_item)
           p.join()
           if not processes:
               shutdown_worker()
               return
       elif result_item is not None:
           work_item = pending_work_items.pop(result_item.work_id, None)
           # work_item can be None if another process terminated (see above)
           if work_item is not None:
               if result_item.exception:
                   work_item.future.set_exception(result_item.exception)
               else:
                   work_item.future.set_result(result_item.result)
               # Delete references to object. See issue16284
               del work_item
       # Check whether we should start shutting down.
       executor = executor_reference()
       # No more work items can be added if:
       #   - The interpreter is shutting down OR
       #   - The executor that owns this worker has been collected OR
       #   - The executor that owns this worker has been shutdown.
       if shutting_down():
           try:
               # Since no new work items can be added, it is safe to shutdown
               # this thread if there are no pending work items.
               if not pending_work_items:
                   shutdown_worker()
                   return
           except Full:
               # This is not a problem: we will eventually be woken up (in
               # result_queue.get()) and be able to send a sentinel again.
               pass
       executor = None
```

这个方法最主要的目的就是将`result_queue`中的返回绑定到对应的future实例上去，这个实例就是`sumbit`最终返回的。

（未完待续）