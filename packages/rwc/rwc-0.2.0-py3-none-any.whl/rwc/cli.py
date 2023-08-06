import os
import sys
import argparse
from pathlib import Path
from rwc import __version__
from rwc.render import can_render, wordcount


def argument_parser():
    parser = argparse.ArgumentParser(description='reStructuredText and Markdown wordcounter')
    parser.add_argument('--version', action='version', version=f"%(prog)s {__version__}")
    parser.add_argument('paths', metavar='PATH', nargs='+', help='paths to count')
    return parser 


def main():
    parser = argument_parser()
    args = parser.parse_args()

    # for each path given, check if it's a file or a directory
    # if it's a directory, get a list of all files in that directory
    paths = []
    for path in args.paths:
        path = Path(path)
        if path.is_file():
            paths.append(path)

        elif path.is_dir():
            for subpath in path.glob('**/*'):
                if subpath.is_file():
                    paths.append(subpath)

    # perform counts
    counts = {}
    for path in paths:
        if can_render(path):
            with open(path, 'r') as fh:
                count = wordcount(str(path), fh.read())
                if count is not None:
                    counts[str(path)] = count

    # print the per-file counts
    for path in counts.keys():
        print(f"{path}: {counts[path]} words")

    # and print the total
    print("-----")
    print(f"total: {sum(counts.values())} words")

    return 0
