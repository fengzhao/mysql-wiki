# 快速导入数据

MySQL支持使用`LOAD DATA LOCAL INFILE`语句，即可将客户端本地的文件中的数据INSERT到MySQL的某张表中。
注意，还有个`LOAD DATA INFILE`语句，这是加载服务端的文件而非客户端的。

这条命令设计就是为了快速导入。文件格式类似CSV，可以手动指定分隔符等等。详细用法请参考文档。



`LOAD DATA LOCAL INFILE`的工作过程大致如下：
1.用户在客户端输入：load data local file “/data.txt” into table test；
2.客户端->服务端：我想把我本地的/data.txt文件插入到test表中；
3.服务端->客户端：把你本地的/data.txt文件发给我；
4.客户端->服务端：/data.txt文件的内容；


```SQL
-- 逻辑导出可以使用 mysqldump或select ... into outfile 语句，然后使用 mysqlimport 或 load data 等语句来导入数据
--  优点：恢复速度非常快，比insert的插入速度快很多，根据官网文档，说是快20倍。
-- 缺点：只能备份表数据，并不能包含表结构；如果表被drop，是无法恢复数据的。（只是select ... into outfile）

-- select into outfile 导出表
select col1， col2 from table-name into outfile  '/path/备份文件名称'

-- 将tt表数据备份到tmp目录下的tt.sql文件(如果tt.sql文件存在，会报错文件已经存在)
select * from tt into outfile '/tmp/tt.sql';

-- 导入数据
LOAD DATA INFILE '/path/备份文件' into table database.tt


-- 将tmp下的tt.sql文件恢复到tt表
load data infile '/tmp/tt.sql' into table db.tt

-- load data与insert速度对比
-- 以插入10万条数据为例，load data需要大概1.4s，insert大概需要12.2s，大概是insert的12倍。


```


为什么是最快的？
- 不需要解析SQL，省CPU省内存。
- 服务器是按一个大块来读取文件的(Big block,应该是read buffer里的block,目前权当字面意义。也可能是把I/O单位弄的很大节约I/O, 批量处理。)
- 会自动禁用索引(UNIQUE除外)
- 引擎会先缓存行再写入一个大块(MyISAM，Aria支持)
- 对于空表，像Aria这样的事务引擎会停止log插入事务。毕竟回滚操作直接删表就行。


## 插入速度优化原理


## 表空间传输

在MySQL 5.6.6版本中引入了一种基于表空间快速迁移的功能（类似Oracle TTS），我们可以直接将表空间复制到另一台服务器数据库中。这对于大表来说是一个非常有用的方法。可传输表空间机制比任何其他导出和导入表的方法都快，因为只需要使用传统的 Linux 命令（cp、scp、rsync）将数据文件复制到目标位置即可。

InnoDB中支持`Transportable Tablespace`功能。也就是表空间可以从一个实例迁移到另一个实例。相比mysqldump来进行导入导出而言，速度更快，而且使用也很便捷。



表空间的导出（export）。在源实例中，执行`FLUSH TABLES t FOR EXPORT`。首先对表上排他锁，即停读写。

其次，停purge线程；最后写脏页并从缓冲区清除。到此文件可以拷贝了。注意，这里停了purge线程，所以在表空间文件中会有未被purge的记录存在。