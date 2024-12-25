# 外部表

FDW (foreign-data wrapper，外部数据包装器)，PostgreSQL FDW 是一种外部访问接口，它可以被用来访问存储在外部的数据，这些数据可以是外部的pg数据库，也可以oracle、mysql等数据库，甚至可以是文件。该模块提供的功能与旧dblink模块的功能基本重叠。

但是postgres_fdw为访问远程表提供了更透明和符合标准的语法，并且在许多情况下可以提供更好的性能。而PostgreSQL内置sharding 也将是基于postgres_fdw实现。

2003 年，SQL/MED（SQL Management of External Data）被加入 SQL 标准，其为外部数据管理提供了规范。在 2011 年发行的 PostgreSQL 9.1 开始支持外部数据读，2013 发行的 PostgreSQL 9.3 开始支持外部数据写。

目前，PostgreSQL 14已提供多种扩展来支持对各种类型外部数据库或文件的操作（如 postgres_fdw 支持连接外部 PostgreSQL 数据库，oracle_fdw 支持连接外部 Oracle 数据库，mysql_fdw 支持连接外部 MySQL 数据库，jdbc_fdw 支持以 JDBC 协议连接外部常用关系型数据库，file_fdw 支持连接外部特定格式的文件等）。file_fdw插件为PG数据库提供了访问外部数据的能力，比如我们常见的文件csv,log等，该插件是内置在PG源码的contrib中。

使用postgres_fdw产要有以下步骤：

- 创建扩展
- 创建服务
- 创建用户映射
- 创建与访问表对应的外表

到此就可以使用SELECT从外部表中访问存储在其底层远程表中的数据。同时可以 UPDATE,INSERT,DELETE远程表数据库，前提是在用户映射中指定的远程用户必须具有执行这些操作的权限。

本文仅关注 postgres_fdw，即 PostgreSQL 数据库如何与外部 PostgreSQL 数据库进行连接以及其如何对外部数据进行管理。


使用 superuser 在远程 PostgreSQL 数据库执行如下语句创建普通用户fdw_user，供后面本地数据库建立 FDW 连接时使用。
```SQL
CREATE USER fdw_user WITH ENCRYPTED PASSWORD 'secret';
```


在远程数据库创建用于测试的天气表weather，插入测试数据，并为用户fdw_user授权针对该表的增删改查权限。

```SQL
CREATE TABLE weather (
    city        varchar(80),  -- city name (城市名)
    temp_low    int,          -- low temperature (最低温度)
    temp_high   int,          -- high temperature (最高温度)
    prcp        real,         -- precipitation (降水量)
    date        date          -- date (日期)
);

INSERT INTO weather (city, temp_low, temp_high, prcp, date)
    VALUES ('Beijing', 18, 32, 0.25, '2021-05-19'),
          ('Beijing', 20, 30, 0.0, '2021-05-20'),
          ('Dalian', 16, 24, 0.0, '2021-05-21');
```