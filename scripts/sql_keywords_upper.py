"""
扫描 docs/ 下所有 .md 文件，对 ```sql / ```mysql / ```postgresql 等
SQL 代码块内的 SQL 关键字转换为大写，同时保留：
  - 单/双引号字符串字面量内容
  - 反引号 `...` 标识符内容
  - -- ... 行注释、# ... 行注释、/* ... */ 块注释
其他语言代码块（python/bash/shell/json/yaml/...）以及代码块外的正文不做改动。

幂等：已经大写的不变；混合大小写（如 Select）会规范化为 SELECT。
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# SQL 关键字（按需保守列出；都是 keyword，而非 function 名称）
# ---------------------------------------------------------------------------
KEYWORDS_RAW = """
SELECT INSERT UPDATE DELETE MERGE FROM WHERE INTO VALUES VALUE SET RETURNING USING

JOIN INNER OUTER LEFT RIGHT FULL CROSS ON NATURAL STRAIGHT_JOIN

AND OR NOT NULL IS IN LIKE BETWEEN EXISTS ANY ALL SOME REGEXP RLIKE XOR DIV MOD

GROUP BY HAVING ORDER ASC DESC LIMIT OFFSET ROLLUP CUBE GROUPING

UNION INTERSECT EXCEPT DISTINCT DISTINCTROW

CREATE DROP ALTER TRUNCATE RENAME TABLE DATABASE SCHEMA INDEX VIEW
FUNCTION PROCEDURE TRIGGER EVENT USER ROLE COLUMN CONSTRAINT
FOREIGN PRIMARY KEY REFERENCES UNIQUE CHECK DEFAULT AUTO_INCREMENT
COMMENT COLLATE CHARACTER CHARSET ENGINE ROW_FORMAT DEFINER INVOKER SECURITY
TEMPORARY REPLACE ADD MODIFY CHANGE AFTER FIRST BEFORE TABLESPACE
PARTITION PARTITIONS SUBPARTITION SUBPARTITIONS HASH RANGE LIST LINEAR
COLUMNS STORAGE GENERATED ALWAYS VIRTUAL STORED INVISIBLE VISIBLE
EXTENDED COMPRESSED DYNAMIC COMPACT REDUNDANT FIXED

INT INTEGER BIGINT SMALLINT TINYINT MEDIUMINT DECIMAL NUMERIC FLOAT DOUBLE REAL
BIT BOOLEAN BOOL DATE DATETIME TIMESTAMP TIME YEAR
CHAR VARCHAR BINARY VARBINARY TINYBLOB BLOB MEDIUMBLOB LONGBLOB
TINYTEXT TEXT MEDIUMTEXT LONGTEXT ENUM JSON
GEOMETRY POINT LINESTRING POLYGON UUID SERIAL UNSIGNED SIGNED ZEROFILL

BEGIN START TRANSACTION COMMIT ROLLBACK SAVEPOINT RELEASE WORK CHAIN

LOCK UNLOCK TABLES READ WRITE SHARED MODE FOR OF NOWAIT SKIP LOCKED
ISOLATION LEVEL REPEATABLE COMMITTED UNCOMMITTED SERIALIZABLE
SHARE EXCLUSIVE

GRANT REVOKE PRIVILEGES TO IDENTIFIED WITH OPTION

IF THEN ELSE ELSEIF END CASE WHEN WHILE LOOP REPEAT UNTIL LEAVE ITERATE
DECLARE CURSOR FETCH OPEN CLOSE HANDLER CONTINUE EXIT FOUND
SQLEXCEPTION SQLWARNING SIGNAL RESIGNAL DETERMINISTIC

AS RECURSIVE WINDOW OVER RANGE ROWS PRECEDING FOLLOWING
CURRENT ROW UNBOUNDED ONLY LAST NULLS

SHOW DESCRIBE EXPLAIN ANALYZE USE HELP KILL FLUSH RESET
OPTIMIZE REPAIR CHECKSUM BACKUP RESTORE LOAD OUTFILE INFILE
IGNORE DELAYED LOW_PRIORITY HIGH_PRIORITY QUICK
FORCE STRAIGHT_JOIN

TRUE FALSE UNKNOWN

CASCADE RESTRICT NO ACTION
"""

KEYWORDS = sorted({w for w in KEYWORDS_RAW.split() if w}, key=lambda x: -len(x))

KEYWORD_ALT = "|".join(re.escape(k) for k in KEYWORDS)

# 词法 token：字符串 / 反引号 / 注释 / 关键字。
# 关键字必须放在最后，且要求左右是 \b。
TOKEN_RE = re.compile(
    rf"""(?ix)
        (                                # 1: 单引号字符串
            ' (?: \\. | '' | [^'\\] )* '
        )
        | (                              # 2: 双引号字符串
            " (?: \\. | "" | [^"\\] )* "
        )
        | (                              # 3: 反引号标识符
            ` (?: `` | [^`] )* `
        )
        | (                              # 4: -- 行注释（要求 -- 后是空白或行尾）
            -- (?:[ \t][^\n]*)? (?=\n|$)
        )
        | (                              # 5: # 行注释
            \# [^\n]*
        )
        | (                              # 6: 块注释
            /\* [\s\S]*? \*/
        )
        | \b ( {KEYWORD_ALT} ) \b        # 7: 关键字
    """,
)

SQL_LANGS = {
    "sql", "mysql", "postgresql", "postgres", "psql", "pgsql",
    "plsql", "sqlite", "oracle", "tsql", "mariadb",
}


def transform_sql(code: str) -> str:
    def repl(m: re.Match) -> str:
        if m.group(7) is not None:
            return m.group(7).upper()
        return m.group(0)

    return TOKEN_RE.sub(repl, code)


FENCE_OPEN_RE = re.compile(r"^(?P<indent>[ \t]*)(?P<fence>`{3,}|~{3,})[ \t]*(?P<lang>[\w\-+#.]*)\s*$")


def process_markdown(text: str) -> tuple[str, int]:
    """返回 (新内容, 被改动的 SQL 块数量)。"""
    lines = text.split("\n")
    out: list[str] = []
    i = 0
    changed_blocks = 0
    while i < len(lines):
        line = lines[i]
        m = FENCE_OPEN_RE.match(line)
        if m:
            indent = m.group("indent")
            fence = m.group("fence")
            lang = m.group("lang").lower()
            # 找到对应的关闭围栏（必须是同样的字符且至少同样长度）
            close_re = re.compile(
                rf"^{re.escape(indent)}{re.escape(fence[0])}{{{len(fence)},}}[ \t]*$"
            )
            j = i + 1
            block: list[str] = []
            while j < len(lines) and not close_re.match(lines[j]):
                block.append(lines[j])
                j += 1
            if j >= len(lines):
                # 没找到关闭，原样输出剩余
                out.append(line)
                i += 1
                continue
            # 处理块内容
            block_text = "\n".join(block)
            if lang in SQL_LANGS:
                new_block = transform_sql(block_text)
                if new_block != block_text:
                    changed_blocks += 1
                # 去掉行内的缩进前缀的处理：保留原样，逐行重写
                new_lines = new_block.split("\n")
            else:
                new_lines = block
            out.append(line)
            out.extend(new_lines)
            out.append(lines[j])
            i = j + 1
        else:
            out.append(line)
            i += 1
    return "\n".join(out), changed_blocks


def main(root: Path, dry_run: bool = False) -> int:
    md_files = sorted(root.rglob("*.md"))
    total_files_changed = 0
    total_blocks_changed = 0
    for f in md_files:
        try:
            original = f.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            print(f"[SKIP non-utf8] {f}")
            continue
        new, changed = process_markdown(original)
        if new != original:
            total_files_changed += 1
            total_blocks_changed += changed
            rel = f.relative_to(root.parent) if root.parent in f.parents else f
            print(f"[mod {changed:>3} blk] {rel}")
            if not dry_run:
                f.write_text(new, encoding="utf-8", newline="\n")
    print(
        f"\nDone. files changed = {total_files_changed}, "
        f"sql blocks changed = {total_blocks_changed}, dry_run={dry_run}"
    )
    return 0


if __name__ == "__main__":
    here = Path(__file__).resolve().parent.parent
    docs = here / "docs"
    dry = "--dry-run" in sys.argv or "-n" in sys.argv
    sys.exit(main(docs, dry_run=dry))
