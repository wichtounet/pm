import os
import subprocess


class project:
    current_branch = ""
    scm = None

    def __init__(self, folder, scm=None):
        self.folder = folder
        self.scm = scm
        self.name = os.path.basename(folder)

    def remotes(self):
        command = ["git", "-C", self.folder, "remote"]

        remotes = subprocess.check_output(command)

        return remotes.splitlines()

    def branch(self):
        if not self.current_branch:
            command = ["git", "-C", self.folder, "branch"]

            branches = subprocess.check_output(command)

            for b in branches.splitlines():
                if "*" in b:
                    self.current_branch = b[2:]
                    return self.current_branch

            self.current_branch = "No current branch"
            return self.current_branch
        else:
            return self.current_branch

    def branches(self):
        command = ["git", "-C", self.folder, "branch"]

        res = subprocess.check_output(command)

        branches = []

        for b in res.splitlines():
            branches.append(b[2:])

        return branches

    def fetch(self, branch):
        command = ["git", "-C", self.folder, "fetch", "--quiet", branch]

        subprocess.check_output(command)

    def fetch_all(self):
        for remote in self.remotes():
            self.fetch(remote)


def dev_directory(dir=None):
    home = os.path.expanduser('~')

    if dir:
        if dir[0] == '/':
            devdir = dir
        else:
            devdir = os.path.join(home, dir)
    else:
        devdir = os.path.join(home, 'dev')

    return devdir


def is_git_project(dirname):
    gitdir = os.path.join(dirname, '.git')

    if os.path.exists(gitdir):
        gitconfig = os.path.join(gitdir, 'config')

        return os.path.exists(gitconfig)
    else:
        return False


def list_projects(all=False, dir=None):
    devdir = dev_directory(dir)

    projects = []

    for f in os.listdir(devdir):
        path = os.path.join(devdir, f)
        if os.path.isdir(path) and (all or is_git_project(path)):
            projects.append(project(path))

    return projects
