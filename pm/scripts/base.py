from __future__ import print_function

import argparse
import sys
import pm
import subprocess

from pm.console import blue_print, green_print, red_print, cyan_print
from pm.projects import list_projects


def build_parser():
    parser = argparse.ArgumentParser(description='')

    parser.add_argument('--version',
                        action='version',
                        version='%(prog)s ' + pm.VERSION)

    subparsers = parser.add_subparsers(help='Subcommands',
                                       description='Valid subcommands')

    parser_status = subparsers.add_parser('status', help='check status')
    parser_status.add_argument('-f', '--fetch',
                               action='store_true',
                               help='fetch remotes before querying status')
    parser_status.add_argument('dir', nargs='?',
                               help=('Look for projects in ~/dir'
                                     ' or dir if absolute'))

    parser_status.set_defaults(func=status)

    parser_ls = subparsers.add_parser('ls', help='List projects')
    parser_ls.set_defaults(func=ls)

    parser_ls.add_argument('dir', nargs='?',
                           help=('Look for projects in ~/dir'
                                 ' or dir if absolute'))

    action = parser_ls.add_mutually_exclusive_group()
    action.add_argument('-a', '--all',
                        action='store_true',
                        help='Show non git projects too')
    action.add_argument('-n', '--non-git-only',
                        action='store_true',
                        help='Show only non git projects')

    return parser


# Return true if the remote exists, false otherwise
def remote_branch_exist(project, branch):
    command = ["git", "-C", project.folder, "branch", "-a"]

    result = subprocess.check_output(command)

    remote_branch = "remotes/" + branch

    return remote_branch in result


# Return the status of the project
def status_branch(project):
    command = ["git", "-C", project.folder, "status"]

    status = subprocess.check_output(command)

    return status


# Return the hash of the current commit of the given branch
def branch_hash(project, branch):
    command = ["git", "-C", project.folder, "rev-parse", "--verify", branch]

    return subprocess.check_output(command)


def status(args=None):
    projects = list_projects(False, args.dir)

    for p in projects:
        print(p.name)

        if args.fetch:
            p.fetch_all()

        status = status_branch(p)

        clean = True

        print("\t", end="")

        blue_print("{0:<30s}".format(p.branch()))

        if "nothing to commit" not in status:
            red_print("Uncommitted changes")
            clean = False

        if "Your branch is ahead of '" in status:
            if not clean:
                print(" - ", end="")
            red_print("Ahead of remote")
            clean = False

        if "Your branch is behind '" in status:
            if not clean:
                print(" - ", end="")
            red_print("Behind remote")
            clean = False

        if "' have diverged" in status:
            if not clean:
                print(" - ", end="")
            red_print("Diverged with remote")
            clean = False

        if clean:
            green_print("Clean")

        print("")

        for branch in p.branches():
            if branch == p.branch():
                continue

            print("\t", end="")

            cyan_print("{0:<30s}".format(branch))

            remote_branch = "origin/" + branch

            if not remote_branch_exist(p, remote_branch):
                red_print("No remote branch {}".format(remote_branch))
            else:
                local_hash = branch_hash(p, branch)
                remote_hash = branch_hash(p, remote_branch)

                if local_hash == remote_hash:
                    green_print("Clean")
                else:
                    red_print("{} not in sync with {}"
                              .format(branch, remote_branch))

            print("")

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
