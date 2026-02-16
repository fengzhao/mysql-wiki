



## 数据更新流程



当我们查询数据的时候，会先去Buffer Pool中查询。如果Buffer Pool中不存在，存储引擎会先将数据从磁盘加载到Buffer Pool中，然后将数据返回给客户端；

同理，当我们更新某个数据的时候，如果这个数据不存在于Buffer Pool，同样会先数据加载进来，然后修改修改内存的数据。被修改过的数据会在之后统一刷入磁盘。



假设我们修改Buffer Pool中的数据成功，但是还没来得及将数据刷入磁盘MySQL就挂了怎么办？按照上图的逻辑，此时更新之后的数据只存在于Buffer Pool中，如果此时MySQL宕机了，这部分数据将会永久的丢失；







## redo和undo



MySQL能够实现崩溃恢复的**事实**来看，MySQL必定实现了某些骚操作。没错，这就是接下来我们要介绍的另外的两个关键功能，**Redo Log**和**Undo Log**。



这两种日志是属于InnoDB存储引擎的日志，和MySQL Server的Binlog不是一个维度的日志。

1. **Redo Log** 记录了此次事务 **「完成后」** 的数据状态，记录的是更新之 **「后」** 的值
2. **Undo Log** 记录了此次事务 **「开始前」** 的数据状态，记录的是更新之 **「前」** 的值

这两种日志有明显的区别。





更新数据还是会判断数据是否存在于Buffer Pool中，不存在则加载进来。上面我们提到了回滚的问题，在更新Buffer Pool中的数据之前，我们需要先将该数据事务开始之前的状态写入Undo Log中。假设更新到一半出错了，我们就可以通过Undo Log来回滚到事务开始前。

然后执行器会更新Buffer Pool中的数据，成功更新后会将数据最新状态写入Redo Log Buffer中。因为一个事务中可能涉及到多次读写操作，写入Buffer中分组写入，比起一条条的写入磁盘文件，效率会高很多。







### undo

undo log 是mysql中比较重要的事务日志之一undo log是一种用于撤销回退的日志。

在一个事务没提交之前，MySQL会先记录更新前的数据到 undo log日志文件里面，当[事务回滚](https://so.csdn.net/so/search?q=事务回滚&spm=1001.2101.3001.7020)时或者数据库崩溃时，可以利用 undo log来进行回退。





在MySQL中，undo log日志的作用主要有两个：



1、提供回滚操作【undo log实现事务的原子性】



在设计DB时，我们假设数据库可能在任何时刻，由于如硬件故障，软件Bug，运维操作等原因突然崩溃。

这个时候尚未完成提交的事务可能已经有部分数据写入了磁盘，如果不加处理，会违反数据库对Atomic的保证，也就是任何事务的修改要么全部提交，要么全部取消。

针对这个问题，直观的想法是等到事务真正提交时，才能允许这个事务的任何修改落盘，也就是No-Steal策略。显而易见，这种做法一方面造成很大的内存空间压力，另一方面提交时的大量随机IO会极大的影响性能。

因此，数据库实现中通常会在正常事务进行中，就不断的连续写入Undo Log，来记录本次修改之前的历史值。

当Crash真正发生时，可以在Recovery过程中通过回放Undo Log将未提交事务的修改抹掉。InnoDB采用的就是这种方式。



我们在进行数据更新操作的时候，不仅会记录redo log，还会记录undo log，如果因为某些原因导致事务回滚，那么这个时候MySQL就要执行回滚（rollback）操作，利用undo log将数据恢复到事务开始之前的状态。

例如如我们执行下面一条删除语句：

```
delete from user where id = 1;
```

那么此时undo log会记录一条对应的insert 语句【反向操作的语句】，以保证在事务回滚时，将数据还原回去。

如果这个修改出现异常，可以使用undo log日志来实现回滚操作，以保证事务的一致性。

 



2、MVCC，即多版本控制。在MySQL数据库InnoDB存储引擎中，用undo Log来实现多版本并发控制(MVCC)。当读取的某一行被其他事务锁定时，它可以从undo log中分析出该行记录以前的数据版本是怎样的，从而让用户能够读取到当前事务操作之前的数据【快照读】。



下面解释一下什么是快照读，与之对应的还有一个是---当前读。

快照读：

SQL读取的数据是快照版本【可见版本】，也就是历史版本，不用加锁，普通的SELECT就是快照读。

当前读：

SQL读取的数据是最新版本。通过锁机制来保证读取的数据无法通过其他事务进行修改UPDATE、DELETE、INSERT、SELECT … LOCK IN SHARE MODE、SELECT … FOR UPDATE都是当前读。





#### undo表空间和存储机制

所谓表空间其实是真实存在于磁盘上的数据文件。而这里的所说的 **undolog表空间** 其实就是磁盘上专门存放 undolog 的文件。

在MySQL5.5以及之前，InnoDB的undo log也是存放在 ibdata1 里面的。一旦出现大事务，这个大事务所使用的undolog占用的空间就会一直在ibdata1里面存在，即使这个事务已经关闭。



MySQL从8.0开始undo 表空间管理已经发生了改变，在5.7版本中一旦MySQL初始化以后，就不能再改变undo表空间了。

所以我们在5.7版本中都是在初始化的时候对undo表空间进行一些设置，类似这样：在my.cnf文件中加入innodb_undo_directory= /data/mysql/undologs 和 innodb_undo_tablespaces=5 这两个参数。

之所以这么改，是因为我们想把undo表空单独从系统表空间idbdata中分离出来，这样就可以消除因undo的问题造成对ibdata系统表空间的影响。

所以上面的参数配置在5.7版本中是我们对MySQL初始化做的一个常规的最佳实践设置，如果不设置，那么在5.7版本中，undo还是默认会放在ibdata中。





从MySQL8.0版本开始，MySQL默认对undo进行了分离操作，使用默认配置初始化时，就会在datadir目录下生成两个10MiB大小的undo表空间文件undo_001 和 undo002 

默认至少初始化2个Undo表空间，最大支持127个Undo表空间，默认表空间名称为undo_001，undo_002



因为大事务可能会导致单个undo文件变的很大，创建额外的表空间文件可以避免这个文件，8.0.14 之后UNDO表空间支持**在线扩缩容**

```sql
CREATE UNDO TABLESPACE tablespace_name ADD DATAFILE 'file_name.ibu';
-- 不支持指定相对路径,只支持绝对路径,且必须是innodb_directories参数定义可识别的路径或默认的数据目录下
```



- - 不支持指定相对路径,只支持绝对路径,且必须是`innodb_directories`参数定义可识别的路径或默认的数据目录下
  - 动态创建的undo表空间必须以.ibu结尾

```
# 8.0.23之前，undo初始化大小依赖于inoodb_page_size，对于默认的16KB的页，undo默认是10MiB
```







````
# 

mysql> show VARIABLES like '%undo%';
+--------------------------+------------+
| Variable_name            | Value      |
+--------------------------+------------+
| innodb_max_undo_log_size | 1073741824 |
| innodb_undo_directory    | ./         |
| innodb_undo_log_encrypt  | OFF        |
| innodb_undo_log_truncate | ON         |
| innodb_undo_tablespaces  | 2          |
+--------------------------+------------+
5 rows in set (0.01 sec)

mysql>


show variables like '%undo%';
+--------------------------+------------+
| Variable_name            | Value      |
+--------------------------+------------+
| innodb_max_undo_log_size | 8589934592 |   
| innodb_undo_directory    | ./         |  
| innodb_undo_log_encrypt  | OFF        |
| innodb_undo_log_truncate | ON         |
| innodb_undo_tablespaces  | 2          |
+--------------------------+------------+

show variables like '%truncate%';
+--------------------------------------+-------+
| Variable_name                        | Value |
+--------------------------------------+-------+
| innodb_purge_rseg_truncate_frequency | 128   |
| innodb_undo_log_truncate             | ON    |
+--------------------------------------+-------+

show variables like '%segment%';
+-------------------------------+-----------+
| Variable_name                 | Value     |
+-------------------------------+-----------+
| innodb_rollback_segments      | 128       |
| innodb_segment_reserve_factor | 12.500000 |
+-------------------------------+-----------+

innodb_undo_log_truncate	--控制是否自动做UNDO的truncate收缩操作，默认为ON，只有为ON时，下面2个参数才生效
innodb_max_undo_log_size	--控制UNDO做truncate收缩操作的阈值,当UNDO达到该值时才出发收缩操作
innodb_purge_rseg_truncate_frequency 
		-- Batch UNDO清理的次数,默认最大值128,也就是128次后才会触发一次UNDO的truncate,而每次清理的undo page由innodb_purge_batch_size参数决定,innodb_purge_batch_size默认为300,也就是300*128个UNDO小批次清理后才会触发UNDO表空间的truncate(也就是UNDO表空间的收缩)操作

innodb_undo_tablespaces
-- 控制生成的UNDO表空间的数量,默认2个,在8.0对该参数做了废弃,但并未提供其他参数控制UNDO数量,当前依旧可以使用该参数做UNDO表空间数量配置,通常建议配置为3(手工收缩UNDO时需要至少3个UNDO表空间)

innodb_rollback_segments			-- UNDO表空间回滚段的数量,默认为最大值128
````





#### UNDO 表空间运维



```sql
-- 可以查看到undo的表空间名称/文件路径/初始大小/扩展大小/磁盘文件大小/可用空间及是否启用的状态等
SELECT T1.SPACE AS SPACE_ID,
       T1.NAME AS TABLESPACE_NAME,
       T2.FILE_NAME,
       ROUND(T2.INITIAL_SIZE / 1024 / 1024, 2) AS "INITIAL_SIZE(M)",
       ROUND(T2.AUTOEXTEND_SIZE / 1024 / 1024, 2) AS "AUTOEXTEND_SIZE(M)",
       ROUND(T1.FILE_SIZE / 1024 / 1024, 2) AS "FILE_SIZE_DISK(M)",
       ROUND(T2.DATA_FREE / 1024 / 1024, 2) AS "DATA_FREE(M)",
       T2.STATUS,
       T1.STATE
  FROM INFORMATION_SCHEMA.INNODB_TABLESPACES T1,
       INFORMATION_SCHEMA.FILES              T2
 WHERE T1.SPACE = T2.FILE_ID
   AND T1.ROW_FORMAT = 'Undo';
   
   
   
   
   
-- 创建一个新的UNDO表空间
CREATE UNDO TABLESPACE undo_004 ADD DATAFILE 'undo_004.ibu';

-- 可以用前面的命令查看创建后的状态

-- 可以将已有的UNDO表示为inactive(也可理解为UNDO表空间收缩)
-- PS:设置为INACTIVE的表空间的STATE为empty,表示这个表空间不包含任何事务回滚数据,且表空间也收缩为默认大小
ALTER UNDO TABLESPACE undo_003 SET INACTIVE;

-- 可以将inactive的UNDO转为active
ALTER UNDO TABLESPACE innodb_undo_001 SET ACTIVE;

-- 可以将inactive的UNDO表空间进行删除
-- PS:默认以innodb_开头初始化的undo表空间不可被删除
DROP UNDO TABLESPACE innodb_undo_001;
ERROR: 3119 (42000): InnoDB: Tablespace names starting with `innodb_` are reserved.

-- 非系统默认的UNDO在inactive后可被删除
ALTER UNDO TABLESPACE undo_003 SET ACTIVE;
Query OK, 0 rows affected (0.0030 sec)




```



#### 影响UNDO inactive(truncate)性能的因素

- UNDO 表空间的大小
- UNDO 表空间的数量
- UNDO LOGS的数量(实际INSERT/UPDATE/DELETE这类事务回滚段的数据量)
- 磁盘IO的能力/当前系统的负载
- 是否存在长事务在使用该UNDO表空间

PS:通常对表空间做收缩前最简单避免性能的方式是提前创建一个UNDO表空间,收缩完后再删除或一直保留均可