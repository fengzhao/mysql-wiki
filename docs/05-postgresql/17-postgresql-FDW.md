在2003年，SQL标准引入了一项访问远程数据的规范，称为SQL外部数据管理（SQL/MED），自9.1版本（于2011年9月发布）起，PostgreSQL便开始开发各项功能以支持SQL/MED标准。

2003 年，SQL/MED（SQL Management of External Data）被加入 SQL 标准，其为外部数据管理提供了规范。

在 2011 年发行的 PostgreSQL 9.1 开始支持外部数据读，2013 发行的 PostgreSQL 9.3 开始支持外部数据写。

目前，PostgreSQL （本文写作时，使用的版本为 PostgreSQL 19）已提供多种扩展来支持对各种类型外部数据库或文件的操作（如 postgres_fdw 支持连接外部 PostgreSQL 数据库，oracle_fdw 支持连接外部 Oracle 数据库，mysql_fdw 支持连接外部 MySQL 数据库，jdbc_fdw 支持以 JDBC 协议连接外部常用关系型数据库，file_fdw 支持连接外部特定格式的文件等）。

对于一定规模的系统而言，数据仓库往往需要访问外部数据来完成分析和计算。外部数据包装器（Foreign Data Wrapper， 简称 FDW）是 PostgreSQL 提供的访问外部数据源机制。用户可以使用简单的 SQL 语句访问和操作外部数据源，就像操作本地表一样。

FDW 是 PostgreSQL 中的一项关键特性，它赋予数据库用户直接通过 SQL 语句访问存储于外部数据源的能力。FDW 遵循 SQL/MED 标准设计，使 PostgreSQL 能够无缝对接多种异构数据库系统以及非数据库类数据源。

FDW 可以用于以下场景：

1.  跨数据库查询：在 PostgreSQL 数据库中，我们可以通过 FDW 直接请求和查询其他 PostgreSQL 实例，或是其他数据库如 MySQL、Oracle、DB2、SQL Server 等。

2.  数据整合：当我们需要从不同数据源整合数据时，例如 REST API、文件系统、NoSQL 数据库以及流式系统等，FDW 能够帮助我们轻松实现这种跨来源的数据整合。

3.  数据迁移：利用 FDW，我们可以高效地将数据从旧系统迁移到新的 PostgreSQL 数据库中。

4.  实时数据访问：通过 FDW，我们能够访问外部实时更新的数据源。

PostgreSQL 支持非常多常见的 FDW，能够直接访问多种类型的外部数据源。例如，可以连接并查询远程的 PostgreSQL，或者主流的 SQL 数据库如 Oracle、MySQL、DB2 以及 SQL Server。同时，PostgreSQL FDW 也具备灵活的接口，支持用户自定义外部访问方式。

此外，对于 NoSQL 数据库，如 HBase、Cassandra、ClickHouse，以及实时数据库如 InfluxDB、消息队列如 Kafka、文档型数据库如 MongoDB 等等都能通过 FDW 实现数据访问。

常见的文本格式数据，如 CSV、JSON、Parquet 和 XML，也可以通过 FDW 轻松访问。大数据组件如 Elasticsearch、BigQuery，以及 Hadoop 生态系统中的 HDFS 和 Hive 等等都可以通过 FDW 实现无缝集成。

## 核心概念

FDW 机制由四个核心组件构成：

1. Foreign Data Wrapper：特定于各数据源的库，定义了如何建立与外部数据源的连接、执行查询及处理其他操作。例如：
   - postgres_fdw用于连接其他 PostgreSQL 服务器，
   - mysql_fdw 则专门连接 MySQL 数据库。

2. Foreign Server：在本地 PostgreSQL 中定义一个外部服务器对象，对应实际的远程或非本地数据存储实例。

3. User Mapping：为每个外部服务器设置用户映射，明确哪些本地用户有权访问，并提供相应的认证信息，如用户名和密码。

4. Foreign Table：在本地数据库创建表结构，作为外部数据源中表的映射。对这些外部表发起的 SQL 查询将被转换并传递给相应的 FDW，在外部数据源上执行。

## 连接外部MySQL实战

在开始之前，需要确保 mysql_fdw 已经安装在你的PostgreSQL服务器上。不同的操作系统和PostgreSQL版本可能有不同的安装步骤。在一些Linux发行版上，你可以使用包管理器来安装它

```



```

## 连接外部PostgreSQL实战
