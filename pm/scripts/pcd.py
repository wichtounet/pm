import argparse
import os
import pm
import sys

from pm.projects import dev_directory


def build_parser():
    parser = argparse.ArgumentParser(description='')

    parser.add_argument('--version',
                        action='version',
                        version='%(prog)s ' + pm.VERSION)
    parser.add_argument('directory')
    parser.add_argument('dir', nargs='?',
                        help='Look for projects in ~/dir or dir if absolute')

    return parser


def main(args=None):
    # Parse command line
    parser = build_parser()
    args = parser.parse_args(args)

    devdir = dev_directory(args.dir)
    projectdir = os.path.join(devdir, args.directory)

    if os.path.isdir(projectdir):
        print(projectdir)

        return 0
    else:
        if not os.path.exists(projectdir):
            print("{} does not exist".format(projectdir))
        else:
            print("{} is not a directory".format(projectdir))

        return 1

if __name__ == '__main__':
    sys.exit(main(sys.argv))
