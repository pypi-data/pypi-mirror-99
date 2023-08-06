"""
Copyright 2016-2017 Louis Moresi, Ben Mather, Romain Beucher

This file is part of Quagmire.

Quagmire is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as published by
the Free Software Foundation, either version 3 of the License, or any later version.

Quagmire is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License
along with Quagmire.  If not, see <http://www.gnu.org/licenses/>.
"""

import pkg_resources as _pkg_resources
from distutils import dir_util as _dir_util
import os


def install_documentation(path="./Cloudstor-Notebooks"):
    """Install the example notebooks for cloudstor in the given location

    WARNING: If the path exists, the Notebook files will be written into the path
    and will overwrite any older, existing files with which they collide. The default
    path ("./Cloudstor-Notebooks") is chosen to make collision less likely / problematic

    The documentation for cloudstor is in the form of jupyter notebooks.

    You may also browse the github repository at https://github.com/underworldcode/cloudstor

    """

    ## Question

    Notebooks_Path = _pkg_resources.resource_filename('cloudstor', os.path.join("Examples", 'Notebooks'))

    ct = _dir_util.copy_tree(Notebooks_Path, path, preserve_mode=1, preserve_times=1, preserve_symlinks=1, update=1, verbose=1, dry_run=0)

    return
