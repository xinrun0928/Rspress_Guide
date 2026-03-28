#!/usr/bin/env python3
"""
统计目录下文件的行数、词数、中文字数、字符数。

Usage:
    python scripts/count.py [path] [--ext EXT] [--exclude PATTERN]
"""

import argparse
import os
import re
import sys
from pathlib import Path
from typing import Optional


def count_file(filepath: Path) -> tuple[int, int, int, int]:
    """统计单个文件的行数、词数、中文字数、字符数。"""
    lines = 0
    tokens = 0
    cchars = 0
    all_chars = 0
    chinese_pattern = re.compile(r"[\u4e00-\u9fff]")

    with open(filepath, encoding="utf-8") as f:
        for raw_line in f:
            lines += 1
            line = raw_line.rstrip("\n\r")
            tokens += len(line.split())
            cchars += len(chinese_pattern.findall(line))
            all_chars += len(line)

    return lines, tokens, cchars, all_chars


def format_number(n: int, width: int = 6) -> str:
    return f"{n:>{width},}"


def walk(
    root: Path,
    extensions: Optional[set[str]] = None,
    exclude_patterns: Optional[list[str]] = None,
) -> list[tuple[Path, int, int, int, int]]:
    """遍历目录，返回 (文件路径, 行数, 词数, 中文字数, 字符数) 列表。"""
    results: list[tuple[Path, int, int, int, int]] = []
    exclude_patterns = exclude_patterns or []

    for dirpath, dirnames, filenames in os.walk(root):
        # 排除隐藏目录和指定目录
        dirnames[:] = [
            d
            for d in dirnames
            if not d.startswith(".") and not any(p in d for p in exclude_patterns)
        ]

        for filename in filenames:
            if filename.startswith("."):
                continue
            filepath = Path(dirpath) / filename

            # 按扩展名过滤
            if extensions and filepath.suffix not in extensions:
                continue

            # 排除匹配的文件
            if any(p in filepath.name for p in exclude_patterns):
                continue

            try:
                lines, tokens, cchars, all_chars = count_file(filepath)
                results.append((filepath, lines, tokens, cchars, all_chars))
            except (UnicodeDecodeError, OSError):
                continue  # 跳过二进制或无法读取的文件

    return results


class Node:
    """树节点，支持文件和目录。"""

    def __init__(
        self,
        name: str,
        depth: int,
        is_dir: bool = False,
    ) -> None:
        self.name = name
        self.depth = depth
        self.is_dir = is_dir
        self.children: list[Node] = []
        self.file: Optional[tuple[int, int, int, int]] = (
            None  # (lines, tokens, cchars, all_chars)
        )

    def totals(self) -> tuple[int, int, int, int]:
        """返回当前节点（含所有后代文件）的统计汇总。"""
        lines = tokens = cchars = all_chars = 0
        if self.file:
            lines, tokens, cchars, all_chars = self.file
        for child in self.children:
            cl, ct, cc, ca = child.totals()
            lines += cl
            tokens += ct
            cchars += cc
            all_chars += ca
        return lines, tokens, cchars, all_chars


def build_tree(
    results: list[tuple[Path, int, int, int, int]],
    root: Path,
) -> list[Node]:
    """将文件列表构建为目录树。"""
    nodes: list[Node] = []
    path_to_node: dict[str, Node] = {}

    # 先按路径排序，确保父目录在子文件之前
    sorted_results = sorted(results, key=lambda r: str(r[0]))

    for filepath, lines, tokens, cchars, all_chars in sorted_results:
        rel = filepath.relative_to(root)
        parts = rel.parts  # 如 ("java", "collection", "hashmap.mdx")
        depth = len(parts)

        for i in range(1, depth + 1):
            node_path = root.joinpath(*parts[:i])
            node_key = str(node_path)
            if node_key in path_to_node:
                continue

            name = parts[i - 1]
            is_dir = i < depth  # 除了最后一个部分，前面都是目录
            node = Node(name=name, depth=i, is_dir=is_dir)

            # 挂到父节点
            if i == 1:
                nodes.append(node)
            else:
                parent_key = str(root.joinpath(*parts[: i - 1]))
                path_to_node[parent_key].children.append(node)

            path_to_node[node_key] = node

        # 最后一个节点是文件，挂载统计数据
        node_key = str(filepath)
        if node_key in path_to_node:
            path_to_node[node_key].file = (lines, tokens, cchars, all_chars)
        else:
            # 不太可能发生，但兜底
            node = Node(name=rel.parts[-1], depth=depth, is_dir=False)
            node.file = (lines, tokens, cchars, all_chars)
            nodes.append(node)
            path_to_node[node_key] = node

    return nodes


def print_tree(nodes: list[Node], root: Path) -> None:
    """先序遍历打印树，同时统计全局总量。"""

    total_lines = total_tokens = total_cchars = total_all_chars = 0
    file_count = 0

    # 收集所有节点用于列宽计算
    all_rows: list[tuple[int, int, int, int, int, int]] = (
        []
    )  # (depth, indent, lines, tokens, cchars, all_chars)

    def collect(node: Node) -> None:
        nonlocal total_lines, total_tokens, total_cchars, total_all_chars, file_count
        indent = node.depth - 1
        if node.file:
            lines, tokens, cchars, all_chars = node.file
            total_lines += lines
            total_tokens += tokens
            total_cchars += cchars
            total_all_chars += all_chars
            file_count += 1
        else:
            lines, tokens, cchars, all_chars = node.totals()
        all_rows.append((node.depth, indent, lines, tokens, cchars, all_chars, node.name, node.is_dir))

    def walk_nodes(ns: list[Node]) -> None:
        for n in ns:
            collect(n)
            walk_nodes(n.children)

    walk_nodes(nodes)

    if not all_rows:
        print("未找到任何文件。")
        return

    # 确定列宽
    max_lines = max(r[2] for r in all_rows) if all_rows else 0
    max_tokens = max(r[3] for r in all_rows) if all_rows else 0
    max_cchars = max(r[4] for r in all_rows) if all_rows else 0
    max_all_chars = max(r[5] for r in all_rows) if all_rows else 0

    # 文件名列宽 = 基准 4（"文件"）与最深缩进后所有标签的最大视觉宽度
    label_w = 4
    for depth, indent, _, _, _, _, name, is_dir in all_rows:
        prefix = "  " * indent + ("📂 " if is_dir else "📄 ")
        label_w = max(label_w, len(prefix) + len(name))

    lines_w = max(len(format_number(total_lines)), len(f"{max_lines:,}")) + 1
    tokens_w = max(len(format_number(total_tokens)), len(f"{max_tokens:,}")) + 1
    cchars_w = max(len(format_number(total_cchars)), len(f"{max_cchars:,}")) + 1
    all_chars_w = max(len(format_number(total_all_chars)), len(f"{max_all_chars:,}")) + 1

    # 打印表头
    print(
        f"{'文件':<{label_w}}"
        f" {'行数':<{lines_w}}"
        f" {'词数':<{tokens_w}}"
        f" {'中文字数':<{cchars_w}}"
        f" {'字符数':<{all_chars_w}}"
    )
    print(f"{'─' * label_w} {'─' * lines_w}  {'─' * tokens_w}  {'─' * cchars_w}  {'─' * all_chars_w}")

    # 打印每一行
    for depth, indent, lines, tokens, cchars, all_chars, name, is_dir in all_rows:
        prefix = "  " * indent + ("📂 " if is_dir else "📄 ")
        label = prefix + name
        style = "\033[1m" if is_dir else ""
        reset = "\033[0m" if is_dir else ""
        print(
            f"{style}{label:<{label_w}}{reset}"
            f" {format_number(lines):<{lines_w}}"
            f" {format_number(tokens):<{tokens_w}}"
            f" {format_number(cchars):<{cchars_w}}"
            f" {format_number(all_chars):<{all_chars_w}}"
        )

    # 打印总计
    print(f"{'─' * label_w} {'─' * lines_w}  {'─' * tokens_w}  {'─' * cchars_w}  {'─' * all_chars_w}")
    print(
        f"{'总计':<{label_w}}"
        f" {format_number(total_lines):<{lines_w}}"
        f" {format_number(total_tokens):<{tokens_w}}"
        f" {format_number(total_cchars):<{cchars_w}}"
        f" {format_number(total_all_chars):<{all_chars_w}}"
    )
    print(f"\n共 {file_count} 个文件")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="统计目录下文件的行数、词数、中文字数、字符数"
    )
    parser.add_argument(
        "path",
        nargs="?",
        default="docs",
        help="要统计的目录路径，默认为 docs",
    )
    parser.add_argument(
        "--ext",
        "-e",
        dest="extensions",
        metavar="EXT",
        help="按扩展名过滤，如 md mdx（如需多个，用逗号分隔）",
    )
    parser.add_argument(
        "--exclude",
        "-x",
        dest="exclude",
        metavar="PATTERN",
        action="append",
        default=[],
        help="排除包含该字符串的文件或目录（可多次指定）",
    )
    args = parser.parse_args()

    root = Path(args.path).resolve()
    if not root.exists():
        print(f"错误：路径不存在: {root}", file=sys.stderr)
        sys.exit(1)
    if not root.is_dir():
        print(f"错误：路径不是目录: {root}", file=sys.stderr)
        sys.exit(1)

    # 解析扩展名
    extensions: Optional[set[str]] = None
    if args.extensions:
        raw = args.extensions.strip().lstrip(".,")
        if raw:
            extensions = {f".{ext.strip().lstrip('.')}" for ext in raw.split(",")}

    results = walk(root, extensions=extensions, exclude_patterns=args.exclude)
    print(f"\n📊 统计目录: {root}\n")
    nodes = build_tree(results, root)
    print_tree(nodes, root)


if __name__ == "__main__":
    main()
