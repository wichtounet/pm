import argparse
import sys
import pm

from pm.projects import list_projects


def build_parser():
    parser = argparse.ArgumentParser(description='')

    parser.add_argument('--version',
                        action='version',
                        version='%(prog)s ' + pm.VERSION)

    action = parser.add_mutually_exclusive_group()
    action.add_argument('-a', '--all',
                        action='store_true',
                        help='Show non git projects too')
    action.add_argument('-n', '--non-git-only',
                        action='store_true',
                        help='Show only non git projects')

    return parser


def main(args=None):
    # Parse command line
    parser = build_parser()
    args = parser.parse_args(args)

    if not args.non_git_only:
        projects = list_projects(args.all)
    else:
        all = list_projects(True)
        git = list_projects(False)

        projects = list(set(all) - set(git))

    for p in projects:
        print(p.name)

    print("")
    print("{} projects".format(len(projects)))

    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv))
