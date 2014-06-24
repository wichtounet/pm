import os

from setuptools import setup, find_packages
from setuptools.command.install import install
from setuptools.command.develop import develop

def read(filename):
    try:
        return open(os.path.join(os.path.dirname(__file__), filename)).read()
    except:
        raise

def friendly(command_subclass):
    orig_run = command_subclass.run

    def modified_run(self):
        orig_run(self)
        print("")
        print("=======================================================")
        print("To make full use of this program, you should install the"
              "following function in your shell (bash or zsh):")
        print("function pcd { dir=`pcdi $1` ; if (( $? == 0 )) ; "
              "then cd $dir; fi ; }")
        print("=======================================================")
        print("")

    command_subclass.run = modified_run
    return command_subclass

@friendly
class DevelopCommand(develop):
    pass

@friendly
class InstallCommand(install):
    pass

setup(
        name='pm',
        version='0.1.1',
        description='Command-line utility to mange development projects',
        author='Baptiste Wicht',
        author_email='baptiste.wicht@gmail.com',
        url='https://github.com/wichtounet/pm',
        download_url='https://github.com/wichtounet/pm/tarball/0.0.1',
        license='MIT',
        packages=find_packages(),
        package_dir = {'pytex': 'pytex'},
        entry_points = read('entry-points.ini'),
        cmdclass={
            'install': InstallCommand,
            'develop': DevelopCommand,
        },
)
