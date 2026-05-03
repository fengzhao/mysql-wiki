## 为什么你必须写好SQL?

在我们工作中，无论是业务人员，还是开发人员，或是管理者，如今，几乎每个人都必须使用某种形式的数据，因为数据毕竟是信息的呈现，要获取信息必须得依赖数据，而这些数据通常是以电子表格或是数据库的形式存放。        

现状1：从业务人员视角来看，在企业里面，我们当前的现状就是，业务人员想要看哪些数据得依赖开发人员从数据库中提取数据，而这一过程需要漫长的等待，影响工作效率，如果我们懂简单的SQL，自己能从数据库提取数据，那么工作效率就会有大的提升，在同样的岗位中能够脱颖而出       

现状2：从数据分析师视角来看，习SQL几乎成为数分必备的技能，如果这个技能不达标，基本上很难通过面试，而且近几年SQL面试的题目也越来越难，要想通过面试几乎成为数据分析师必须且深度掌握的技能。       

现状3：从数据开发者角度来看，对于数据开发者来讲，典型的像数仓同学，基本天天与SQL打交道，这里其实与数据分析岗位有交叉的部分，对于SQL的掌握不言而喻。


SQL语法很简单，但几乎没几个人写的很好

这里不得不提国内语言的鄙视链，在大多数程序员眼里，他们认为SQL称不上一门语言，因为门槛太低，语法很简单就几个命令就能搞定，不需要专门学，或是成为一种岗位。有这种认识的往往都不是从事数据相关的人员，他们实际工作中使用SQL语言也很简单，就是简单的增删改查，甚至有时候面试问他们分组TOPN的问题都会难倒一大片，而对从事数据开发或数据分析师来讲，分组TOPN问题却很简单，这就是平时工作方向的不同带来的误区。不同的岗位有不同的工作方向和重点，我们不能以语言简单程度来区分岗位的优劣，或有鄙视心里，因为毕竟语言只是一种工具，而程序员最重要的还是逻辑思维能力，如果我拿语法比较简单的语言比如SQL去处理复杂的业务逻辑，其实未必就是一件简单的事情，他背后需要的是数据处理的逻辑思维及业务知识，其实此时SQL仅仅只是个工具。


在国外Data Science面试中，对SQL的考察，其实要求很高，很多公司要求必须熟练掌握SQL相关基础语法，并具备极强的数据处理思维逻辑，很多面试者也在SQL考察环节栽了跟头。在众多求职者中，我们分析其原因，这些求职者并不是不懂SQL语法，而是缺乏数据分析的思维能力，缺乏必要的实战技巧。甚至我们经常跟很多经验丰富数仓开发同学去聊，他们在用SQL解决实际业务问题时，都是这样的处理逻辑，遇到要分析的指标，先分析指标的含义，搞清楚逻辑及需要取数的源表后，就开始像套公式般找各种内置的函数去套，看看哪种函数能帮我解决业务问题，像极了某些语言开发者去寻找API的过程。但作为成熟的开发者来说，我们在处理数据问题或写代码时是这样吗？这里我们先打个问号，留给读者自己体会。倘若我们的业务逻辑稍微复杂些，套用函数或API套不动了怎么办？业务不做了吗？去跟业务撕逼吗？哈哈，我想办法总比困难多。这也就是我们所说的工作了好多年，你发现没几个人会把SQL写的很好，实际上呢？遇到复杂的业务逻辑或面试题也会凉凉。。。。。。当然实在不行了，我们也可以换语言实现嘛，总之办法总比困难多。最后，对于一个成熟的SQLer，不仅仅只是停留在实现业务逻辑的角度，更重要的一点还要从底层执行引擎的角度去理解SQL执行过程，看懂执行计划，并能写出性能较高的SQL。
 

## SQL题目练习


```SQL

--创建表student
CREATE TABLE student(
	name VARCHAR(10),
	kecheng VARCHAR(10),
	fengshu INT
)
 
--插入数据到表student中
INSERT INTO student VALUES('张三','语文',81);
INSERT INTO student VALUES('张三','数学',75);
INSERT INTO student VALUES('李四','语文',76);
INSERT INTO student VALUES('李四','数学',90);
INSERT INTO student VALUES('王五','语文',81);
INSERT INTO student VALUES('王五','数学',100);
INSERT INTO student VALUES('王五','英语',90);


-- 查询出每门课都大于80分的学生姓名

-- 因为一个学生有多门课程，可能所有课程都大于80分，可能有些课程大于80分，另外一些课程少于80分，也可能所有课程都小于80分。
-- 那么我们要查找出所有大于80分的课程的学生姓名，我们可以反向思考，找出课程小于80分(可以找出有一些课程小于80分，所有课程小于80分的学生)的学生姓名再排除这些学生剩余的就是所有课程都大于80分的学生姓名了。 

SELECT DISTINCT name FROM student WHERE name NOT IN (SELECT DISTINCT name FROM student WHERE fengshu<=80);

/* not in */ 
SELECT DISTINCT A.name FROM student A WHERE A.name NOT IN(SELECT DISTINCT S.name FROM student S WHERE S.score <80);

/* not exists */ 
SELECT DISTINCT A.name FROM student A  WHERE NOT EXISTS (SELECT 1 FROM student S WHERE  S.score <80 AND S.name =A.name);
```


## SQL案例题



```SQL

-- 建库
CREATE DATABASE `emp`;

-- 打开库
USE emp;

-- 部门信息表(部门编号，部门名称，位置)
CREATE TABLE `dept`( 
    `deptno` INT(2) NOT NULL, 
    `dname` VARCHAR(14), 
    `loc` VARCHAR(13), 
    CONSTRAINT pk_dept PRIMARY KEY(deptno) 
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 员工信息表（员工编号，员工姓名，工作职位，上级领导，入职日期，月薪，津贴，部门编号）
CREATE TABLE `emp` ( 
    `empno` INT(4) NOT NULL PRIMARY KEY, 
    `ename` VARCHAR(10), 
    `job` VARCHAR(9), 
    `mgr` INT(4), 
    `hiredate` DATE, 
    `sal` FLOAT(7,2), 
    `comm` FLOAT(7,2), 
    `deptno` INT(2), 
    CONSTRAINT fk_deptno FOREIGN KEY(deptno) REFERENCES dept(deptno) 
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 薪水等级信息表（等级，最低薪水，最高薪水）
CREATE TABLE `salgrade` ( 
    `grade` INT, 
    `losal` INT, 
    `hisal` INT 
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


-- 数据
INSERT INTO dept VALUES (10,'ACCOUNTING','NEW YORK'); 
INSERT INTO dept VALUES (20,'RESEARCH','DALLAS');
INSERT INTO dept VALUES (30,'SALES','CHICAGO'); 
INSERT INTO dept VALUES (40,'OPERATIONS','BOSTON');
INSERT INTO emp VALUES (7369,'SMITH','CLERK',7902,'1980-12-17',800,NULL,20); 
INSERT INTO emp VALUES (7499,'ALLEN','SALESMAN',7698,'1981-02-20',1600,300,30); 
INSERT INTO emp VALUES (7521,'WARD','SALESMAN',7698,'1981-02-22',1250,500,30); 
INSERT INTO emp VALUES (7566,'JONES','MANAGER',7839,'1981-04-02',2975,NULL,20);
INSERT INTO emp VALUES (7654,'MARTIN','SALESMAN',7698,'1981-09-28',1250,1400,30); 
INSERT INTO emp VALUES (7698,'BLAKE','MANAGER',7839,'1981-05-01',2850,NULL,30); 
INSERT INTO emp VALUES (7782,'CLARK','MANAGER',7839,'1981-06-09',2450,NULL,10); 
INSERT INTO emp VALUES (7788,'SCOTT','ANALYST',7566,'1987-07-13',3000,NULL,20); 
INSERT INTO emp VALUES (7839,'KING','PRESIDENT',NULL,'1981-11-07',5000,NULL,10); 
INSERT INTO emp VALUES(7844,'TURNER','SALESMAN',7698,'1981-09-08',1500,0,30); 
INSERT INTO emp VALUES (7876,'ADAMS','CLERK',7788,'1987-07-13',1100,NULL,20); 
INSERT INTO emp VALUES (7900,'JAMES','CLERK',7698,'1981-12-03',950,NULL,30); 
INSERT INTO emp VALUES (7902,'FORD','ANALYST',7566,'1981-12-03',3000,NULL,20); 
INSERT INTO emp VALUES (7934,'MILLER','CLERK',7782,'1982-01-23',1300,NULL,10);
INSERT INTO salgrade VALUES (1,700,1200); 
INSERT INTO salgrade VALUES (2,1201,1400); 
INSERT INTO salgrade VALUES (3,1401,2000); 
INSERT INTO salgrade VALUES (4,2001,3000); 
INSERT INTO salgrade VALUES (5,3001,9999);
```

```SQL
-- 1. 列出与"SCOTT"从事相同工作的所有员工及部门名称。

-- 获取SCOTT的工作  
SELECT job FROM emp WHERE ename='SCOTT'

-- 关联部门表，获取部门名称，查出（员工，部门）    
SELECT e.ename, d.dname FROM emp e, dept d WHERE e.job =( SELECT job FROM emp WHERE ename = 'SCOTT' ) AND e.ename<>'SCOTT' AND e.deptno=d.deptno


-- 2. 列出公司各个工资等级雇员的数量、平均工资。
SELECT s.grade,count(*),avg(e.sal) FROM emp e LEFT JOIN salgrade s ON e.sal BETWEEN s.losal AND s.hisal GROUP BY s.grade ;

-- 3. 列出薪金高于在部门30工作的所有员工的薪金的员工姓名和薪金、部门名称。
SELECT ename,sal,d.dname,d.deptno FROM emp e LEFT JOIN dept d ON e.deptno = d.deptno WHERE e.sal > (SELECT max(sal) FROM emp WHERE deptno = 30);

-- 4. 列出在每个部门工作的员工数量、平均工资和平均服务期限。
SELECT count(*),avg(sal),avg(YEAR(now())-YEAR(hiredate)) FROM emp GROUP BY deptno;

-- 5. 列出所有员工的姓名、部门名称和工资。
SELECT e.ename,d.dname,e.sal FROM emp e LEFT JOIN dept d ON d.deptno = e.deptno;

-- 6. 列出所有部门的详细信息和部门人数
SELECT d.*,count(e.ename) FROM dept d LEFT JOIN emp e ON e.deptno = d.deptno GROUP BY d.deptno;

-- 7. 列出各种工作的最低工资及从事此工作的雇员姓名。
SELECT t.job ,a.ename , t.minsal FROM emp a LEFT JOIN (SELECT e.job AS job , min(e.sal) AS minsal FROM emp e GROUP BY e.job) t ON a.job = t.job;

-- 8. 列出各个部门的MANAGER(经理)的最低薪金、姓名、部门名称、部门人数。
SELECT a.mm,c.ename,c.job,b.dname,b.cc FROM (SELECT d.deptno,min(sal) mm FROM emp e LEFT JOIN dept d ON e.deptno = d.deptno WHERE job = 'MANAGER' GROUP BY deptno) a LEFT JOIN (SELECT d.deptno,d.dname,count(*) cc FROM emp e LEFT JOIN dept d ON e.deptno = d.deptno GROUP BY d.deptno) b ON a.deptno = b.deptno LEFT JOIN emp c ON c.sal = a.mm AND b.deptno = c.deptno ;

-- 9. 列出所有员工的年工资，所在部门名称，按年薪从低到高排序。
SELECT empno,ename,sal * 12 ,d.dname FROM emp LEFT JOIN dept d ON d.deptno = emp.deptno ORDER BY sal * 12 ASC;

-- 10. 查出某个员工的上级主管及所在部门名称，并要求出这些主管中的月薪超过3000

-- 11. 求出部门名称中，带"S"字符的部门员工的、工资合计、部门人数。

-- 12. 给任职日期超过30年或者在87年雇佣的雇员加薪，加薪原则：10部门增长10%，20部门增长20%， 30部门增长30%，依次类推。

-- 13. 列出至少有一个员工的所有部门的信息。
SELECT  DISTINCT d.* FROM dept d JOIN emp e ON d.deptno = e.deptno; 

-- 14. 列出月薪比JAMES低的所有员工。
SELECT * FROM emp WHERE sal < (SELECT sal FROM emp WHERE ename = 'JAMES')

-- 15. 列出所有员工的姓名以及其直接上级的姓名。
SELECT a.empno,a.ename AS 'e_name',b.ename AS 'm_name' FROM emp a LEFT JOIN emp b ON a.mgr = b.empno;

-- 16. 列出受雇日期早于其直接上级的所有员工的编号、姓名，部门名称。
-- 17. 列出部门名称和这些部门的员工信息，同时列出那些没有员工的部门。
-- 18. 列出所有"CLERK(职员)"的姓名以及部门名称，部门的人数。
-- 19. 列出最低薪金大于1500的各种工作以及从事此工作的全部雇员人数。
-- 20. 列出在部门"SALES"工作的员工的姓名，假定不知道销售部的部门编号。
-- 21. 列出薪金高于公司平均薪金的所有员工，所在部门，上级领导，公司的工资等级。
-- 22. 列出至少有一个员工的所有部门编号、名称，并统计出这些部门的平均工资、最低工资、最高工 资。
-- 23. 列出薪金比“SMITH”或“ALLEN”多的所有员工的编号、姓名、部门名称、其领导姓名。
-- 24. 列出所有员工的编号、姓名及其直接上级的编号、姓名，显示的结果按领导年工资的降序排列。
-- 25. 列出受雇日期早于其直接上级的所有员工的编号、姓名、部门名称、部门位置、部门人数。
-- 26. 列出部门名称和这些部门的员工信息（数量、平均工资），同时列出那些没有员工的部门。
-- 27. 列出所有“CLERK”（办事员）的姓名及其部门名称，部门的人数，工资等级。
-- 28. 列出最低薪金大于1500的各种工作及此从事此工作的全部雇员人数及所在部门名称、位置、平均工 资。
-- 29. 列出在部门“SALES”（销售部）工作的员工的姓名、基本工资、雇佣日期、部门名称，假定不知道 销售部的部门编号。
-- 30. 列出薪金高于公司平均薪金的所有员工，所在部门，上级领导，公司的工资等级。
-- 31. 列出与“SCOTT”从事相同工作的所有员工及部门名称，部门人数。
-- 32. 查询dept表的结构
-- 33. 检索emp表，用is a 这个字符串来连接员工姓名和工种两个字段
-- 34. 检索emp表中有提成的员工姓名、月收入及提成。

```


















```SQL

-- DDL

-- 学生表
-- Student(SId,Sname,Sage,Ssex)
-- SId 学生编号,Sname 学生姓名,Sage 出生年月,Ssex 学生性别

-- 课程表
-- Course(CId,Cname,TId)
-- CId 课程编号,Cname 课程名称,TId 教师编号

-- 教师表
-- Teacher(TId,Tname)
-- TId 教师编号,Tname 教师姓名

-- 成绩表
-- SC(SId,CId,score)
-- SId 学生编号,CId 课程编号,score 分数

CREATE TABLE Student(sid VARCHAR(10),sname VARCHAR(10),sage DATETIME,ssex nvarchar(10));  
INSERT INTO Student VALUES('01' , '赵雷' , '1990-01-01' , '男');  
INSERT INTO Student VALUES('02' , '钱电' , '1990-12-21' , '男');  
INSERT INTO Student VALUES('03' , '孙风' , '1990-05-20' , '男');  
INSERT INTO Student VALUES('04' , '李云' , '1990-08-06' , '男');  
INSERT INTO Student VALUES('05' , '周梅' , '1991-12-01' , '女');  
INSERT INTO Student VALUES('06' , '吴兰' , '1992-03-01' , '女');  
INSERT INTO Student VALUES('07' , '郑竹' , '1989-07-01' , '女');  
INSERT INTO Student VALUES('08' , '王菊' , '1990-01-20' , '女');  
CREATE TABLE Course(cid VARCHAR(10),cname VARCHAR(10),tid VARCHAR(10));  
INSERT INTO Course VALUES('01' , '语文' , '02');  
INSERT INTO Course VALUES('02' , '数学' , '01');  
INSERT INTO Course VALUES('03' , '英语' , '03');  
CREATE TABLE Teacher(tid VARCHAR(10),tname VARCHAR(10));  
INSERT INTO Teacher VALUES('01' , '张三');  
INSERT INTO Teacher VALUES('02' , '李四');  
INSERT INTO Teacher VALUES('03' , '王五');  
CREATE TABLE SC(sid VARCHAR(10),cid VARCHAR(10),score DECIMAL(18,1));  
INSERT INTO SC VALUES('01' , '01' , 80);  
INSERT INTO SC VALUES('01' , '02' , 90);  
INSERT INTO SC VALUES('01' , '03' , 99);  
INSERT INTO SC VALUES('02' , '01' , 70);  
INSERT INTO SC VALUES('02' , '02' , 60);  
INSERT INTO SC VALUES('02' , '03' , 80);  
INSERT INTO SC VALUES('03' , '01' , 80);  
INSERT INTO SC VALUES('03' , '02' , 80);  
INSERT INTO SC VALUES('03' , '03' , 80);  
INSERT INTO SC VALUES('04' , '01' , 50);  
INSERT INTO SC VALUES('04' , '02' , 30);  
INSERT INTO SC VALUES('04' , '03' , 20);  
INSERT INTO SC VALUES('05' , '01' , 76);  
INSERT INTO SC VALUES('05' , '02' , 87);  
INSERT INTO SC VALUES('06' , '01' , 31);  
INSERT INTO SC VALUES('06' , '03' , 34);  
INSERT INTO SC VALUES('07' , '02' , 89);  
INSERT INTO SC VALUES('07' , '03' , 98);



-- 1. 查询“01”课程比“02”课程成绩高的所有学生的学号；
SELECT DISTINCT t1.sid AS sidfrom   
    (SELECT * FROM sc WHERE cid='01')t1  
LEFT JOIN   
    (SELECT * FROM sc WHERE cid='02')t2  
ON t1.sid=t2.sid  
WHERE t1.score>t2.score

-- 2. 查询平均成绩大于60分的同学的学号和平均成绩；
SELECT   
    sid  
    ,avg(score)  
FROM sc  
GROUP BY sid  
HAVING avg(score)>60

-- 3. 查询所有同学的学号、姓名、选课数、总成绩
SELECT  
    student.sid AS sid  
    ,sname  
    ,count(DISTINCT cid) course_cnt  
    ,sum(score) AS total_score  
FROM student  
LEFT JOIN sc  
ON student.sid=sc.sid  
GROUP BY sid,sname

-- 4. 查询姓“李”的老师的个数；
SELECT  
    count(DISTINCT tid) AS teacher_cnt  
FROM teacher  
WHERE tname LIKE '李%'

-- 5. 查询没学过“张三”老师课的同学的学号、姓名；
SELECT  
    sid,sname  
FROM student  
WHERE sid NOT IN   
    (  
        SELECT  
            sc.sid  
        FROM teacher  
        LEFT JOIN course  
            ON teacher.tid=course.tid  
        LEFT JOIN sc  
            ON course.cid=sc.cid  
        WHERE teacher.tname='张三'  
    )

-- 6. 查询学过“01”并且也学过编号“02”课程的同学的学号、姓名；
SELECT  
    t.sid AS sid  
    ,sname  
FROM   
    (  
        SELECT  
            sid  
            ,count(IF(cid='01',score,NULL)) AS count1  
            ,count(IF(cid='02',score,NULL)) AS count2  
        FROM sc  
        GROUP BY sid  
        HAVING count(IF(cid='01',score,NULL))>0 AND count(IF(cid='02',score,NULL))>0  
    )t  
LEFT JOIN student  
    ON t.sid=student.sid

-- 7. 查询学过“张三”老师所教的课的同学的学号、姓名；
SELECT  
    student.sid  
    ,sname  
FROM   
    (  
        SELECT  
            DISTINCT cid   
        FROM course  
        LEFT JOIN teacher   
        ON course.tid=teacher.tid  
        WHERE teacher.tname='张三'  
    )course  
LEFT JOIN sc   
    ON course.cid=sc.cid  
LEFT JOIN student  
    ON sc.sid=student.sid  
GROUP BY student.sid,sname

-- 8. 查询课程编号“01”的成绩比课程编号“02”课程低的所有同学的学号、姓名；
SELECT  
    t1.sid,sname  
FROM   
    (  
        SELECT DISTINCT t1.sid AS sid  
        FROM   
            (SELECT * FROM sc WHERE cid='01')t1  
        LEFT JOIN   
            (SELECT * FROM sc WHERE cid='02')t2  
        ON t1.sid=t2.sid  
        WHERE t1.score>t2.score  
    )t1  
LEFT JOIN student  
    ON t1.sid=student.sid

-- 9. 查询所有课程成绩小于60分的同学的学号、姓名；
SELECT  
    t1.sid,sname  
FROM   
    (  
        SELECT  
            sid,max(score)  
        FROM sc  
        GROUP BY sid  
        HAVING max(score<60)  
    )t1  
LEFT JOIN student  
    ON t1.sid=student.sid

-- 10. 查询没有学全所有课的同学的学号、姓名；
SELECT  
    t1.sid,sname  
FROM   
    (  
        SELECT  
            count(cid),sid  
        FROM sc  
        GROUP BY sid  
        HAVING count(cid) < (SELECT count(DISTINCT cid) FROM course)  
    )t1  
LEFT JOIN student  
    ON t1.sid=student.sid

-- 11. 查询至少有一门课与学号为“01”的同学所学相同的同学的学号和姓名；
SELECT  
    DISTINCT sc.sid  
FROM   
    (  
        SELECT  
            cid  
        FROM sc  
        WHERE sid='01'  
    )t1  
LEFT JOIN sc  
    ON t1.cid=sc.cid

-- 12. 查询和"01"号的同学学习的课程完全相同的其他同学的学号和姓名
#注意是和'01'号同学课程完全相同但非学习课程数相同的,这里我用左连接解决这个问题select  
    t1.sid,sname  
FROM  
    (  
        SELECT  
            sc.sid  
            ,count(DISTINCT sc.cid)  
        FROM   
            (  
                SELECT  
                    cid  
                FROM sc  
                WHERE sid='01'  
            )t1 #选出01的同学所学的课程  
        LEFT JOIN sc  
            ON t1.cid=sc.cid  
        GROUP BY sc.sid  
        HAVING count(DISTINCT sc.cid)= (SELECT count(DISTINCT cid) FROM sc WHERE sid = '01')  
    )t1  
LEFT JOIN student  
    ON t1.sid=student.sid  
WHERE t1.sid!='01'

-- 13. 把“SC”表中“张三”老师教的课的成绩都更改为此课程的平均成绩；
-- 暂跳过update题目


-- 14. 查询没学过"张三"老师讲授的任一门课程的学生姓名
SELECT   
    sname  
FROM student  
WHERE sid NOT IN  
    (  
        SELECT  
            DISTINCT sid  
        FROM sc  
        LEFT JOIN course  
            ON sc.cid=course.cid  
        LEFT JOIN teacher  
            ON course.tid=teacher.tid   
        WHERE tname='张三'  
    )

-- 15. 查询两门及其以上不及格课程的同学的学号，姓名及其平均成绩
SELECT  
    t1.sid,sname,avg_score  
FROM   
    (  
        SELECT  
            sid,count(IF(score<60,cid,NULL)),avg(score) AS avg_score  
        FROM sc  
        GROUP BY sid  
        HAVING count(IF(score<60,cid,NULL)) >=2  
    )t1  
LEFT JOIN student  
    ON t1.sid=student.sid

-- 16. 检索"01"课程分数小于60，按分数降序排列的学生信息
SELECT   
    sid,IF(cid='01',score,100)FROM sc  
WHERE IF(cid='01',score,100)<60  
ORDER BY IF(cid='01',score,100) DESC

-- 17. 按平均成绩从高到低显示所有学生的平均成绩
SELECT sid,avg(score)  
FROM sc  
GROUP BY sid  
ORDER BY avg(score) DESC

-- 18. 查询各科成绩最高分、最低分和平均分：以如下形式显示：课程ID，课程name，最高分，最低分，平均分，及格率
SELECT  
    sc.cid  
    ,cname  
    ,max(score) AS max_score  
    ,min(score) AS min_score  
    ,avg(score) AS avg_score  
    ,count(IF(score>=60,sid,NULL))/count(sid) AS pass_rate  
 FROM sc   
 LEFT JOIN course  
    ON sc.cid=course.cid  
 GROUP BY sc.cid

-- 19. 按各科平均成绩从低到高和及格率的百分数从高到低顺序
#这里先按照平均成绩排序，再按照及格百分数排序，  
SELECT   
    cid  
    ,avg(score) AS avg_score  
    ,count(IF(score>=60,sid,NULL))/count(sid) AS pass_rate  
FROM sc  
GROUP BY cid  
ORDER BY avg_score,pass_rate DESC

-- 20. 查询学生的总成绩并进行排名
SELECT  
    sid  
    ,sum(score) AS sum_score  
FROM sc  
GROUP BY sid  
ORDER BY sum_score DESC

-- 21. 查询不同老师所教不同课程平均分从高到低显示
SELECT  
    tid  
    ,avg(score) AS avg_score  
FROM course  
LEFT JOIN sc  
    ON course.cid=sc.cid  
GROUP BY tid  
ORDER BY avg_score DESC

-- 22. 查询所有课程的成绩第2名到第3名的学生信息及该课程成绩
SELECT  
    sid,rank_num,score,cid  
FROM  
    (  
        SELECT  
            rank() OVER(PARTITION BY cid ORDER BY score DESC) AS rank_num  
            ,sid  
            ,score  
            ,cid  
        FROM sc  
    )t  
WHERE rank_num IN (2,3)

-- 23. 统计各科成绩各分数段人数：课程编号,课程名称,[100-85],[85-70],[70-60],[0-60]及所占百分比
SELECT  
    sc.cid  
    ,cname  
    ,count(IF(score BETWEEN 85 AND 100,sid,NULL))/count(sid)  
    ,count(IF(score BETWEEN 70 AND 85,sid,NULL))/count(sid)  
    ,count(IF(score BETWEEN 60 AND 70,sid,NULL))/count(sid)  
    ,count(IF(score BETWEEN 0 AND 60,sid,NULL))/count(sid)  
FROM sc  
LEFT JOIN course  
    ON sc.cid=course.cid  
GROUP BY sc.cid,cname

-- 24. 查询学生平均成绩及其名次
SELECT  
    sid  
    ,avg_score  
    ,rank() OVER (ORDER BY avg_score DESC)  
FROM   
    (  
        SELECT  
            sid  
            ,avg(score) AS avg_score  
        FROM sc  
        GROUP BY sid  
    )t

-- 25. 查询各科成绩前三名的记录
SELECT  
    sid,cid,rank1from   
    (  
        SELECT  
            cid  
            ,sid  
            ,rank() OVER(PARTITION BY cid ORDER BY score DESC) AS rank1  
        FROM sc  
    )twhere rank1<=3

-- 26. 查询每门课程被选修的学生数
SELECT  
    count(sid)  
    ,cid  
FROM sc  
GROUP BY cid

-- 27. 查询出只选修了一门课程的全部学生的学号
SELECT  
    sid  
FROM sc  
GROUP BY sid  
HAVING count(cid) =1

-- 28. 查询男生、女生人数
SELECT  
    ssex  
    ,count(DISTINCT sid)  
FROM student          
GROUP BY ssex

-- 29. 查询名字中含有"风"字的学生信息
SELECT  
    sid,sname  
FROM student  
WHERE sname LIKE '%风%'

-- 30. 查询同名同性学生名单，并统计同名人数
SELECT  
    ssex  
    ,sname  
    ,count(sid)  
FROM student  
GROUP BY ssex,sname  
HAVING count(sid)>=2

-- 31. 查询1990年出生的学生名单(注：Student表中Sage列的类型是datetime)
SELECT  
    sid,sname,sage  
FROM student  
WHERE YEAR(sage)=1990

-- 32. 查询每门课程的平均成绩，结果按平均成绩升序排列，平均成绩相同时，按课程号降序排列
SELECT  
    cid,avg(score) AS avg_score  
FROM sc  
GROUP BY cid  
ORDER BY avg_score,cid DESC

-- 33. 查询不及格的课程，并按课程号从大到小排列
SELECT  
    cid,sid,score  
FROM sc  
WHERE score<60  
ORDER BY cid DESC,sid

-- 34. 查询课程编号为"01"且课程成绩在60分以上的学生的学号和姓名；
SELECT  
    sid,cid,score  
FROM sc  
WHERE cid='01' AND score>60

-- 35. 查询选修“张三”老师所授课程的学生中，成绩最高的学生姓名及其成绩
SELECT  
    sc.sid,sname,cname,score  
FROM sc  
LEFT JOIN course  
    style="font-weight: 600;">=course.cid  
LEFT JOIN teacher  
    style="font-weight: 600;">=teacher.tid  
LEFT JOIN student  
    style="font-weight: 600;">=student.sid  
WHERE tname='张三'  
ORDER BY score DESC  
LIMIT 1;

-- 36. 查询每门功课成绩最好的前两名
SELECT  
    cid,sid,rank1  
FROM   
    (  
        SELECT  
            cid  
            ,sid  
            ,rank() OVER(PARTITION BY cid ORDER BY score DESC) AS rank1  
        FROM sc   
    )t  
WHERE rank1 <=2

-- 37. 统计每门课程的学生选修人数（超过5人的课程才统计）。要求输出课程号和选修人数，查询结果按人数降序排列，若人数相同，按课程号升序排列
SELECT  
    cid  
    ,count(sid) AS cnt  
FROM sc  
GROUP BY cid  
HAVING cnt>=5  
ORDER BY count(sid) DESC,cid

-- 38. 检索至少选修两门课程的学生学号
SELECT  
    sid  
    ,count(cid)  
FROM sc  
GROUP BY sid  
HAVING count(cid)>=2

-- 39. 查询选修了全部课程的学生信息
SELECT  
    sid  
    ,count(cid)  
FROM sc  
GROUP BY sid  
HAVING count(cid)=(SELECT count(DISTINCT cid) FROM sc)

-- 40. 查询各学生的年龄
SELECT  
    sid,sname,YEAR(curdate())-YEAR(sage) AS sage  
FROM student

-- 41. 查询本周过生日的学生
SELECT  
    sid,sname,sage  
FROM student  
WHERE weekofyear(sage)=weekofyear(curdate())

-- 42. 查询下周过生日的学生
SELECT   
    sid,sname,sage  
FROM student  
WHERE weekofyear(sage) = weekofyear(date_add(curdate(),interval 1 week))

-- 43 查询本月过生日的学生
SELECT  
    sid,sname,sage  
FROM student  
WHERE month(sage) = month(curdate())

-- 44. 查询下月过生日的学生
SELECT  
    sid,sname,sage  
FROM student  
WHERE month(date_sub(sage,interval 1 month)) = month(curdate())

```




