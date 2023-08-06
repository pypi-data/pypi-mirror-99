# -*- coding: utf-8 -*-

"""
bootstrap_62cb
==============

Problem
-------

1. A brief informal statement of the problem

  - give examples

2. The precise correctness conditions required of a solution


Solution
--------

3. Describe the solution

  - Whenever needed, explain the "why" of the design

"""


# Imports

import os
import logging
import argparse
from shutil import rmtree
import re
from uuid import uuid4 as uuid
from program_9ef5 import Instruction, Program
from functools import partial
from pathlib import Path
logger = logging.getLogger(__name__)


# Implementation

def get_env_value(name, is_path=False, is_bool=False, is_optional=False):
    try:
        val = os.environ[name]
    except KeyError as e:
        if is_optional:
            return None
        else:
            raise e

    if is_path:
        return Path(val).resolve()
    if is_bool:
        return val == "true"
    else:
        return val

get_env_path = partial(get_env_value, is_path=True)
get_env_bool = partial(get_env_value, is_bool=True, is_optional=True)

def mkdir(path):
    path.mkdir(mode=0o700, parents=True, exist_ok=False)
    return path



def mkfile(path, content, is_exec=False):
    with path.open(mode="w", encoding="utf-8") as a_file:
        a_file.write(content)
        if is_exec:
            path.chmod(0o700)
        else:
            path.chmod(0o600)

    return path

mkfile_rw = partial(mkfile, is_exec=False)
mkfile_rwx = partial(mkfile, is_exec=True)


@Instruction
def get_debug_bool(debug):
    debug = get_env_bool('debug')
    if debug:
        logging.basicConfig(
            level=logging.DEBUG, force=True, format="%(levelname)s: %(message)s"
        )

    return debug


@Instruction
def get_root_path(debug, root_path):
    return get_env_path('root_path')

@Instruction
def build_container(root_path, identifier, container):
    return mkdir(root_path / identifier)

@Instruction
def build_src(container, src_path):
    return mkdir(container / 'src')



@Instruction
def build_ops(container, ops_path):
    return mkdir(container / 'ops')

@Instruction
def build_doc(container, doc_path):
    return mkdir(container / 'doc')

@Instruction
def build_build(container, build_path):
    return mkdir(container / 'build')

@Instruction
def build_data(pkg_path, data_path):
    return mkdir(pkg_path / 'data')

@Instruction
def build_dist(container, dist_path):
    return mkdir(container / 'dist')

@Instruction
def build_bin(container, bin_path):
    return mkdir(container / 'bin')

@Instruction
def build_test(container, test_path):
    return mkdir(container / 'test')

@Instruction
def build_dev_req(container, dev_req_path):
    dev_req_path = container / 'requirements.dev.txt'
    content = '''wheel
build
twine
pytest
pyinstaller
sphinx
black
isort
pylint
pydeps
setuptools
radon
toolz
'''
    return mkfile_rw(dev_req_path, content)


@Instruction
def build_environment(container, environment):
    dev_req_path = container / 'environment'
    content = '''export root_path=.
'''
    return mkfile_rw(dev_req_path, content)


@Instruction
def get_proj_name(debug, proj_name):
    parser = argparse.ArgumentParser(description="Project name.")
    arg_name = "project_name"
    parser.add_argument(
        arg_name,
        help="name of the project. Example: todo_list",
    )
    return vars(parser.parse_args())[arg_name]

@Instruction
def get_id(debug, id):
    return str(uuid()).split("-")[1]


@Instruction
def get_identifier(proj_name, id, identifier):
    return f"{proj_name}_{id}"


@Instruction
def build_pkg(src_path, identifier, pkg_path):
    return mkdir(src_path / identifier)


@Instruction
def build_init(pkg_path, init):
    path = pkg_path / "__init__.py"
    content = f'''# -*- coding: utf-8 -*-

"""
__init__
========
"""

__version__ = '0.0.1'

# Defines what is exposed when importing this package.
from .impl import something
'''

    return mkfile(path, content)


@Instruction
def build_impl(identifier, pkg_path, impl):
    path = pkg_path / "impl.py"
    content = f'''
# -*- coding: utf-8 -*-

"""
{identifier}
{re.sub('.', '=', identifier)}

Problem
-------

1. A brief informal statement of the problem

  - give examples

2. The precise correctness conditions required of a solution


Solution
--------

3. Describe the solution

  - Whenever needed, explain the "why" of the design

"""


# Imports

import logging
logger = logging.getLogger(__name__)


# Implementation

def somethingelse():
    """docstring"""
    return 1


# Interface
# Exported through the __init__.py file

def something():
    """docstring"""
    return somethingelse()
'''

    return mkfile_rw(path, content)


@Instruction
def build_main(identifier, pkg_path, main):
    path = pkg_path / "__main__.py"
    content = f"""
# -*- coding: utf-8 -*-


# Import

from {identifier} import something


def main():
    print(something())

# Execution

if __name__ == "__main__":
    main()
"""

    return mkfile_rw(path, content)


@Instruction
def build_pyproject(container, pyproject):
    path = container / "pyproject.toml"
    content = f"""[build-system]
# gives a list of packages that are needed to build your package. Listing something
# here will only make it available during the build, not after it is installed.
requires = [
    "setuptools>=42",
    "wheel"
]
build-backend = "setuptools.build_meta"
"""
    return mkfile_rw(path, content)

@Instruction
def build_ops_release(ops_path, ops_release):
    path = ops_path / "release"
    content = '''#!/usr/bin/env bash
set -euo pipefail
IFS=$'\n\t'
this_path="$(readlink -f ${BASH_SOURCE[0]})"
parent_path="${this_path%/*}"
root_path="$parent_path/.."
cd $root_path
python setup.py sdist bdist_wheel
'''
    return mkfile_rwx(path, content)


@Instruction
def build_ops_release(ops_path, ops_doc):
    path = ops_path / "doc"
    content = '''#!/usr/bin/env bash
set -euo pipefail
IFS=$'\n\t'
this_path="$(readlink -f ${BASH_SOURCE[0]})"
parent_path="${this_path%/*}"
root_path="$parent_path/.."
cd $root_path/doc
make html
echo doc/build/html/index.html
'''
    return mkfile_rwx(path, content)


@Instruction
def build_ops_bin(identifier, ops_path, ops_bin):
    path = ops_path / "bin"
    content = f'''#!/usr/bin/env bash
set -euo pipefail
IFS=$'\n\t'
this_path="$(readlink -f ${{BASH_SOURCE[0]}})"
parent_path="${{this_path%/*}}"
root_path="$parent_path/.."
cd $root_path
pyinstaller \
  --distpath bin \
  --workpath build \
  --onefile \
  --name {identifier} \
  --upx-dir=/usr/bin/ \
  ./src/{identifier}/__main__.py
'''
    return mkfile_rwx(path, content)


@Instruction
def build_ops_publih(ops_path, ops_publish):
    path = ops_path / "publish"
    content = '''#!/usr/bin/env bash
set -euo pipefail
IFS=$'\n\t'
this_path="$(readlink -f ${BASH_SOURCE[0]})"
parent_path="${this_path%/*}"
root_path="$parent_path/.."
cd $root_path

# for testing
twine upload --repository-url https://test.pypi.org/legacy/ dist/*

# not for testing
# twine upload dist/*
'''
    return mkfile_rwx(path, content)

@Instruction
def build_ops_publih(ops_path, ops_test):
    path = ops_path / "test"
    content = '''#!/usr/bin/env bash
set -euo pipefail
IFS=$'\n\t'
this_path="$(readlink -f ${BASH_SOURCE[0]})"
parent_path="${this_path%/*}"
root_path="$parent_path/.."
cd $root_path
pytest
'''
    return mkfile_rwx(path, content)

@Instruction
def build_requirements(container, requirements):
    path = container / "requirements.txt"
    content = f"""# https://caremad.io/posts/2013/07/setup-vs-requirement/
# -e https://github.com/foo/bar.git#egg=bar
-e .
"""
    return mkfile_rw(path, content)

@Instruction
def build_impl_test(identifier, test_path, impl_test):
    path = test_path / "impl_test.py"
    content = f'''# -*- coding: utf-8 -*-

# Imports

from {identifier} import something


# Implementation

def test_impl():
    """docstring"""
    assert something() == 1

'''
    return mkfile_rw(path, content)


@Instruction
def build_readme(container, readme):
    path = container / "README.rst"
    content = "Very explicit readme\n"
    return mkfile_rw(path, content)


@Instruction
def build_gitignore(container, gitignore):
    path = container / ".gitignore"
    content = '''# general things to ignore
build/
dist/
*.egg-info/
*.egg
*.py[cod]
__pycache__/
*.so
*~

# due to using pytest
.cache
'''
    return mkfile_rw(path, content)

@Instruction
def build_license(container, license):
    path = container / "LICENSE.txt"
    content = "https://www.mozilla.org/en-US/MPL/2.0/\n"
    return mkfile_rw(path, content)


@Instruction
def build_setup_cfg(container, identifier, setupcfg):
    path = container / "setup.cfg"
    content = f"""# doc: https://github.com/pypa/sampleproject/blob/main/setup.py
[metadata]
license_files = LICENSE.txt
name = {identifier}
version = attr: {identifier}.__version__
author = Pierre-Henry Fröhring
author_email = contact@phfrohring.com
description = A small example package
licence = Mozilla Public License Version 2.0
long_description = file: README.rst, LICENSE.txt
long_description_content_type = text/x-rst
url = https://github.com/phfrohring/python
project_urls =
    Bug Tracker = https://github.com/phfrohring/python/issues
classifiers =
    Programming Language :: Python :: 3
    License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)
    Operating System :: OS Independent

[options]
include_package_data = True
packages = find:
package_dir=
    =src
python_requires = >=3.8
install_requires=

[options.packages.find]
where=src

[options.package_data]
{identifier} = data/*


[options.entry_points]
console_scripts =
    {identifier} = {identifier}.__main__:main
"""

    return mkfile_rw(path, content)


@Instruction
def build_setup_py(container, identifier, setuppy):
    path = container / "setup.py"
    content = f"""import setuptools
setuptools.setup()
"""

    return mkfile_rw(path, content)


@Instruction
def build_makefile(container, makefile):
    path = container / "makefile"
    content = """SHELL=/bin/bash
src_dir := src
test_dir := test
bin_dir := bin
dist_dir := dist
doc_path := doc/build/html/index.html


# Actions
.PHONY: bin doc publish release test

all: test doc release bin


bin_files := $(shell find $(bin_dir) -type f)
src_files := $(shell find $(src_dir) -name "*.py")
doc_files := $(doc_path)
dist_files := $(shell find $(dist_dir) -type f)


bin: $(bin_files)
$(bin_files): $(src_files)
\t@ops/bin
\t@echo $@


doc: $(doc_files)
$(doc_files): $(src_files)
\t@ops/doc
\t@echo $@


release: $(dist_files)
$(dist_files): $(src_files)
\t@ops/release


publish: release
\t@ops/publish


test:
\t@ops/test
"""

    return mkfile_rw(path, content)

program = Program(Instruction.all())

# Interface
# Exported through the __init__.py file

def build():
    """docstring"""
        # Context of execution

    logs = program.execute()
    container = logs['container']
    identifier = logs['identifier']
    msg = f"""The package {identifier} has been built at: container.
container: {container}

To install in development mode:
  pip install -e {container}
"""
    print(msg)
