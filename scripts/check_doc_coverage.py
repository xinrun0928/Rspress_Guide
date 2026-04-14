#!/usr/bin/env python3
"""
文档完成度检查脚本
检查 sidebar 配置中的文章是否都已创建，以及 docs 目录下是否有多余的文件未被 sidebar 收录。
支持指定 docs 下的任意目录，默认为 docs 目录。

用法:
    python check_doc_coverage.py                  # 检查 docs 目录
    python check_doc_coverage.py java             # 检查 docs/java 目录
    python check_doc_coverage.py questions        # 检查 docs/questions 目录
"""

import re
import sys
from pathlib import Path
from typing import Optional

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
SIDEBAR_DIR = PROJECT_ROOT / "theme_config" / "sidebar"
DOCS_DIR = PROJECT_ROOT / "docs"


# ---------------------------------------------------------------------------
# 提取 sidebar 链接
# ---------------------------------------------------------------------------

def _extract_links_from_jsobj(content: str) -> set[str]:
    """从 JS 模块内容中提取所有 link 字段，返回干净的相对路径。"""
    links = set()
    for m in re.finditer(r"link\s*:\s*['\"]([^'\"]+)['\"]", content):
        link = m.group(1).strip().lstrip("/").rstrip("/")
        if link:
            links.add(link)
    return links


def _extract_sidebar() -> dict[str, set[str]]:
    """返回 { group: {link, ...}, ... }，link 为相对于 docs 的路径。"""
    modules = [
        ("cs", SIDEBAR_DIR / "cs.js"),
        ("database", SIDEBAR_DIR / "database.js"),
        ("design", SIDEBAR_DIR / "design.js"),
        ("distributed", SIDEBAR_DIR / "distributed.js"),
        ("framework", SIDEBAR_DIR / "framework.js"),
        ("interview-prep", SIDEBAR_DIR / "interview-prep.js"),
        ("java", SIDEBAR_DIR / "java.js"),
        ("questions", SIDEBAR_DIR / "questions.js"),
    ]
    result: dict[str, set[str]] = {}
    for group, fpath in modules:
        if fpath.exists():
            result[group] = _extract_links_from_jsobj(fpath.read_text(encoding="utf-8"))
    return result


# ---------------------------------------------------------------------------
# 扫描 docs 目录
# ---------------------------------------------------------------------------

def _scan_docs(docs_root: Path, prefix: Optional[str] = None) -> dict[str, set[str]]:
    """
    扫描 docs 目录，返回 { group: {doc_path, ...} }。
    - docs_root: 扫描的根目录
    - prefix: 可选，为所有 doc_path 添加此前缀
    - group: 第一层子目录名（无 prefix 时）或 prefix（docs_subdir 扫描时固定为 docs_subdir）
    - doc_path: 相对于 docs 的路径（去掉 .mdx；index.mdx -> 目录路径）
    """
    groups: dict[str, set[str]] = {}
    for fpath in docs_root.rglob("*.mdx"):
        rel = fpath.relative_to(docs_root)
        if rel.name == "index.mdx":
            parts = list(rel.parts[:-1])
        else:
            parts = list(rel.parts)
            if parts[-1].endswith(".mdx"):
                parts[-1] = parts[-1].rsplit(".", 1)[0]

        if not parts:
            continue

        group_key = parts[0]
        doc_path = "/".join(parts)

        if prefix:
            doc_path = f"{prefix}/{doc_path}"
            # 整组归入 docs_subdir 名下
            group_key = prefix

        groups.setdefault(group_key, set()).add(doc_path)

    return groups


# ---------------------------------------------------------------------------
# 输出
# ---------------------------------------------------------------------------

def _print_group_diff(group: str, missing: set[str], extra: set[str]) -> None:
    print(f"┌─ [{group}]")
    has_diff = False
    if missing:
        has_diff = True
        print(f"│  🔴 缺失 {len(missing)} 篇:")
        for m in sorted(missing):
            print(f"│      docs/{m}.mdx")
    if extra:
        has_diff = True
        print(f"│  🟠 多余 {len(extra)} 篇:")
        for e in sorted(extra):
            print(f"│      docs/{e}.mdx")
    if not has_diff:
        print(f"│  ✅ 无差异")
    print(f"└")


def _print_group_diff_detailed(group: str, missing: set[str], extra: set[str]) -> None:
    """questions 分组按二级子分组展示"""
    missing_by_sub: dict[str, list[str]] = {}
    extra_by_sub: dict[str, list[str]] = {}

    for m in sorted(missing):
        parts = m.split("/", 2)
        sub = parts[1] if len(parts) > 1 else "root"
        missing_by_sub.setdefault(sub, []).append(m)

    for e in sorted(extra):
        parts = e.split("/", 2)
        sub = parts[1] if len(parts) > 1 else "root"
        extra_by_sub.setdefault(sub, []).append(e)

    all_subs = sorted(set(list(missing_by_sub) + list(extra_by_sub)))

    print(f"┌─ [{group}]")
    has_diff = False
    for sub in all_subs:
        mis = missing_by_sub.get(sub, [])
        ext = extra_by_sub.get(sub, [])
        if mis:
            has_diff = True
            print(f"│  🔴 [{sub}] 缺失 {len(mis)} 篇:")
            for m in mis:
                print(f"│      docs/{m}.mdx")
        if ext:
            has_diff = True
            print(f"│  🟠 [{sub}] 多余 {len(ext)} 篇:")
            for e in ext:
                print(f"│      docs/{e}.mdx")
    if not has_diff:
        print(f"│  ✅ 无差异")
    print(f"└")


# ---------------------------------------------------------------------------
# 主检查
# ---------------------------------------------------------------------------

def check_coverage(docs_subdir: Optional[str] = None) -> None:
    if docs_subdir:
        target_docs = DOCS_DIR / docs_subdir
        target_name = docs_subdir
    else:
        target_docs = DOCS_DIR
        target_name = "docs"

    print(f"\n{'='*60}")
    print(f"  文档完成度检查  |  目录: {target_name}/")
    print(f"{'='*60}\n")

    # 1. 提取 sidebar
    sidebar_group_map = _extract_sidebar()

    # 2. 扫描 docs
    if docs_subdir:
        # 扫描 docs/<docs_subdir>/
        # group_key 固定为 docs_subdir；doc_path 加上 docs_subdir 前缀
        # 例如: docs/questions/java-basic/oop.mdx
        #   -> group_key="questions", doc_path="questions/java-basic/oop"
        scanned = _scan_docs(target_docs, prefix=docs_subdir)
        # sidebar 中对应的组是 docs_subdir（若存在），需确保只比对这个组
        # sidebar_group_map 不变，scanned 产生的 group_key = docs_subdir
    else:
        # 扫描 docs/；group_key = 顶级子目录名；doc_path 不带前缀
        scanned = _scan_docs(target_docs, prefix=None)
        # sidebar_group_map 不变
        # 注意：docs/start、docs/public 等无对应 sidebar 组的目录会被过滤

    # 4. 过滤：只保留有 sidebar 对应的 group
    if docs_subdir:
        if docs_subdir not in sidebar_group_map:
            print(f"  ⚠️  警告: sidebar 中未找到分组 '{docs_subdir}'，已跳过\n")
            scanned = {}
        else:
            all_paths: set[str] = set()
            for v in scanned.values():
                all_paths.update(v)
            scanned = {docs_subdir: all_paths}
    else:
        scanned = {k: v for k, v in scanned.items() if k in sidebar_group_map}

    # 5. 比较差异（只遍历有数据的 group）
    total_missing = total_extra = total_sidebar = total_docs = 0
    all_groups = sorted(set(sidebar_group_map.keys()) & set(scanned.keys()))

    for group in all_groups:
        sidebar_links = sidebar_group_map.get(group, set())
        doc_files = scanned.get(group, set())

        # 只比较具体文章链接（带 / 的，排除顶层 group link 如 "java"）
        sidebar_articles = {l for l in sidebar_links if "/" in l}
        doc_articles = {l for l in doc_files if "/" in l}

        missing = sidebar_articles - doc_articles
        extra = doc_articles - sidebar_articles

        total_sidebar += len(sidebar_articles)
        total_docs += len(doc_articles)
        total_missing += len(missing)
        total_extra += len(extra)

        if group == "questions":
            _print_group_diff_detailed(group, missing, extra)
        else:
            _print_group_diff(group, missing, extra)

    # 5. 汇总
    print(f"\n{'─'*60}")
    print(f"  汇总")
    print(f"{'─'*60}")
    print(f"  sidebar 配置文章总数:  {total_sidebar}")
    print(f"  docs 实际文章总数:     {total_docs}")
    print(f"  缺失（sidebar有/文章无）: {total_missing} 篇")
    print(f"  多余（文章有/sidebar无）: {total_extra}  篇")
    if total_missing == 0 and total_extra == 0:
        print(f"\n  ✅ 完美，sidebar 与 docs 完全匹配！")
    else:
        print(f"\n  ⚠️  存在差异，请检查上方详情")
    print(f"\n{'='*60}\n")


def main() -> None:
    docs_subdir: Optional[str] = None
    args = sys.argv[1:]
    if args:
        first = args[0]
        if first in ("-h", "--help"):
            print(__doc__)
            sys.exit(0)
        target = DOCS_DIR / first
        if not target.exists():
            print(f"错误: 目录不存在 docs/{first}/", file=sys.stderr)
            sys.exit(1)
        docs_subdir = first
    check_coverage(docs_subdir)


if __name__ == "__main__":
    main()
