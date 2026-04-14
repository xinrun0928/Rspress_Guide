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

---

## check_doc_coverage.py

检查 sidebar 导航配置与 `docs/` 目录下实际文章之间的完成度，找出缺失和多余的文档。

### 基本用法

```bash
python3 scripts/check_doc_coverage.py [子目录]
```

### 参数说明

| 参数 | 说明 |
|------|------|
| 无参数 | 检查整个 `docs/` 目录 |
| `子目录` | 只检查 `docs/<子目录>`，如 `java`、`questions`、`framework` |
| `-h` / `--help` | 显示帮助信息 |

### 示例

```bash
# 检查整个 docs 目录
python3 scripts/check_doc_coverage.py

# 只检查 docs/java 目录
python3 scripts/check_doc_coverage.py java

# 只检查 docs/questions 目录
python3 scripts/check_doc_coverage.py questions
```

### 输出说明

- 🔴 **缺失**：sidebar 中已配置，但 `docs/` 下没有对应的 `.mdx` 文件
- 🟠 **多余**：`docs/` 下有文件，但 sidebar 中没有配置该路径
- ✅ **无差异**：该分组完全匹配，无需处理

### 输出示例

```
============================================================
  文档完成度检查  |  目录: docs/
============================================================

┌─ [java]
│  ✅ 无差异
└
┌─ [questions]
│  🔴 [collection] 缺失 3 篇:
│      docs/questions/collection/architecture.mdx
│      docs/questions/collection/arrays.mdx
│      docs/questions/collection/collections.mdx
│  🔴 [java-basic] 缺失 1 篇:
│      docs/questions/java-basic/module.mdx
└

────────────────────────────────────────────────────────────
  汇总
────────────────────────────────────────────────────────────
  sidebar 配置文章总数:  305
  docs 实际文章总数:     297
  缺失（sidebar有/文章无）: 4 篇
  多余（文章有/sidebar无）: 0  篇

  ⚠️  存在差异，请检查上方详情
```

### 工作原理

脚本从 `theme_config/sidebar/*.js` 提取 sidebar 中的所有链接，与 `docs/` 目录下扫描到的 `.mdx` 文件路径进行对比：

1. **解析 sidebar 配置**：读取 `theme_config/sidebar/` 下的 8 个分组配置文件（cs、database、design、distributed、framework、interview-prep、java、questions），提取其中所有 `link` 字段
2. **扫描实际文档**：遍历 `docs/` 目录下的所有 `.mdx` 文件（`index.mdx` → 对应目录路径，其他 → 文件路径去掉 `.mdx` 后缀）
3. **按组对比**：以 sidebar 分组为维度，分别计算缺失与多余的文章
4. **汇总统计**：输出所有分组的差异情况及总计
