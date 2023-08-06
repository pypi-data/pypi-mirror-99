import pathlib
from setuptools import setup, find_packages

INSTALL_REQUIRES = [
]

setup(name='mould',
      version='0.0.3',
      description='A minimalistic python templating library',
      long_description=open('README.md').read(),
      long_description_content_type='text/markdown',
      author='Ramakrishnan H',
      license='MIT',
      AUTHOR_EMAIL='ernest.thornhill.corp@gmail.com',
      URL='https://github.com/ramk95/mould',
      install_requires=INSTALL_REQUIRES,
      packages=find_packages()
      )
