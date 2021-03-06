#=======================================================================
# Copyright (c) 2014 Baptiste Wicht
# Distributed under the terms of the MIT License.
# (See accompanying file LICENSE or copy at
#  http://opensource.org/licenses/MIT)
#=======================================================================

import os

from pm.scm.git import Git


class subproject:
    def __init__(self, name):
        self.name = name
        self.subs = []


class project:
    current_branch = ""
    scm = None
    scm_i = None

    def __init__(self, folder, scm=None):
        self.folder = folder
        self.scm = scm
        self.name = os.path.basename(folder)

    def get_scm(self):
        if self.scm_i is not None:
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

    # Return the current branch
    def branch(self):
        return self.get_scm().branch()

    # Return the hash of the current commit of the given branch
    def hash(self, branch):
        return self.get_scm().hash(branch)

    # Return the status of the project
    def status(self):
        return self.get_scm().status()

    # Return the status of a submodule
    def submodule_status(self, sub):
        return self.get_scm().submodule_status(sub)

    def is_behind(self):
        return self.get_scm().is_behind()

    def print_status(self):
        self.get_scm().print_status()

    def print_submodule_status(self, sub):
        self.get_scm().print_submodule_status(sub)

    def branches(self):
        return self.get_scm().branches()

    def subprojects(self):
        return self.get_scm().subprojects()

    def update(self):
        self.get_scm().update()

    def fetch(self, remote):
        self.get_scm().fetch(remote)

    def fetch_all(self):
        for remote in self.remotes():
            self.fetch(remote)

    def fetch_submodule(self, p):
        self.get_scm().fetch_sub(p)

        for sp in p.subs:
            self.fetch_submodule(sp)

    def fetch_submodules(self):
        for p in self.subprojects():
            self.fetch_submodule(p)

    def cache(self, submodule):
        if submodule:
            for p in self.subprojects():
                self.submodule_status(p)

        self.branches()
        self.status()


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
