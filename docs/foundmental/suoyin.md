## 索引基本概念

数据库中的索引，就像是书籍中的目录一样。或者是我们去图书馆看书时，通常在图书馆网络上查找到想看的书的索书号，然后根据图书馆分类索引去查找对应的书架找到书籍。

在数据库中的索引，也是这个概念。

在学生表中，为了根据给定 ID 检索一条 *student* 记录，数据库系统会先查找索引，找到记录所在的磁盘块，然后读取所需的 *student* 记录。

索引是一种典型的 **空间换取时间** 的算法思想，在磁盘中花费一些额外空间来存储一些额外的索引数据，来提高查找效率。

这里的查找，并不是简单的查询，无论是增删改查，都需要查找相应的位置进行插入，或者找到相应的记录再进行删除和修改。


**所以索引提高的并不仅仅只是查询效率。**



根据索引的作用：无论是增删改查，都是要先查找到相应的记录，**而且在增删改时也要修改索引数据。索引也会带来一些额外的维护开销**。

**评价索引性能大概有如下几种因素**：

- **访问类型**：索引能够支持的访问类型，主要的访问类型包括：特定记录的查找（等值查找），范围查找 。
- **访问时间**：在查询中，使用索引技术查找到记录的时间。
- **插入时间**：插入新数据项的时间，包括找到正确的位置插入数据项和更新索引所需要的时间。
- **删除时间**：删除数据项的时间，包括找到要被删除的项和更新索引所需要的时间。
- **空间开销**：索引结构占用的额外的空间开销。



## 索引的基本数据结构

根据索引的数据结构分类，有两种基本的索引类型：

**散列索引（哈希索引）**

- 散列索引主要的数据结构就是哈希表。只有精确匹配索引这种等值查询才有效。

  - 对于每一行数据，存储引擎都会对索引列计算一个哈希码，哈希码是一个较小的值，并且不同键值的行计算出来的哈希码也不一样（少数情况也可能有哈希冲突）。
  - 哈希索引将所有的哈希码存储在索引中，同时在哈希表中保存指向每个数据行的指针。
  - **也就是说，由于哈希查找比起B-Tree索引，其本身对于单行查询的时间复杂度更低，有了哈希索引后明显可加快单行查询速度。**

  - **哈希索引不是按照索引值顺序存储的，所以也就无法用于排序查找。**
  - **散列索引仅支持  仅能满足 "=","IN"和"<=>"查询，不能使用范围查询，例如 " where price > 100"（注意 "<=>" 和 "<" ,">" 是不同的运算符。）**
  - 其检索效率非常高，索引的检索可以一次定位，不像B-Tree 索引需要从根节点到枝节点，最后才能访问到页节点这样多次的IO访问。所以 Hash 索引的查询效率要远高于 B-Tree 索引。
  - MySQL 的 InnoDB 存储引擎中有个功能叫 **自适应哈希索引( adaptive hash index)**，当 InnoDB 注意到某些索引值使用的非常频繁时，它会在内存中基于 B -Tree 索引之上再创建一个哈希索引，这样就让 B-Tree 也具有哈希索引的一些优点，比如快速查找，这是一个自动的、内部的行为，用户无法控制或配置，不过如果有必要，可以自己关掉。

  

**顺序索引**

顺序索引的主要数据结构是 B+Tree 。将索引列按照B+tree这种数据结构来存储，本质上就是一种排好序的数据结构。加快数据查找效率。


索引项是由索引码值和指向具有该索引码的一条或多条记录的指针组成。


面试题二：为什么不用红黑树？而是B树

- 红黑树一个索引节点空间中只有一个元素，如果海量数据时，则树的高度会非常高，效率一样很低。

- B-树 ，每个索引节点的


面试题一：为什么是B+tree ，而不是 B-tree ？ (其实就是在问这两个数据结构有什么不同？)

- B+tree 树非叶子节点中不存储数据元素，只存储冗余索引（一层可以放更多索引）。

- B+Tree叶子节点是顺序排列的，并且相邻的节点具有顺序引用(有指针)的关系。（提高区间查找访问能力）

- **B+Tree叶子节点包含所有索引字段**





### InnoDB存储引擎

                                                                                                             


### MySQL中的哈希索引

MySQL 最常用存储引擎 InnoDB 和 MyISAM 都不支持 Hash 索引，它们默认的索引都是 B-Tree。

但是如果你在创建索引的时候定义其类型为 Hash，成功建表，而且你通过 SHOW CREATE TABLE  和 show index from table 来看，实际还是 B-Tree 。

查阅官网文档，可以发现InnoDB支持的所有特性，其中对Hash index特征的支持描述是：

> No (InnoDB utilizes hash indexes internally for its Adaptive Hash Index feature.)

> 不支持（InnoDB在内部利用hash索引来实现其自适应hash索引特性）


根据文档发现，自适应索引是InnoDB引擎的内存结构中的一种特性。对自适应hash索引的描述:

> 自适应hash索引特性使InnoDB能够在具有适当的工作负载和足够的缓冲池内存的系统上执行更像内存中的数据库，而不牺牲事务特性或可靠性。

总的来说就是提高了查询性能。**这里的自适应指的是不需要人工来制定，而是系统根据情况来自动完成的。**

那什么情况下才会使用自适应Hash索引呢？如果某个数据经常会访问到，当满足一定条件的时候，就会将这个数据页的地址存放到Hash表中。这样下次查询的时候，就可以直接找到这个页面的所在位置。需要说明的是： 

- 自适应哈希索引只保存热数据（经常被使用到的数据），并非全表数据。因此数据量并不会很大，可以让自适应Hash放到缓冲池中，也就是InnoDB buffer pool，进一步提升查找效率。 

- InnoDB中的自适应Hash相当于是“索引的索引”，采用Hash索引存储的是B+树索引中的页面的地址。这也就是为什么可以称**自适应Hash为索引的索引**。采用自适应Hash索引目的是可以根据SQL的查询条件加速定位到叶子节点，特别是当B+树比较深的时候，通过自适应Hash索引可以提高数据的检索效率。 

- 自适应Hash采用Hash函数映射到一个哈希表中，所以对于字典类型的数据查找非常方便 哈希表是数组+链表的形式。通过Hash函数可以计算索引键值所对应的bucket（桶）的位置，如果产生Hash冲突，如果产生哈希冲突，就需要遍历链表来解决。 

- 是否开启了自适应Hash，可以通过innodb_adaptive_hash_index变量来查看，比如：mysql> show variables like '%adaptive_hash_index'; 

所以，总结下InnoDB本身不支持Hash，但是提供自适应Hash索引，不需要用户来操作，而是存储引擎自动完成的。

自适应Hash也是InnoDB三大关键特性之一，另外两个分别是插入缓冲（Insert Buffer）和二次写(Double Write)。

**虽然常见存储引擎并不支持 Hash 索引，但 InnoDB 有另一种实现方法：自适应哈希索引。**

**InnoDB 存储引擎会监控对表上索引的查找，如果观察到建立哈希索引可以带来速度的提升，则建立哈希索引。**  

### 稠密索引

索引是连续的，即在要索引列的每一行中，都有索引项。索引项包括

稠密索引的特点是占用空间大，搜索效率高。**绝大多数关系型数据库的索引都是稠密索引。**


### 稀疏索引

索引是非连续的。

在稀疏索引中，只为搜索码的某些值建立索引项。只有当数据是按照

考虑一本字典，每一页的页眉都顺序的列出了该页中按字母顺序出现的第一个单词，这个字典所有页的页眉构成了这个字典的稀疏索引。



显然，稠密索引是可以快速定位一条记录的。

但是稀疏索引的优点在于：

- 占用更少的空间。
- 插入和删除时的开销更小。

系统设计者必须在存取时间和空间开销之间权衡。尽管有关这一权衡的决定依赖于具体的应用，但是为每个块建立稀疏索引是比较好的折中。**设计索引的粒度很重要**



**处理数据库查询的开销，主要是把块从磁盘读取到内存中的时间。一旦块被读入内存，扫描整个块的时间几乎是可以忽略的。**

（磁盘被读取到内存是以块为单位，一个数据块中的可以存取多条记录）



## 多级索引

假设要在 100 000 000 行数据上建立了稠密索引，1个 4KB 的数据块可以容纳 100 条索引项。这样索引文件就需要占用 1 000 000 个数据块。即 4GB。

这个索引文件以顺序的方式存储在磁盘中。

如果索引小到可以放到内存中。那么搜索一个索引项的时间非常小。（即使索引比内存小，也不可能全部读入内存，内存还需要处理其他任务）

在索引文件中，用二分查找法来进行搜索。





多级索引简单说，其实就是索引的索引。 再



## 索引的更新

无论采用什么形式的索引，每当有记录插入或者删除时，索引都需要更新。

如果有记录更新，任何该记录上的搜索码受影响的索引也必须更新。

例如，如果一个教师的系发生了变化，那么 instructor 上的 dept_name 列上的索引也必须相应的更新。

索引的更新可以认为是删除旧的索引，随后插入对应的新记录。因此，只需要考虑索引的插入和删除。











## 索引类型

按照索引的数据结构，MySQL 中的 **索引方法** 可以分为

- 哈希索引（HASH）(其实 MySQL 并不支持哈希索引)

- BTREE索引（BREE）

按照索引类型，可以分为：

- 普通索引（NORMAL）
- 唯一索引（UNIQUE）
- 全文索引（FULLTEXT）（MySQL8.0）
- 地理索引（SPATIAL）





```sql
-- 索引语法：ALTER TABLE table1 ADD (UNIQUE| SPATIAL | FULLTEXT )INDEX idx_name(column(length)) USING  BTREE |HASH ;
-- 索引语法：ALTER TABLE table1 ADD INDEX idx_name(column) USING  BTREE |HASH ;

-- 添加普通的B-tree索引
ALTER TABLE t1   ADD INDEX idx_name(column(10)) USING BTREE;
-- 添加unique的B-tree索引
ALTER TABLE t1   ADD INDEX unique idx_name(column(10)) USING BTREE;




```





### 隐藏索引

MySQL 8.0.19 中新增了三种索引方式：隐藏索引、降序索引、函数索引


**隐藏索引概述**

MySQL 8.0.19 及以上支持隐藏索引（invisible index），也称为不可见索引。**隐藏索引不会默认被优化器使用。主键不能设置为隐藏（包括显式设置或隐式设置）**

实际上，通过这种方式创建的索引，索引文件还是存在的，只是默认不会被优化器使用。

**这个功能在测试评估索引有效性时非常有用。DBA对希望删除的索引开启该功能，经过完整验证，确认之后，可以放心删除索引。**



所有的索引默认是可见的，可以在 CREATE TABLE, CREATE INDEX,  ALTER TABLE的时候，对新索引设置为不可见。使用方法如下：

```sql
CREATE TABLE t1 (
  i INT,
  j INT,
  k INT,
  INDEX i_idx (i) INVISIBLE  -- 隐藏索引
) ENGINE = InnoDB;
CREATE INDEX j_idx ON t1 (j) INVISIBLE;  -- 隐藏索引
ALTER TABLE t1 ADD INDEX k_idx (k) INVISIBLE; -- 隐藏索引

-- 隐藏索引与可见索引的转换
ALTER TABLE t1 ALTER INDEX i_idx INVISIBLE;
ALTER TABLE t1 ALTER INDEX i_idx VISIBLE;

-- 查看表中索引是否为隐藏索引 show index from t1;
	
SELECT INDEX_NAME, IS_VISIBLE FROM INFORMATION_SCHEMA.STATISTICS  WHERE TABLE_SCHEMA = 'db1' AND TABLE_NAME = 't1';

+------------+------------+
| INDEX_NAME | IS_VISIBLE |
+------------+------------+
| i_idx      | YES        |
| j_idx      | NO         |
| k_idx      | NO         |
+------------+------------+
```



当将索引设置为不可见时，可以通过下面几个方法确认优化器是否需要使用到该索引：

- 使用到该索引的索引提示语句会发生错误。(index hint)

- 查询的执行计划和之前的不同

- 查询出现在慢日志中

- Performance Schema里面相关的查询工作量会增加



**隐藏索引的相关说明**

- 除了主键，其他索引都可以设置为隐藏索引。
- 对于唯一键：例外情况: 没有主键的情况下，第一个唯一键 不可隐藏，第二个唯一键可隐藏。
  -  **MySQL在没有主键的情况下 是把第一个唯一建做为主键。**

- 系统变量 optimizer_switch 的 use_invisible_indexes 值控制了优化器构建执行计划时是否使用隐藏索引。
  - 如果设置为 off （默认值），优化器将会忽略隐藏索引（与引入该属性之前的行为相同）。
  - 如果设置为 on，隐藏索引仍然不可见，但是优化器在构建执行计划时将会考虑这些索引。



**总结**

不可见索引特性可以用于测试删除某个索引对于查询性能的影响，同时又不需要真正删除索引，也就避免了错误删除之后的索引重建。

对于一个大表上的索引进行删除重建将会非常耗时，而将其设置为不可见或可见将会非常简单快捷。





### 全文索引

我们在用一个东西前，得知道为什么要用它，使用全文索引无非有以下原因:

1、like查询太慢、json字段查询太慢（车太慢了）

2、没时间引入ElasticSearch、Solr或者Sphinx这样的软件，或者根本就不会用

3、加索引、联合索引啥的都已经慢得不行了（限速80，车顶盖都卸了也只能开到30）

4、为了提升一下自己的逼格（人家问你有没有开过法拉利，你说开过肯定更有气质一点）

简单的说，全文索引就相当于大词典中的目录，通过查询目录可以快速定位到想看的内容。

全文索引通过建立`倒排索引`来快速匹配文档（仅在mysql5.6版本以上支持），全文索引将连续的`字母、数字和下划线`当做一个单词，分割单词一般用空格/逗号/句号。


MySQL 中的InnoDB存储引擎中对于表索引的管理是采用B+树结构的，所以我们可以通过索引字段的前缀进行查找。

```SQL
-- 下述sql语句可以在blog中查找内容以xxx开头的文章，并且只要content添加了B+树索引，那么就可以利用索引快速的进行查询。
SELECT * FROM blog WHERE content like "xxx%";

```



问题：

但是在实际的用户查询操作中，上述查询并不符合用户的要求。因为在大多数的情况下，用户需要查询的是包含xxx的文章，而不是以xxx开头的文章。

```SQL
-- 实际上，这种查询并不是B+树索引所能很好的完成的工作。
SELECT * FROM blog WHERE content like "%xxx%";
```

全文检索的一般实现————倒排索引



什么是全文查询的“分词机制”？


分词机制，也常称为“分词”或“词条化”（Tokenization），是将一段连续的文本切分成若干独立的词汇或词条的过程。在很多文本处理和信息检索的任务中，分词是首要且关键的步骤。

分词机制的重要性主要体现在以下几个方面：

- 信息检索：搜索引擎在索引和查询时，需要对文本内容进行分词，以便快速定位和检索相关内容。
- 文本分析：在自然语言处理中，很多任务（如词性标注、命名实体识别等）在进行前，需要对文本进行分词处理。
- 数据压缩：在某些情况下，通过分词可以更有效地压缩文本数据。

分词的难度和具体方法取决于所处理的语言特性：

- 英文分词：英文等使用空格作为单词分隔符的语言，分词相对简单。通常可以使用空格和一些标点符号来分割文本。

- 中文分词：中文和其他不使用空格分隔的语言，分词就变得比较复杂。中文分词通常需要借助特定的算法和大量的词库资源，如基于统计的分词方法、基于规则的分词方法等。

在MySQL的FULLTEXT索引中，分词机制的工作是由特定的分词系统完成的。这个分词系统会根据不同的语言和字符集来处理和索引文本。例如，英文文本通常会根据空格、标点和其他特殊字符进行分词，而对于其他语言，如中文或日文，则可能需要特定的插件或工具来实现分词。



全文索引的理念和普通 B 树索引的理念刚好相反，B 树索引的构建是基于某个字段值的全部或者一部分；

全文索引是把某个字段值的全部数据按照一定的分隔符（停止词）与字符长度（也叫分词长度）一起组成各种排列，进而在索引中记录这些字符出现的位置，次数等静态信息。


全文索引（也叫倒排索引）有点类似于 HASH 索引的存储，只不过 KEY 为单词，VALUE 为关键词所属的文档 ID 与对应位置信息。

比如 "YTT" 一词出现在 4 个文档里的某个位置，也就是 4 行记录里某个位置，`FTS_DOC_ID` 指的是文档的 ID，每条记录对应一个 ID，类似于表的主键。


```SQL
CREATE SCHEMA test_fulltext;	
CREATE TABLE test_fulltext.opening_lines (
    id INT UNSIGNED AUTO_INCREMENT NOT NULL PRIMARY KEY,
    opening_line TEXT(500),
    author VARCHAR(200),
    title VARCHAR(200),
    FULLTEXT idx (opening_line)
) ENGINE=InnoDB;
	
-- 对表建立全文索引后，MySQL 用一些辅助表来保存全文索引字段的相关数据指向。如果表 opening_lines 不属于共享表空间，那对应磁盘目录上也能看到这些表。
SELECT table_id, name, space FROM INFORMATION_SCHEMA.INNODB_TABLES  WHERE name LIKE 'test_fulltext/%';
11171	test_fulltext/opening_lines	                                10114
11172	test_fulltext/fts_0000000000002ba3_being_deleted	        10115
11173	test_fulltext/fts_0000000000002ba3_being_deleted_cache	    10116
11174	test_fulltext/fts_0000000000002ba3_config	                10117
11175	test_fulltext/fts_0000000000002ba3_deleted	                10118
11176	test_fulltext/fts_0000000000002ba3_deleted_cache	        10119
11177	test_fulltext/fts_0000000000002ba3_000000000000a964_index_1	10120
11178	test_fulltext/fts_0000000000002ba3_000000000000a964_index_2	10121
11179	test_fulltext/fts_0000000000002ba3_000000000000a964_index_3	10122
11180	test_fulltext/fts_0000000000002ba3_000000000000a964_index_4	10123
11181	test_fulltext/fts_0000000000002ba3_000000000000a964_index_5	10124
11182	test_fulltext/fts_0000000000002ba3_000000000000a964_index_6	10125
```


其中，以 _index_1-6 为后缀的被称为辅助表`Auxiliary Table `，也会被持久化道磁盘中。里面顺序存放倒排索引的真实数据。

至于分了六张表的原因，可以理解为对字段添加全文索引并且对数据分词的并行化。参考参数`innodb_ft_sort_pll_degree`，可以控制并发数量。

例如，表名 `test/fts_0000000000002ba3_000000000000a964_index_1` ，其中 test 代表数据库名，fts_ 开头和 _index_n 结尾表示辅助表。

0000000000002ba3 代表对应的表ID的十六进制值，000000000000a964 代表加 `fulltext索引ID` 对应的十六进制值。


<details>
  <summary>SQL</summary>

```SQL	
SELECT 
	b.name as table_name,
    a.table_id,
    HEX(a.table_id),
	a.name as index_name
    a.index_id,
    HEX(a.index_id),
FROM
    information_schema.innodb_indexes a,
    information_schema.innodb_tables b
WHERE
    a.table_id = b.table_id
        AND b.name = 'test_fulltext/opening_lines'
        AND a.name = 'idx';

--Innodb 存储引擎允许用户查看指定倒排索引的Auxiliary Table中分词的信息，可以通过设置参数 innodb_ft_aux_table 来观察倒排索引的 Auxiliary Table。

SET GLOBAL innodb_ft_aux_table="test_fulltext/opening_lines";

--查看分词情况
SELECT * FROM INFORMATION_SCHEMA.INNODB_FT_INDEX_TABLE ORDER BY doc_id, position;



```

</details>


剩下的不包含全文索引字段 ID 的表为通用辅助表，记录索引表的配置信息、以及有关索引删除的信息。

带有`delete`的这四张表存在的意义在于可以避免在全文索引字段频繁的写入操作导致对应的六张磁盘索引表成为热点。由此带来的问题是删除的记录被保存多份，没有及时的删除，占用额外的磁盘空间。不过可以用 MySQL 语句 `optimize table` 来手动提前释放这些空间，这个语句默认只对 B+ 树聚簇索引进行整理，不会对全文索引做整理。这里MySQL 提供了一个参数 `innodb_optimize_fulltext_only`，默认关闭，打开这个参数后，语句 optimize table 只会对全文索引整理磁盘空间。



全文索引有一个缓冲池：information_schema.innodb_ft_index_cache。用来缓存全文索引字段的写入操作（insert/update），标记分词以及其他相关信息，和 MySQL 其他的缓存一样，目的是把多次频繁刷盘变为按照定义的缓冲池大小写满后合并一次性刷盘（刷新到之前的六张辅助表）。

刷盘后表 information_schema.innodb_ft_index_cache 被清空，下次根据全文索引字段来过滤时，直接查询对应的磁盘索引表；如果此时对全文索引字段值有更新但是还没有触发刷盘，MySQL 会把缓冲池的数据和磁盘索引表的数据一起返回给客户端。

其中控制单表缓冲池大小的变量为：`innodb_ft_cache_size`，默认8MB，最小 1.6MB，最大 80MB。

控制整个 MySQL 实例缓冲池大小的变量为：`innodb_ft_total_cache_size`，默认 640M，最小 32MB，最大 1.6GB。



DOC_ID 是关键词映射的索引表记录 ID，每条记录被当作一个文档， 映射为 MySQL 全文索引表的一个字段 `FTS_DOC_ID`。

如果全文索引表没有显式指定这个字段，MySQL 默认建立一个隐藏字段。为了避免后期加列的开销，这个字段不会随着全文索引的销毁而删除。也就是说这个字段会一直存在，除非这张表被删掉。

```SQL
mysql> 
mysql> SHOW EXTENDED COLUMNS FROM test_fulltext.opening_lines;
+--------------+--------------+------+-----+---------+----------------+
| Field        | Type         | Null | Key | Default | Extra          |
+--------------+--------------+------+-----+---------+----------------+
| id           | int unsigned | NO   | PRI | NULL    | auto_increment |
| opening_line | text         | YES  | MUL | NULL    |                |
| author       | varchar(200) | YES  |     | NULL    |                |
| title        | varchar(200) | YES  |     | NULL    |                |
| FTS_DOC_ID   |              | NO   |     | NULL    |                |
| DB_TRX_ID    |              | NO   |     | NULL    |                |
| DB_ROLL_PTR  |              | NO   |     | NULL    |                |
+--------------+--------------+------+-----+---------+----------------+
7 rows in set (0.00 sec)

mysql> 


-- 如果想显式自定义这个字段，并且手动维护值的唯一性，在建表的时候，或者是在全文索引没有建立之前，可以指定一个名字为 FTS_DOC_ID 字段，类型为无符号 INT64（注意，这个字段必须为大写）

```



```SQL

-- ----------------------------
-- Table structure for t_article
-- ----------------------------
CREATE TABLE `t_article`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `content` text CHARACTER SET utf8 COLLATE utf8_general_ci NULL,
  PRIMARY KEY (`id`) USING BTREE,
  FULLTEXT INDEX `fulltext_title_content`(`title`, `content`) WITH PARSER `ngram`
) ENGINE = InnoDB AUTO_INCREMENT = 15 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of t_article
-- ----------------------------
INSERT INTO `t_article` VALUES (1, '八荣八耻 1', '以热爱祖国为荣、以危害祖国为耻');
INSERT INTO `t_article` VALUES (2, '八荣八耻 2', '以服务人民为荣、以背离人民为耻');
INSERT INTO `t_article` VALUES (3, '八荣八耻 3', '以崇尚科学为荣，以愚昧无知为耻');
INSERT INTO `t_article` VALUES (4, '八荣八耻 4', '以辛勤劳动为荣，以好逸恶劳为耻');
INSERT INTO `t_article` VALUES (5, '八荣八耻 5', '以团结互助为荣，以损人利己为耻');
INSERT INTO `t_article` VALUES (6, '八荣八耻 6', '以诚实守信为荣，以见利忘义为耻');
INSERT INTO `t_article` VALUES (7, '八荣八耻 7', '以遵纪守法为荣，以违法乱纪为耻');
INSERT INTO `t_article` VALUES (8, '八荣八耻 8', '以艰苦奋斗为荣，以骄奢淫逸为耻');
INSERT INTO `t_article` VALUES (9, '满江红', '靖康耻，尤未雪');
INSERT INTO `t_article` VALUES (10, '第一生产力', '科学技术是第一 生产力');
INSERT INTO `t_article` VALUES (11, '团结互助', '团结就是力量');
INSERT INTO `t_article` VALUES (12, 'Blue Red', 'Red Black');
INSERT INTO `t_article` VALUES (13, '我是奇迹 1', '你好，我是奇迹2');
INSERT INTO `t_article` VALUES (14, '恭喜发财', '你好');

-- 添加全文索引

-- 可以多字段联合索引
ALTER TABLE `t_article` ADD FULLTEXT INDEX fulltext_title_content(`title`,`content`) WITH PARSER ngram; 

-- 可以单字段索引
ALTER TABLE `t_article` add FULLTEXT INDEX fulltext_content(`content`) WITH PARSER ngram;


--------------------------------------------------------------------------------------------------------
-- 自然语言检索IN NATURAL LANGUAGE MODE
-- 自然语言模式是 MySQL 默认的全文检索模式。自然语言模式不能使用操作符，不能指定关键词必须出现或者必须不能出现等复杂查询。

-- 查询 title 或者 content 中包含"祖国"的记录
SELECT *, MATCH (title, content) AGAINST ('祖国')  AS score
    FROM t_article WHERE MATCH (title, content) AGAINST ('祖国' IN NATURAL LANGUAGE MODE);


-- 查询 title 或者 content 中包含"团结劳动"的记录
-- 查询结果，默认会按照得分 score ，从高到低排序
SELECT *, MATCH (title, content) AGAINST ('团结劳动') AS score
    FROM t_article WHERE MATCH (title, content) AGAINST ('团结劳动' IN NATURAL LANGUAGE MODE);


-- 查询 title 或者 content 中包含"团"的记录
SELECT *, MATCH (title, content) AGAINST ('团') AS score
    FROM t_article WHERE MATCH (title, content) AGAINST ('团' IN NATURAL LANGUAGE MODE);
-- 查不到结果。原因是设置的全局变量 ngram_token_size 的值为 2
--------------------------------------------------------------------------------------------------------



--------------------------------------------------------------------------------------------------------
-- 布尔检索（IN BOOLEAN MODE）剔除一半匹配行以上都有的词

-- 每行都有this这个词的话，那用this去查时，会找不到任何结果，这在记录条数特别多时很有用，原因是数据库认为把所有行都找出来是没有意义的，这时，this几乎被当作是stopword(中断词)；




-- 查询 content 中包含"诚实守信"和"见利忘义"的语句
SELECT  * , MATCH (content) AGAINST ('+诚实守信 +见利忘义') as score 
    FROM  t_article where MATCH (content) AGAINST ('+诚实守信 +见利忘义' IN BOOLEAN MODE);

```


**布尔检索**


IN BOOLEAN MODE的特色:

- 不剔除50%以上符合的row。 
- 不自动以相关性反向排序。 
- 可以对没有FULLTEXT index的字段进行搜寻，但会非常慢。 
- 限制最长与最短的字符串。 
- 套用Stopwords。

搜索语法规则：
- +   一定要有(不含有该关键词的数据条均被忽略)。 
- -   不可以有(排除指定关键词，含有该关键词的均被忽略)。 
- >   提高该条匹配数据的权重值。 
- <   降低该条匹配数据的权重值。
- ~   将其相关性由正转负，表示拥有该字会降低相关性(但不像-将之排除)，只是排在较后面权重值降低。 
- *   万用字，不像其他语法放在前面，这个要接在字符串后面。 
- " " 用双引号将一段句子包起来表示要完全相符，不可拆字。



在全文索引底层是有一个切词的概念的，比如 "祝中国越来越强大" 这样的词，全文索引按照一个规则切词，有可能会被切成 祝 、 中国、 越来越强大。

那么切词的依据是什么呢？全文索引又是怎么切词的呢？？


MySQL 中使用全局变量 `ngram_token_size` 来配置 ngram 中 n 的大小，它的取值范围是1到10，默认值是 2。

通常`ngram_token_size`设置为要查询的单词的最小字数。如果需要搜索单字，就要设置为1。在默认值是2的情况下，搜索单字是得不到任何结果的。

因为中文单词最少是两个汉字，推荐使用默认值2。






### 降序索引

MySQL8.0开始真正支持降序索引，只有 InnoDB 引擎支持降序索引，且必须是 BTREE 降序索引，MySQL8.0不再对 group by 操作进行隐式排序。

MySQL 支持降序索引：索引定义中的 DESC 不再被忽略，而是按降序存储键值。以前，可以以相反的顺序扫描索引，但是会导致性能损失。

当只有索引只包含一个字段时，无论是使用降序索引还是升序索引，整个查询过程的性能是一样的。



```sql
-- 同一个建表语句
create table slowtech.t1(c1 int,c2 int,index idx_c1_c2(c1,c2 desc));

-- MySQL5.7  
mysql> show create table slowtech.t1\G
*************************** 1. row ***************************
      Table: t1
Create Table: CREATE TABLE `t1` (
  `c1` int(11) DEFAULT NULL,
  `c2` int(11) DEFAULT NULL,
  KEY `idx_c1_c2` (`c1`,`c2`)  -- 虽然c2列指定了desc，但在实际的建表语句中还是将其忽略了
) ENGINE=InnoDB DEFAULT CHARSET=latin1
1 row in set (0.00 sec)


-- 在t1表中，针对b,c,d三个字段创建一个联合索引。其实等价于下面的语句
create index idx_t1_bcd on t1(b,c,d); 

create index idx_t1_bcd on t1(b asc,c asc,d asc); 

-- asc表示的是升序，使用这种语法创建出来的索引叫做升序索引。也就是我们平时在创建索引的时候，创建的都是升序索引。




-- MySQL8.0
mysql> show create table slowtech.t1\G
*************************** 1. row ***************************
      Table: t1
Create Table: CREATE TABLE `t1` (
  `c1` int(11) DEFAULT NULL,
  `c2` int(11) DEFAULT NULL,
  KEY `idx_c1_c2` (`c1`,`c2` DESC) --保留了desc子句
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
1 row in set (0.00 sec)


```



#### 降序索引的意义

如果一个查询，需要对多个列进行排序，且顺序要求不一致。在这种场景下，要想避免数据库额外的排序- "filesort"，只能使用降序索引。

比如，先按 c1 升序，然后按照 c2 降序

还是上面这张表，来看看有降序索引和没降序索引区别。

```sql
-- mysql5.7
mysql> explain select * from slowtech.t1 order by c1,c2 desc;
+----+-------------+-------+------------+-------+---------------+-----------+---------+------+------+----------+-----------------------------+
| id | select_type | table | partitions | type  | possible_keys | key      | key_len | ref  | rows | filtered | Extra                      |
+----+-------------+-------+------------+-------+---------------+-----------+---------+------+------+----------+-----------------------------+
|  1 | SIMPLE      | t1    | NULL      | index | NULL          | idx_c1_c2 | 10      | NULL |    1 |  100.00 | Using index; Using filesort |
+----+-------------+-------+------------+-------+---------------+-----------+---------+------+------+----------+-----------------------------+
1 row in set, 1 warning (0.00 sec)
```



#### MySQL group by 隐式排序



在 MySQL5.7 中，group by 子句会隐式排序。

默认情况下 GROUP BY 会隐式排序（即 group by id 后面没有 asc 和 desc 关键字）。但是 group by 自己会排序 

- 不推荐 **GROUP BY 隐式排序（group by id）**  或**GROUP BY 显式排序( group by id desc)**。

- 要生成给定的排序 ORDER，请提供ORDER BY子句。`group by id order by id `

```sql
 CREATE TABLE t (id INTEGER,  cnt INTEGER);
 
INSERT INTO t VALUES (4,1),(3,2),(1,4),(2,2),(1,1),(1,5),(2,6),(2,1),(1,3),(3,4),(4,5),(3,6);

-- 在MySQL5.7中，下面这三条sql看起来执行的效果是一样的

-- 推荐，5.7和8.0效果一致
select id, SUM(cnt) from t group by id order by id; 
-- 不推荐  --8.0中不会排序
select id, SUM(cnt) from t group by id ; 
-- 不推荐  --8.0中直接报错
select id, SUM(cnt) from t group by id  asc; 

+------+----------+
| id   | SUM(cnt) |
+------+----------+
|    1 |       13 |
|    2 |        9 |
|    3 |       12 |
|    4 |        6 |
+------+----------+
4 rows in set (0.00 sec)

-- 从 MySQL8.0 开始，不支持 GROUP BY隐式排序 和 GROUP BY显式排序
https://dev.mysql.com/blog-archive/removal-of-implicit-and-explicit-sorting-for-group-by/
```
要对一组数据进行分组，MySQL优化器会选择不同的方法。其中之一是分组之前对数据排序。这使得连续分组变得很容易。

如果有一个索引可用于获取排序的数据，那么使用它的成本会非常低廉。

如果没有索引，MySQL优化器仍然可以决定在分组之前进行外部（filesort）排序。




### 表达式索引和函数索引

一个索引列并不一定是底层表的一个列，也可以是从表的一列或多列计算而来的一个函数或者标量表达式。这种特性对于根据计算结果快速获取表中内容是有用的。

索引表达式的维护代价较为昂贵，因为在每一个行被插入或更新时都得为它重新计算相应的表达式。索引表达式在进行索引搜索时却不需要重新计算，因为它们的结果已经被存储在索引中了。对于查询条件是WHERE indexedcolumn = 'constant' 查询的速度将等同于其他简单索引查询。因此，表达式索引对于检索速度远比插入和更新速度重要的情况非常有用。

从MySQL 8.0.13起，开始支持函数索引功能，该功能可以很好的帮助开发人员或者DBA去优先生产环境的SQL语句。通常，我们是并建议在SQL语句的查询条件中对列进行任何的函数计算的，因为这种做很有可能导致原本可以使用索引的查询条件，变得无法使用索引。


```SQL
-- 身份证前6位查询
SELECT * FROM user_info WHERE substr(id_card_no,1,6) = '330106';

-- 该表的id_card_no上原本是存在索引的，但是上面的写法则会导致SQL无法正常使用id_card_no列上的索引。一般来说，我们会建议开发人员，避免这种写法，更多的是将表达式放到右侧

SELECT * FROM user_info WHERE id_card_no like '330106%';




```

MySQL的函数索引是8.0版本引入的重要特性之一。它允许开发人员在查询中使用函数，并且依旧可以有效地加速查询性能。具体的，函数索引的作用是通过在函数表达式上创建索引，在处理字符串、日期、数值等类型的数据时特别有用。例如，以前面的取身份证号码前六位为例子介绍如何使用函数索引。


函数索引也有一些限制和注意事项。首先，函数索引的创建必须基于已经存在的函数，且函数必须是确定性的，即对于相同的输入始终返回相同的输出。此外，函数索引的选择应谨慎，因为不适当的函数选择可能会导致索引无效，或者在查询时产生性能问题。

在实际使用中，我们应该根据具体的业务需求和查询模式来决定是否使用函数索引。在某些情况下，创建额外的虚拟列可能更适合，或者通过优化查询语句来避免使用函数索引。

总而言之，MySQL的函数索引功能为开发人员提供了更多灵活性和效率，可以加速复杂查询和特定数据操作。然而，在使用函数索引时需要注意选择合适的函数和索引类型，并根据具体情况进行性能测试和调优。掌握函数索引的原理和最佳实践，将有助于提高MySQL数据库的性能和响应速度。


### 部分索引

在 PostgreSQL 数据库中，部分索引（partial index）是指对表中满足特定条件的数据行进行索引。由于它不需要对全部数据进行索引，因此索引会更小，在特定场景下通过部分索引查找数据时性能会更好。

PostgreSQL 在创建索引时可以通过一个 WHERE 子句指定需要索引的数据行，从而创建一个部分索引。

```SQL
CREATE TABLE orders (
  id INT PRIMARY KEY,
  customer_id INT,
  status TEXT
);

INSERT INTO orders (id, customer_id, status)
SELECT
  i,
  (random()*10000)::INT,
  CASE (random() * 100)::int
    WHEN 0 THEN 'pending'
    WHEN 1 THEN 'shipped'
    ELSE 'completed'
  END
    FROM generate_series(1, 1000000) i;

-- 该表中总共有 1000000 个订单，通常绝大部的订单都处于完成状态。一般情况下，我们只需要针对某个用户未完成的订单进行查询跟踪，因此可以创建一个基于用户编号和状态的部分索引：    
```

## 索引组织表

目前的流行的 MySQL 存储引擎中，InnoDB 是最优先的引擎选型，我们在部署和规划的过程中，应该首选为 InnoDB 作为存储引擎的首选。

在 InnoDB 存储引擎中，因为表都是按照主键的顺序进行存放的，我们称之为 **索引组织表(index organized table ，IOT)**

因为在 InnoDB 中，数据文件本身就是根据**主键索引**排序的 B+Tree 的数据结构进行存储，其中叶子节点包含了完整的数据记录。


==堆表中的数据无序存放，数据的排序完全依赖于索引（Oracle、Microsoft SQL Server、PostgreSQL 早期默认支持的数据存储都是堆表结构）。
堆表的组织结构中，数据和索引分开存储。索引是排序后的数据，而堆表中的数据是无序的，索引的叶子节点存放了数据在堆表中的地址，当堆表的数据发生改变，且位置发生了变更，所有索引中的地址都要更新，这非常影响性能，特别是对于 OLTP 业务。==

==而索引组织表，数据根据主键排序存放在索引中，主键索引也叫聚集索引（Clustered Index）。在索引组织表中，数据即索引，索引即数据。MySQL InnoDB 存储引擎就是这样的数据组织方式；Oracle、Microsoft SQL Server 后期也推出了支持索引组织表的存储方式。但是，PostgreSQL 数据库因为只支持堆表存储，不适合 OLTP 的访问特性，虽然它后期对堆表有一定的优化，但本质是通过空间换时间，对海量并发的 OLTP 业务支持依然存在局限性。==

> 
>
> clustered index
>
> The InnoDB term for a primary key index. InnoDB table storage is organized based on the values of the primary key columns, 
>
> to speed up queries and sorts involving the primary key columns. For best performance,
>
> choose the primary key columns carefully based on the most performance-critical queries. Because modifying
>
> the columns of the clustered index is an expensive operation, choose primary columns that are rarely or never updated.
>
> In the Oracle Database product, this type of table is known as an index-organized table.
>
> See Also index, primary key, secondary index.



既然 MySQL InnoDB 表默认是主键索引的 B+Tree 存放的。那么默认不带任何条件和排序的全表扫描是默认按照什么顺序返回结果呢？

> 理解SQL最重要的一点就是要明白表不保证是有序的，因为表是为了代表一个集合（如果有重复项，则是多集），而集合是无序的。
>
> 如果在查询表时不指定ORDER BY子句，那么虽然查询可以返回一个结果表，但MySQL Server可以自由地按任意顺序对结果中的行进行排序。（注意，这个不一定可靠）
>
> 为了确保结果中的行按照一定的顺序进行排序，唯一的方法就是显示地指定一个ORDER BY子句。

[MySQL论坛](https://forums.mysql.com/read.php?21,239471,239688)



###  聚集索引(clustered index)



**innodb 表中的主键，就是聚簇索引（或者说聚集索引）。**

主键索引的叶子节点存的是整行数据。由于表里的数据行只能按照一颗B+树排序，因此**一张表只能有一个聚簇索引。**

- **如果在建表时没有主键，MySQL内部会尝试找一个可以做为唯一索引（唯一不重复且不可为空的列）的列做为主键，成为此表的聚簇索引。当表中有多个非空唯一索引，InnoDB选择建表时定义的第一个非空唯一索引为主键。**

- **如果上述条件不满足，InnoDB内部会隐式自动创建一个6字节大小的指针**

**一般建议在建表的时候显式指定主键（这样MySQL就自动根据这个主键索引去存储数据）。**


_rowid介绍

在MySQL中存在一个隐藏列 _rowid 来标记唯一标识。但是需要注意的是 _rowid 并不是一个真实存在的列，本质是一个非空唯一列的别名。因此，在某些情况下 _rowid 是不存在的。它只存在于以下情况：

1、当表中存在一个数字类型的单列主键时， _rowid 其实指的就是这个主键列

2、当表中不存在主键但存在一个数字类型的非空唯一列时，  _rowid 其实指的就是这个对应的非空唯一列

```shell

# 详见MySQL文档 https://dev.mysql.com/doc/refman/8.0/en/create-index.html

If a table has a PRIMARY KEY or UNIQUE NOT NULL index that consists of a single column that has an integer type, you can use _rowid to refer to the indexed column in SELECT statements, as follows:

_rowid refers to the PRIMARY KEY column if there is a PRIMARY KEY consisting of a single integer column. If there is a PRIMARY KEY but it does not consist of a single integer column, _rowid cannot be used.

Otherwise, _rowid refers to the column in the first UNIQUE NOT NULL index if that index consists of a single integer column. If the first UNIQUE NOT NULL index does not consist of a single integer column, _rowid cannot be used.
```

```shell

mysql> create table test(a int primary key,b varchar(5));
Query OK, 0 rows affected (0.03 sec)

mysql> insert into test values(1,'a'),(2,'b'),(3,'c'),(4,'c'),(5,'d');
Query OK, 5 rows affected (0.00 sec)
Records: 5  Duplicates: 0  Warnings: 0

mysql> select _rowid from test;
+--------+
| _rowid |
+--------+
|      1 |
|      2 |
|      3 |
|      4 |
|      5 |
+--------+
5 rows in set (0.00 sec)

```



**在InnoDB中，聚簇索引默认就是主键索引**。

**如果在建表后，并且表中已经有大量数据时，再为这个表创建主键索引或者修改主键索引的代价是很高的。这个操作其实就是重建表。**

```sql
-- 重建表
alter table T engine=InnoDB;

```

### 索引扩展

MySQL InnoDB的二级索引（Secondary Index）会自动补齐主键，将主键列追加到二级索引列后面。

InnoDB的二级索引（Secondary Index）除了存储索引列key值，还存储着主键的值(而不是指向主键的指针)。


```SQL

CREATE TABLE t1 (
  i1 INT NOT NULL DEFAULT 0,
  i2 INT NOT NULL DEFAULT 0,
  d DATE DEFAULT NULL,
  PRIMARY KEY (i1, i2),
  INDEX k_d (d)
) ENGINE = InnoDB;
-- 这个t1表包含主键和二级索引k_d，二级索引k_d（d）的元组在InnoDB内部实际被扩展成（d,i1,i2），即包含主键值。
-- 因此在设计主键的时候，常见的一条设计原则是要求主键字段尽量简短，以避免二级索引过大(因为二级索引会自动补齐主键字段)。
```

默认情况下，索引扩展（use_index_extensions）选项是开启的。可以在当前会话通过修改优化器开关optimizer_switch开启、关闭此选项。

```SQL
INSERT INTO t1 VALUES
(1, 1, '1998-01-01'), (1, 2, '1999-01-01'),
(1, 3, '2000-01-01'), (1, 4, '2001-01-01'),
(1, 5, '2002-01-01'), (2, 1, '1998-01-01'),
(2, 2, '1999-01-01'), (2, 3, '2000-01-01'),
(2, 4, '2001-01-01'), (2, 5, '2002-01-01'),
(3, 1, '1998-01-01'), (3, 2, '1999-01-01'),
(3, 3, '2000-01-01'), (3, 4, '2001-01-01'),
(3, 5, '2002-01-01'), (4, 1, '1998-01-01'),
(4, 2, '1999-01-01'), (4, 3, '2000-01-01'),
(4, 4, '2001-01-01'), (4, 5, '2002-01-01'),
(5, 1, '1998-01-01'), (5, 2, '1999-01-01'),
(5, 3, '2000-01-01'), (5, 4, '2001-01-01'),
(5, 5, '2002-01-01');


show variables like '%optimizer_switch%';

SET optimizer_switch = 'use_index_extensions=off';

-- 这种情况下，优化器不会使用主键，因为主键由字段（i1,i2）组成，但是该查询中没有引用t2字段;优化器会选择二级索引 k_d(d) 。

-- 这个查询，忽略了
EXPLAIN  SELECT COUNT(*) FROM t1 WHERE i1 = 3 AND d = '2000-01-01';


SET optimizer_switch = 'use_index_extensions=on';



```



### 如何正确选择主键

#### 自增主键



自增主键是指自增列上定义的主键，在建表语句中一般是这么定义的：

```sql
create table t1 (
    -- 创建自增列
	`rid` int(11)  NOT NULL  AUTO_INCREMENT,
	-- 以自增列创建主键
    PRIMARY KEY (`id`),
 )   
```

插入新记录的时候可以不指定 ID 的值，系统会获取当前 ID 最大值加 1 作为下一条记录的 ID 值。

也就是说，自增主键的插入数据模式，正符合了我们前面提到的递增插入的场景。

每次插入一条新记录，都是追加操作，都不涉及到挪动其他记录，也不会触发叶子节点的分裂。

**而用业务逻辑的字段做主键，则往往不容易保证有序插入，这样写数据成本相对较高。一般多数情况建议使用业务无关的自增列作为主键。**

对于业务中需要唯一的，可以使用唯一约束。



除了性能外，还可以从存储空间来看，假设表中确实有一个唯一字段。比如字符串类型的身份证号，那应该用身份证号做主键，还是用自增字段做主键呢？



**为什么不建议过长的字段做主键？**

由于每个非主键索引的叶子节点上都是主键的值。如果用身份证号做主键，

那么每个二级索引的叶子节点占用约20个字节，而如果用整型做主键，则只要4个字节，如果是长整型（bigint）则是8个字节。

**显然，主键长度越小，普通索引的叶子节点就越小，普通索引占用的空间也就越小。**

**所以从性能和存储来看，自增主键往往是更合适的选择。**


主键性能问题不是一个单一的问题，需要MySQL方向持续改造的，将技术价值和业务价值结合起来。很多业务很多人都知道主键最好设置成自增列，但是大多数情况下，这种自增列却没有实际的业务含义，尽管是主键列保证了ID的唯一性，但是业务开发无法直接根据主键自增列来进行查询，于是他们需要寻找新的业务属性，添加一系列的唯一性索引，非唯一性索引等等，这样一来我们坚持的规范和业务使用的方式就存在了偏差。


从另外一个维度来说，我们对于主键的理解是有偏差的，我们不能单一的认为主键就一定是从1开始的整数类型，我们需要结合业务场景来看待，比如我们的身份证其实就是一个不错的例子，把证号分成了几个区段，偏于检索和维护；或者是外出就餐时得到的流水单号，它都有一定的业务属性在里面，对于我们去理解业务的使用是一种不错的借鉴。


**为什么是自增的主键？**

因为主键插入后，在B+tree中其实应该要有有序的，如果是无序的，会导致一些页分裂的情况。





### **非聚集索引(secondary index)**

非主键索引，其实是另外一颗单独的 B+Tree，叶子结点中只存放主键索引的值。

通过非主键索引查找数据时，先去查找索引所在的B+树上进行查找。然后再根据索引的值，再回去主键索引的B+树上进行查找。

第二个过程被称为**回表查询，**即要查询的列不在非主键索引中。

```sql
-- 查看表中的索引详情
SHOW INDEX FROM table_name;
-- 创建唯一索引
ALTER TABLE table_name ADD UNIQUE (column);
```



#### Multi-Range Read（MRR）

------

在 secondary index 上进行范围查询或等值查询时，返回的一系列主键索引值可能是无序的。后续的回表查询就变成了随机读。

MRR 要把主键排序，这样之后对磁盘的操作就是由顺序读代替之前的随机读。

从资源的使用情况上来看就是让 CPU 和内存多做点事，来换磁盘的顺序读。然而排序是需要内存的，这块内存的大小就由参数 read_rnd_buffer_size 来控制。

MRR在通过二级索引获取到主键ID后，将ID值放入read_rnd_buffer中，然后对其进行排序，利用排序后的ID数组遍历主键索引查找记录并返回结果集，优化了回表性能。

read_rnd_buffer_size  这是一个内存中的buffer用于分配给每个客户端用的。默认值是0.25MB，最大值为 2GB

所以不能设置 global 全局变量太大，所以只能客户端自己运行大查询时进行设置。



https://opensource.actionsky.com/20200616-mysql/



### **索引覆盖**

索引覆盖（index covering），故名思义，要查询的数据列都在索引树上查询完成了，不需要再回主键的这颗二叉树上进行**回表查询**。

> An index that provides all the necessary results for a query is called a covering index.

**由于覆盖索引可以减少树的搜索次数，显著提升查询性能，所以使用覆盖索引是一个常用的性能优化手段。**

**通常使用联合索引来提升查询性能。**比如有一个市民信息表，身份证号是市民的唯一标识：

```sql
CREATE TABLE `tuser` (
  `id` int(11) NOT NULL,
  `id_card` varchar(32) DEFAULT NULL,
  `name` varchar(32) DEFAULT NULL,
  `age` int(11) DEFAULT NULL,
  `ismale` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `id_card` (`id_card`),
  KEY `name_age` (`name`,`age`)
) ENGINE=In
```



如果要根据市民身份证号查询市民信息的需求，在身份证号字段上建立索引就够了。

现在如果有一个高频请求，要根据市民的身份证号查询他的姓名，就可以建立



### 联合索引

https://www.cnblogs.com/xuwc/p/14007766.html

MySQL可以创建联合索引（即在多列上创建一个索引，一个索引可以包含最多16列。），英文叫 [Multiple-Column Indexes](https://dev.mysql.com/doc/refman/8.0/en/multiple-column-indexes.html)


如果分别为每个列创建索引，则即使一个条件查找中利用了多个索引列字段去匹配，那么SQL引擎查找也只会选择用一个合适的索引条件去查找，然后通过索引合并的方式查找。或者只会选择用一个索引列去匹配查找(策略是判断哪个列过滤排除的数据更多)



联合索引的好处：

- 建一个联合索引 `(col1,col2,col3)`，实际相当于建了 `(col1)`，`(col1,col2)`，`(col1,col2,col3)` 三个索引。每多一个索引，都会增加写操作的开销和磁盘空间的开销。对于大量数据的表，使用联合索引会大大的减少开销！

- 一般DBA都会建议尽量多使用联合索引。



对于联合主键和索引组织表的理解

```sql
CREATE TABLE `geek` (
  `a` int(11) NOT NULL,
  `b` int(11) NOT NULL,
  `c` int(11) NOT NULL,
  `d` int(11) NOT NULL,
  PRIMARY KEY (`a`,`b`),
  KEY `c` (`c`),
  KEY `ca` (`c`,`a`),
  KEY `cb` (`c`,`b`)
) ENGINE=InnoDB;


-- 主键(a，b)的聚簇索引组织顺序相当于order by a,b ，也就是先按a排序，再按b排序，c无序。

-- 在(a,b)主键索引排好序之后，再按照索引c来组织数据

–a--|–b--|–c--|–d--
1 2 3 d
1 3 2 d
1 4 3 d
2 1 3 d
2 2 2 d
2 3 4 d
```


#### 最左前缀匹配原则

所谓的索引有效，是指**使用了索引的快速搜索功能，并且有效的减少了扫描行**，所以**全索引扫描**（辅助索引树）和**全表扫描**（主键索引树）都不能称为真正的**索引有效**


谈到联合索引，一定要讲**最左前缀匹配**，有如下原则：

- **如果查询的时候查询条件可以通过索引精确匹配左边连续一列或几列，则此列就可以被用到**。

- 注意，一定要是指精准匹配。

```sql
CREATE TABLE test (
	id INT NOT NULL,
	last_name CHAR(30) NOT NULL,
	first_name CHAR(30) NOT NULL,
	age INT NULL ,    
	PRIMARY KEY (id),
	INDEX name (last_name,first_name,age)
);

-- name 是一个包含了 last_name,first_name,age 三列的联合索引。


-- 对于这个表，使用 (last_name) 和 (last_name,first_name) (last_name,first_name,age) 这样的条件过滤才可以走索引
-- 这里需要注意的是，查询的时候如果两个条件都用上了但是顺序不同。
-- 如 first_name= xx and last_name ＝xx，那么现在的查询引擎会自动优化为匹配联合索引的顺序，这样是能够命中索引的。
-- 由于最左前缀原则，在创建联合索引时，索引字段的顺序需要考虑字段值去重之后的个数，较多的放前面。ORDER BY子句也遵循此规则。


SELECT * FROM test WHERE last_name='Jones';
SELECT * FROM test WHERE last_name='Jones' AND first_name='John';
SELECT * FROM test WHERE last_name='Jones' AND (first_name='John' OR first_name='Jon');
SELECT * FROM test WHERE last_name='Jones' AND first_name >='M' AND first_name < 'N';
select * FROM test where last_name like '张%' and age=10 ;

-- 下面的查询无法用到这个索引
SELECT * FROM test WHERE first_name='John';
SELECT * FROM test WHERE last_name='Jones' OR first_name='John';
```





### 前缀索引

我们在给一个字段加索引的时候，实际上仅可以针对字段的前 n 位加索引。使用 `col_name(N)` 这样的格式。

有点类似于 Oracle 中对字段使用 Left 函数来建立函数索引，只不过 MySQL 的这个前缀索引在查询时是内部自动完成匹配的，并不需要使用 Left 函数。


一般来说，当某个字段的数据量太大，而且查询又非常的频繁时，使用前缀索引能有效的减小索引文件的大小，让每个索引页可以保存更多的索引值，从而提高了索引查询的速度。

比如，客户店铺名称，有的名称很长，有的很短，如果完全按照全覆盖来建索引，索引的存储空间可能会非常的大，有的表如果索引创建的很多，甚至会出现索引存储的空间都比数据表的存储空间大很多，因此对于这种文本很长的字段，我们可以截取前几个字符来建索引，在一定程度上，既能满足数据的查询效率要求，又能节省索引存储空间。

**在 varchar , blob , text 等类型的字段上建立索引时，必须指定索引长度，没必要对全字段建立索引，根据实际文本区分度决定索引长度即可。**

**索引长度和区分度其实是相互矛盾的。**

**索引长度过短，那么区分度就很低，查找时扫描的行越多，把索引长度加长，区分度就高，但是索引占用空间大，因此要掌握一个平衡点。**

当某个字段内容的前几位区分度很高的时候，这个时候采用前缀索引，可以在查询性能和空间存储方面达到一个很高的性价比。

索引其实都是排好序的数据结构，若是区分度高排序越快，区分度越低，排序慢；

举个例子： （张，张三，张三哥），如果索引长度取1的话，那么每一行的索引都是 `张` 这个字，完全没有区分度，你让它怎么排序？

结果这样三行完全是随机排的，因为索引都一样；

如果长度取2，那么排序的时候至少前两个是排对了的，如果取3，区分度达到100%，排序完全正确；

等等，那你说是不是索引越长越好？ 答案肯定是错的。

比如 (张,李,王) 和 （张三啦啦啦，张三呵呵呵，张三呼呼呼）；

前者在内存中排序占得空间少，排序也快，后者明显更慢更占内存，在大数据应用中这一点点都是很恐怖的；



#### 前缀索引优化原则

------

索引长度的判断公式：

test是要加索引的字段，5是索引长度，

```sql
-- 查询表中某个字段最长的记录
select  `字段`, length(`字段`)  from 表名  where  length(`字段`) = ( select max(length(`字段`)) from 表名  )
-- 查询表中某个字段最短的记录
select  `字段`, length(`字段`)  from 表名  where  length(`字段`) = ( select min(length(`字段`)) from 表名  )

-- left函数取test字段的前5位，对前5位去重，这个
select count(distinct left(test,5))/count(*) from table;  

-- 随着索引字段长度的扩大，这个区分度的值是越来越趋近于1，等于1即表示


-- 给字段指定前10位加索引
CREATE TABLE test (blob_col BLOB, INDEX(blob_col(10)));


```



### 索引基数

了解前缀索引之后，了解一下索引基数

**索引基数**（cardinality）：索引中不重复的索引值的数量；

例如，例如，某个数据列包含值1、3、7、4、7、3，	那么它的**索引基数**就是4。

**索引基数相对于数据表行数较高（也就是说，列中包含很多不同的值，重复的值很少，值很分散）的时候，它的工作效果最好。**

- 如果某数据列含有很多不同的年龄，索引会很快地分辨数据行。

- 如果某个数据列用于记录性别（只有”M”和”F”两种值），那么索引的用处就不大。

- 如果值出现的几率几乎相等，那么无论搜索哪个值都可能得到一半的数据行。

  在这些情况下，最好根本不要使用索引，因为查询优化器发现某个值出现在表的数据行中的百分比很高的时候。

  它一般会忽略索引，进行全表扫描。惯用的百分比界线是”30%”。



使用 show index from table 语句，





#### **索引维护的代价**

索引维护，B+树为了维护索引有序性，在插入新值的时候需要做必要的维护。

如果你的主键的值是不连续的，那么在插入索引的时候，就要有移动B+树上节点的操作。

如果插入值时父节点所在的数据页已经满了，根据B+树的算法，这时候需要申请一个新的数据页，然后挪动部分数据过去。

**这个过程称为页分裂。在这种情况下，性能自然会受影响。**

除了性能外，页分裂操作还影响数据页的利用率。原本放在一个页的数据，现在分到两个页中，整体空间利用率降低大约50%。

**当然有分裂就有合并。当相邻两个页由于删除了数据，利用率很低之后，会将数据页做合并。合并的过程，可以认为是分裂过程的逆过程。**




### 索引下推（ICP）

在联合索引的最左前缀匹配时，以 INDEX name (last_name,first_name,age) 这个索引为例。有如下查询

```sql
select * FROM test where last_name like '张%' and age=10 ;
```

在 5.6 之前，这个语句在搜索索引树的时候，使用第一个字段的条件去匹配。找到所有匹配的行，逐行去主键索引上找到数据行，对比后面的条件。

在 5.6 之后，MySQL 引入了**索引下推**优化，可以在索引遍历的过程中，对索引包含的字段先做判断，过滤掉不满足要求的行，减少回表次数。




### 索引合并


[官网](https://dev.mysql.com/doc/refman/8.0/en/index-merge-optimization.html)

MySQL5.0之前，一个表一次只能使用一个索引，无法同时使用多个索引分别进行条件扫描。

但是从5.1开始，引入了 index merge 优化技术，对同一个表可以使用多个索引分别进行条件扫描。

当单表使用了多个索引，每个索引查找都可能返回一个结果集，mysql会将其求交集或者并集，或者是交集和并集的组合。

也就是说一次查询中可以使用多个索引。



```sql
-- 可以使用索引合并的语句示例

SELECT * FROM tbl_name WHERE key1 = 10 OR key2 = 20;

SELECT * FROM tbl_name
  WHERE (key1 = 10 OR key2 = 20) AND non_key = 30;

SELECT * FROM t1, t2
  WHERE (t1.key1 IN (1,2) OR t1.key2 LIKE 'value%')
  AND t2.key1 = t1.some_col;

SELECT * FROM t1, t2
  WHERE t1.key1 = 1
  AND (t2.key1 = t1.some_col OR t2.key2 = t1.some_col2);
  
-- 对于第一条语句：使用索引并集访问算法，得到key1=10的主键有序集合，得到key2=20的主键有序集合，再进行求并集；最后回表查找。

-- 对于第二条语句：先丢弃non_key=30,因为它使用不到索引，where子句就变成了where key10 or key2=20，使用索引先根据索引合并并集访问算法。
-- 先通过索引查找算法查找后缩小结果集，在小表中再进行全表匹配查询。

-- 
```

> 
>
> **注意：**
>
> 索引合并优化算法具有以下已知限制：
>
> - 如果您的查询具有深度 AND/OR 嵌套的复杂 WHERE 子句，并且 MySQL 没有选择最佳计划，请尝试使用以下转换后表达方式来满足条件：
>
>   ```sql
>   (x AND y) OR z => (x OR z) AND (y OR z)
>   (x OR y) AND z => (x AND z) OR (y AND z)
>   ```
>
> - 索引合并不适用于全文索引。



索引合并访问方法有几个算法，这些算法显示在 EXPLAIN 输出的 `Extra` 字段中：

- `Using intersect(...)`
- `Using union(...)`
- `Using sort_union(...)`

 



### index merge intersection access algorithm（索引合并-交集访问算法）

对于每一个使用到的索引进行查询，查询主键值集合，然后进行合并，求交集，也就是 and 运算。下面是使用到该算法的两种必要条件：



- **在二级索引列上进行等值查询**；如果是组合索引，组合索引的每一位都必须覆盖到，不能只是部分

  ```sql
  --所有查询的字段都有索引，并且都是等值查询
  key_part1 = const1 AND key_part2 = const2 ... AND key_partN = constN
  ```

  

- InnoDB表上的主键范围查询条件



```sql
-- 例子

-- 主键可以是范围查询，二级索引只能是等值查询
SELECT * FROM innodb_table  WHERE primary_key < 10 AND key_col1 = 20;

-- 没有主键的情况
SELECT * FROM tbl_name  WHERE key1_part1 = 1 AND key1_part2 = 2 AND key2 = 2;
```



## 优化器提示（Optimizer Hints）



## 索引提示(index hint)



MySQL 可以使用索引提示（Index Hints）， 用于告诉**查询优化器**在查询中如何选择索引。

索引提示只能用于 select 和 update 语句中。MySQL 共有三种索引提示，分别是：USE INDEX、IGNORE INDEX和FORCE INDEX。

- use index(index_list)  告诉MySQL用索引列表中的其中一个索引去做本次查询

  - ```sql
    -- 强制使用这两个索引去进行查找
    SELECT * FROM table1 USE INDEX (col1_index,col2_index)
      WHERE col1=1 AND col2=2 AND col3=3;
    ```

- ignore index：ignore index告诉mysql不要使用某些索引去做本次查询

  - ```sql
    SELECT * FROM table1 IGNORE INDEX (col3_index)
    WHERE col1=1 AND col2=2 AND col3=3;
    ```

- force index：force index和use index功能类似，都是告诉mySQL去使用某些索引。

  - force index 和 use index 的区别是，如果使用force index，那么全表扫描就会被假定为需要很高代价，除非不能使用索引，否则不会考虑全表扫描；

  - 而使用 use index 的话，如果MySQL觉得全表扫描代价更低的话，仍然会使用全表扫描。

  - ```sql
    SELECT * FROM table1 FORCE INDEX (col3_index)
    WHERE col1=1 AND col2=2 AND col3=3;
    ```





### 索引提示的用途

可以在索引提示的后边使用FOR语句指定提示的范围，索引提示共有三种适用范围，分别是FOR JOIN、FOR ORDER BY、FOR GROUP BY：

  

## MySQL优化器开关



```sql
SELECT @@optimizer_switch;

index_merge=on,
index_merge_union=on,
index_merge_sort_union=on,
index_merge_intersection=on,
engine_condition_pushdown=on
index_condition_pushdown=on,
mrr=on,
mrr_cost_based=on,
block_nested_loop=on,
batched_key_access=off,
materialization=on,
semijoin=on,
loosescan=on,
firstmatch=on,
duplicateweedout=on,
subquery_materialization_cost_based=on,
use_index_extensions=on,
condition_fanout_filter=on,
derived_merge=on,
use_invisible_indexes=off,
skip_scan=on,
hash_join=on


-- 修改优化器
SET [GLOBAL|SESSION] optimizer_switch='command[,command]...';

-- command语法如下：
-- default          --重置为默认
-- opt_name=default	--选项默认 
-- opt_name=off	    --关掉某项优化
-- opt_name=on	    --开启某项优化

```









## 尽量避免全表扫描

https://cloud.tencent.com/developer/article/1404687

http://zhongmingmao.me/2019/03/08/mysql-full-table-scan/

在 expain 查看一个 SQL 的执行计划时，如果 type 字段是 ALL ，则会进行全表扫描。

SQL 优化的一条最基本的原则就是，当真正出现性能问题时或者影响到业务时，才考虑优化。



全表扫描的情况：

- 表足够小，数据量足够少，全表扫描的速度甚至比索引查找还要快。通常是 10 行之内的表。
- on 连接的字段，或者 where 条件的字段没有索引列，或者根本不带 where 条件。
- 





## MySQL优化准则

https://github.com/kekobin/blog/issues/87



https://github.com/Snailclimb/JavaGuide/blob/main/docs/database/mysql/mysql-high-performance-optimization-specification-recommendations.md




# 性能优化概述

数据库性能优化在数据库层面有很多因素，例如，表，查询语句，数据库配置等。

数据库操作最终是作用在硬件层面的CPU计算和磁盘的IO操作上。所以要尽可能让开销足够小。

**数据库层面的优化**

- 表结构设计是否合理？是否满足三范式？范式和反范式的设计？https://www.zhihu.com/question/19900437
  
  - oltp: 事务型，读多写少，关联查询比较少的，尽量遵守三范式，减少数据冗余。

  - olap：分析型，建宽表，增大冗余，减少关联查询。

- 字段的数据类型是否合适？

- 索引设计是否合理？

- 是否选用合适的存储引擎？

- 表是否有正确的row格式？


优化的几个简单原则：

1. 减少数据访问： 设置合理的字段类型，启用压缩，通过索引访问等减少磁盘IO
2. 返回更少的数据： 只返回需要的字段和数据分页处理 减少磁盘IO及网络IO
3. 减少交互次数： 批量DML操作，函数存储等减少数据连接次数
4. 减少服务器CPU开销： 尽量减少数据库排序操作以及全表查询，减少 cpu 内存占用
5. 利用更多资源： 使用表分区，可以增加并行操作，更大限度利用cpu资源



## 优化器和查询成本

一般来说一个sql查询可以有不同的执行方案，可以选择走某个索引进行查询，也可以选择全表扫描。

**查询优化器**则会比较并选择其中成本最低的方案去执行查询。



查询成本分大体为两种：

- **I/O成本**：磁盘读写的开销。一个查询或一个写入，都要从磁盘中读写数据，要一定的IO开销。

- **CPU成本**：关联查询，条件查找，都要CPU来进行计算判断，一定的计算开销。

MySQL使用的InnoDB引擎会把数据和索引都存储到磁盘上，当查询的时候需要先把数据先加载到内存中在进行下一步操作，这个加载的时间就是I/O成本。

当数据被加载到内存中后，CPU会计算查询条件匹配，对数据排序等等操作，这一步所消耗的时间就是CPU成本。

**但是查询优化器并不会真正的去执行sql，只会去根据优化的结果去预估一个成本。**

**InnoDB引擎规定读取一个页面花费的成本默认约是0.25，读取以及检测一条记录是否符合搜索条件的成本默认约是0.1。**

为什么都是约呢，因为MySQL内部的计算成本比较复杂这里提取了两个主要的计算参数。

```shell
## MySQL server 层面的各种开销
mysql> select * from mysql.server_cost;
+------------------------------+------------+---------------------+---------+---------------+
| cost_name                    | cost_value | last_update         | comment | default_value |
+------------------------------+------------+---------------------+---------+---------------+
| disk_temptable_create_cost   |       NULL | 2021-09-24 14:47:20 | NULL    |            20 |
| disk_temptable_row_cost      |       NULL | 2021-09-24 14:47:20 | NULL    |           0.5 |
| key_compare_cost             |       NULL | 2021-09-24 14:47:20 | NULL    |          0.05 |
| memory_temptable_create_cost |       NULL | 2021-09-24 14:47:20 | NULL    |             1 |
| memory_temptable_row_cost    |       NULL | 2021-09-24 14:47:20 | NULL    |           0.1 |
| row_evaluate_cost            |       NULL | 2021-09-24 14:47:20 | NULL    |           0.1 |
+------------------------------+------------+---------------------+---------+---------------+
6 rows in set (0.00 sec)

mysql>

## MySQL 存储引擎层面的各种开销
mysql> select * from mysql.engine_cost;
+-------------+-------------+------------------------+------------+---------------------+---------+---------------+
| engine_name | device_type | cost_name              | cost_value | last_update         | comment | default_value |
+-------------+-------------+------------------------+------------+---------------------+---------+---------------+
| default     |           0 | io_block_read_cost     |       NULL | 2021-09-24 14:47:20 | NULL    |             1 |
| default     |           0 | memory_block_read_cost |       NULL | 2021-09-24 14:47:20 | NULL    |          0.25 |
+-------------+-------------+------------------------+------------+---------------------+---------+---------------+
2 rows in set (0.00 sec)

mysql>
```







#### 基于成本的优化

在一条单表查询语句真正执行之前，Mysql的查询优化器会找出执行该语句所有可能使用的方案，对比之后找出成本最低的方案。

这个成本最低的方案就是所谓的**执行计划**，之后才会调用存储引擎提供的接口真正的执行查询。

**多数情况下，一条查询可以有很多种执行方式，最后都返回相应的结果。优化器的作用就是找到这其中最好的执行计划。**

MySQL采用了基于开销的优化器，以确定处理查询的最解方式，也就是说执行查询之前，都会先选择一条自认为最优的方案，然后执行这个方案来获取结果。

在很多情况下，MySQL能够计算最佳的可能查询计划，但在某些情况下，MySQL没有关于数据的足够信息，或者是提供太多的相关数据信息，估测就不那么友好了。



**对于一些执行起来十分耗费性能的语句，MySQL 还是依据一些规则，竭尽全力的把这个很糟糕的语句转换成某种可以比较高效执行的形式，这个过程也可以被称作查询重写**。



MySQL 使用基于成本的优化器，**它尝试预测一个查询使用某种执行计划时的成本，并选择其中成本最小的一个。**

在 MySQL 可以通过查询当前会话的 last_query_cost 的值来得到其计算当前查询的成本。





## 数据库层面的优化



- 表结构设计是否合理？是否满足三范式？范式和反范式的设计？https://www.zhihu.com/question/19900437
  - 字段的数据类型是否合适？
  - 经常更新的应用应该设计为多个表，很少列。数据分析的应该设计为大宽表。
- 索引设计是否合理？

- 是否选用合适的存储引擎？

- 表是否有正确的row格式？

## 顺序索引

为了快速随机访问文件中的记录，可以使用索引结构，每个索引结构与一个特定的搜索码关联。

被索引的文件











# 索引失效或不走索引的原因


- 对索引列进行了运算或使用函数计算

```sql
-- 索引失效原因：索引是针对原值建的二叉树，将列值进行了各种计算后，原来的二叉树就用不上了。
select * from t where id*3=3000


-- 从 MySQL 8.0 开始，索引特性增加了函数索引，即可以针对函数计算后的值建立一个索引，也就是说该索引的值是函数计算后的值，所以就可以通过扫描索引来查询数据。

--通过下面这条语句，对 length(name) 的计算结果建立一个名为 idx_name_length 的索引
alter table t_user add key idx_name_length ((length(name)));

```


- 索引列字段数据类型不一致

  在MySQL中，字符串和数字做比较的话，是将字符串转换成数字。



- 两个表的索引列的字段数据类型不一致

  - 索引列字段和常量比较时，数据类型不一致。

- 字符集不一致

  要比较的字段字符集不一致

- 





# MySQL 多表连接



驱动表的概念是指多表关联查询时，第一个被处理的表，使用此表的记录去关联其他表。

驱动表的确定很关键，会直接影响多表连接的关联顺序，也决定了后续关联时的查询性能。

- 驱动表/主表/前表
- 被驱动表/副表/后表

驱动表的选择遵循一个原则：**`在对最终结果集没影响的前提下，优先选择结果集最小的那张表作为驱动表`**。

**改变驱动表就意味着改变连接顺序，只有在不会改变最终输出结果的前提下才可以对驱动表做优化选择。**

https://blog.csdn.net/lkforce/article/details/102940091



## 连接查询

写过或者学过 SQL 的人应该都知道 left join，知道 left join 的实现的效果，就是保留左表的全部信息，然后把右表往左表上拼接，如果拼不上就是 null。

除了 left join 以外，还有 inner join、outer join、right join，这些不同的 join 能达到的什么样的效果，大家应该都了解了。



驱动表的选择原则

MySQL 会如何选择驱动表，按从左至右的顺序选择第一个？





多表连接的顺序？

假设我们有 3 张表：A、B、C，和如下 SQL

```sql
-- 伪 SQL，不能直接执行
A LEFT JOIN B ON B.aId = A.id  LEFT JOIN C ON C.aId = A.id
WHERE A.name = '666' AND B.state = 1 AND C.create_time > '2019-11-22 12:12:30'
```

是 A 和 B 联表处理完之后的结果再和 C 进行联表处理，还是 A、B、C 一起联表之后再进行过滤处理 ，还是说这两种都不对，有其他的处理方式 ？



join 主要有 Nested Loop、Hash Join、Merge Join 这三种算法方式，最普遍最好的理解的 Nested Loop join 。

顾名思义就是嵌套循环连接。

但是根据场景不同可能有不同的变种：

- Simple Nested-Loop join
- Index Nested-Loop join
- Block Nested-Loop join
- Betched Key Access join



Nested Loop join 翻译过来就是**嵌套循环连接**的意思，那什么又是嵌套循环呢？

嵌套大家应该都能理解，就是一层套一层；那循环呢，你可以理解成是 for 循环。





在正式开始之前，先介绍两个概念：

- 驱动表（也叫主表）：



小表驱动大表。



我们常说，**小表驱动大表，驱动表一定是小表吗？其实更精准一点是指的是根据条件获得的子集合一定要小，而不是说实体表本身一定要小，大表如果获得的子集合小，一样可以简称这个大表为驱动表。 ，最好选择与其他表的主键字段进行比较，或者与已经索引的字段进行比较，这样一来，就有意识地将业务需求的主表**

和被驱动表（也叫非驱动表，还可以叫匹配表，亦可叫内表），简单来说，驱动表就是主表，left join 中的左表就是驱动表，right join 中的右表是驱动表。

一个是驱动表，那另一个就只能是非驱动表了，在 join 的过程中，其实就是从驱动表里面依次（注意理解这里面的依次）取出每一个值，然后去非驱动表里面进行匹配，那具体是怎么匹配的呢？这就是我们接下来讲的这三种连接方式。









## Simple Nested-Loop Join



Simple Nested-Loop Join 是这三种方法里面最简单，最好理解，也是最符合大家认知的一种连接方式。

现在有两张表 table A 和 table B，我们让 **table A left join table B**，如果是用第一种连接方式去实现的话，会是怎么去匹配的呢？直接上图：



![img](assets/1153954-20201210195552830-1911874625.png)





- 上面的 left join 会从**驱动表 table A** 中**逐行取出每一个值**。（在外层循环中）
- 然后去**非驱动表 table B**   中从**上往下依次匹配**。（在内存循环中）

- 然后把匹配到的值进行返回，最后把所有返回值进行合并，这样我们就查找到了 table A left join table B 的结果。

利用这种方法，如果 table A 有 100 行，table B 有 100 行，总共需要执行 10 x 10 = 100 次循环。

**嵌套循环连接join（Nested-Loop Join Algorithms）：是每次匹配1行，匹配速度较慢，需要的内存较少。**

```java
//伪代码表示
List<Row> result = new ArrayList<>();
for(Row r1 in List<Row> t1){
	for(Row r2 in List<Row> t2){
		if(r1.id = r2.tid){
			result.add(r1.join(r2));
		}
	}
}

// 很多人说
```





```sql
-- 在实际 inner join 中，数据库引擎会自动选取数量小的表做为驱动表
-- 驱动表是 t2，被驱动表是 t1。先执行查找的就是驱动表(执行计划结果的id如果一样则按从上到下顺序执行sql);优化器一般会优先选择小表做驱动表。
-- 所以使用 inner join 时，排在前面的表并不一定就是驱动表。
-- 当使用join时，mysql会选择数据量比较小的表作为驱动表，大表作为被驱动表。

-- 当使用left join时，左表是驱动表，右表是被驱动表，当使用right join时，右表时驱动表，左表是被驱动表。

-- 使用了 NLJ算法。一般 join 语句中，如果执行计划 Extra 中未出现 Using join buffer 则表示使用的 join 算 法是NLJ
select * from t1 inner join t2 on t1.id=t2.tid

-- 从表 t2 中读取一行数据(如果t2表有查询过滤条件的，会从过滤结果里取出一行数据);
```





这种暴力匹配的方式在数据库中一般不使用。



举个例子：

select * from t1 inner join t2 on t1.id=t2.tid

（1）t1称为外层表，也可称为驱动表。
（2）t2称为内层表，也可称为被驱动表。



```java
//伪代码表示：
List<Row> result = new ArrayList<>();
for(Row r1 in List<Row> t1){
	for(Row r2 in List<Row> t2){
		if(r1.id = r2.tid){
			result.add(r1.join(r2));
		}
	}
}
```



```shell
# 对于t1,t2,t3这样三个表，t1范围查找，t2索引查找，t3全扫描


Table   Join Type
t1      range
t2      ref
t3      ALL


for each row in t1 matching range {
  for each row in t2 matching reference key {
    for each row in t3 {
      if row satisfies join conditions, send to client
    }
  }
}


# 因为NLJ算法是通过外循环的行去匹配内循环的行，所以内循环的表会被扫描多次。
```

https://blog.csdn.net/weixin_44663675/article/details/112190762

## Block Nested-Loop Join Algorithm

https://dev.mysql.com/doc/refman/8.0/en/nested-loop-joins.html

https://dev.mysql.com/doc/refman/8.0/en/server-system-variables.html#sysvar_join_buffer_size

前面的算法， 逐行查找，每次磁盘IO都读很少数据，自然效率很低。

**块嵌套循环联接（BNL）算法**，将外循环的行缓存起来，读取缓存中的行，减少内循环的表被扫描的次数。

**例如，如果10行读入缓冲区并且缓冲区传递给下一个内循环，在内循环读到的每行可以和缓冲区的10行做比较。**

**这样使内循环表被扫描的次数减少了一个数量级。**



**在 MySQL 8.0.18 之前，如果连接字段没有索引，MySQL 默认会使用这个算法。**

在 MySQL 8.0.18 之后。



MySQL使用联接缓冲区时，会遵循下面这些原则：

- join_buffer_size 系统变量的值决定了每个 join_buffer 的大小。
- 联接类型为ALL、index、range时（换句话说，联接的过程会扫描索引或全表扫描时），MySQL会使用 join_buffer 。
- join_buffer 是分配给每一个能被缓冲的 join，所以一个查询可能会使用多个 join_buffer 。
- 使用到的列才会放到 join_buffer 中，并不是每一个整行数据。
- 缓冲区是分配给每一个能被缓冲的联接，所以一个查询可能会使用多个联接缓冲区。



**注意**

```sql
-- 注意 在 MySQL 中， CROSS JOIN  等价于  INNER JOIN ， 这两个可以互换使用。
-- 但是在标准SQL中，这两个并不一样。

SELECT * FROM t1 LEFT JOIN (t2, t3, t4)  ON (t2.a=t1.a AND t3.b=t1.b AND t4.c=t1.c)

SELECT * FROM t1 LEFT JOIN (t2 CROSS JOIN t3 CROSS JOIN t4)  ON (t2.a=t1.a AND t3.b=t1.b AND t4.c=t1.c)
```













## Index Nested-Loop Join

Index Nested-Loop Join  翻译成中文叫 **索引嵌套循环连接查询**



Index Nested-Loop Join 这种方法中，我们看到了 Index，大家应该都知道这个就是索引的意思。



**这个 Index 是要求非驱动表上要有索引，有了索引以后可以减少匹配次数，匹配次数减少了就可以提高查询的效率了。**

为什么会有了索引以后可以减少查询的次数呢？这个其实就涉及到数据结构里面的一些知识了，给大家举个例子就清楚了



1. 索引嵌套循环连接是基于索引进行连接的算法，索引是基于内层表的，通过**外层表匹配条件**直接与**内层表索引**进行匹配，避免和内层表的每条记录进行比较， 从而利用索引的查询减少了对内层表的匹配次数，优势极大的提升了 join的性能：

> 原来的匹配次数 = 外层表行数 * 内层表行数
> 优化后的匹配次数= 外层表的行数 * 内层表索引的高度

1. 使用场景：只有内层表 join 的列有索引时，才能用到 Index Nested-LoopJoin 进行连接。
2. 由于用到索引，如果索引是辅助索引而且返回的数据还包括内层表的其他数据，则会回内层表查询数据，多了一些IO操作。
3. 





MySQL8.0正式引入了Hash Join 的连接方式。





## 实例



```sql
-- 建表t2
CREATE TABLE `t2` (
  `id` int(11) NOT NULL,
  `a` int(11) DEFAULT NULL,
  `b` int(11) DEFAULT NULL,
  `c` int(11) DEFAULT NULL,
  `d` int(11) DEFAULT NULL, 
  PRIMARY KEY (`id`),
  KEY `a` (`a`),
  KEY `b` (`b`),
  KEY `c` (`c`),
  KEY `d` (`d`)
) ENGINE=InnoDB;

-- t2测试数据
delimiter ;;
create procedure idata2()
begin
  declare i int;
  set i=1;
  while(i<=1000)do
    insert into t2 values(i, i+1, i+2, i+2, i+4);
    set i=i+1;
  end while;
end;;

delimiter ;

-- 调用存储过程
call idata2();


-- 建表t1
create table t1 like t2;
insert into t1 (select * from t2 where id<=100);


-- t1测试数据
delimiter ;;
create procedure idata1()
begin
  declare i int;
  set i=2000;
  while(i<=3000)do
    insert into t1 values(i, i, i, i, i);
    set i=i+1;
  end while;
end;;

delimiter ;

-- 调用存储过程
call idata1();




-- t1 的数据  1-100  2000-3000  一共是1101条数据
-- t2 的数据  1-1000  一共是1000条数据

-- 直接多表查询，笛卡尔积：1101*1000 条数据，一般很少有这样的查询
select *  from t1 , t2   



-- 内连接查询，匹配到了1-100这100行数据
select count(*)  from t1  join t2 on  t1.id=t2.id

-- 查看执行计划


explain select count(*)  from t1  join t2 on  t1.id=t2.id
-- 此时驱动表是t2


explain select t1.* from t1  join t2 on  t1.id=t2.id

explain select t2.* from t1  join t2 on  t1.id=t2.id

-- 不等值连接查询
explain select count(*) from t1  join t2 on  t1.id != t2.id




-- t1 的数据  1-100  2000-3000  一共是1101条数据
-- t2 的数据  1-1000  一共是1000条数据


```









# MySQL 执行计划

在MySQL中，我们可以通过 **EXPLAIN** 命令获取MySQL如何执行 SELECT 语句的信息，包括在 SELECT 语句执行过程中表如何连接和连接的顺序。

Explain 可以使用在` SELECT, DELETE, INSERT, REPLACE, and UPDATE` 语句中，执行的结果会在每一行显示用到的每一个表的详细信息。



简单语句可能结果就只有一行，但是复杂的查询语句会有很多行数据。


MySQL 8.0.18 推荐使用 EXPLAIN ANALYZE，该语句可以输出语句的执行时间和以下信息:


- 预计执行时间
- 预计返回的行数
- 返回第一行的时间
- 迭代器的执行时间，单位毫秒
- 迭代器返回的行数
- 执行循环的次数

查询信息以 TREE 的形式输出，每个节点代表一个迭代器。EXPLAIN ANALYZE 可以用于 SELECT 语句，以及多表的 UPDATE 和 DELETE 语句，MySQL 8.0.19 以后也可以用于 TABLE 语句。EXPLAIN ANALYZE 不能使用 FOR CONNECTION 。MySQL 8.0.20 以后可以通过 KILL QUERY 或 CTRL-C 终止该语句的执行。



### `Explain` 的使用

在 SQL 语句前面加上 `explain `，如：` EXPLAIN SELECT * FROM a;`


```SQL

EXPLAIN [explain_type] {explainable_stmt }
explain_type: 
{ EXTENDED | PARTITIONS | FORMAT = format_name}
 
format_name:
{ TRADITIONAL | JSON}
explainable_stmt:
{ SELECT statement | DELETE statement | INSERT statement | REPLACE statement | UPDATE statement }

-- 以JSON格式显示explain输出
EXPLAIN  format="JSON"  SELECT * FROM a

```




### `Explain` 输出的字段内容

```
id, select_type, table, partitions, type, possible_keys, key, key_len, ref, rows,filtered,extra
```

| 列名          | 含义                                                  |
| :------------ | :---------------------------------------------------- |
| id            | 查询语句的标识                                        |
| select_type   | 查询的类型                                            |
| table         | 当前行所查的表                                        |
| partitions    | 匹配的分区                                            |
| type          | 访问类型                                              |
| possible_keys | 查询可能用到的索引                                    |
| key           | mysql 决定采用的索引来优化查询                        |
| key_len       | 索引 key 的长度                                       |
| ref           | 显示了之前的表在key列记录的索引中查找值所用的列或常量 |
| rows          | 查询扫描的行数，预估值，不一定准确                    |
| filtered      | 查询的表行占表的百分比                                |
| extra         | 额外的查询辅助信息                                    |





### select_type类型

**select_type**:表示查询类型，常见的取值有：

|   类型   |               说明                |
| :------: | :-------------------------------: |
|  SIMPLE  |   简单表，不使用表连接或子查询    |
| PRIMARY  |      主查询，即最外层的查询       |
|  UNION   | UNION中的第二个或者更新后面的查询语句 |
| SUBQUERY |         子查询中的第一个          |
| DERIVED  |              派生表               |





**table**:输出结果集的表（表别名）



### type类型

表示MySQL在表中找到所需行的方式，或者叫访问类型。常见访问类型如下，从上到下，性能由差到最好：

|         ALL         |         全表扫描         | 一般是没有where条件或者where条件没有使用索引的查询语句       |
| :-----------------: | :----------------------: | ------------------------------------------------------------ |
|      **index**      |      **索引全扫描**      | **MySQL遍历整个索引来查询匹配行，并不会扫描表，一般是查询的字段有索引的语句** |
|      **range**      |     **索引范围扫描**     | **索引范围扫描，常用于对索引字段进行 <、<=、>、>=、between等查询操作**          |
| **index_subquery**  |      **索引子查询**      |                                                              |
| **unique_subquery** |    **唯一索引子查询**    |   value IN (SELECT primary_key FROM single_table WHERE some_expr)                                                           |
|   **index_merge**   |       **索引合并**       |                                                              |
|   **ref_or_null**   |                          |                                                              |
|    **fulltext**     |     **全文索引扫描**     |                                                              |
|       **ref**       |    **非唯一索引扫描**    | **使用非唯一索引或唯一索引的前缀扫描，返回匹配某个单独值的记录行** |
|     **eq_ref**      |     **唯一索引扫描**     | **类似ref，区别在于使用的索引是唯一索引，对于每个索引键值，表中只有一条记录匹配** |
|  **const,system**   | **单表最多有一个匹配行** | **单表中最多有一条匹配行，查询起来非常迅速，所以这个匹配行的其他列的值可以被优化器在当前查询中当作常量来处理** |
|      **NULL**       |   **不用扫描表或索引**   |                                                              |



#### ALL场景

**全表扫描，一般是没有where条件或者where条件没有使用索引的查询语句**

> 全表扫描：MySQL要从磁盘读取整个表，逐行遍历并进行计算匹配比对的过程。

```sql
-- customer表中的active字段没有索引：逐行读取并跟查询条件比对
EXPLAIN SELECT * FROM customer WHERE active=0;
```

#### index场景

**索引全扫描，MySQL遍历整个索引来查询匹配行，并不会扫描表**

```sql
-- 一般是查询的字段都有索引的查询语句
EXPLAIN SELECT store_id FROM customer;
```

#### range场景

**索引范围扫描，常用于 <、<=、>、>=、between等操作，仅扫描部分索引行的数据**

```sql
-- 在这种情况下，注意比较的字段要加上索引。否则就是全表扫描
-- 这种也不是绝对的，也有可能走全表扫描，无论什么情况下，只查询需要的列
EXPLAIN SELECT * FROM customer WHERE customer_id>=10 AND customer_id<=20;
EXPLAIN select  apprdate from temp_policy_org_base where apprdate > '8' and apprdate < '10' ;

```

#### [`index_subquery`](https://dev.mysql.com/doc/refman/8.0/en/explain-output.html#jointype_index_subquery)

#### [`unique_subquery`](https://dev.mysql.com/doc/refman/8.0/en/explain-output.html#jointype_unique_subquery)

#### [`index_merge`](https://dev.mysql.com/doc/refman/8.0/en/explain-output.html#jointype_index_merge)

#### [`ref_or_null`](https://dev.mysql.com/doc/refman/8.0/en/explain-output.html#jointype_ref_or_null)

#### fulltext场景

#### ref场景

- 根据索引字段进行等值查询，**返回匹配某个单独值的记录行** （非唯一索引，或者唯一索引的前缀扫描。）

  ```sql
  SELECT * FROM ref_table WHERE key_column=expr;
  ```

- join联表查询

**ref_table、other_table** 表关联查询，关联字段`customer.customer_id`（主键），`payment.customer_id`（非唯一索引）

```sql
    SELECT * FROM ref_table,other_table  WHERE ref_table.key_column=other_table.column;
```



关联查询时必定会有一张表进行全表扫描，此表一定是几张表中记录行数最少的表，然后再通过非唯一索引寻找其他关联表中的匹配行，以此达到表关联时扫描行数最少。



因为**customer**、**payment**两表中**customer**表的记录行数最少，所以**customer**表进行全表扫描，**payment**表通过非唯一索引寻找匹配行。







#### eq_ref场景

表示对于前表的每一个结果，都只能匹配到后表的一行结果。并且查询的比较操作通常是 `=`，查询效率较高。



```shell
SELECT * FROM ref_table,other_table  WHERE ref_table.key_column=other_table.column;
SELECT * FROM ref_table,other_table  WHERE ref_table.key_column_part1=other_table.column AND ref_table.key_column_part2=1;
```





#### system/const场景

**单表中最多有一条匹配行，查询起来非常迅速，所以这个匹配行的其他列的值可以被优化器在当前查询中当作常量来处理。**

场景：将唯一索引或主键，跟常量进行等值匹配查找。

```shell
SELECT * FROM tbl_name WHERE primary_key=1;
SELECT * FROM tbl_name  WHERE primary_key_part1=1 AND primary_key_part2=2;


```

system查找，表中只有一行。system是特殊的const查找情况。







### Extra 类型

Extra 描述了MySQL内部如何进行额外的处理。

关于如何理解MySQL执行计划中Extra列的Using where、Using Index、Using index condition，Using index,Using where这四者的区别。

首先，我们来看看官方文档关于三者的简单介绍（官方文档并没有介绍Using index,Using where这种情况）



#### **Using where**

  表示MySQL Server在存储引擎收到记录后进行"后过滤"（Post-filter）。

如果查询未能使用索引，Using where的作用只是提醒我们MySQL将用where子句来过滤结果集。这个一般发生在MySQL服务器，而不是存储引擎层。

**一般发生在不能走索引扫描的情况下或者走索引扫描，但是有些查询条件不在索引当中的情况下。**

注意，Using where过滤元组和执行计划是否走全表扫描或走索引查找没有关系。

Using where: 仅仅表示MySQL服务器在收到存储引擎返回的记录后进行“后过滤”（Post-filter）。

 不管SQL语句的执行计划是全表扫描（type=ALL)或非唯一性索引扫描（type=ref)。

网上有种说法"Using where：表示优化器需要通过索引回表查询数据" ，上面实验可以证实这种说法完全不正确。



#### **Using Index**

 [覆盖索引](###索引覆盖)：表示直接访问索引就能够获取到所需要的数据（），不需要通过回表查询。

注意：执行计划中的Extra列的“Using index”跟type列的“index”不要混淆。Extra列的“Using index”表示索引覆盖。而type列的“index”表示Full Index Scan。



#### **Using Index Condition**

[索引下推](###索引下推ICP)：会先条件过滤索引，过滤完索引后找到所有符合索引条件的数据行，随后用 WHERE 子句中的其他条件去过滤这些数据行；



#### 




# MySQL排序优化


`order by`排序是一个常见的业务功能，将结果根据指定的字段排序，满足前端展示的需求。


- **通过有序索引顺序扫描直接返回有序数据**

因为索引的数据结构是B+树，索引中的数据是有序的，所以通过where过滤后的结果集如果已经有序，就能避免额外的排序开销操作。

==使用`EXPLAIN`分析查询时，Extra显示为`Using index`表示用到了索引的排序==

比如这样的例子：

```SQL

-- 索引列(key_part1 , key_part2)

--如果是InnoDB表，那么主键也是索引的一部分，这种查询可以使用索引排序
SELECT pk, key_part1, key_part2 FROM t1
  ORDER BY key_part1, key_part2;

-- key_part1是常量，所有通过索引访问到的记录都会按照key_part2 来排序，并且如果where子句有足够的选择性使得索引范围扫描比全表扫描开销更小的话，那么覆盖了(key_part1, key_part2)的复合索引就可以避免排序操作。
SELECT * FROM t1
  WHERE key_part1 = constant
  ORDER BY key_part2;

```

- **Filesort排序，对返回的数据进行排序**

不是通过索引直接返回的已排好序结果的操作都是Filesort排序，也就是说进行了额外的排序操作。

为了获取用于 filesort 操作的内存，优化器会预先分配一个固定大小为`sort_buffer_size`个字节。每个 session 会话可以通过改变这个值来避免过度的内存消耗，或者在必要时分配更多内存。



==使用`EXPLAIN`分析查询时，Extra显示为`Using filesort`表示没有用到索引，用到了额外的排序==

  

**其实 MySQL 会给每个线程分配一块内存用于排序，称为 sort_buffer，由sort_buffer_size这个参数控制，默认是256KB**。



## ORDER BY优化的核心原则



### 全字段排序



**「全字段排序是指，只要与最终结果集有关的字段都会被放进 sort buffer，而不管该字段本身是否参与排序。」**



```sql
create table 't' (
	'id' int(11) not null,
	'city' vachar(16) not null,
	'name' vachar(16) not null,
	'age' vachar(16) not null,
	'addr' varchar(128) default null,
	primary key('id'),
	key 'city'('city')
)engine = InnoDB;

-- 查询city是"杭州"的所有人名字，并且按照name排序返回前 1000 个人的name、age
select city,name,age from t where city = '杭州' order by name limit 1000;
```

为了避免全表扫描，需要在city字段上加上索引

假设满足`city = '杭州'`条件的行是从ID_X到ID_(X+N)的这些记录。

执行流程：

1. 初始化sort_buffer，确定放入name、city、age三个字段;
2. 从索引city找到第一个满足 `city = '杭州'` 条件的主键id，也就是ID_X;
3. 到主键id索引取出整行，取name、city、age三个字段值，存入sort_buffer;
4. 从索引city取下一个记录的主键id;
5. 重复step3、4直到city的值不满足查询条件为止，对应的ID(X+N);
6. 对sort_buffer中的数据按照字段name做快速排序（MySQL内部使用是的**快排算法**）
7. 按照排序结果取前1000行返回给客户端


> tips，sort_buffer是MySQL分配给每个线程用于排序的内存。
sort_buffer是MySQL分配给每个线程用于排序的内存。sort_buffer_size是sort_buffer的大小，如果要排序的数据量小于sort_buffer_size，排序就在内存中完成，如果排序数据量过大，就得使用外部文件（一般磁盘临时文件）辅助排序。外部排序一般使用**归并排序算法**。


简单说，就是通过索引字段查找符合条件的记录之后，然后把结果集需要的全部字段都加载到内存。最后再排序。

显而易见，全字段排序方法缺点：单行大的话占用内存空间。

可以看到当查询条件本身有索引可用的话，全字段排序的排序过程都在 sort buffer（内存）进行，回表次数为符合条件的数据个数。

当然，如果我们建立的是`(city、name、age)`的联合索引，还可以实现"索引覆盖"，即在一棵索引树上取得全部所需数据，减少回表（随机读）次数。

不过针对每个查询或排序语句建立联合索引，会导致索引过多，大大降低写入更新数据的速度，以及大大提升数据所需要的存储空间。

生产上对索引的建立修改需要格外谨慎。



### rowid排序

rowId 就是 MySQL 对每行数据的唯一标识符。

当数据表有主键时，rowId 就是表主键；当数据表没有主键或者主键被删除时，MySQL 会自动生成一个长度为 6 字节的 rowId 为作为 rowId。

==「rowId 排序是指只将与排序相关的字段和 rowId 放入 sort buffer，其余结果集需要用到的数据在排序完成后，通过 rowId 回表取得。」==

全字段排序的流程看着已经十分合理，为什么还需要有个 rowId 排序？

这是我们只需要输出三个字段的情况，假如我们有上百个字段需要返回呢？sort buffer 默认只有 256 KB。能够装下多少行的原始数据行？

所以当待排序的数据行很大的时候，使用全字段排序必然会导致"外部排序"。而且是使用很多临时文件的"外部排序"，效率很低下。

相比全字段排序，rowId 排序的好处是在`sort buffer`大小固定的情况下，`sort buffer`能够容纳更多的数据行，能够避免使用或者少使用"外部排序文件"。

缺点是最终返回结果集的时候，需要再次进行**回表**。


```SQL
SELECT nick_name, age, phone 
FROM t_user 
WHERE city = "深圳" 
ORDER BY nick_name;

```


rowId 排序全过程：

1. 从 city 索引树上找到第一条值为深圳的数据，取得 id 之后回表（回到主键索引）取得 nick_name 这个与排序相关的字段和主键 id 一起放入 sort buffer
2. 从 city 索引树取下一条值为深圳的数据，重复 1 过程，直到下一条数据不满足值为深圳条件
3. 这时候，所有 city = 深圳 的数据都在 sort buffer 了（sort buffer 里面的数据包含两个字段：id 和 nick_name）。对 nick_name 执行快速排序
4. 利用排序好的数据，使用主键 id 再次回表取其他字段，将结果返回

> 注意：在步骤 4 中不会等所有排序好的 id 回表完再返回，而是每个 id 回表一次，取得该行数据之后立即返回，所以不会消耗额外的内存。

[参考1](https://cloud.tencent.com/developer/article/1788764)

[参考2](https://juejin.cn/post/7215736946253430844)



### 优先队列排序

无论是使用全字段排序还是 rowId 排序，都不可避免了对所有符合 WHRER 条件的数据进行了排序。如果我们还搭配着 LIMIT 使用呢？

例如我们在排序语句后添加 LIMIT 3 ，哪怕查出来的数据有 10W 行，我们也只需要前 3 行有序。

为了得到前 3 行数据，而不得不将 10W 行数据载入内存，大大降低了 sort buffer 的利用率。

这时候你可能想到利用"最小堆"、"最大堆"来进行排序。

没错，这正是 MySQL 针对带有 LIMIT 的 ORDER BY 语句的优化：使用优先队列进行排序

[参考3](https://blog.csdn.net/minghao0508/article/details/129463749)

### 如何选择?

现在我们知道有全字段排序和 rowId 排序，那么 MySQL 是如何在这两种排序方案中做选择呢？

由于 rowId 排序相对于全字段排序，不可避免的多了一次回表操作，回表操作意味着随机读，而随机 IO 是数据库中最昂贵的操作。

所以 MySQL 会在尽可能的情况下选择全字段排序。

那么什么情况下 MySQL 会选择 rowId 排序呢，是否有具体的值可以量度？




答案是有的，通过参数`max_length_for_sort_data`可以控制用于排序的行数据最大长度，默认值为 1024 字节。

当单行数据长度超过该值，MySQL 就会觉得如果还用全字段排序，会导致 sort buffer 容纳下的行数太少，从而转为使用 rowId 排序。

==max_length_for_sort_data 只对8.0.20之前的有效==

如果你使用的是其之后的版本，那么无论怎么修改 max_length_for_sort_data 

大部分正常情况下 MySQL 就两种排序方式。如果 sort_buffer_size 够用，那么就在内存中使用快速排序完成排序。


### 临时表排序

通常对于一个执行较慢的排序语句，在使用 EXPLAIN 进行执行过程分析的时候除了能看到`Using filesort`以外，还能看到`Using temporary`，代表在排序过程中使用到了临时表。



**内存临时表排序**

MySQL 优先使用内存临时表。当 MySQL 使用内存临时表时，临时表存储引擎为`memory`

如果当前 MySQL 使用的是内存临时表的话，将会直接使用 rowId 排序，因为这时候所谓的"回表"只是在内存表中读数据，操作不涉及硬盘的随机 IO 读。

使用 rowId 可以在 sort buffer 容纳给多的行，避免或减少外部排序文件的使用。


**磁盘临时表排序**

如果系统中很多需要使用临时表的排序语句执行，而又不加以限制，全都使用临时表的话，内存很快就会被打满。

所以 MySQL 提供了`tmp_table_size`参数限制了内存临时表的大小，默认值是 16M。如果临时表大小超过了tmp_table_size，那么内存临时表就会转成磁盘临时表。

当使用磁盘临时表的时候，表储存引擎将不再是 memory，而是由`internal_tmp_disk_storage_engine`参数控制，默认为 InnoDB 。

这时候 MySQL 会根据单行大小是否超过 max_length_for_sort_data 决定采用全字段排序还是 rowId 排序。


### orderby中的一些小坑

MySQL中，order by 和 limit 使用时有一些小坑，一定要注意。

问题：ORDER BY 排序后，用LIMIT取前几条，发现返回的结果集的顺序与预期的不一样。


```SQL
--先说现象：当order by排序字段存在重复时，不带limit可以正常排序。带了limit发现乱序了。

select * from ratings order by category;
select * from ratings order by category limit 5
```

关于这个现象，官网中有一段描述。

> 在使用ORDER BY对列进行排序时，如果对应（ORDER BY的列）列存在多行相同数据，MySQL Server会按照任意顺序返回这些行，并且可能会根据整体执行计划以不同的方式返回。

对于这种情况，为了保证每次都返回的顺序一致可以额外增加一个排序字段（比如：id），用两个字段来尽可能减少重复的概率。于是，改成 order by status, id;


# group by 优化




# MySQL count 优化



```sql
select count(*) from api_runtime_log;


```



在 **InnoDB 存储引擎**中，**count(\*)** 函数是先从内存中读取数据到**内存缓冲区**，然后进行扫描获得行记录数。

- 这里 InnoDB 会**优先走二级索引**；
- 如果同时存在多个二级索引，会选择**key_len 最小**的二级索引；
- 如果不存在二级索引，那么会走**主键索引**；
- 如果连主键都不存在，那么就走**全表扫描**！





# MySQL 数据转型



[官网手册](https://dev.mysql.com/doc/refman/5.7/en/type-conversion.html)

MySQL 中有各种数据类型，包括：数字，字符、字符串、时间  等几种大类型。



当不同类型的数据进行计算时，可能会发生隐式或显式转换。显式转换一般是各种函数：CONVERT()  CAST() 等等。



> 当操作符与不同类型的操作数一起使用时，会发生类型转换以使操作数兼容。
>
> 举个例子，当操作数是字符跟数字时， MySQL 会根据使用的操作符，转换字符到数字或转换数字成字符。
>
> ```
> mysql> SELECT 1+'1';
>      -> 2
> mysql> SELECT CONCAT(2,' test');
>      -> '2 test'
> ```
>
> 





## 比较操作的隐式转换



- 两个参数至少有一个是 NULL 时，比较的结果也是 NULL，例外是使用 <=> 对两个 NULL 做比较时会返回 1，这两种情况都不需要做类型转换。

  ```sql
  select 1=NULL   -- 结果也是null
  ```

  

- 两个参数都是字符串，会按照字符串来比较，不做类型转换

- 两个参数都是整数，按照整数来比较，不做类型转换



- 字符串和数字比较时，会尝试将字符串转换为数字。









# MySQL 排序和比较规则





## 字符集和校验规则



### 1.1、二进制

binary 。计算机底层存储数据只是一大堆二进制的0和1。

### 1.2、字符

character 。现在有各种各样的字符，包括英文字母，阿拉伯数字，中文，emoji 等等各种特殊字符。



### 1.3 字符编码



### 1.4、字符集

character set 。想要把各种人类可以理解的字符存储到计算机中，就需要建立字符与二进制数字的映射关系。

字符集就是这样的一种映射关系，不同的字符集表示的字符数量不同，字符集越大，所能表示的字符越多，需要占用的二进制位更多，需要的磁盘空间就越大。

MySQL中所支持的字符集存在 `information_schema.CHARACTER_SETS` 表中。

utf8 是 MySQL 中的一种字符集，只支持最长三个字节的 UTF-8 字符，也就是 Unicode 中的基本多文本平面。

**其中 utf8mb4 字符集兼容性最好，它可以存各种语言的字符，包括 emoji 表情等。一般都可以直接使用 utf8mb4  字符集。**



字符集的作用范围：

- schema
- table 
- column 



### 1.5、校验规则(排序规则)



collation 。检验规则，又称排序规则，是用于比较字符和排序的一套规则，即字符的排序规则。比如有的规则区分大小写，有的则无视。

比如我们在比较

如果指定校验规则为"不区分大小写"，那么a和A，e和E就是等价的。

世界上的文字很多，所以才会有“不区分音调”的要求，这时候e、ē、é、ě、è就是等价的。

那么假设我们要进行拼音查找，只要按e去找就可以全部列出来，很方便。甚至，它们也和ê、ë也是等价的，这样就更方便了。

每种字符集都可能有多种检验规则，并且都有一个默认的检验规则(information_schema. CHARACTER_SETS.DEFAULT_COLLATE_NAME)

**每个校验规则只能用于一个字符集，因此字符集与校验规则是一对多的关系。**

校验规则存储在  information_schema. COLLATIONS 表中。一般使用  utf8mb4_general_ci 排序规则。

排序规则命名惯例：字符集名\_对应的语言排序规则_ai/as/ci/cs/ks/bin

​	

- ai  口音不敏感（accent-sensitive ）
- 口音不敏感
- 大写敏感
- 小写敏感
- 

​	语言名一般都是用 general 	

​	其中ci表示大小写不敏感性，cs表示大小写敏感性，bin表示二进制。

​	按字母排序，或者按照二进制排序



utf8mb4_tr_0900_ai_ci

utf8mb4_hu_0900_ai_ci

utf8mb4_turkish_ci

utf8mb4_hungarian_ci





#### 英文排序规则





## 中文字段排序和比较

要进行中文排序，比如通讯录里面的排序列表。啊XX 排到 曾XX 等等。

如果存储汉字的字段编码使用的是GBK字符集，因为GBK内码编码时本身就采用了拼音排序的方法

（常用一级汉字3755个采用拼音排序，二级汉字就不是了，但考虑到人名等都是常用汉字，因此只是针对一级汉字能正确排序也够用了）.

直接在查询语句后面添加 `ORDER BY name ASC`，查询结果将按照姓氏的升序排序；



如果存储字段的不是采用 GBK 编码 。需要在排序的时候对字段进行转码，对应的 SQL 是 `ORDER BY convert(name using gbk) ASC `









