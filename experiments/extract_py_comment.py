import io
import tokenize
from pathlib import Path

root = Path(__file__).parent

code = (root / "datasets/python_comments.py").read_text()

tokens = tokenize.generate_tokens(io.StringIO(code).readline)

for token in tokens:
    if token.type == tokenize.COMMENT:
        print(token.string)
    elif token.type == tokenize.STRING:
        print(token.string)
