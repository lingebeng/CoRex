from rich.console import Console
from rich.text import Text
from rich.tree import Tree
from tree_sitter import Parser
from tree_sitter_languages import get_language

# 初始化 rich 控制台
console = Console()

# 初始化 Tree-sitter 解析器
parser = Parser()
parser.set_language(get_language("python"))

# 解析代码
code = b"""
def func(n):
    '''This is a docstring'''
    # This is a comment
    ans = 0
    for i in range(n):
        if i % 2 == 0:
            ans += i  # Inline comment
    return ans
print(func(10))
"""

tree = parser.parse(code)
root = tree.root_node


# 构建 rich 树
def build_tree(node, code):
    # 节点文本（取代码片段）
    snippet = (
        code[node.start_byte : node.end_byte]
        .decode("utf-8")
        .strip()
        .replace("\n", "⏎ ")
    )
    if len(snippet) > 60:
        snippet = snippet[:60] + "..."

    # 富文本显示
    label = Text()
    label.append(f"{node.type}", style="bold cyan")
    label.append(
        f"  [{node.start_point[0] + 1}:{node.start_point[1]}→{node.end_point[0] + 1}:{node.end_point[1]}]",
        style="dim",
    )
    label.append(f"  “{snippet}”", style="green")

    rich_node = Tree(label)
    for child in node.children:
        rich_node.add(build_tree(child, code))
    return rich_node


if __name__ == "__main__":
    ast_tree = build_tree(root, code)
    console.print(ast_tree)
