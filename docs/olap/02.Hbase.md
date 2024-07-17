HBase是一种分布式、可扩展、支持海量数据存储的NoSQL数据库。

逻辑上，HBase的数据模型同关系型数据库很类似，数据存储在一张表中，有行有列。但从HBase的底层物理存储结构（K-V）来看，HBase更像是一个多维度的map

它主要适用于海量明细数据（十亿、百亿）的随机实时查询，如日志明细、交易清单、轨迹行为等。

它使用的文件系统是可插拔的，也就是说它既可以使用本地的文件系统，又可以使用更高一层抽象的系统如HDFS作为文件系统，实际上HDFS是HBase最常用的文件系统。




## 术语

> Namespace

命名空间，类似于关系型数据库的DataBase概念，每个命名空间下有多个表。HBase有两个自带的命名空间分别是hbase和default。hbase中存放的是HBase内置的表， default表是用户默认使用的命名空间。

2）Region

按照数据量切分的行组成的切片称为Region。

3）Row

HBase表中的每行数据都由一个RowKey和多个Column（列）组成，数据是按照RowKey的字典顺序存储的，并且查询数据时只能根据 RowKey 进行检索，所以RowKey的设计十分重要。

4）Column

HBase中的每个列都由Column Family（列族）和Column Qualifier（列限定符）进行限定。建表时只需指明列族，而列限定符无需预先定义。

5）Timestamp

用于标识数据的不同版本（version），每条数据写入时，如果不指定时间戳，系统会自动为其加上该字段，其值为写入HBase的时间。

6）Cell

由{rowkey, column Family:column Qualifier, timestamp}唯一确定的单元。cell中的数据是没有类型的，全部是字节码形式存储。



```xml

<!-- 每个regionServer的共享目录,用来持久化Hbase,默认情况下在/tmp/hbase下面 -->  
<property> 
  <name>hbase.rootdir</name>  
  <value>/hbase</value>  
</property>  

<!-- hbase集群模式,false表示hbase的单机，true表示是分布式模式 -->  
<property>  
  <name>hbase.cluster.distributed</name>  
  <value>true</value>  
</property>  

<!-- hbase master节点的端口 -->  
<property>  
  <name>hbase.master.port</name>  
  <value>16000</value>
</property> 

<!-- hbase master的web ui页面的端口 -->  
<property>  
  <name>hbase.master.info.port</name>  
  <value>16010</value>  
</property>  

<!-- hbase master的web ui页面绑定的地址 -->  
<property> 
  <name>hbase.master.info.bindAddress</name>  
  <value>0.0.0.0</value>
</property>

<!-- hbase依赖的zk地址 -->  
<property>  
  <name>hbase.zookeeper.quorum</name>  
  <value>centos161,centos162,centos163</value>  
</property>

<!-- zookeeper的工作目录 -->
<property>  
  <name>hbase.zookeeper.property.dataDir</name>  
  <value>/opt/module/zookeeper/data</value>  
</property>  

<!-- 一个region进行major compaction合并的周期，在这个点的时候，这个region下的所有hfile会进行合并，默认是7天。major   
        compaction非常耗资源,建议生产关闭(设置为0)，在应用空闲时间手动触发【compact 表名】 -->  
<property>  
  <name>hbase.hregion.majorcompaction</name>  
  <value>604800000</value>  
</property>  

<!-- 一个抖动比例，意思是说上一个参数设置是7天进行一次合并，也可以有50%的抖动比例，生产环境majorcompaction应该被关闭，此参数就不重要了 -->  
<property>  
  <name>hbase.hregion.majorcompaction.jitter</name>  
  <value>0.50</value>  
</property>  

<!-- 一个store里面允许存的hfile的个数，超过这个个数会被写到新的一个hfile里面 也即是每个region的每个列族对应的memstore在fulsh为hfile的时候，默认情况下当达到3个hfile的时候就会对这些文件进行合并重写为一个新文件，设置个数越大可以减少触发合并的时间，但是每次合并的时间就会越长 -->  
<property>  
  <name>hbase.hstore.compactionThreshold</name>  
  <value>3</value>  
</property>

<!-- #######################################以下是非必须配置参数####################################### -->
<!-- regionServer的全局memstore的大小，超过该大小会触发flush到磁盘的操作，默认是堆大小的40%，而且regionserver级别的flush会阻塞客户端读写 -->  
<property>  
  <name>hbase.regionserver.global.memstore.size</name>  
  <value></value>  
</property> 

<!-- 可以理解为一个安全的设置，有时候集群的“写负载”非常高，写入量一直超过flush的量，这时我们就希望memstore不要超过一定的安全设置。在这种情况下，写操作就要被阻塞一直到memstore恢复到一个“可管理”的大小，这个大小就是默认值是堆大小*0.4*0.95，也就是当regionserver级别的flush操作发送后，会阻塞客户端写，一直阻塞到整个regionserver级别的memstore的大小为堆大小*0.4*0.95为止 -->  
<property>  
  <name>hbase.regionserver.global.memstore.size.lower.limit</name>  
  <value></value>  
</property>  

<!-- 内存中的文件在自动刷新之前能够存活的最长时间，默认是1h -->  
<property>  
  <name>hbase.regionserver.optionalcacheflushinterval</name>  
  <value>3600000</value>  
</property>


<!-- 单个region里memstore的缓存大小，超过那么整个HRegion就会flush,默认128M -->  
<property>  
  <name>hbase.hregion.memstore.flush.size</name>  
  <value>134217728</value>  
</property>  

```