#!/usr/bin/env python3
"""
读取 docs 目录下（含子目录）所有 _meta.json，递归构建完整的 JSON 层级结构，
按一级模块分别保存到 theme_config/sidebar_extract/ 目录下。

Usage:
    python scripts/scan_sidebar.py [docs_path] [--output OUTPUT_DIR]
"""

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Any


def resolve_meta(dir_path: Path) -> list[str | dict[str, Any]]:
    """读取指定目录下的 _meta.json，返回 parsed list。文件不存在或解析失败时返回空列表。"""
    meta_file = dir_path / "_meta.json"
    if not meta_file.exists():
        return []
    try:
        with open(meta_file, encoding="utf-8") as f:
            raw = json.load(f)
        if isinstance(raw, list):
            return raw
        return []
    except (json.JSONDecodeError, OSError) as e:
        print(f"  [警告] 无法解析 {meta_file}：{e}", file=sys.stderr)
        return []


def _normalize_entry(entry: str | dict[str, Any]) -> dict[str, Any]:
    """
    将字符串条目规范化为 dict。
    - 字符串：视为 file 类型，name = 字符串本身，label = 去掉连字符的 name
    - dict：原样返回
    """
    if isinstance(entry, str):
        return {"type": "file", "name": entry, "label": entry.replace("-", " ").replace("_", " ")}
    return entry


def expand_entry(
    entry: dict[str, Any],
    base_dir: Path,
) -> dict[str, Any]:
    """
    递归展开 _meta.json 中的一个条目：
      - dir / dir-section-header / section-header / file / custom-link：保留原字段
      - divider：保留原字段
      - dir / dir-section-header 类型且有子目录时：递归 children
    返回一个可序列化的字典。
    """
    entry = _normalize_entry(entry)
    entry_type = entry.get("type", "")
    result: dict[str, Any] = {k: v for k, v in entry.items() if k != "items"}

    if entry_type == "dir" or entry_type == "dir-section-header":
        sub_dir = base_dir / entry.get("name", "")
        children_meta: list[str | dict[str, Any]] = resolve_meta(sub_dir)
        if children_meta:
            children: list[dict[str, Any]] = []
            for child in children_meta:
                child_expanded = expand_entry(child, sub_dir)
                if child_expanded:
                    children.append(child_expanded)
            result["children"] = children

    elif entry_type == "file":
        pass  # file 条目不需要额外处理

    elif entry_type == "custom-link":
        if "items" in entry and isinstance(entry["items"], list):
            result["items"] = [
                expand_entry(item, base_dir) for item in entry["items"]
            ]

    return result


def build_module_tree(
    top_meta: list[dict[str, Any]],
    top_dir: Path,
) -> dict[str, Any]:
    """
    从顶级 _meta.json 构建完整树，返回结构：
      {
        "module": "模块目录名",
        "label": "模块标签",
        "children": [ ...展开后的条目列表 ]
      }
    """
    module_name = top_dir.name
    tree: dict[str, Any] = {
        "module": module_name,
        "children": [],
    }

    # 尝试从 top_dir 的父目录寻找同名 .mdx/index.mdx 获取 label
    index_file = top_dir / "index.mdx"
    label = module_name
    if not index_file.exists():
        index_file = top_dir.parent / f"{module_name}.mdx"
    if index_file.exists():
        label = _extract_title(index_file) or module_name

    tree["label"] = label

    for entry in top_meta:
        expanded = expand_entry(entry, top_dir)
        if expanded:
            tree["children"].append(expanded)

    return tree


def _extract_title(index_file: Path) -> str | None:
    """从 index.mdx 的 frontmatter 或第一行标题中提取 title/label。"""
    try:
        with open(index_file, encoding="utf-8") as f:
            content = f.read(600)
        if content.startswith("---"):
            end = content.find("\n---\n")
            if end != -1:
                frontmatter = content[: end + 5]
                for line in frontmatter.splitlines():
                    if line.strip().startswith("title:"):
                        return line.split("title:", 1)[1].strip().strip('"').strip("'")
                    if line.strip().startswith("label:"):
                        return line.split("label:", 1)[1].strip().strip('"').strip("'")
        # 无 frontmatter 时取第一个 # 标题
        import re
        m = re.search(r"^#\s+(.+)$", content, re.MULTILINE)
        if m:
            return m.group(1).strip()
    except OSError:
        pass
    return None


def scan_docs(docs_dir: Path) -> list[dict[str, Any]]:
    """
    扫描 docs_dir 下所有直接子目录（视为一级模块），
    对每个子目录读取其 _meta.json 并构建完整树。
    返回 [{ module, label, children }] 列表。
    """
    if not docs_dir.exists() or not docs_dir.is_dir():
        print(f"错误：路径不存在或不是目录: {docs_dir}", file=sys.stderr)
        sys.exit(1)

    modules: list[dict[str, Any]] = []

    # 按目录名排序，保证输出顺序稳定
    subdirs = sorted(
        (d for d in docs_dir.iterdir() if d.is_dir() and not d.name.startswith(".")),
        key=lambda d: d.name,
    )

    for subdir in subdirs:
        meta_file = subdir / "_meta.json"
        if not meta_file.exists():
            continue

        print(f"正在处理模块：{subdir.name}")
        top_meta = resolve_meta(subdir)
        if not top_meta:
            print(f"  [跳过] {subdir.name} 的 _meta.json 为空")
            continue

        tree = build_module_tree(top_meta, subdir)
        modules.append(tree)

    return modules


def save_outputs(
    modules: list[dict[str, Any]],
    output_dir: Path,
    indent: int = 2,
) -> None:
    """将每个模块的树保存为独立 JSON 文件到 output_dir。"""
    output_dir.mkdir(parents=True, exist_ok=True)

    for module_tree in modules:
        filename = f"{module_tree['module']}.json"
        out_path = output_dir / filename
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(module_tree, f, ensure_ascii=False, indent=indent)
        print(f"  ✓ 已保存：{out_path}")

    # 同时输出一份 all-in-one
    all_path = output_dir / "all_modules.json"
    with open(all_path, "w", encoding="utf-8") as f:
        json.dump(modules, f, ensure_ascii=False, indent=indent)
    print(f"  ✓ 已保存：{all_path}")


def print_summary(modules: list[dict[str, Any]]) -> None:
    """打印模块概览。"""
    print("\n========== 模块概览 ==========")
    for module_tree in modules:
        name = module_tree.get("module", "?")
        label = module_tree.get("label", "?")
        child_count = _count_items(module_tree.get("children", []))
        print(f"  • {name}  ({label})  — 共 {child_count} 个条目")

    print(f"\n共扫描到 {len(modules)} 个模块")

    grand_total = sum(
        _count_items(m.get("children", [])) for m in modules
    )
    print(f"总计 {grand_total} 个导航条目")


def _count_items(children: list[dict[str, Any]]) -> int:
    """递归统计 children 中的条目总数（含嵌套）。"""
    total = 0
    for child in children:
        total += 1
        if "children" in child and isinstance(child["children"], list):
            total += _count_items(child["children"])
    return total


def main() -> None:
    parser = argparse.ArgumentParser(
        description="扫描 docs 目录下的 _meta.json，构建完整侧边栏 JSON 结构并输出"
    )
    parser.add_argument(
        "docs",
        nargs="?",
        default="docs",
        help="docs 目录路径，默认为 docs",
    )
    parser.add_argument(
        "--output",
        "-o",
        dest="output",
        default="theme_config/sidebar_extract",
        metavar="DIR",
        help="输出目录，默认为 theme_config/sidebar_extract",
    )
    parser.add_argument(
        "--indent",
        "-i",
        dest="indent",
        type=int,
        default=2,
        metavar="N",
        help="JSON 缩进空格数，默认为 2",
    )
    parser.add_argument(
        "--no-summary",
        dest="no_summary",
        action="store_true",
        help="不打印模块概览",
    )

    args = parser.parse_args()

    docs_dir = Path(args.docs).resolve()
    output_dir = Path(args.output).resolve()

    print(f"文档目录：{docs_dir}")
    print(f"输出目录：{output_dir}\n")

    modules = scan_docs(docs_dir)

    if not modules:
        print("未扫描到任何模块（请确认 docs 目录下存在子目录且包含 _meta.json）")
        sys.exit(0)

    save_outputs(modules, output_dir, indent=args.indent)

    if not args.no_summary:
        print_summary(modules)


if __name__ == "__main__":
    main()
