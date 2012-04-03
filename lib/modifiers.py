"""modifications to apply to Ngl plotting methods""" 
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


import Ngl

from defaults import ngldefaults as defaults
from modification import PlotModifier



class NglStrings(PlotModifier):
    """
    Plot modifier adding functionality equivalent to the 'gsn' string
    NCL resources to Ngl plotting functions.

    This modifier makes the following resources available to Ngl
    plotting functions:

        'nglLeftString'
        'nglLeftStringFontColor'
        'nglLeftStringFontHeightF'
        'nglLeftStringParallelPosF'
        'nglLeftStringOrthogonalPosF'
        'nglRightString'
        'nglRightStringFontColor'
        'nglRightStringFontHeightF'
        'nglRightStringParallelPosF'
        'nglRightStringOrthogonalPosF'
        'nglCenterString'
        'nglCenterStringFontColor'
        'nglCenterStringFontHeightF'
        'nglCenterStringParallelPosF'
        'nglCenterStringOrthogonalPosF'

    These nglXXX special resources have the same meaning as their gsnXXX
    equivalents.

    http://www.ncl.ucar.edu/Document/Graphics/Resources/gsn.shtml

    """

    # Must declare the names of the special resources that can be used by
    # this modifier. This allows ModificationManager to remove them before
    # passing resources to Ngl plotting functions.
    resource_names = (
            'nglLeftString',
            'nglLeftStringFontColor',
            'nglLeftStringFontHeightF',
            'nglLeftStringParallelPosF',
            'nglLeftStringOrthogonalPosF',
            'nglRightString',
            'nglRightStringFontColor',
            'nglRightStringFontHeightF',
            'nglRightStringParallelPosF',
            'nglRightStringOrthogonalPosF',
            'nglCenterString',
            'nglCenterStringFontColor',
            'nglCenterStringFontHeightF',
            'nglCenterStringParallelPosF',
            'nglCenterStringOrthogonalPosF',)

    def preplot(self, *args):
        """Gather information about which strings should be added."""
        # We search for resources objects since some Ngl plotting routines may
        # accept two sets of resources and both should be considered.
        resource_vars = list()
        for arg in args:
            if isinstance(arg, Ngl.Resources):
                resource_vars.append(arg)
        # Re-define the resource names in a manner that allows the position
        # of the string ('left', 'right' or 'center) to be defined
        # programatically.
        resource_name_templates = ('ngl%sString', 'ngl%sStringFont',
                'ngl%sStringFontHeightF', 'ngl%sStringFontColor',
                'ngl%sStringParallelPosF', 'ngl%sStringOrthogonalPosF')
        # Define the default values to be used in string specifications. These
        # are the font number, font height, color, parallel position and
        # orthogonal position respectively.
        string_defaults = (defaults['font']['ngl'],
                defaults['fontheight']['ngl'], 1, 0., 0.)
        # Initialize a dictionary to store the specification for each of the
        # left, right and center strings.
        self.string_specs = dict(left=[], right=[], center=[])
        # Loop over each resource variable provided, handling the special
        # resource values.
        for res in resource_vars:
            # Iterate over each potential string position determining if the
            # string is requested and defining its properties if it is.
            for string_position in ('left', 'right', 'center'):
                # Construct the names of all the resources associated with a
                # string in the current position.
                special_resource_names = \
                        map(lambda s: s % string_position.capitalize(),
                            resource_name_templates)
                # Get a list of the values in the specifier for this string.
                special_resources_list = self._handle_special(
                        res, special_resource_names, string_defaults)
                if special_resources_list is not None:
                    # Record these values if they exist.
                    self.string_specs[string_position].append(
                            special_resources_list)

    def postplot(self, wks, plot):
        """Annotate the plot with title strings."""
        for position in ('left', 'right', 'center'):
            for string_spec in self.string_specs[position]:
                # Create text and annotation resource variables based on the
                # current string specification.
                txres = self._text_resources(string_spec, position)
                anres = self._annotation_resources(string_spec, position)
                # Create the actual text object.
                text_object = Ngl.text_ndc(wks, string_spec['string'], 0.,
                        0., txres)
                # Add the text object to the plot as an annotation. The plot
                # is a mutable object so doing this attaches the annotation to
                # the input plot.
                anno = Ngl.add_annotation(plot, text_object, anres)

    def _text_resources(self, string_spec, string_type):
        """Create resources to create text in the correct format."""
        justification = {'left': 'BottomLeft', 'right': 'BottomRight',
                'center': 'BottomCenter'}
        txres = Ngl.Resources()
        txres.nglDraw = False
        txres.txJust = justification[string_type]
        txres.txFont = string_spec.get(
                'ngl%sStringFont' % string_type.capitalize())
        txres.txFontColor = string_spec.get(
                'ngl%sStringFontColor' % string_type.capitalize())
        txres.txFontHeightF = string_spec.get(
                'ngl%sStringFontHeightF' % string_type.capitalize())
        return txres

    def _annotation_resources(self, string_spec, string_type):
        """
        Construct annotation resources suitable for attaching text to a
        plot in a given position.

        Note: Orthogonal and Parallel specifications are deliberately
        swapped so that the results correspond to NCL conventions. This
        is necessary since we use the left and right sides of the plot
        as a reference for the annotation and the Parallel and
        Orthogonal positions of these strings are typically referenced
        relative to the top of the plot in NCL.

        """
        justification = {'left': ('Left', 'BottomLeft'),
                'right': ('Right', 'BottomRight'),
                'center': ('Left', 'BottomCenter')}
        offset = {'left': .5, 'right': .5, 'center': 0.}
        anres = Ngl.Resources()
        anres.amSide, anres.amJust = justification[string_type]
        anres.amParallelPosF = string_spec.get(
                'ngl%sStringOrthogonalPosF' % string_type.capitalize()) + .55
        anres.amOrthogonalPosF = string_spec.get(
                'ngl%sStringParallelPosF' % string_type.capitalize()) + \
                        offset[string_type]
        return anres

    def _handle_special(self, res, resource_names, default_values):
        """Handle special resources.

        Creates a list of the values of the resources specified,
        substituting with the provided defaults if required, and removes
        all specified resource names from the resource variable.

        EDIT: does not remove resources. This is done by the applying
        decorator through the resource_names class variable.

        """
        # The main resource is the one that turns the string on if set:
        # 'ngl<Position>String'.
        main_resource = getattr(res, resource_names[0], None)
        if main_resource is not None:
            # Create an empty string specifier. Just a dictionary.
            string_spec = {'string': main_resource}
            for name, default in zip(resource_names[1:], default_values):
                # Update the specification with the value of the required
                # resource or its default value if not specified.
                string_spec.update({name: getattr(res, name, default)})
            return string_spec
        return None


if __name__ == '__main__':
    pass

