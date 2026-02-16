# 继承



PostgreSQL 支持高级的 object-relational 机制————继承，继承允许一张表继承一张（或多张）表的列属性，来建立 parent-child 关系。

子表可以继承父表的字段以及约束，同时可以拥有自己的字段。

当执行一个父表查询的时候，这个查询可以获取来自本表和它的子表，也可以指定只查询本表。在子表中查询，则不会返回父表的数据。

Inheritance是PostgreSQL独有的，也是前文中我们提到的"使用面向对象的思想来组织数据库"的具体体现之一。


```SQL
CREATE TABLE IF NOT EXISTS cities (   --父表:城市表 
    name            text,
    population      float,
    elevation       int     -- in feet
);


CREATE TABLE IF NOT EXISTS capitals (  --子表:省会表
    state           char(2)
) INHERITS (cities);

```

capitals表继承自cities表的所有属性。

在PostgreSQL里，一个表可以从零个或多个其它表中继承属性，也而且一个查询既可以引用父表中的所有行，可以引用父表的所有行加上其所有子表的行，其中后者是缺省行为。

在这个例子中，父表是城市表。

省会其实也是城市，只是比普通的城市多了一个state字段，表明是哪个省的省会。在上例中capitals表继承了cities表中的所有字段。



假设有洛阳，郑州和开封三个城市，其中郑州是省会城市。插入数据时只需要向capitals插入郑州的数据即可。

根据面向对象的思想，我们可以认为表中的每一行就是一个实例化后的对象，而郑州只应该被实例化一次。

```SQL
INSERT INTO cities VALUES ('洛阳',1500, 50);  --父表插入数据1
INSERT INTO cities VALUES ('开封',1000, 50);  --父表插入数据2
INSERT INTO capitals VALUES ('郑州',2000, 50, 'HN');  --子表插入数据
```

父子表共同的字段的关系并不仅仅是装饰用的。在子表中插入数据，同样在父表是可见，但是只能看到共享的字段。如果你想要在查询父表的数据，忽略子表，可以使用 ONLY 关键字。

>  注意：给子表插入数据的时候，并不是同时把数据中的共享字段插入到父表中，只是简单通过继承关系使子表的数据在父表可见。如果你指定了 ONLY 关键字，则查询不在从子表中获取数据。

```SQL

SELECT * FROM cities ;                        --不带条件查父表，子表和父表数据均被取出：洛阳，开封，郑州
SELECT * FROM cities WHERE population > 0;    --带条件查父表，子表和父表数据均被取出：洛阳，开封，郑州
SELECT * FROM cities WHERE population > 1700; --查父表，子表父表都查，仅查出符合条件的：郑州


-- ONLY关键字表示该查询应该只对cities进行查找而不包括继承级别低于cities的表。SELECT/UPDATE/DELETE都支持这个ONLY关键字
SELECT name, elevation FROM ONLY  cities WHERE population > 1000;  -- 只查父表，only关键字：仅查出符合条件的：洛阳

```

- 由于继承表的本质原因，一些约束条件可能会被打破；例如，声明一个唯一字段，可能在查询结果中2条相同的值。
-  因此，在使用的继承的过程中，你要特别注意约束；因为他们在各自的表中没有违反约束条件；因此，如果你在查询父表的时候没有指定 ONLY 字段，那它可能会返回你非预期的结果。




注意事项

数据删除
如果直接truncate父表，此时父表和其所有子表的数据均被删除。
如果只是truncate子表，那么其父表的数据将不会变化，只是子表中的数据被清空。





- 确定数据来源

```SQL
-- 有时候你可能想知道某条记录来自哪个表。在每个表里我们都有一个系统隐含字段tableoid，它可以告诉你表的来源
SELECT tableoid, name, elevation FROM cities WHERE elevation > 500;
-- 通过tableiod查表名，查的是父表，数据来源实际是子表
SELECT p.relname, c.name, c.elevation FROM cities c,pg_class p WHERE c.elevation > 500 and c.tableoid = p.oid;
```

- 继承并不自动从INSERT或者COPY中向继承级别中的其它表填充数据。在我们的例子里，下面的INSERT语句不会成功：
      INSERT INTO cities (name, population, altitude, state) VALUES ('New York', NULL, NULL, 'NY');
- 我们可能希望数据被传递到capitals表里面去，但是这是不会发生的：INSERT总是插入明确声明的那个表。
- 从设计的角度来看，父子和子表可以各有各的功用。城市表，可以看成是一个更宽泛的概念。
- 继承特性的一个严重的局限性是索引(包括唯一约束)和外键约束只施用于单个表，而不包括它们的继承的子表。
- 这一点不管对引用表还是被引用表都是事实，因此在上面的例子里，如果我们声明cities.name为UNIQUE或者是一个PRIMARY KEY，那么也不会阻止capitals表拥有重复了名字的cities数据行。
- 并且这些重复的行缺省时在查询cities表的时候会显示出来。实际上，缺省时capitals将完全没有唯一约束，因此可能包含带有同名的多个行。
- 你应该给capitals增加唯一约束，但是这样做也不会避免与cities的重复。类似，如果我们声明cities.name REFERENCES某些其它的表，这个约束不会自动广播到capitals。
- 在这种条件下，你可以通过手工给capitals 增加同样的REFERENCES约束来做到这点。



- 多表继承
- 一个表可以从多个父表继承，这种情况下它拥有父表们的字段的总和。子表中任意定义的字段也会加入其中。
- 如果同一个字段名出现在多个父表中，或者同时出现在父表和子表的定义里，那么这些字段就会被"融合"，这样在子表里面就只有一个这样的字段。-
- 要想融合，字段必须是相同的数据类型，否则就会抛出一个错误。融合的字段将会拥有它所继承的字段的所有约束。




