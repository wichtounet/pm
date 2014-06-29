import os
import subprocess

class project:
    def __init__(self, folder):
        self.folder = folder
        self.name = os.path.basename(folder)

    def remotes(self):
        command = ["git", "-C", self.folder, "remote"]

        remotes = subprocess.check_output(command)

        return remotes.splitlines()

    def fetch(self, branch):
        command = ["git", "-C", self.folder, "fetch", "--quiet", branch]
        
        subprocess.check_output(command)

    def fetch_all(self):
        for remote in self.remotes():
            self.fetch(remote)


def dev_directory():
    home = os.path.expanduser('~')
    devdir = os.path.join(home, 'dev')

    return devdir


def is_git_project(dirname):
    gitdir = os.path.join(dirname, '.git')

    if os.path.exists(gitdir):
        gitconfig = os.path.join(gitdir, 'config')

        return os.path.exists(gitconfig)
    else:
        return False


def list_projects(all=False):
    devdir = dev_directory()

    projects = []

    for f in os.listdir(devdir):
        path = os.path.join(devdir, f)
        if os.path.isdir(path) and (all or is_git_project(path)):
            projects.append(project(path))

    return projects
