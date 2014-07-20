from __future__ import print_function

import subprocess
import os

from pm.console import green_print, red_print
from pm.scm.base import subproject
from pm.memoized import memoized


class submodule:
    def __init__(self, name):
        self.name = name
        self.subs = dict()


def to_subproject(sm, parent=None):
    p = subproject(sm.name)
    p.parent = parent

    for key in sm.subs:
        m = sm.subs[key]

        p.subs.append(to_subproject(m, p))

    return p


def exec_command(command):
    return subprocess.check_output(command, universal_newlines=True)


class Git:
    def __init__(self, project):
        self.project = project

    def folder(self):
        return self.project.folder

    def fetch(self, remote):
        command = ["git", "-C", self.folder(), "fetch", "--quiet", remote]

        exec_command(command)

    def sub_folder(self, sub):
        parts = []

        while sub.parent is not None:
            parts.append(sub.name)

            sub = sub.parent

        parts.append(sub.name)

        path = self.folder()

        for part in reversed(parts):
            path = os.path.join(path, part)

        return path

    def fetch_sub(self, sub):
        path = self.sub_folder(sub)

        for remote in self.remotes_f(path):
            command = ["git", "-C", path, "fetch", "--quiet", remote]

            exec_command(command)

    def remotes_f(self, folder):
        command = ["git", "-C", folder, "remote"]

        remotes = exec_command(command)

        return remotes.splitlines()

    def remotes(self):
        return self.remotes_f(self.folder())

    @memoized
    def subprojects(self):
        command = ["git", "-C", self.folder(), "submodule", "status",
                   "--recursive"]

        output = exec_command(command)

        if not output:
            return []

        submodules = dict()

        for line in output.splitlines():
            name = line.split()[1]

            if '/' not in name:
                submodules[name] = submodule(name)
            else:
                search = submodules
                parentsub = None

                while '/' in name:
                    parent = name.split("/")[0]

                    if parent in search:
                        parentsub = search[parent]
                        search = parentsub.subs
                        name = name[name.index("/")+1:]
                    else:
                        break

                if parentsub is None:
                    submodules[name] = submodule(name)
                else:
                    parentsub.subs[name] = submodule(name)

        subprojects = []

        for key in submodules:
            m = submodules[key]

            subprojects.append(to_subproject(m))

        return subprojects

    # Return the current branch
    @memoized
    def branch(self):
        command = ["git", "-C", self.folder(), "branch"]

        branches = exec_command(command)

        for b in branches.splitlines():
            if "*" in b:
                self.current_branch = b[2:]
                return self.current_branch

        return "No current branch"

    # Return true if the remote exists, false otherwise
    def remote_branch_exist_f(self, folder, branch):
        command = ["git", "-C", folder, "branch", "-a"]

        result = exec_command(command)

        remote_branch = "remotes/" + branch

        return remote_branch in result

    # Return true if the remote exists, false otherwise
    def remote_branch_exist(self, branch):
        return self.remote_branch_exist_f(self.folder(), branch)

    # Return the hash of the given object
    def hash_f(self, folder, o):
        command = ["git", "-C", folder, "rev-parse", "--verify", o]

        return exec_command(command).splitlines()[0]

    # Return the hash of the given object
    def hash(self, o):
        return self.hash_f(self.folder(), o)

    # Return the porcelain status of the project
    @memoized
    def status(self):
        command = ["git", "-C", self.folder(), "status",
                   "--porcelain", "--branch"]

        status = exec_command(command)

        return status

    def has_diverged(self):
        status = self.project.status()

        branch_line = status.splitlines()[0]

        return "ahead" in branch_line and "behind" in branch_line

    def is_behind(self):
        status = self.project.status()

        branch_line = status.splitlines()[0]

        return not self.has_diverged() and "behind" in branch_line

    def print_status(self):
        status = self.project.status()

        branch_line = status.splitlines()[0]

        clean = True

        if " M " in status or " D " in status:
            red_print("Uncommitted changes")
            clean = False

        if "ahead" in branch_line and "behind" in branch_line:
            if not clean:
                print(" - ", end="")
            red_print("Diverged with remote")
            clean = False

        elif " [ahead" in branch_line:
            if not clean:
                print(" - ", end="")
            red_print("Ahead of remote")
            clean = False

        elif " [behind" in branch_line:
            if not clean:
                print(" - ", end="")
            red_print("Behind remote")
            clean = False

        if clean:
            green_print("Clean")

    # Return the porcelain status of a submodule project
    @memoized
    def submodule_status(self, sub):
        path = self.sub_folder(sub)

        command = ["git", "-C", path, "status", "--porcelain", "--branch"]

        status = exec_command(command)

        return status

    def find_detached_source_branch(self, path):
        command = ["git", "-C", path, "for-each-ref",
                   "--format='%(objectname) %(refname:short)'", "refs"]

        ref_branches = exec_command(command).splitlines()

        command = ["git", "-C", path, "show-ref", "-s", "--", "HEAD"]
        current_commit = exec_command(command).splitlines()[0]

        branch_name = ""

        for ref_branch in ref_branches:
            if current_commit in ref_branch:
                branch_name = ref_branch[1:-1].split()[1]

        return branch_name

    def print_submodule_status(self, sub):
        status = self.project.submodule_status(sub)

        branch_line = status.splitlines()[0]

        clean = True

        if " M " in status or " D " in status:
            red_print("Uncommitted changes")
            clean = False

        if "(no branch)" in branch_line:
            if not clean:
                print(" - ", end="")

            clean = False

            path = self.sub_folder(sub)

            branch_name = self.find_detached_source_branch(path)

            if not branch_name:
                red_print("Detached (unable to find source")
            else:
                red_print("Detached (from {})".format(branch_name))

                remote_branch = "remotes/" + branch_name

                if self.remote_branch_exist_f(path, remote_branch):
                    print(" - ", end="")
                    red_print("No remote branch {}".format(remote_branch))
                else:
                    local_hash = self.hash_f(path, "HEAD")
                    remote_hash = self.hash_f(path, remote_branch)

                    if local_hash == remote_hash:
                        print(" - ", end="")
                        green_print("In sync")
                    else:
                        print(" - ", end="")
                        red_print("Not in sync with {}".format(remote_branch))

        if "ahead" in branch_line and "behind" in branch_line:
            if not clean:
                print(" - ", end="")
            red_print("Diverged with remote")
            clean = False

        elif " [ahead" in branch_line:
            if not clean:
                print(" - ", end="")
            red_print("Ahead of remote")
            clean = False

        elif " [behind" in branch_line:
            if not clean:
                print(" - ", end="")
            red_print("Behind remote")
            clean = False

        if clean:
            green_print("Clean")

    @memoized
    def branches(self):
        command = ["git", "-C", self.folder(), "branch"]

        res = exec_command(command)

        branches = []

        for b in res.splitlines():
            branches.append(b[2:])

        return branches
