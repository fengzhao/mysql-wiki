# 概述

在如今开源数据库的时代，越来越多的人开始研究数据库的源码，并给社区贡献代码，MySQL 官方每次发布新版本都要感谢一些在社区上贡献代码的程序员。
现在新的数据库时代也给 DBA 提出了更高的要求，学会调试源码，通过源码定位问题，这是 DBA 进阶的方向。MySQL 的源码有几百上千万行，想全部搞懂几乎是不可能的，研究源码一般推荐从某个功能点入手。
而学会调试源码，不管对研究源码或通过源码定位问题，都是必备的技能。

一般在实际应用中，`MySQL` 都是运行在 `Linux` 平台下，在 `Linux` 平台下一般是通过 `GDB(GNU symbolic debugger)`工具进行调试，`C/C++` 项目的开发和调试包括故障排查都是利用 `GDB` 完成的。

此外， `VSCODE` 这种 `IDE` 工具可以在本地的 `Windows` 操作系统下，通过 `ssh` 远程调试 `Linux` 平台下的 `MySQL` 。如果要在 Windows 上调试 Windows Vscode 插件

- 中文语言包
- Remote
- C/C++
- C/C++ Clang Command Adapter
- CodeLLDB
- CMake Tools

装完后，左侧会显示：分上下两栏。上栏是你本地 `Windows` 上装的 VSCode 插件；下栏是你远端 `Linux` 上装的 `VSCode` 插件。

- **<span style="color:red">重要的事情提前说：mysql8.x 是天坑，编译时文件解压的空间强烈建议>40G！！！！30G 真得很勉强，成功全靠运气！编译等了 one hour，系统告诉你硬盘空间不足：）</span>**
- **<span style="color:red">重要的事情提前说：请准备好足够的时间，我 8 核 16G 的服务器，编译了很长时间，大概是三个多小时。</span>**
- **<span style="color:red">重要的事情提前说：编译异常后，需要删除对应的 cmake cache 后再次进行编译，否则每次都会读取缓存进行相同的报错。</span>**

**源代码版本选择**

首先需要从[官网](https://cdn.mysql.com//Downloads/MySQL-8.4/mysql-8.4.10.tar.gz)下载源码，操作系统选择为 `source code`，操作系统版本选择为 `ALL OPERATING SYSTEM`，下载带 `boost` 头文件的源码包。如果对 `MySQL` 的版本没有特别要求的话，一般推荐下载最新版本的。
因为老版本中存在 `bug` 的概率较大，编译过程需要解决这些 `bug`，比如在 `8.0.23` 版本中编译过程中报了这个错：`buf0buf.cc:1227:44: error: ‘SYS_gettid’ was not declared in this scope`。
参考 `MySQL` 官方论坛：https://forums.mysql.com/read.php?117,674410,676378#msg-676378，在`storage/innobase/buf/buf0flu.cc`文件代码中加上声明`#include <sys/syscall.h>`，解决了这个报错。

"从 MySQL 8.3 开始，你再也不用自己去下载 Boost 库了，官方已经把它直接内置（Bundled）在 MySQL 的源码包里了。"

**环境配置**

- 硬件环境配置：8 核 + 16GiB + 200GiB 的服务器
- 操作系统环境：Ubuntu 24.04.3 LTS
- 软件环境
  - cmake version 3.16.3 （（Require 需要源码安装 cmake3.5.1+，但 cmake 不要升级到最新。 3.5.1 版本、3.5.2 版本即可。因为 3.20+版本编译 mysql8.0 会报各种错误）
  - GNU Make 4.2.1 （Require GNU make 3.75 or later GNU Make 4.2.1）
  - GCC gcc version 9.4.0 ( MySQL 8.4 source code permits use of C++17 features , Linux: GCC 10 )

```bash
# 准备环境
apt install -y cmake make gcc g++ libncurses5-dev bison openssl libssl-dev git autoconf automake libtool  unzip build-essential perl pkg-config libtirpc-dev

# 创建目录
mkdir -p /data/{mysql_source_code,mysql_install_dir,mysql_data}  && cd /data/mysql_source_code

# 直接去 https://dev.mysql.com/downloads/mysql/ 直接下载带 Boost 第三方库依赖的源码。8.3之后的源代码包内置了boost库，所以不需要去下载boost库。
# Boost 是一个功能强大、构造精巧、跨平台、开源并且完全免费的 C++ 程序库，可以认为是半个C++标准库。
# MySQL 的代码依赖 Boost库，所以直接下载一个携带Boost库的源码比较省心，不需要再去下载对应的Boost库。
wget https://cdn.mysql.com//Downloads/MySQL-8.4/mysql-8.4.10.tar.gz  -P  /data/mysql_source_code

# libboost-all-dev 包会安装 Boost 库的所有主要组件（包括头文件和编译好的库文件），涵盖了开发所需的一切。
sudo apt update
sudo apt install libboost-all-dev

# wget https://cdn.mysql.com//Downloads/MySQL-8.4/mysql-8.4.10.tar.gz

# 解压
cd /data/mysql_source_code/  && tar -zxvf mysql-8.4.10.tar.gz

# 在源代码目录里面，创建build目录并进入
mkdir -p /data/mysql_source_code/mysql-8.4.10/build/ && cd /data/mysql_source_code/mysql-8.4.10/build/

# Configure , 负责将源代码与当前系统进行配置和适配。
cmake .. \
    -DWITH_DEBUG=1 \
    -DCMAKE_BUILD_TYPE=Debug \
    -DWITH_INNOBASE_STORAGE_ENGINE=1 \
    -DWITH_ARCHIVE_STORAGE_ENGINE=1 \
    -DWITH_BLACKHOLE_STORAGE_ENGINE=1 \
    -DWITH_FEDERATED_STORAGE_ENGINE=1 \
    -DWITH_PARTITION_STORAGE_ENGINE=1 \
    -DMYSQL_TCP_PORT=3306 \
    -DENABLED_LOCAL_INFILE=1 \
    -DEXTRA_CHARSETS=all \
    -DDEFAULT_CHARSET=utf8mb4 \
    -DDEFAULT_COLLATION=utf8mb4_general_ci \
    -DMYSQL_USER=mysql \
    -DCMAKE_INSTALL_PREFIX=/data/mysql_install_dir

# 参数含义
# DWITH_DEBUG=1                         这个是最关键的配置，是为了开启debug调试模式;
# DCMAKE_INSTALL_PREFIX=                表示编译状态的路径，选择源码文件夹之外的一个自建的build文件夹;
# DWITH_BOOST=                          指定 boost 路径，可以直接指向源码文件夹下的boost文件夹；
# DCMAKE_BUILD_TYPE=1                   表示开启debug，方便后续代码调试；
# DWITH_BLACKHOLE_STORAGE_ENGINE=1      表示开启BLACKHOLE存储引擎
# DWITH_PARTITION_STORAGE_ENGINE=1      表示开启PARTITION存储引擎
# DWITH_FEDERATED_STORAGE_ENGINE=1      表示开启FEDERATED存储引擎
# DCMAKE_INSTALL_PREFIX=                这个表示BASEDIR路径，默认是/usr/local/mysql，是各种配置的路径前缀PREFIX
# DMYSQL_DATADIR：                      这个表示表示MySQL默认的数据目录，选择build文件夹下的data文件
# 其他详细参数参考官网 https://dev.mysql.com/doc/refman/8.4/en/source-configuration-options.html
# Cmake构建参数，主要分为几类：
# 1. 通用参数：
# 2. 安装布局参数：
# 3. 存储参数：
# 4. 特性参数：

# 根据 Makefile 中的规则进行实际的编译过程，生成可执行文件或库。
make -j4

# 负责将最终编译好的文件复制到指定的安装目录中，相当于常规软件的编译安装一样。
make install

# 当然，也可以使用make package来生成安装包（就像二进制包一样）
# 这样输出就是mysql-8.4.10-linux-x86_64.tar.gz格式的二进制包了


# 接着make install成功后，配置一个简单的常规配置文件/etc/my.cnf，就可以初始化数据库并启动数据库了。
[mysqld]
basedir  = /data/mysql_install_dir
datadir  = /data/mysql_data
socket   = /data/mysql_data/mysql.sock

groupadd mysql
useradd -r -g mysql -s /bin/false mysql
chown -R mysql:mysql  /data/mysql_data/

/data/mysql_install_dir/bin/mysqld  --initialize-insecure --user=mysql

/data/mysql_install_dir/bin/mysqld_safe --user=mysql &


# 启动完数据库后，登录数据库可以发现现在已经是debug模式了。
/data/mysql_install_dir/bin/mysql  -u root -p'password'  -S /data/mysql_data/mysql.sock

# 查版本，提示第一次必须改密码
mysql> select version();
ERROR 1820 (HY000): You must reset your password using ALTER USER statement before executing this statement.

# 改密码
mysql> alter user root@localhost identified by 'QHdata@12345';
Query OK, 0 rows affected (0.01 sec)

# 查版本，显示是debug状态
mysql> select version();
+--------------+
| version()    |
+--------------+
| 8.4.10-debug |
+--------------+
1 row in set (0.00 sec)

mysql>

```

## 修改 MySQL 版本

`/include/mysql_version.h`这是一个 C 语言的头文件，是在编译的过程中生成的，通过 cmake 和 make 之后就会生成。源代码目录中实际并不存在这个文件。

源代码实际上只有`/include/mysql_version.h.in` ，这种.h.in 是一个模板文件，它是在 cmake 或者 automake 的过程中产生的一个用于输入设置信息等功能的中间文件。它会在你调用 confing、automake 等.sh 文件之后，自动生成一个相应的.h 文件，然后就可以在源码中调用。

```shell

# Bug #31466846 RENAME THE VERSION FILE TO MYSQL_VERSION

# version 是 C++11 的一个头文件。  MySQL 以往都是在源代码中用 VERSION 这个文件来表示版本号的

# 在引入文件时又因 macOS 不区分文件大小写，产生了冲突，导致编译时报错中断。所以后面改成了MYSQL_VERSION
```

- ./mysql-8.4.10/include/mysql_version.h.in             源代码中的模版文件，这个文件没有硬编码，只是定义了一系列宏
- ./mysql-8.4.10/MYSQL_VERSION                          版本文件，定义了版本号：MYSQL_VERSION_MAJOR.MYSQL_VERSION_MINOR.MYSQL_VERSION_PATCH
- ./mysql-8.4.10/build/include/mysql_version.h          make 之后生成的版本文件
- ./mysql-8.4.10/cmake/mysql_server.cmake 版本构建脚本

https://dev.mysql.com/doc/dev/mysql-server/8.4.10/mysql_8h_source.html

https://cloud.tencent.com/developer/article/2223495





build之后，整个 `/data/mysql_source_code/mysql-8.4.10/build/` 目录结构如下：

| 条目                                | 类型 | 类别        | 说明                                     | 对应源码/来源              |
| :---------------------------------- | :--- | :---------- | :--------------------------------------- | :------------------------- |
| `CMakeCache.txt`                    | 文件 | CMake 总控  | 缓存所有 cmake 变量与 `-D` 配置,重来可删 | cmake 配置阶段生成         |
| `Makefile`                          | 文件 | CMake 总控  | 顶层构建调度外壳(706KB,自动生成)         | cmake 生成                 |
| `CMakeFiles/`                       | 目录 | CMake 总控  | CMake 内部状态/依赖图/进度,勿动          | cmake 生成                 |
| `CPackConfig.cmake`                 | 文件 | 打包        | 二进制包配置 → `make package`            | cmake 生成                 |
| `CPackSourceConfig.cmake`           | 文件 | 打包        | 源码包配置 → `make package_source`       | cmake 生成                 |
| `CTestTestfile.cmake`               | 文件 | 测试        | 测试定义 → `make test`(ctest)            | cmake 生成                 |
| `cmake_install.cmake`               | 文件 | 安装        | `make install` 实际执行脚本              | cmake 生成                 |
| `VERSION.dep`                       | 文件 | 版本        | `MYSQL_VERSION` 副本,触发 cmake 重跑     | `mysql_version.cmake` 生成 |
| `abi_check.out`                     | 文件 | 校验        | ABI 兼容性检查输出                       | `cmake/abi_check.cmake`    |
| `info_macros.cmake`                 | 文件 | 脚本        | 信息/版本宏相关 cmake 脚本               | 源码 `cmake/`              |
| `make_dist.cmake`                   | 文件 | 脚本        | 制作发行包(dist)脚本                     | 源码 `cmake/`              |
| `bin` → `runtime_output_directory/` | 软链 | 编译产物    | 可执行文件入口                           | CMake 输出目录约定         |
| `lib` → `library_output_directory/` | 软链 | 编译产物    | 库文件入口                               | CMake 输出目录约定         |
| `runtime_output_directory/`         | 目录 | 编译产物    | 所有可执行文件(mysqld/mysql/mysqldump…)  | 集中输出                   |
| `library_output_directory/`         | 目录 | 编译产物    | 所有动态/静态库(.so/.a)                  | 集中输出                   |
| `archive_output_directory/`         | 目录 | 编译产物    | 静态归档库(.a)                           | 集中输出                   |
| `plugin_output_directory/`          | 目录 | 编译产物    | 插件 .so(auth/audit/keyring…)            | 集中输出                   |
| `libgtest.a`                        | 文件 | 测试库      | GoogleTest 框架库                        | 自编译                     |
| `libgtest_main.a`                   | 文件 | 测试库      | GTest main 入口库                        | 自编译                     |
| `libgmock.a`                        | 文件 | 测试库      | GoogleMock 框架库                        | 自编译                     |
| `libgmock_main.a`                   | 文件 | 测试库      | GMock main 入口库                        | 自编译                     |
| `icudt77l.lnk`                      | 文件 | 国际化      | ICU 数据文件链接(字符集/排序)            | bundled ICU                |
| `boost_patch_diffs`                 | 文件 | 依赖        | Boost 补丁差异记录                       | bundled Boost              |
| `server_unittest_library_dummy.c`   | 文件 | 杂项        | 占位空文件,满足目标依赖                  | cmake 生成                 |
| `sql/`                              | 目录 | 模块-服务器 | **mysqld 服务器本体**(最重)              | `sql/`                     |
| `sql-common/`                       | 目录 | 模块-共用   | 服务端/客户端共用 SQL 辅助               | `sql-common/`              |
| `client/`                           | 目录 | 模块-客户端 | 命令行客户端工具(mysql 等)               | `client/`                  |
| `libmysql/`                         | 目录 | 模块-库     | C 客户端库 libmysqlclient                | `libmysql/`                |
| `libchangestreams/`                 | 目录 | 模块-库     | 变更流库(克隆/备份)                      | `libchangestreams/`        |
| `libservices/`                      | 目录 | 模块-库     | 插件服务接口库                           | `libservices/`             |
| `mysys/`                            | 目录 | 模块-基建   | 系统抽象层(文件/线程/内存)               | `mysys/`                   |
| `strings/`                          | 目录 | 模块-基建   | 字符串/字符集处理                        | `strings/`                 |
| `vio/`                              | 目录 | 模块-基建   | 网络 I/O 抽象                            | `vio/`                     |
| `extra/`                            | 目录 | 模块-工具   | 额外小工具                               | `extra/`                   |
| `utilities/`                        | 目录 | 模块-工具   | 通用工具                                 | `utilities/`               |
| `libs/`                             | 目录 | 模块-库     | 杂项依赖库                               | `libs/`                    |
| `storage/`                          | 目录 | 模块-引擎   | 存储引擎(InnoDB/MyISAM/NDB…)             | `storage/`                 |
| `plugin/`                           | 目录 | 模块-插件   | 插件源码构建区                           | `plugin/`                  |
| `components/`                       | 目录 | 模块-组件   | 组件框架(service 化模块)                 | `components/`              |
| `router/`                           | 目录 | 模块-路由   | MySQL Router(自带 harness)               | `router/`                  |
| `unittest/`                         | 目录 | 测试        | 单元测试(GTest 驱动)                     | `unittest/`                |
| `testclients/`                      | 目录 | 测试        | 测试用客户端                             | `testclients/`             |
| `mysql-test/`                       | 目录 | 测试        | 回归套件(mysql-test-run.pl)              | `mysql-test/`              |
| `include/`                          | 目录 | 生成头文件  | mysql_version.h / my_config.h 等         | `configure_file` 生成      |
| `share/`                            | 目录 | 安装数据    | 字符集/错误消息/时区表(运行时必需)       | 源码 `share/`              |
| `scripts/`                          | 目录 | 安装脚本    | 运维脚本(mysqld_safe 等)                 | 源码 `scripts/`            |
| `support-files/`                    | 目录 | 安装数据    | 示例 my.cnf、启动模板                    | 源码 `support-files/`      |
| `man/`                              | 目录 | 文档        | man 手册页                               | 源码 `man/`                |
| `Docs/`                             | 目录 | 文档        | 文档                                     | 源码 `Docs/`               |
| `debian/`                           | 目录 | 打包        | Debian/Ubuntu 打包                       | 源码 `debian/`(若存在)     |
| `packaging/`                        | 目录 | 打包        | RPM/DEB 打包定义                         | 源码 `packaging/`          |











## VSCODE REMOTE-SSH 工作原理

从官方介绍文档中的这张原理图我们可以看到，用户本地的`VS Code`是通过`SSH`通道连接到远程主机的。用户的开发代码、运行环境、调试环境都是在远程主机上。

远程连接是基于`Visual Studio Code Remote - SSH`这个扩展来实现的。

当用户进行远程连接时，`VS Code`会在远程主机上安装一个 server 包，这个安装过程是在首次连接时自动完成的。由于 Server 包是安装和运行在远端服务器上，而本地的 VS Code 只是编辑和展示的窗口，两者之间通过`SSH Tunnel`通信，因此实际的工作环境完全是在远端，如果需要使用第三方的扩展，也可以直接安装在远端服务器环境。

1、具体的连接过程如下：

首次连接时，下载`VS Code Server` ，`VS Code Server`包的版本取决于你本地使用的`VS Code`的版本，下载地址为：

```
x86: https://update.code.visualstudio.com/commit:${commit_id}/server-linux-x64/stable
arm: https://update.code.visualstudio.com/commit:${commit_id}/server-linux-arm64/stable
```

其中`commit_id`是变化的，每个不同版本的`VS Code`的`commit_id`都不同，可以在`VS Code`的 Help -> About 中查看

```ini
[client]
port    = 3306
socket = /usr/local/mysql/mysql.sock

[mysql]
prompt="\u@\h \R:\m:\s [\d]> "
no-auto-rehash

[mysqld]
user    = root
port    = 3306
admin_address = 127.0.0.1
basedir = /usr/local/mysql
datadir = /data/mysql_data/
socket    = /usr/local/mysql/mysql.sock
pid-file = /usr/local/mysql/mysqld.pid
character-set-server = utf8mb4


```







## MySQL是怎么启动的？



众所周知，MySQL Server 在服务器上运行，服务端的可执行程序就是 `mysqld`，它在服务器上启动后，体现为一个后台进程。





`sql/mysqld.cc` 是 **MySQL 服务端守护进程 `mysqld` 的实现文件**——也就是整个数据库服务器"本体"的 C++ 源码(`.cc` = C++ 源文件,不是头文件)。

 `mysqld` 启动的那个进程，代码就在这里。





`mysqld_main` 函数是 MySQL 服务器进程 (`mysqld`) 在操作系统上启动后执行的 **主入口函数**。它是整个服务器启动序列的起点和协调中心。

这个函数通常位于 MySQL 源代码的 `sql/mysqld.cc` 文件中（路径可能因版本略有差异）。





```c++
/* File: ./sql/mysqld.cc, Line: 8900 */

int mysqld_main(int argc, char **argv) {
    
    // sql/check_stack.cc:70。它声明两个局部变量、比较地址，判断栈是向高地址（向上）还是低地址（向下）增长，
    initialize_stack_direction();
    
    // mysqld.cc:1764 , 把 argv[0] 换成可执行文件的完整路径。的：让 my_progname 永远是完整路径，这样下一步才能可靠地从路径反推 basedir
    substitute_progpath(argv);		
    
    // 连接 systemd 的通知 socket
	sysd::notify_connect();
  	
    // 给 systemd 报个状态
    sysd::notify("STATUS=Server startup in progress\n");
    
    // 记下mysqld自己的完整路径：例如/usr/local/mysql/bin/mysqld
	my_progname = argv[0];
    
    // mysqld.cc:8725，从路径反推 MYSQL_HOME
	calculate_mysql_home_from_my_progname();

	// Performance Schema 模块初始化，有时候也叫PSI
    pre_initialize_performance_schema();
    
    /* MySQL 启动时要合并三个来源的选项（命令行参数、my.cnf 配置文件、持久化的只读配置），它把它们拼成一个"超长的参数列表"。
    	然后在启动过程中让各个子系统轮流从这个列表里"认领"自己关心的参数，认领完剩下的就越来越少，最后必须清空，否则启动失败。
    */	
    
    // 1、解析命令行参数：先备份成原始值
    orig_argc = argc;     // int 类型，参数个数。注意它包含程序名本身。所以 mysqld --datadir=... 里， argc = 2（1 个程序名 + 1 个真参数）
  	orig_argv = argv;	  // 参数数组，argv[0] = 程序自身路径（"mysqld"）, argv[1] 起 = 真正的命令行参数, argv[2]第二个参数

  	my_getopt_use_args_separator = true;  // 布尔值：打开"参数分隔符"：让解析器能区分哪些选项来自配置文件、哪些来自真正命令行
  	my_defaults_read_login_file = false;  // 布尔值：关闭读取客户端专用的加密登录文件 .mylogin.cnf（服务端不该读）
    
    // 2、解析配置文件启动参数，从配置文件中读取选项, 并把他们放在 argc 和 argv 中已有的参数之前。符合MySQL配置文件优先级最高原则。
    // # 深拷贝追加。 注意：这里传参是指针，所以会直接改写参数列表。
    /* load_defaults 是 my_load_defaults() 的封装（my_default.cc:660）
    	核心工作：按约定顺序搜索 my.cnf、读出里面的配置项、把这些选项"伪装成命令行参数"追加进 argv，并做深拷贝。 
    		1、MYSQL_CONFIG_NAME：普通的宏，在include/mysql_version.h.in中定义，就是my.cnf的文件名的意思。
    		2、load_default_groups： 要读哪些 [group]（如 [mysqld]、[server]、[mysqld-8.4] 等），是一个以 NULL 结尾的指针数组
    		3、&argc	： 参数个数指针
    		4、&argv	： 参数数组指针
    		5、&argv_alloc： 一个 MEM_ROOT（内存池），新 argv 在这上面分配
    */        
    if (load_defaults(MYSQL_CONFIG_NAME, load_default_groups, &argc, &argv, &argv_alloc)) {
   		flush_error_log_messages();
    	return 1;
  	}
	
    // 3、再存一份。 把"合并后的全量参数"冻结一份快照，存进 MySQL 自己的内存池。供启动后插件/组件加载时查阅，始终不被"吃掉"。
    argc_cached = argc;		
  	argv_cached = new (&argv_alloc) char *[argc_cached + 1];
    // 浅拷贝：从argv拷贝到argv_cached。  memcpy(dst, src, n) 是 C 标准库按字节复制：从 src 复制 n 个字节到 dst 
    memcpy(argv_cached, argv, argc_cached * sizeof(char *));
  	argv_cached[argc_cached] = nullptr;	// 末尾放 nullptr 哨兵。( C++ 空指针，等价于 NULL)
    
  // 1、用 get_relative_path 把编译默认的 MYSQL_DATADIR 转成相对 basedir 的路径
  // 2、再用 MySQL 自己的 strmake（保证 NUL 结尾、比 strncpy 安全）把它复制进 mysql_real_data_home 全局变量，作为数据目录的初始值
  // 3、其实后面也会会被 --datadir 配置覆盖。
    strmake(mysql_real_data_home, get_relative_path(MYSQL_DATADIR), sizeof(mysql_real_data_home) - 1);
    
    // 确保初始化
    system_charset_info = &my_charset_utf8mb3_general_ci;
    
    // 写错误日志
    local_message_hook = error_log_print;
    
    sys_var_init();



    
}
```



