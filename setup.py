from setuptools import setup, find_packages

setup(
    name='Jouranl',
    description='A cli note-taking tool',
    version='0.1',
    author='Dimitris Chrysomallis',
    packages=find_packages(),
    install_requires=['markdown'],
    entry_points={
        'console_scripts': [
            'jour=jouranl.cli:main'
        ]
    }
)