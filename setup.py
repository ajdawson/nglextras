"""Build and install nglextras."""
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


from distutils.core import setup


setup(
    name='nglextras',
    version='0.2',
    description='Extra tools for PyNGL',
    author='Andrew Dawson',
    author_email='dawson@atm.ox.ac.uk',
    packages=['nglextras'],
    package_dir={'nglextras': 'lib'},
)

