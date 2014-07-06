import os
import subprocess


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

    def branches(self):
        command = ["git", "-C", self.folder(), "branch"]

        res = subprocess.check_output(command)

        branches = []

        for b in res.splitlines():
            branches.append(b[2:])

        return branches
