## like

用在**where**的条件中，直接使用类似=号的作用

like + %，这个%代表任意字符，类似*

## group by

这个语句用来根据某列的值进行分组，然后对分组的数据进行sum，avg，count之类的操作。

### with rollup

在分组统计的基础上再做一次汇总统计，然后用coalesce来给键赋值。

## join

联表查询，用on来代替where的作用

A join B ，A是左表，B是右表，默认是取交集，left join的话就是左表的全部元素，右表没对应的则为null

## 事务

仅Innodb支持

- **原子性：**一组事务，要么成功；要么撤回。
- **稳定性 ：**有非法数据（外键约束之类），事务撤回。
- **隔离性：**事务独立运行。一个事务处理后的结果，影响了其他事务，那么其他事务会撤回。事务的100%隔离，需要牺牲速度。
- **可靠性：**软、硬件崩溃后，InnoDB数据表驱动会利用日志文件重构修改。

可靠性和高速度不可兼得， innodb_flush_log_at_trx_commit 选项 决定什么时候把事务保存到日志里。

显式地用begin关键字来启用事务，然后进行操作，最后用rollback或者commit来提交。

或者设置全局变量 set autocommit

## 防止重复

双主键 PRIMARY KEY 或者 唯一 UNIQUE

## 去重关键字

DISTINCT

## HAVING

WHERE 关键字无法与合计函数一起使用，所以having来实现where相应的功能