# 概述

什么是条件索引呢？条件索引就是在索引列上根据WHERE条件进行一定的过滤后产生的索引。 这样的索引有以下优势：

- 第一点， 比基于这个列的全部索引占用空间来的小。
- 第二点， 特别是基于`FULL INDEX SCAN`的时候，占用空间小的索引对内存占用也小很多。

PostgreSQL,SQLServer 等都支持条件索引，所以我们先来看下条件索引的实际情况。

参考[官网](http://www.postgres.cn/docs/14/indexes-partial.html)


用数据库存网站访问日志，包括访客IP和URL等，大部分访客IP来自局域网，少数来自互联网。如果主要通过IP搜索来自于外部的访问，那就没有必要索引对应于我们组织内网的IP范围。

```SQL
CREATE TABLE access_log (
    url_path varchar,
    client_ip inet,
    acess_time date
);



CREATE INDEX access_log_client_ip_ix ON access_log (client_ip)
WHERE NOT (client_ip > inet '192.168.100.0' AND client_ip < inet '192.168.100.255');

-- 这个查询可以被部分索引覆盖
SELECT *
FROM access_log
WHERE url = '/index.html' AND client_ip = inet '212.78.10.32';
```



**如果我们有一个表包含已上账和未上账的订单，其中未上账的订单在整个表中占据一小部分且它们是最经常被访问的行。我们可以通过只在未上账的行上创建一个索引来提高性能。**