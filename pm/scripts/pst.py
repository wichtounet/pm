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
    parser.add_argument('-f', '--fetch',
                        action='store_true',
                        help='fetch remotes before querying status')
    parser.add_argument('dir', nargs='?',
                        help='Look for projects in ~/dir or dir if absolute')

    return parser

color_red = "\033[0;31m"
color_green = "\033[0;32m"
color_off = "\033[0;3047m"

def green_print(message):
    print(color_green + message + color_off)

def red_print(message):
    print(color_red + message + color_off)

def main(args=None):
    # Parse command line
    parser = build_parser()
    args = parser.parse_args(args)

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

    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv))
