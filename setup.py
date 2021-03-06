import os
from setuptools import setup, find_packages

# package description and keywords
description = ('Python tools for obtaining and working with spherical harmonic'
    'coefficients from the NASA/DLR GRACE and NASA/GFZ GRACE Follow-on missions')
keywords = 'GRACE, GRACE-FO, Gravity, satellite geodesy, spherical harmonics'
# get long_description from README.rst
with open("README.rst", "r") as fh:
    long_description = fh.read()
long_description_content_type = "text/x-rst"

# install requirements and dependencies
on_rtd = os.environ.get('READTHEDOCS') == 'True'
if on_rtd:
    install_requires = []
    dependency_links = []
else:
    # get install requirements
    with open('requirements.txt') as fh:
        install_requires = [line.split().pop(0) for line in fh.read().splitlines()]
    # dependency links
    dependency_links = ['https://github.com/tsutterley/read-GRACE-geocenter/tarball/main',
        'https://github.com/tsutterley/geoid-toolkit/tarball/tarball/main']

# get version
with open('version.txt') as fh:
    version = fh.read()

# list of all scripts to be included with package
scripts=[os.path.join('scripts',f) for f in os.listdir('scripts') if f.endswith('.py')]
scripts.append(os.path.join('gravity_toolkit','grace_date.py'))
scripts.append(os.path.join('gravity_toolkit','grace_months_index.py'))

setup(
    name='gravity-toolkit',
    version=version,
    description=description,
    long_description=long_description,
    long_description_content_type=long_description_content_type,
    url='https://github.com/tsutterley/read-GRACE-harmonics',
    author='Tyler Sutterley',
    author_email='tsutterl@uw.edu',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Physics',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    keywords=keywords,
    packages=find_packages(),
    install_requires=install_requires,
    dependency_links=dependency_links,
    scripts=scripts,
    include_package_data=True,
)
