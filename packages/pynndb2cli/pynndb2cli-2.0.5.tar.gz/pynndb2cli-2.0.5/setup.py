import os
from setuptools import setup, find_packages
from pipenv.project import Project
from pipenv.utils import convert_deps_to_pip
from pkg_resources import get_distribution
from setuptools_scm import get_version
pfile = Project(chdir=False).parsed_pipfile
requirements = convert_deps_to_pip(pfile['packages'], r=False)
requirements.append('Pipfile')

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

version = get_version().split('b')[0]

setup(
    version=version,
    name='pynndb2cli',
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'pynndb2=pynndb2cli.__main__:main'
        ]
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Database :: Database Engines/Servers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],
    keywords=['pynndb2', 'cli', 'shell', 'python', 'database'],
    install_requires=requirements,
    data_files=[('', ['Pipfile', 'requirements.txt'])],
    long_description=long_description,
    description='PyNNDB2 CLI',
    url='https://gitlab.com/oddjobz/pynndb2-cli',
    license='MIT',
    author='Gareth Bult',
    author_email='gareth@bult.co.uk',
)
