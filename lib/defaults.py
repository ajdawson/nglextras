"""system for managing default parameters for Ngl plots"""
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


import os
import re


# Define default values. These will be used when the user does not have a
# ~/.nglrc file or the ~/.nglrc file does not have a value for a given entry.
_default_values = {
        'font': {
                'title': 22,
                'ngl': 4,
                'labelbar': 4,
                'axislabel': 4,
                'axistitle': 4,
        },
        'fontheight': {
                'title': 0.012,
                'ngl': 0.01,
                'labelbar': 0.03,
                'axislabel': 0.008,
                'axistitle': 0.008,
        },
        'ticksize': {
                'major': 0.0056,
                'minor': 0.0028,
                'majoroutward': 0.0056,
                'minoroutward': 0.0028,
        },
}


def _strip_rc_comments(line):
    """Remove comments from a line."""
    line = re.sub(re.compile('#.*?\n'), '', line)
    return line


def _handle_value(value, category, option):
    """Process values from the user's rc file.

    Currently just converts to float. This should be updated to
    undertand different types for certain categories/options.

    """
    return float(value)


def _parse_nglrc():
    """Read defaults from an Ngl rc file."""
    rcfilename = os.path.expanduser('~/.nglrc')
    if not os.path.exists(rcfilename):
        # Just return an empty dictionary when no ~/.nglrc file is found.
        return dict()
    with open(rcfilename, 'r') as rcfile:
        # Read every line in the file.
        rclines = rcfile.readlines()
    # Remove whitespace and blank lines.
    rclines = [line.strip() for line in rclines]
    rclines = [line for line in rclines if line]
    # Strip comments from lines.
    rclines = map(_strip_rc_comments, rclines)
    # Now each line should be an rc assignment.
    # - split on = sign (stripping whitespace
    # - split lhs on dots to get dict path.
    rccommands = [(l.strip(), r.strip()) for l, r in \
            [line.split('=') for line in rclines]]
    rcdict = dict()
    for lhs, rhs in rccommands:
        try:
            category, option = lhs.split('.')
            assert category and option
        except (ValueError, AssertionError):
            raise ValueError("invalid key '%s' in rcfile" % lhs)
        if category not in rcdict.keys():
            rcdict[category] = dict()
        rcdict[category][option] = _handle_value(rhs, category, option)
    return rcdict


def _update_defaults_dict(defaults, updates):
    """Update a defaults dictionary.

    This function changes the values in the dictionary 'defaults'.

    """
    for category in updates.keys():
        if category not in defaults.keys():
            defaults[category] = dict()
        defaults[category].update(updates[category])


def _setup_defaults():
    defaults = dict()
    # Update this dictionary with the default values.
    _update_defaults_dict(defaults, _default_values)
    # Get default values specified in the user's rc file.
    rcdefaults = _parse_nglrc()
    # Update the defaults file with the user's settings.
    _update_defaults_dict(defaults, rcdefaults)
    return defaults


# Create a dictionary of defaults.
ngldefaults = _setup_defaults()


if __name__ == '__main__':
    pass

