import argparse
import sys
import pm
import subprocess

from pm.projects import list_projects


def build_parser():
    parser = argparse.ArgumentParser(description='')

    parser.add_argument('--version',
                        action='version',
                        version='%(prog)s ' + pm.VERSION)
    parser.set_defaults(func=status)

    subparsers = parser.add_subparsers(help='Subcommands', 
                                       description='Valid subcommands')

    parser_status = subparsers.add_parser('status', help='check status')
    parser_status.add_argument('-f', '--fetch',
                               action='store_true',
                               help='fetch remotes before querying status')
    parser_status.add_argument('dir', nargs='?',
                        help='Look for projects in ~/dir or dir if absolute')

    parser_status.set_defaults(func=status)
    
    parser_ls = subparsers.add_parser('ls', help='List projects')
    parser_ls.set_defaults(func=ls)
    
    parser_ls.add_argument('dir', nargs='?',
                        help='Look for projects in ~/dir or dir if absolute')

    action = parser_ls.add_mutually_exclusive_group()
    action.add_argument('-a', '--all',
                        action='store_true',
                        help='Show non git projects too')
    action.add_argument('-n', '--non-git-only',
                        action='store_true',
                        help='Show only non git projects')

    return parser

color_red = "\033[0;31m"
color_green = "\033[0;32m"
color_off = "\033[0;3047m"

def green_print(message):
    print(color_green + message + color_off)


def red_print(message):
    print(color_red + message + color_off)


def status(args=None):
    projects = list_projects(False, args.dir)

    for p in projects:
        print(p.name)

        if args.fetch:
            p.fetch_all()

        command = ["git", "-C", p.folder, "status"]

        status = subprocess.check_output(command)

        clean = True

        if not "nothing to commit" in status:
            red_print("\tUncommitted changes")
            clean = False

        if "Your branch is ahead of '" in status:
            red_print("\tAhead of remote")
            clean = False

        if "Your branch is behind '" in status:
            red_print("\tBehind remote")
            clean = False

        if clean:
            green_print("\tClean")

        print("")


def ls(args=None):
    if not args.non_git_only:
        projects = list_projects(args.all, args.dir)
    else:
        all = list_projects(True, args.dir)
        git = list_projects(False, args.dir)

        projects = list(set(all) - set(git))

    for p in projects:
        print(p.name)

    print("")
    print("{} projects".format(len(projects)))


def main(args=None):
    # Parse command line
    parser = build_parser()
    args = parser.parse_args(args)

    # Call the sub command
    args.func(args)

    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv))
