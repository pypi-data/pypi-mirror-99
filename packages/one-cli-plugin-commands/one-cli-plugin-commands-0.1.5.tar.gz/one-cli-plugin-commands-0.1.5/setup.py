#!/usr/bin/env python

from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

install_requires = []

__version__ = '0.1.5'

setup(
    name='one-cli-plugin-commands',
    version=__version__,
    py_modules=['plugin_commands'],
    include_package_data=True,
    description='This is a one-cli plugin that allow to create new commands during runtime to the CLI.',
    license="Apache License 2.0",
    url='https://github.com/DNXLabs/plugin-commands',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='DNX Solutions',
    author_email='contact@dnx.solutions',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Natural Language :: English',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8'
    ],
    packages=find_packages(),
    install_requires=install_requires,
    python_requires='>=3.6'
)
