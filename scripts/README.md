# Scripts 使用指南

本目录包含文档维护中常用的脚本工具。

---

## count.py

统计目录下文件的行数、字数、字符数。

### 基本用法

```bash
python3 scripts/count.py [路径] [--ext 扩展名] [--exclude 排除项]
```

### 参数说明

| 参数 | 说明 |
|---|---|
| `路径` | 要统计的目录，默认为 `docs` |
| `--ext` / `-e` | 按扩展名过滤，多个用逗号分隔 |
| `--exclude` / `-x` | 排除包含指定字符串的文件或目录（可多次指定） |

### 示例

```bash
# 统计 docs 目录（默认）
python3 scripts/count.py docs

# 仅统计 md/mdx 文件
python3 scripts/count.py docs --ext md,mdx

# 排除 interview 目录
python3 scripts/count.py docs --exclude interview

# 组合使用
python3 scripts/count.py docs --ext md,mdx --exclude interview --exclude .vitepress

# 统计其他目录
python3 scripts/count.py ./src
```

### 输出示例

```
📊 统计目录: /path/to/Guide/docs

文件                                     行数       词数       中文字数       字符数
────────────────────────────────────── ────────  ──────────  ──────────  ──────────
📂 cs                                  49,822   120,316    165,580    1,087,386
  📂 algorithm                         10,050    26,392     33,038      185,042
    📄 array-linkedlist.mdx              292       650      1,522        5,136
    📄 avl-tree.mdx                       449     1,126      1,112        8,756
    📄 index.mdx                          96       175      1,170        1,793
  📂 design-pattern                       104       250      1,296        2,450
    📄 index.mdx                          104       250      1,296        2,450
────────────────────────────────────── ────────  ──────────  ──────────  ──────────
总计                                    49,822   120,316    165,580    1,087,386

共 1577 个文件
```

输出包含：
- 按目录层级缩进显示，`📂` 表示目录汇总行，`📄` 表示文件
- 目录行自动汇总其下所有文件的统计值
- 底部输出总计行
