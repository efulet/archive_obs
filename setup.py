#!/usr/bin/env python

from setuptools import setup, find_packages


with open('README.md') as readme_file:
    readme = readme_file.read()

requirements = [
    'astropy',
    'matplotlib',
    'progressbar2',
    'pyquery',
    'requests',
]

setup_requirements = [
]

test_requirements = [
    'pytest',
    'flake8',
    'flake8-colors',
    'flake8-commas',
    'flake8-comprehensions',
    'flake8-debugger',
    'flake8-quotes',
]

setup(
    name='archive_obs',
    version='0.1.0',
    description='',
    long_description=readme,
    author='Exequiel Fuentes Lettura',
    author_email='efulet@gmail.com',
    url='',
    packages=find_packages(),
    license='',
    install_requires=requirements,
    zip_safe=False,
    setup_requires=setup_requirements,
    entry_points={
        'console_scripts': [
            'archive_obs=archive_obs.__main__:main',
        ],
    },
    test_suite='test',
    tests_require=test_requirements,
    classifiers=[
        # https://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3.5',
        'Topic :: Scientific/Engineering :: Astronomy',
    ],
)
