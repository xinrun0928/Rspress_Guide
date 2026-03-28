# Scripts 使用指南

本目录包含文档维护中常用的脚本工具。

---

## md-to-mdx.js

批量将目录下的 `.md` 文件转换为 `.mdx` 文件。

### 基本用法

```bash
node scripts/md-to-mdx.js <目标目录>
```

示例：

```bash
# 转换 docs/guide 目录
node scripts/md-to-mdx.js ./docs/guide

# 转换整个 docs 目录
node scripts/md-to-mdx.js ./docs
```

### 工作逻辑

1. 递归扫描目标目录，找出所有 `.md` 文件
2. 检查对应的 `.mdx` 文件是否已存在
3. 若已存在，跳过；若不存在，直接将 `.md` 重命名为 `.mdx`
4. 输出转换统计

### 输出示例

```
🔍 正在扫描目录: /path/to/docs/guide

📄 找到 5 个 .md 文件：

✅ 转换完成: /path/to/docs/guide/intro.md -> /path/to/docs/guide/intro.mdx
✅ 转换完成: /path/to/docs/guide/install.md -> /path/to/docs/guide/install.mdx
⚠️  跳过（已存在）: /path/to/docs/guide/config.mdx

📊 统计：转换 2 个，跳过 1 个。
```

### 注意事项

- 脚本只做文件重命名（`.md` → `.mdx`），**不会修改文件内容**
- 如果已有同名的 `.mdx` 文件，`.md` 文件会被保留，不会覆盖
- 转换前建议先提交 git，防止误操作

---

## scan_sidebar.py

递归扫描 `docs` 目录下所有子模块的 `_meta.json`，将侧边栏配置展开为完整的 JSON 层级结构，按模块分别输出到 `theme_config/sidebar/` 目录。

### 基本用法

```bash
python3 scripts/scan_sidebar.py [docs_path] [options]
```

示例：

```bash
# 扫描 docs 目录（默认）
python3 scripts/scan_sidebar.py

# 指定 docs 目录
python3 scripts/scan_sidebar.py ./docs

# 指定输出目录
python3 scripts/scan_sidebar.py --output ./theme_config/sidebar
```

### 参数说明

| 参数 | 说明 |
|---|---|
| `docs_path` | `docs` 目录路径，默认为 `docs` |
| `--output` / `-o` | 输出目录，默认为 `theme_config/sidebar` |
| `--indent` / `-i` | JSON 缩进空格数，默认为 `2` |
| `--no-summary` | 不打印模块概览 |

### 工作逻辑

1. 扫描 `docs/` 下所有一级子目录（视为一级模块）
2. 对每个子目录读取其 `_meta.json`
3. 递归展开 `dir`、`dir-section-header` 类型的嵌套条目
4. 自动从 `index.mdx` 或同名 `.mdx` 的 frontmatter / 首行标题中提取模块 label
5. 每个模块输出为一个独立的 JSON 文件，同时输出一份 `all_modules.json` 汇总

### 输出文件

假设 `docs/java/_meta.json` 存在，脚本运行后生成：

```
theme_config/sidebar/
├── java.json        # java 模块的完整侧边栏树
├── spring.json       # spring 模块的完整侧边栏树
├── ...
└── all_modules.json  # 所有模块汇总（all-in-one）
```

### 输出示例

```
文档目录：/path/to/Guide/docs
输出目录：/path/to/Guide/theme_config/sidebar

正在处理模块：java
正在处理模块：spring
正在处理模块：jvm
  ✓ 已保存：/path/to/Guide/theme_config/sidebar/java.json
  ✓ 已保存：/path/to/Guide/theme_config/sidebar/spring.json
  ✓ 已保存：/path/to/Guide/theme_config/sidebar/jvm.json
  ✓ 已保存：/path/to/Guide/theme_config/sidebar/all_modules.json

========== 模块概览 ==========
  • java  (Java 核心)  — 共 42 个条目
  • spring  (Spring 框架)  — 共 28 个条目
  • jvm  (JVM 原理)  — 共 15 个条目

共扫描到 3 个模块
总计 85 个导航条目
```

### 输出 JSON 结构

生成的 JSON 文件结构如下：

```json
{
  "module": "java",
  "label": "Java 核心",
  "children": [
    {
      "type": "file",
      "name": "getting-started",
      "label": "getting started"
    },
    {
      "type": "dir",
      "name": "collection",
      "label": "集合框架",
      "collapsible": true,
      "collapsed": false,
      "children": [
        {
          "type": "file",
          "name": "hashmap",
          "label": "HashMap"
        }
      ]
    }
  ]
}
```

### 注意事项

- 脚本仅读取和重组数据，**不会修改** `docs` 目录下的任何文件
- 只有包含 `_meta.json` 的目录才会被识别为模块
- `--no-summary` 适合在 CI/CD 流水线中抑制非必要输出
- JSON 中的 `label` 字段优先级：`index.mdx` frontmatter `title` > frontmatter `label` > 首行 `# 标题` > 目录名

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
