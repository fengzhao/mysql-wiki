# MySQL是如何打开和关闭表的？

MySQL是多线程的，可能在同一时刻有很多的客户端访问某张特定的表。为了能最小化多个客户端在相同表上的不同状态问题，并发会话中访问的每张表都会单独打开。虽然这可能消耗过多的内存，但是通常会提高系统的性能。


我们知道mysql是一个支持多线程的数据库，尤其在innodb存储引擎出现后，对mysql的事务，并发，锁支持得到了极大提高。

在高并发的访问的应用场景中，应用端大量并发的进程发问数据库，而数据库中的数据表在磁盘上以数据文件存放，在unix，linux的系统调用中，是依赖于文件描述符的。

不同的os对文件描述符的限制不同（非Unix/linux 操作系统无文件描述符概念，在windows中称作文件句柄），如在linux中/etc/security/limits.conf配置文件中设置他们的文件描述符极限。


## 数据字典

数据字典是数据库重要的组成部分之一，那么什么是数据字典？数据字典包含哪些内容呢？数据字典是对数据库中的数据、库对象、表对象等的元信息的集合。

在MySQL中，数据字典信息内容就包括表结构、数据库名或表名、字段的数据类型、视图、索引、表字段信息、存储过程、触发器等内容。

`MySQL.INFORMATION_SCHEMA` 库提供了对数据局元数据、统计信息、以及有关MySQL server的访问信息（例如：数据库名或表名，字段的数据类型和访问权限等）。

**该库中保存的信息也可以称为MySQL的数据字典。**

在MySQL8.0之前，MySQL的数据字典信息并没有全部存放在系统数据库表中，部分字典信息存放于文件中，其余的数据字典信息存放于数据字典库中（INFORMATION_SCHEMA,MYSQL,SYS）。


> 在MySQL8.0之前，如果我们使用了默认的存储引擎innodb创建一张表，那么在文件夹下面就会出现表名.frm和表名.ibd两个文件，如果我们使用的是Myisam存储引擎，那么就会出现三个文件。其中ibd文件是innodb的表数据文件，而frm文件是innodb的表结构文件，mysiam存储引擎的表中，frm是表结构，MYI文件是索引文件，而MYD文件是数据文件，从这里也可以看出，innodb存储引擎的索引和数据是在一起的，而Myisam存储引擎索引和数据是分开的。 **注意：这个frm文件和ibd文件不是文本文件，都是不能直接用编辑器打开的。** 早期，5.6版本之前，MyISAM是MySQL的默认存储引擎，而作为MyISAM存储引擎，它是没有数据字典的。只有表结构信息记录在.frm文件中。MySQL5.6版本之后，将InnoDB存储引擎作为默认的存储引擎。在InnoDB存储引擎中，添加了一些数据字典文件用于存放数据字典元信息，例如：.opt文件，记录了每个库的一些基本信息，包括库的字符集等信息，.TRN，.TRG文件用于存放触发器的信息内容。


最新的MySQL 8.0 发布之后，对数据库数据字典方面做了较大的改进。

- 首先是，将所有原先存放于数据字典文件中的信息，全部存放到数据库系统表中，即将之前版本的.frm,.opt,.par,.TRN,.TRG,.isl文件都移除了，不再通过文件的方式存储数据字典信息。

- 其次是对INFORMATION_SCHEM，mysql，sys系统库中的存储引擎做了改进，原先使用MyISAM存储引擎的数据字典表都改为使用InnoDB存储引擎存放。从不支持事务的MyISAM存储引擎转变到支持事务的InnoDB存储引擎，为原子DDL的实现，提供了可能性。


https://opensource.actionsky.com/20200709-mysql/



**table cache的主要作用应该用于缓存文件描述符，当有新的请求时不需要重新的打开，使用结束时也不用立即关闭。**


