#!/usr/bin/env python

import os

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'django',
    'djangorestframework',
    'django-session-security',
    'uwsgi',
]

setup_requirements = []

test_requirements = []

setup(
    author="Ralph Brecheisen",
    author_email='r.brecheisen@maastrichtuniversity.nl',
    python_requires='>=3.5',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="Prediction for Surgical Treatment and Oncology (PRESTO)",
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='prestoweb',
    name='prestoweb',
    packages=find_packages(include=['prestoweb', 'prestoweb.*']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/rbrecheisen/prestoweb',
    version=os.environ['VERSION'],
    zip_safe=False,
    scripts=['prestoweb-run.sh'],
)
