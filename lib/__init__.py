"""extra tools for working with PyNGL"""
# (c) Copyright 2012 Andrew Dawson. All Rights Reserved. 
#
# This file is part of nglextras.
# 
# nglextras is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# nglextras is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with nglextras.  If not, see <http://www.gnu.org/licenses/>.


import modifiers
import modification

from plotting import PanelPlot
from plotting import xy, y
from plotting import map
from plotting import contour, contour_map
from plotting import streamline, streamline_map
from plotting import streamline_scalar, streamline_scalar_map
from plotting import vector, vector_map
from plotting import vector_scalar, vector_scalar_map
from plotting import histogram

from resources import Resources, MapResources

from defaults import ngldefaults


# Create a dictionary of default values for Ngl plotting.


__all__ = [
        # Module objects for the plot modification system. These are for more
        # advanced use so are left as top-level modules.
        'modification',
        'modifiers',

        # Customized plotting classes and routines. These are imported
        # directly and are accessible from the top-level package.
        'PanelPlot',
        'xy',
        'y',
        'map',
        'contour',
        'contour_map',
        'streamline',
        'streamline_map',
        'streamline_scalar',
        'streamline_scalar_map',
        'vector',
        'vector_map',
        'vector_scalar',
        'vector_scalar_map',

        # Overridden resource objects, available directly at the top-level.
        'Resources',
        'MapResources',

        # Defaults system, available directly at the top level.
        'ngldefaults',
]

