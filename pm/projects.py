import os
import subprocess

from pm.scm.git import Git

class project:
    current_branch = ""
    scm = None
    scm_i = None

    def __init__(self, folder, scm=None):
        self.folder = folder
        self.scm = scm
        self.name = os.path.basename(folder)

    def get_scm(self):
        if not self.scm_i == None:
            return self.scm_i

        if self.scm == "Git":
            self.scm_i = Git(self)
            return self.scm_i

        return None

    def remotes(self):
        return self.get_scm().remotes()

    # Return true if the remote exists, false otherwise
    def remote_branch_exist(self, branch):
        return self.get_scm().remote_branch_exist(branch)

    def branch(self):
        if not self.current_branch:
            self.current_branch = self.get_scm().branch()

        return self.current_branch

    # Return the hash of the current commit of the given branch
    def hash(self, branch):
        return self.get_scm().hash(branch)

    # Return the status of the project
    def status(self):
        return self.get_scm().status()

    def branches(self):
        return self.get_scm().branches()

    def fetch(self, branch):
        self.get_scm().fetch(branch)

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
        git = is_git_project(path)

        if os.path.isdir(path) and (all or git):
            projects.append(project(path, "Git" if git else None))

    return projects
