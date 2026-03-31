import argparse
import textwrap


arg_parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description="codetwin - Code Similarity Detection",
    epilog=textwrap.dedent(
        """
        AST-based code similarity checking for specified programming language and files.
        """
    ),
)
arg_parser.add_argument(
    "source_filenames",
    nargs='+',
    help="The source code files you want to check."
)
arg_parser.add_argument(
    "-f",
    dest="function_name",
    default="*",
    help="The specific function you want to check."
)
arg_parser.add_argument(
    "--threshold",
    type=int,
    default=5,
    help="The threshold value controlling the granularity of the matching. Default 5.",
)
