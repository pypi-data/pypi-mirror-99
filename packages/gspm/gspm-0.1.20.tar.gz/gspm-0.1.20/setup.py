
import gspm
import re 
import io
from setuptools import setup, find_packages

long_desc = "missing"

with io.open('README.md') as t_file:
    long_desc = t_file.read()

i_requires = ['pyyaml', 'gitpython', 'dotmap', 'wget', 'packaging', 'cookiecutter']
t_requires = []

setup(

    name=gspm.__id__,
    version=gspm.__version__,
    description=gspm.__desc__,
    long_description=long_desc,
    long_description_content_type='text/markdown',
    url='https://gitlab.com/godot-stuff/gs-project-manager.git',
    author='Paul Hocker',
    author_email='paul@spocker.net',
    license='MIT',
    packages=find_packages('.'),
    #package_data={'gspm': ['./gspm/templates/*.*', './gspm/assets/*.*']},
    include_package_data=True,
    install_requires=i_requires,
    zip_safe=True,
    tests_require=t_requires,
    entry_points={
        'console_scripts': ['gspm=gspm.gspm:run'],
    },
    classifiers=[
        # Picked from
        #   http://pypi.python.org/pypi?:action=list_classifiers
        'Development Status :: 2 - Pre-Alpha',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: MacOS',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.4',
        'Topic :: Utilities',
        'Topic :: Games/Entertainment',
        'Environment :: Console',
    ]
)
