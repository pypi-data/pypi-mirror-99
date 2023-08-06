from setuptools import setup

from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


setup(name='releasemon',
      version='1.0.1',
      license='GPLv3',
      description='Supervisor plugin to watch a build version file and restart '
                  'programs on update. Specifically built to support Laravel Queues.',
      long_description=long_description,
      long_description_content_type='text/markdown',
      author='James Cundle',
      author_email='james@blueworldmedia.com',
      url='https://github.com/blueworldmedia/releasemon',
      install_requires=['supervisor', 'watchdog'],
      scripts=['releasemon']
      )
