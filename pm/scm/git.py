from __future__ import print_function

import subprocess

from pm.console import blue_print, green_print, red_print, cyan_print

class Git:
    def __init__(self, project):
        self.project = project

    def folder(self):
        return self.project.folder

    def fetch(self, branch):
        command = ["git", "-C", self.folder(), "fetch", "--quiet", branch]

        subprocess.check_output(command)

    def remotes(self):
        command = ["git", "-C", self.folder(), "remote"]

        remotes = subprocess.check_output(command)

        return remotes.splitlines()

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

    # Return the status of the project
    def status(self):
        command = ["git", "-C", self.folder(), "status"]

        status = subprocess.check_output(command)

        return status

    # Return the porcelain status of the project
    def porcelain_status(self):
        command = ["git", "-C", self.folder(), "status", "--porcelain", "--branch"]

        status = subprocess.check_output(command)

        return status

    def print_status(self):
        status = self.porcelain_status()

        branch_line = status.splitlines()[0]

        clean = True

        if " M " in status:
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

    def branches(self):
        command = ["git", "-C", self.folder(), "branch"]

        res = subprocess.check_output(command)

        branches = []

        for b in res.splitlines():
            branches.append(b[2:])

        return branches
