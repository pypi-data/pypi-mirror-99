#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

# with open('HISTORY.rst') as history_file:
#     history = history_file.read()

requirements = ['Click>=7.0', 'colorama>=0.4.3']

setup_requirements = ['pytest-runner', ]

test_requirements = ['pytest>=3', ]

setup(
    author="Matias Canepa Gonzalez",
    author_email='macanepa@miuandes.cl',
    python_requires='>=3.5',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="Python Boilerplate contains all the boilerplate you need to create a Python package.",
    entry_points={
        'console_scripts': [
            'mcutils=mcutils.cli:main',
        ],
    },
    install_requires=requirements,
    license="GNU General Public License v3",
    long_description=readme, #+ '\n\n' + history,
    include_package_data=True,
    keywords='mcutils',
    name='mcutils',
    packages=find_packages(include=['mcutils', 'mcutils.*']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/macanepa/mcutils',
    version='1.1.2',
    zip_safe=False,
)
