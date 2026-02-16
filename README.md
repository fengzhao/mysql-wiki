# MySQL WIKI

> MySQL 技术文档与学习资源

[![Build Status](https://github.com/fengzhao/mysql-wiki/actions/workflows/publish_docs.yml/badge.svg)](https://github.com/fengzhao/mysql-wiki/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

📖 在线访问：[https://mysql.fengzhao.me](https://mysql.fengzhao.me)

## 内容概览

- **MySQL**: 入门 → 基础 → 高级 → 调优
- **其他数据库**: PostgreSQL, Oracle, Redis, MongoDB, SQLite
- **分布式系统**: 分布式事务
- **大数据**: HDFS, Hive, OLAP
- **网络基础**: 计算机网络概述

## 快速开始

### 本地运行

```bash
# 克隆项目
git clone https://github.com/fengzhao/mysql-wiki.git
cd mysql-wiki

# 安装依赖
pip install -r requirements.txt

# 本地预览
mkdocs serve
```

访问 http://127.0.0.1:8000 查看文档。

### 构建静态站点

```bash
mkdocs build
```

生成的站点文件在 `site/` 目录。

## 目录结构

```
docs/
├── 01-mysql-basics/      # MySQL 入门
├── 02-mysql-fundamental/ # MySQL 基础
├── 03-mysql-advanced/    # MySQL 高级
├── 04-mysql-optimize/    # MySQL 调优
├── 05-postgresql/        # PostgreSQL
├── 06-oracle/            # Oracle
├── 07-nosql/             # NoSQL (Redis, MongoDB)
├── 08-distributed/       # 分布式系统
├── 09-olap/              # OLAP
├── 10-bigdata/           # 大数据 (HDFS, Hive)
├── 11-network/           # 网络基础
├── 12-sqlite/            # SQLite
└── 13-algorithm/         # 算法
```

## 贡献

欢迎提交 Issue 和 Pull Request！

## 许可

MIT License
