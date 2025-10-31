"""
This is a module-level docstring.
It can span multiple lines and is used to document modules.
"""

# Single-line comment
# This is the most common type of comment in Python


def function_with_docstring(x, y):
    """
    This is a function docstring.

    Args:
        x: First parameter
        y: Second parameter

    Returns:
        The sum of x and y
    """
    return x + y


def another_function(a, b):
    """
    Triple single quotes also work for docstrings.

    Parameters:
        a (int): First number
        b (int): Second number

    Returns:
        int: The product of a and b
    """
    # Inline comment on the same line
    result = a * b  # Comment at end of line
    return result


class SampleClass:
    """
    Class-level docstring.

    This class demonstrates different types of comments.
    """

    def __init__(self):
        """Constructor docstring."""
        self.value = 0  # Attribute comment

    def method(self):
        """Method docstring."""
        pass


# TODO: This is a TODO comment
# FIXME: This is a FIXME comment
# NOTE: This is a NOTE comment
# XXX: This is a warning comment


def multiline_comment_example():
    """
    Multi-line comments can be achieved using:
    1. Multiple single-line comments
    2. Triple-quoted strings (docstrings)
    """

    # This is a multi-line comment
    # using multiple single-line comments
    # Each line starts with #

    """
    This is NOT a true multi-line comment,
    but a string literal that gets ignored.
    Often used as a multi-line comment workaround.
    """

    x = 10

    return x


# === Section divider comment ===

### Another style of section comment ###

#############################################
# Box-style comment block
#############################################

"""
Special comment patterns:
"""

# Comment with special characters: é, ñ, 中文, 日本語
# Comment with code: print("Hello")
# Comment with URL: https://example.com
# Comment with email: user@example.com
