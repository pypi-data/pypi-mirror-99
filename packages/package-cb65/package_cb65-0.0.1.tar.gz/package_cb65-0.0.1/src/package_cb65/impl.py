"""
package_cb65
============

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

import argparse
import logging
import os
import pprint
import re
from pathlib import Path
from uuid import uuid4 as uuid

from program_9ef5 import Instruction, Program

logger = logging.getLogger(__name__)


# Implementation


def mkdir(path):
    path.mkdir(mode=0o700, parents=True, exist_ok=False)
    return path


def mkfile(path, content):
    with path.open(mode="w", encoding="utf-8") as a_file:
        a_file.write(content)
        path.chmod(0o600)

    return path


@Instruction
def get_deps_path(deps_path):
    return Path(os.environ["deps_path"])


@Instruction
def get_name(name):
    parser = argparse.ArgumentParser(description="Install user defined packages.")
    arg_name = "component_name"
    parser.add_argument(
        arg_name,
        help="name of the component. Example: a_component",
    )
    return vars(parser.parse_args())[arg_name]


@Instruction
def get_id(id):
    return str(uuid()).split("-")[1]


@Instruction
def get_identifier(name, id, identifier):
    return f"{name}_{id}"


@Instruction
def build_container(deps_path, identifier, container):
    return mkdir(deps_path / identifier)


@Instruction
def build_src(container, src):
    return mkdir(container / "src")


@Instruction
def build_pkg(src, identifier, pkg):
    return mkdir(src / identifier)


@Instruction
def build_test(container, test):
    return mkdir(container / "test")


@Instruction
def build_impl(identifier, pkg, impl):
    path = pkg / "impl.py"
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

    return mkfile(path, content)


@Instruction
def build_init(pkg, init):
    path = pkg / "__init__.py"
    content = f'''"""
# -*- coding: utf-8 -*-

__init__
========
"""

# Defines what is exposed when importing this package.
from .impl import something
'''

    return mkfile(path, content)


@Instruction
def build_main(identifier, pkg, main):
    path = pkg / "__main__.py"
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

    return mkfile(path, content)


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
    return mkfile(path, content)


@Instruction
def build_requirements(container, requirements):
    path = container / "requirements.txt"
    content = f"""# https://caremad.io/posts/2013/07/setup-vs-requirement/
# -e https://github.com/foo/bar.git#egg=bar
-e .
"""
    return mkfile(path, content)


@Instruction
def build_impl_test(identifier, test, impl_test):
    path = test / "impl_test.py"
    content = f'''# -*- coding: utf-8 -*-

# Imports

from {identifier} import something


# Implementation

def test_impl():
    """docstring"""
    assert something() == 1

'''
    return mkfile(path, content)


@Instruction
def build_readme(container, readme):
    path = container / "README"
    content = "README"
    return mkfile(path, content)


@Instruction
def build_license(container, license):
    path = container / "LICENSE"
    content = "https://www.mozilla.org/en-US/MPL/2.0/"
    return mkfile(path, content)


@Instruction
def build_setup_cfg(container, identifier, setupcfg):
    path = container / "setup.cfg"
    content = f"""[metadata]
name = {identifier}
version = 0.0.1
author = Pierre-Henry Fröhring
author_email = contact@phfrohring.com
description = A small example package
long_description = README
long_description_content_type = text/x-rst
url = https://github.com/phfrohring/python
project_urls =
    Bug Tracker = https://github.com/phfrohring/python/issues
classifiers =
    Programming Language :: Python :: 3
    License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)
    Operating System :: OS Independent

[options]
package_dir=
    =src
packages = find:
python_requires = >=3.6
install_requires=

[options.packages.find]
where=src

[options.entry_points]
console_scripts =
    {identifier} = {identifier}.__main__:main
"""

    return mkfile(path, content)


@Instruction
def build_setup_py(container, identifier, setuppy):
    path = container / "setup.py"
    content = f"""import setuptools
setuptools.setup()
"""

    return mkfile(path, content)


program = Program(Instruction.all())

# Interface


def build():
    """docstring"""

    # Context of execution
    debug = os.environ.get("debug") == "true"
    if debug:
        logging.basicConfig(
            level=logging.DEBUG, force=True, format="%(levelname)s: %(message)s"
        )

    program.execute()
