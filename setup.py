import os

from setuptools import setup, find_packages


def read(filename):
    try:
        return open(os.path.join(os.path.dirname(__file__), filename)).read()
    except:
        raise


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
        entry_points = read('entry-points.ini')
)