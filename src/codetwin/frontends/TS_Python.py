import os
import json
from tree_sitter import Parser, Language
from tree_sitter_python import language as get_python_language
from typing import List

import codetwin
from codetwin.AST import AST
from codetwin.args import arg_parser
from codetwin.driver import driver


# Get Python language (returns a PyCapsule)
PYTHON_LANG_CAPSULE = get_python_language()
# Wrap it in Language object for compatibility
try:
    PYTHON_LANG = Language(PYTHON_LANG_CAPSULE)
except TypeError:
    # If that fails, store the capsule for direct use
    PYTHON_LANG = PYTHON_LANG_CAPSULE
PYTHON_FUNCTION_KIND = "function_definition"
PYTHON_IDENTIFIER_KIND = "identifier"
PYTHON_COMMENT_KIND = "comment"

PYTHON_IGNORE_KINDS = {
    PYTHON_COMMENT_KIND
}


class Python_AST(AST):
    def __init__(self, parent=None, name=None, text=None, start_pos=None, end_pos=None, kind=None):
        AST.__init__(self, parent, name, text, start_pos, end_pos, kind)

    @classmethod
    def create(cls, path):
        def helper(cursor, parent=None):
            python_ast_node = Python_AST(
                parent=parent,
                name="",
                text=cursor.node.text,
                start_pos=cursor.node.start_point,
                end_pos=cursor.node.end_point,
                kind=cursor.node.type
            )

            if cursor.node.type == PYTHON_FUNCTION_KIND:
                for node in cursor.node.children:
                    if node.type == PYTHON_IDENTIFIER_KIND:
                        python_ast_node.name = node.text
                        break

            python_ast_node.weight = 1

            has_more_children = cursor.goto_first_child()
            if not has_more_children:
                return python_ast_node

            while has_more_children:
                if cursor.node.type in PYTHON_IGNORE_KINDS:
                    has_more_children = cursor.goto_next_sibling()
                    continue

                child_node = helper(cursor, python_ast_node)
                python_ast_node.children.append(child_node)
                python_ast_node.weight += child_node.weight

                has_more_children = cursor.goto_next_sibling()

            cursor.goto_parent()
            return python_ast_node

        with open(path, "rb") as f:
            parser = Parser()
            try:
                # Try new API (tree-sitter 0.20+)
                parser.language = PYTHON_LANG
            except TypeError:
                # Fall back to old API
                parser.set_language(PYTHON_LANG)

            tree = parser.parse(f.read())
            cursor = tree.walk()
            return helper(cursor)


def main(
    source_filenames: List[str],
    function_name: str,
    threshold: int
):
    return driver(
        Python_AST,
        source_filenames=source_filenames,
        function_name=function_name,
        function_kind=PYTHON_FUNCTION_KIND,
        threshold=threshold
    )


if __name__ == "__main__":
    args = arg_parser.parse_args()

    result = main(
        source_filenames=args.source_filenames,
        function_name=args.function_name,
        threshold=args.threshold,
    )

    print(json.dumps(result, indent=2, default=str))
