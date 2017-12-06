# Fixtures

## 写在前面

**Fixtures**，个人翻译为固件。ps：我知道是很low，但重点不在这，ok？个人理解为，`fixtures`就是一个**可靠且可以重复使用的部件**，它的作用与平常我们写在`Unittest`中的`setup`/`teardown`方法类似，不过它有以下特点：

* 固件有它自己（明确）的名字，而且可以显式地被其他测试函数/方法/类/模块调用
* 固件是可以组合起来使用的，任意固件都可以调用其他固件
* 可以通过设置固件的参数，和测试的参数，在其他地方复用这些固件

值得一提的是，`pytest`能够兼容标准的测试框架，所以都是可以混着用的。

## 将固件作为函数参数

```python
# content of ./test_smtpsimple.py
import pytest

@pytest.fixture
def smtp():
    import smtplib
    return smtplib.SMTP("smtp.gmail.com", 587, timeout=5)

def test_ehlo(smtp):
    response, msg = smtp.ehlo()
    assert response == 250
    assert 0 # for demo purposes
```

这个例子很好地说明了固件的常见用法：先用`pytest.fixture`装饰器将一个函数包装成固件，然后将固件作为一个参数传给测试用例，身为固件的那个函数会在被引用的时候调用（生成实例对象）。这种感觉就像是在写传统测试框架时，在`setup`的时候，定义了某个属性，接着再在后面调用这个属性，或者是说定义了一个方法来给测试用例调用，那么为什么要用固件呢，个人理解它的其中一个优点就是这个固件它不是那个测试框架的私有属性/方法，也就是说这个固件具有可复用性。

### conftest.py

可以将一些通用的固件放在`conftest.py`这个文件里，而不需要我们手动导入，框架会在测试的时候按

```Flowchart 
graph LR;
Test Clss-->Test Modules;
Test Modules-->conftest.py;
conftest.py-->builtin/third party;
```

这个顺序去找固件。

也是可以通过固件来载入某些数据，方便测试调用。

## Scope

可以通过设置`pytest.fixture`的`scope`参数来让固件在不同的层面生效。如将一个固件放到`conftest.py`中，或者将其设置为`scope="module"`，则在运行模块中的其他测试用例时，可以直接调用这个固件，设置为`session`则是所有都可以调用。

## finalization/executing teardown code

前面讲了固件很像我们在`setup`/`teardown`里面做的事情，那么固件是如何实现类似事后清理的功能呢，答案是用`yield`。

```python
@pytest.fixture(scope="module")
def smtp():
    smtp = smtplib.SMTP("smtp.gmail.com", 587, timeout=5)
    yield smtp  # provide the fixture value
    print("teardown smtp")
    smtp.close()
```

就像这个例子中的，每次调用固件，都会通过`yield`来返回值，然后在模块中的所有测试完成后再调用`yield`语句后面的语句。

当然也是可以用上下文管理器来实现这个功能

```python
@pytest.fixture(scope="module")
def smtp():
    with smtplib.SMTP("smtp.gmail.com", 587, timeout=5) as smtp:
        yield smtp  # provide the fixture value
```

在最后的时候会调用`__exit__`的方法。

要注意的是，如果异常在`yield`语句之前被抛出，则`yield`后面的语句不会执行，也就是类似传统中的，如果`setup`失败了，`teardown`也不会被调用。

除了用`yield`之外，也可以通过传递`request-context`这个对象来用`addfinalizer`注册函数执行cleanup。（这个对象后面会讲）

```python
@pytest.fixture(scope="module")
def smtp(request):
    smtp = smtplib.SMTP("smtp.gmail.com", 587, timeout=5)
    def fin():
        print ("teardown smtp")
        smtp.close()
    request.addfinalizer(fin)
    return smtp  # provide the fixture value
```

`addfinalizer`有两个地方不同于`yield`：

* 可以多次调用来注册多个函数
* 就算`setup`的函数抛出异常，这里注册的函数也还是会被调用

当然，如果异常在注册函数之前被抛出，那就肯定不会执行啦。

##固件能够自省测试上下文

```python
@pytest.fixture(scope="module")
def smtp(request):
    server = getattr(request.module, "smtpserver", "smtp.gmail.com")
    smtp = smtplib.SMTP(server, 587, timeout=5)
    yield smtp
    print ("finalizing %s (%s)" % (smtp, server))
    smtp.close()

```

固件函数会被传入一个上下文对象，就是上面讲到的`request-context`，可以通过这个上下文来实现固件与测试用例之间的交互。

## 参数化固件

```python
@pytest.fixture(scope="module",
                params=["smtp.gmail.com", "mail.python.org"])
def smtp(request):
    smtp = smtplib.SMTP(request.param, 587, timeout=5)
    yield smtp
    print ("finalizing %s" % smtp)
    smtp.close()
```

通过设置`params`参数，可以在测试用例中使用不同的参数，这个`param`是通过上面讲到的`request-context`来传递的。

要在运行结果中看到不同参数的固件的用例表示，可以设置`ids`，然后在运行时加上`--collect=only`选项就可以看到了。

```python
# content of test_ids.py
import pytest

@pytest.fixture(params=[0, 1], ids=["spam", "ham"])
def a(request):
    return request.param

def test_a(a):
    pass

def idfn(fixture_value):
    if fixture_value == 0:
        return "eggs"
    else:
        return None

@pytest.fixture(params=[0, 1], ids=idfn)
def b(request):
    return request.param

def test_b(b):
    pass
```

可以得到以下结果

```
$ pytest --collect-only
=========================== test session starts ============================
platform linux -- Python 3.x.y, pytest-3.x.y, py-1.x.y, pluggy-0.x.y
rootdir: $REGENDOC_TMPDIR, inifile:
collected 10 items
<Module 'test_anothersmtp.py'>
  <Function 'test_showhelo[smtp.gmail.com]'>
  <Function 'test_showhelo[mail.python.org]'>
<Module 'test_ids.py'>
  <Function 'test_a[spam]'>
  <Function 'test_a[ham]'>
  <Function 'test_b[eggs]'>
  <Function 'test_b[1]'>
<Module 'test_module.py'>
  <Function 'test_ehlo[smtp.gmail.com]'>
  <Function 'test_noop[smtp.gmail.com]'>
  <Function 'test_ehlo[mail.python.org]'>
  <Function 'test_noop[mail.python.org]'>

======================= no tests ran in 0.12 seconds =======================
```

## 固件间互相引用

```python
class App(object):
    def __init__(self, smtp):
        self.smtp = smtp

@pytest.fixture(scope="module")
def app(smtp):
    return App(smtp)

def test_smtp_exists(app):
    assert app.smtp
```

需要注意的是固件所指定的范围（`scope`的值），更高级的可以使用低级的，但低级的不可以调用高级的。

## 固件命名空间对执行顺序的影响

最底层的（也就是`scope=function`）可以说是完全独立的，然后每高一层，都会对下层有影响，这么讲有点蠢，我觉得可以用树来表示这个过程

```
	    root
  /    /     \     \
fun1  fun2  mod1  mod2
          /     \
     fun1-mod1  fun2-mod1
```

执行过程类似这样，mod1的`teardown`会在执行完`fun2-mod1`后才被调用。

## 不显式调用固件

```python
@pytest.mark.usefixtures("cleandir")
class TestDirectoryInit(object):
    def test_cwd_starts_empty(self):
        assert os.listdir(os.getcwd()) == []
        with open("myfile", "w") as f:
            f.write("hello")

    def test_cwd_again_starts_empty(self):
        assert os.listdir(os.getcwd()) == []
```

就类似这样（固件被放在`conftest.py`中），这个`pytest.mark.usefixtures`装饰器的作用就相当于在每个类方法中都调用了固件。

文档中提到常见用法是通过直接声明来用`pytestmark=pytest.mark.usefixtures('func_name')`，这里是可以一次传入多个固件的。

## Autouse

个人感觉这个`autouse`的功能与上面讲的`usefixtures`装饰器有点类似，先看一下文档的例子

```python
import pytest

class DB(object):
    def __init__(self):
        self.intransaction = []
    def begin(self, name):
        self.intransaction.append(name)
    def rollback(self):
        self.intransaction.pop()

@pytest.fixture(scope="module")
def db():
    return DB()

class TestClass(object):
    @pytest.fixture(autouse=True)
    def transact(self, request, db):
        db.begin(request.function.__name__)
        yield
        db.rollback()

    def test_method1(self, db):
        assert db.intransaction == ["test_method1"]

    def test_method2(self, db):
        assert db.intransaction == ["test_method2"]
```

显而易见，`db`函数是一个固件，然后测试类中的`transact`方法也作为一个固件，因为它设置了`autouse=True`，所以在测试的时候，这个测试类里的测试用例会自动调用这个方法，而不需要我们显式地调用它。

以下是`scope`对自启动固件`autouse=True`的一些影响：

* 如果`scope='session'`，不管这个自启动固件在哪里被定义，它只会运行一次；如果`scope='class'`，则自启动固件只会在每个测试类中运行一次。
* 如果自启动固件定义在module层面，则这个module内的测试用例都会运行它。
* 如果自启动固件定义在`conftest.py`中，则这个测试框架下的所有测试用例都会运行它。
* 如果自启动固件定义在插件中，则所有安装了这个插件的都会自动运行这个固件。

## 在不同的层面重载固件

### 在文件夹（`conftest.py`）层面

```python
tests/
    __init__.py

    conftest.py
        # content of tests/conftest.py
        import pytest

        @pytest.fixture
        def username():
            return 'username'

    test_something.py
        # content of tests/test_something.py
        def test_username(username):
            assert username == 'username'

    subfolder/
        __init__.py

        conftest.py
            # content of tests/subfolder/conftest.py
            import pytest

            @pytest.fixture
            def username(username):
                return 'overridden-' + username

        test_something.py
            # content of tests/subfolder/test_something.py
            def test_username(username):
                assert username == 'overridden-username'

```

直接同名覆盖就行了，而且还能直接用上一层的固件。

module层面也类似这样。

### 通过参数装饰器直接重载

```python
tests/
    __init__.py

    conftest.py
        # content of tests/conftest.py
        import pytest

        @pytest.fixture
        def username():
            return 'username'

        @pytest.fixture
        def other_username(username):
            return 'other-' + username

    test_something.py
        # content of tests/test_something.py
        import pytest

        @pytest.mark.parametrize('username', ['directly-overridden-username'])
        def test_username(username):
            assert username == 'directly-overridden-username'

        @pytest.mark.parametrize('username', ['directly-overridden-username-other'])
        def test_username_other(other_username):
            assert other_username == 'other-directly-overridden-username-other'
```

在上面这个例子中，固件的返回值被装饰器中的值直接覆盖掉了。