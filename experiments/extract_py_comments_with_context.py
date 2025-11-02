"""
使用 tree_sitter_languages 提取 Python 文件的注释信息。
包括注释所在的行数和函数上下文。
"""

import json
from pathlib import Path
from typing import Any

from tree_sitter_languages import get_parser


class PythonCommentExtractor:
    """Python 注释提取器"""

    def __init__(self):
        self.parser = get_parser("python")
        self.source_code = b""
        self.source_lines = []

    def parse_file(self, file_path: str | Path) -> dict[str, Any]:
        """
        解析 Python 文件并提取注释信息

        Args:
            file_path: Python 文件路径

        Returns:
            包含注释信息的字典
        """
        file_path = Path(file_path)
        self.source_code = file_path.read_bytes()
        self.source_lines = self.source_code.decode("utf-8").split("\n")

        tree = self.parser.parse(self.source_code)
        root_node = tree.root_node

        comments = []
        self._extract_comments(root_node, comments)

        return {
            "file": str(file_path),
            "total_comments": len(comments),
            "comments": comments,
        }

    def _extract_comments(self, node, comments: list) -> None:
        """
        递归提取所有注释节点

        Args:
            node: tree-sitter 节点
            comments: 注释列表
        """
        # 提取 # 注释
        if node.type == "comment":
            comment_info = self._extract_comment_info(node)
            comments.append(comment_info)

        # 提取 docstring（字符串字面量作为表达式语句）
        elif node.type == "expression_statement":
            if node.children and node.children[0].type == "string":
                string_node = node.children[0]
                # 判断是否为 docstring
                if self._is_docstring(node):
                    comment_info = self._extract_docstring_info(string_node, node)
                    comments.append(comment_info)

        # 递归处理子节点
        for child in node.children:
            self._extract_comments(child, comments)

    def _is_docstring(self, expr_stmt_node) -> bool:
        """
        判断表达式语句是否为 docstring

        Docstring 通常是模块、类或函数的第一条语句
        """
        parent = expr_stmt_node.parent
        if parent is None:
            return False

        # 模块级 docstring
        if parent.type == "module":
            # 检查是否为第一个非注释子节点
            for child in parent.children:
                if child.type == "comment":
                    continue
                return child == expr_stmt_node

        # 函数或类的 docstring
        if parent.type in ("function_definition", "class_definition"):
            # 查找 block 节点
            for child in parent.children:
                if child.type == "block":
                    # 检查是否为 block 的第一个表达式语句
                    for block_child in child.children:
                        if block_child.type == "comment":
                            continue
                        return block_child == expr_stmt_node
        return False

    def _extract_comment_info(self, node) -> dict[str, Any]:
        """
        提取单行注释信息

        Args:
            node: comment 节点

        Returns:
            注释信息字典
        """
        start_line = node.start_point[0] + 1  # tree-sitter 行号从 0 开始
        end_line = node.end_point[0] + 1
        comment_text = node.text.decode("utf-8")

        # 查找所在的函数或类
        context = self._find_context(node)

        return {
            "type": "comment",
            "text": comment_text,
            "start_line": start_line,
            "end_line": end_line,
            "context": context,
        }

    def _extract_docstring_info(self, string_node, expr_stmt_node) -> dict[str, Any]:
        """
        提取 docstring 信息

        Args:
            string_node: string 节点
            expr_stmt_node: expression_statement 节点

        Returns:
            docstring 信息字典
        """
        start_line = string_node.start_point[0] + 1
        end_line = string_node.end_point[0] + 1
        docstring_text = string_node.text.decode("utf-8")

        # 查找所在的函数或类
        context = self._find_context(expr_stmt_node)

        return {
            "type": "docstring",
            "text": docstring_text,
            "start_line": start_line,
            "end_line": end_line,
            "context": context,
        }

    def _find_context(self, node) -> dict[str, Any]:
        """
        查找节点所在的上下文（函数或类）

        Args:
            node: tree-sitter 节点

        Returns:
            上下文信息字典
        """
        current = node.parent
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
    # 设置路径
    root = Path(__file__).parent
    dataset_dir = root / "datasets"

    # 创建提取器
    extractor = PythonCommentExtractor()

    # 查找所有 Python 文件
    py_files = list(dataset_dir.glob("*.py"))

    if not py_files:
        print(f"在 {dataset_dir} 中未找到 Python 文件")
        return

    print(f"找到 {len(py_files)} 个 Python 文件")
    print("=" * 80)

    for py_file in py_files:
        print(f"\n处理文件: {py_file.name}")
        print("-" * 80)

        result = extractor.parse_file(py_file)

        print(f"总注释数: {result['total_comments']}\n")

        for i, comment in enumerate(result["comments"], 1):
            print(f"[{i}] {comment['type'].upper()}")
            print(f"    行号: {comment['start_line']}-{comment['end_line']}")
            print(f"    文本: {comment['text'][:100]}...")  # 限制显示长度

            # 显示上下文信息
            context = comment["context"]
            if "chain" in context:
                # 多层嵌套
                chain_info = " -> ".join(
                    [f"{c['type']}:{c['name']}" for c in context["chain"]]
                )
                print(f"    上下文: {chain_info}")
                # 显示最内层函数的代码
                innermost = context["chain"][-1]
                print(
                    f"    所在{innermost['type']}代码 ({innermost['start_line']}-{innermost['end_line']}):"
                )
                print(
                    "    " + "\n    ".join(innermost["code"].split("\n")[:5])
                )  # 显示前5行
            elif context["type"] in ("function", "class"):
                print(f"    上下文: {context['type']}:{context['name']}")
                print(
                    f"    所在{context['type']}代码 ({context['start_line']}-{context['end_line']}):"
                )
                print(
                    "    " + "\n    ".join(context["code"].split("\n")[:5])
                )  # 显示前5行
            else:
                print(f"    上下文: {context['type']}")

            print()

        # 保存到 JSON 文件
        output_file = root / f"{py_file.stem}_comments.json"
        with output_file.open("w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        print(f"\n结果已保存到: {output_file}")
        print("=" * 80)


if __name__ == "__main__":
    main()
