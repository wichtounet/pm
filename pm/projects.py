import os
import sys

def is_git_project(dirname):
    gitdir = os.path.join(dirname, '.git')

    if os.path.exists(gitdir):
        gitconfig = os.path.join(gitdir, 'config')

        return os.path.exists(gitconfig)
    else:
        return False

def list_projects():
    home = os.path.expanduser('~')
    devdir = os.path.join(home, 'dev')

    projects = []

    for f in os.listdir(devdir):
        path = os.path.join(devdir, f)
        if os.path.isdir(path) and is_git_project(path):
            projects.append(os.path.basename(path))

    return projects
