"""
使用 tree_sitter_languages 根据关键词提取代码片段及其上下文信息。
"""

import json
from pathlib import Path
from typing import Any

from tree_sitter_languages import get_parser


class KeywordExtractor:
    """关键词提取器"""

    def __init__(self):
        self.parser = get_parser("python")
        self.source_code = b""
        self.source_lines = []
        self.tree = None

    def parse_file(self, file_path: str | Path, keyword: str) -> dict[str, Any]:
        """
        解析 Python 文件并根据关键词提取代码片段

        Args:
            file_path: Python 文件路径
            keyword: 要搜索的关键词

        Returns:
            包含匹配信息的字典
        """
        file_path = Path(file_path)
        self.source_code = file_path.read_bytes()
        self.source_lines = self.source_code.decode("utf-8").split("\n")

        self.tree = self.parser.parse(self.source_code)

        matches = []
        self._search_keyword(keyword, matches)

        return {
            "file": str(file_path),
            "keyword": keyword,
            "total_matches": len(matches),
            "matches": matches,
        }

    def _search_keyword(self, keyword: str, matches: list) -> None:
        """
        搜索包含关键词的代码行

        Args:
            keyword: 搜索关键词
            matches: 匹配结果列表
        """
        for line_num, line in enumerate(self.source_lines, start=1):
            if keyword in line:
                # 找到匹配的行，提取上下文信息
                match_info = self._extract_match_info(line_num, line, keyword)
                matches.append(match_info)

    def _extract_match_info(
        self, line_num: int, line: str, keyword: str
    ) -> dict[str, Any]:
        """
        提取匹配行的信息

        Args:
            line_num: 行号（从 1 开始）
            line: 行内容
            keyword: 关键词

        Returns:
            匹配信息字典
        """
        # 计算关键词在行中的列位置
        col_start = line.find(keyword)

        # tree-sitter 的行号从 0 开始
        tree_line_num = line_num - 1

        # 在 tree-sitter 中查找该位置的节点
        node = self._find_node_at_position(tree_line_num, col_start)

        # 查找所在的上下文（函数或类）
        context = self._find_context(node)

        return {
            "text": line.strip(),
            "keyword": keyword,
            "start_line": line_num,
            "end_line": line_num,
            "column_start": col_start,
            "column_end": col_start + len(keyword),
            "context": context,
        }

    def _find_node_at_position(self, line: int, column: int):
        """
        查找指定位置的 AST 节点

        Args:
            line: 行号（从 0 开始）
            column: 列号（从 0 开始）

        Returns:
            最小的包含该位置的节点
        """
        root = self.tree.root_node

        def find_smallest_node(node):
            """递归查找最小的包含指定位置的节点"""
            # 检查当前节点是否包含该位置
            if not (
                node.start_point[0] <= line <= node.end_point[0]
                and (line != node.start_point[0] or column >= node.start_point[1])
                and (line != node.end_point[0] or column <= node.end_point[1])
            ):
                return None

            # 递归检查子节点
            for child in node.children:
                result = find_smallest_node(child)
                if result is not None:
                    return result

            # 如果没有更小的子节点包含该位置，返回当前节点
            return node

        return find_smallest_node(root)

    def _find_context(self, node) -> dict[str, Any]:
        """
        查找节点所在的上下文（函数或类）

        Args:
            node: tree-sitter 节点

        Returns:
            上下文信息字典
        """
        if node is None:
            return {"type": "module", "name": None}

        current = node
        context_stack = []

        while current is not None:
            if current.type == "function_definition":
                func_info = self._extract_function_info(current)
                context_stack.append(func_info)
            elif current.type == "class_definition":
                class_info = self._extract_class_info(current)
                context_stack.append(class_info)
            current = current.parent

        # 反转堆栈，使得最外层的上下文在前
        context_stack.reverse()

        if not context_stack:
            return {"type": "module", "name": None}

        return (
            context_stack[-1] if len(context_stack) == 1 else {"chain": context_stack}
        )

    def _extract_function_info(self, func_node) -> dict[str, Any]:
        """
        提取函数信息

        Args:
            func_node: function_definition 节点

        Returns:
            函数信息字典
        """
        func_name = None
        params = []

        for child in func_node.children:
            if child.type == "identifier":
                func_name = child.text.decode("utf-8")
            elif child.type == "parameters":
                params = self._extract_parameters(child)

        start_line = func_node.start_point[0] + 1
        end_line = func_node.end_point[0] + 1

        # 提取函数代码
        func_code = "\n".join(self.source_lines[start_line - 1 : end_line])

        return {
            "type": "function",
            "name": func_name,
            "parameters": params,
            "start_line": start_line,
            "end_line": end_line,
            "code": func_code,
        }

    def _extract_class_info(self, class_node) -> dict[str, Any]:
        """
        提取类信息

        Args:
            class_node: class_definition 节点

        Returns:
            类信息字典
        """
        class_name = None

        for child in class_node.children:
            if child.type == "identifier":
                class_name = child.text.decode("utf-8")
                break

        start_line = class_node.start_point[0] + 1
        end_line = class_node.end_point[0] + 1

        # 提取类代码
        class_code = "\n".join(self.source_lines[start_line - 1 : end_line])

        return {
            "type": "class",
            "name": class_name,
            "start_line": start_line,
            "end_line": end_line,
            "code": class_code,
        }

    def _extract_parameters(self, params_node) -> list[str]:
        """
        提取函数参数

        Args:
            params_node: parameters 节点

        Returns:
            参数列表
        """
        params = []
        for child in params_node.children:
            if child.type == "identifier":
                params.append(child.text.decode("utf-8"))
            elif child.type == "typed_parameter":
                for subchild in child.children:
                    if subchild.type == "identifier":
                        params.append(subchild.text.decode("utf-8"))
                        break
            elif child.type == "default_parameter":
                for subchild in child.children:
                    if subchild.type == "identifier":
                        params.append(subchild.text.decode("utf-8"))
                        break
        return params


def main():
    """主函数"""
    import sys

    # 设置路径
    root = Path(__file__).parent
    dataset_dir = Path("/home/haifeng/data/pytorch/torch")

    # 设置关键词（可以从命令行参数获取）
    keyword = "a * b" if len(sys.argv) < 2 else sys.argv[1]

    # 创建提取器
    extractor = KeywordExtractor()

    # 查找所有 Python 文件
    py_files = list(dataset_dir.glob("*.py"))

    if not py_files:
        print(f"在 {dataset_dir} 中未找到 Python 文件")
        return

    print(f"搜索关键词: '{keyword}'")
    print(f"找到 {len(py_files)} 个 Python 文件")
    print("=" * 80)

    all_results = []

    for py_file in py_files:
        result = extractor.parse_file(py_file, keyword)
        from pprint import pprint

        pprint(
            result,
            indent=4,  # 缩进空格数
            depth=6,  # 只显示到第几层
            sort_dicts=False,  # 是否按键排序
        )
        break
        print()
        if result["total_matches"] > 0:
            print(f"\n文件: {py_file.name}")
            print("-" * 80)
            print(f"找到 {result['total_matches']} 处匹配\n")

            for i, match in enumerate(result["matches"], 1):
                print(f"[{i}] 第 {match['start_line']} 行，列 {match['column_start']}")
                print(f"    代码: {match['text']}")

                # 显示上下文信息
                context = match["context"]

                if "chain" in context:
                    # 多层嵌套
                    chain_info = " -> ".join(
                        [f"{c['type']}:{c['name']}" for c in context["chain"]]
                    )
                    print(f"    上下文: {chain_info}")
                    # 显示最内层函数/类的信息
                    innermost = context["chain"][-1]
                    print(f"    所在{innermost['type']}: {innermost['name']}")
                    print(
                        f"    {innermost['type']}范围: {innermost['start_line']}-{innermost['end_line']} 行"
                    )
                    print(f"    参数: {innermost.get('parameters', 'N/A')}")
                    print(f"\n    完整{innermost['type']}代码:")
                    for line in innermost["code"].split("\n"):
                        print(f"      {line}")
                elif context["type"] in ("function", "class"):
                    print(f"    上下文: {context['type']}:{context['name']}")
                    print(
                        f"    {context['type']}范围: {context['start_line']}-{context['end_line']} 行"
                    )
                    print(f"    参数: {context.get('parameters', 'N/A')}")
                    print(f"\n    完整{context['type']}代码:")
                    for line in context["code"].split("\n"):
                        print(f"      {line}")
                else:
                    print("    上下文: 模块级别")

                print()

            # 保存到 JSON 文件
            output_file = (
                root
                / f"{py_file.stem}_keyword_{keyword.replace(' ', '_').replace('*', 'star')}.json"
            )
            with output_file.open("w", encoding="utf-8") as f:
                json.dump(result, f, ensure_ascii=False, indent=2)
            print(f"结果已保存到: {output_file}")
            print("=" * 80)

            all_results.append(result)

    if not all_results:
        print(f"\n未找到包含关键词 '{keyword}' 的代码")


if __name__ == "__main__":
    main()
