from __future__ import print_function

import argparse
import sys
import pm

from multiprocessing.pool import ThreadPool as Pool

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
    parser_status.add_argument('-s', '--submodule',
                               action='store_true',
                               help='display the status of submodules')
    parser_status.add_argument('-p', '--parallel-fetch',
                               action='store_true',
                               help='Allow parallel fetching')
    parser_status.add_argument("-j", type=int, help="Use J threads")
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
                        help='Show non-versioned  projects too')
    action.add_argument('-n', '--non-scm-only',
                        action='store_true',
                        help='Show only non versioned projects')

    return parser


def print_subproject(project, sp, padder):
    blue_print("   {1}-> {2:<{0}s}".format(30 - len(padder) - 2,
                                           padder, sp.name))

    project.print_submodule_status(sp)

    print()
    for ssp in sp.subs:
        print_subproject(project, ssp, padder + "  ")


def status(args=None):
    projects = list_projects(False, args.dir)

    if args.parallel_fetch and not args.fetch:
        print("Warning: -p has no effect without -f")

    if args.parallel_fetch and not args.j:
        print("Warning: -p has no effect without -j")

    if args.fetch:
        print("Fetch in progres...")

    if args.j:
        pool = Pool(args.j)

        def worker(p):
            p.cache(args.submodule)

            if args.parallel_fetch:
                p.fetch_all()

                if args.submodule:
                    p.fetch_submodules()

        for p in projects:
            pool.apply_async(worker, (p,))

        pool.close()
        pool.join()

    if args.fetch and not (args.j and args.parallel_fetch):
        for p in projects:
            p.fetch_all()

            if args.submodule:
                p.fetch_submodules()

    if args.fetch:
        print("Fetch done")

    for p in projects:
        print(p.name)

        print("    ", end="")

        blue_print("{0:<30s}".format(p.branch()))

        p.print_status()

        print("")

        if args.submodule:
            for sub in p.subprojects():
                print_subproject(p, sub, " ")

        for branch in p.branches():
            if branch == p.branch():
                continue

            print("    ", end="")

            cyan_print("{0:<30s}".format(branch))

            remote_branch = "origin/" + branch

            if not p.remote_branch_exist(remote_branch):
                red_print("No remote branch {}".format(remote_branch))
            else:
                local_hash = p.hash(branch)
                remote_hash = p.hash(remote_branch)

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
        print("{} (scm:{})".format(p.name, p.scm))

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
