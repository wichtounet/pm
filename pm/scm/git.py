from __future__ import print_function

import subprocess
import os

from pm.console import green_print, red_print
from pm.scm.base import subproject


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


class Git:
    def __init__(self, project):
        self.project = project

    def folder(self):
        return self.project.folder

    def fetch(self, remote):
        command = ["git", "-C", self.folder(), "fetch", "--quiet", remote]

        subprocess.check_output(command)

    def sub_folder(self, sub):
        parts = []

        while sub.parent is not None:
            parts.append(sub.name)

            sub = sub.parent

        parts.append(sub.name)

        path = self.folder()

        for part in reversed(parts):
            path = os.path.join(path, part)

        return path;

    def fetch_sub(self, sub):
        path = self.sub_folder(sub)

        for remote in self.remotes_f(path):
            command = ["git", "-C", path, "fetch", "--quiet", remote]

            subprocess.check_output(command)

    def remotes_f(self, folder):
        command = ["git", "-C", folder, "remote"]

        remotes = subprocess.check_output(command)

        return remotes.splitlines()

    def remotes(self):
        return self.remotes_f(self.folder())

    def subprojects(self):
        command = ["git", "-C", self.folder(), "submodule", "status",
                   "--recursive"]

        output = subprocess.check_output(command)

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

    def branch(self):
        command = ["git", "-C", self.folder(), "branch"]

        branches = subprocess.check_output(command)

        for b in branches.splitlines():
            if "*" in b:
                self.current_branch = b[2:]
                return self.current_branch

        return "No current branch"

    # Return true if the remote exists, false otherwise
    def remote_branch_exist(self, branch):
        command = ["git", "-C", self.folder(), "branch", "-a"]

        result = subprocess.check_output(command)

        remote_branch = "remotes/" + branch

        return remote_branch in result

    # Return the hash of the current commit of the given branch
    def hash(self, branch):
        command = ["git", "-C", self.folder(), "rev-parse", "--verify", branch]

        return subprocess.check_output(command)

    # Return the porcelain status of the project
    def status(self):
        command = ["git", "-C", self.folder(), "status",
                   "--porcelain", "--branch"]

        status = subprocess.check_output(command)

        return status

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
    def submodule_status(self, sub):
        path = self.sub_folder(sub)

        command = ["git", "-C", path, "status", "--porcelain", "--branch"]

        status = subprocess.check_output(command)

        return status

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

            red_print("Not on a branch")
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

    def branches(self):
        command = ["git", "-C", self.folder(), "branch"]

        res = subprocess.check_output(command)

        branches = []

        for b in res.splitlines():
            branches.append(b[2:])

        return branches
