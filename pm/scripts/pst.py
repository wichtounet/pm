import argparse
import sys
import pm

from pm.projects import list_projects


def build_parser():
    parser = argparse.ArgumentParser(description='')

    parser.add_argument('--version',
                        action='version',
                        version='%(prog)s ' + pm.VERSION)

    return parser


def main(args=None):
    # Parse command line
    parser = build_parser()
    args = parser.parse_args(args)

    projects = list_projects(False)

    for p in projects:
        print(p.name)

    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv))
