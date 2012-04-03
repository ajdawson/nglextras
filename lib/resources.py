"""Ngl resource creation and management"""
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


class Resources(object, Ngl.Resources):
    """
    Wrapper for Ngl.Resources allowing for some resources to be pre-set.
    
    """

    def __init__(self):
        try:
            # Call the parent class constructor to inherit anything it sets
            # there.
            Ngl.Resources.__init__(self)
        except:
            # We don't worry if this fails. Currently the Ngl.Resources class
            # has no __init__ method, but we do this in case one is added in
            # the future.
            pass
        # By default we do not want plots to be drawn on the workstation or
        # the workstation frame to be advanced.
        self.nglDraw = False
        self.nglFrame = False
        # We want the user to specify the size of the plot.
        self.nglMaximize = False
        # Define the font size to be used for some of the standard plot
        # elements. The defaults system is used to set these values. The user
        # may change the defaults.
        self.tiMainFontHeightF = defaults['fontheight']['title']
        self.tiXAxisFontHeightF = defaults['fontheight']['axistitle']
        self.tiYAxisFontHeightF = defaults['fontheight']['axistitle']
        self.tmXBLabelFontHeightF = defaults['fontheight']['axislabel']
        self.tmXTLabelFontHeightF = defaults['fontheight']['axislabel']
        self.tmYLLabelFontHeightF = defaults['fontheight']['axislabel']
        self.tmYRLabelFontHeightF = defaults['fontheight']['axislabel']
        # Define the fonts to be used for some standard plot elements. Again
        # these values come from the defaults system.
        self.tiMainFont = defaults['font']['title']
        self.tiXAxisFont = defaults['font']['axistitle']
        self.tiYAxisFont = defaults['font']['axistitle']
        self.tmXBLabelFont = defaults['font']['axislabel']
        self.tmXTLabelFont = defaults['font']['axislabel']
        self.tmYLLabelFont = defaults['font']['axislabel']
        self.tmYRLabelFont = defaults['font']['axislabel']
        # Set the length of tick marks.
        self.tmXBMajorLengthF = defaults['ticksize']['major']
        self.tmXTMajorLengthF = defaults['ticksize']['major']
        self.tmYLMajorLengthF = defaults['ticksize']['major']
        self.tmYRMajorLengthF = defaults['ticksize']['major']
        self.tmXBMinorLengthF = defaults['ticksize']['minor']
        self.tmXTMinorLengthF = defaults['ticksize']['minor']
        self.tmYLMinorLengthF = defaults['ticksize']['minor']
        self.tmYRMinorLengthF = defaults['ticksize']['minor']


class MapResources(Resources):
    """Resources tailored to map plots."""

    def __init__(self, dims=None):
        """Create a map resources object."""
        # Call the parent class constructor to inherit all the base resources.
        super(MapResources, self).__init__()
#        Resources.__init__(self)
        # Set the plot size if provided.
        if dims is not None:
            self.vpWidthF, self.vpHeightF = dims
        # Turn off the map grid.
        self.mpGridAndLimbOn = False
        # Allow the aspect ratio of a map to be anything the user wants.
        self.mpShapeMode = 'FreeAspect'
        # Turn on tick marks for the top and right map edges.
        self.tmXTOn = True
        self.tmYROn = True
        # Define the size, orientation and position of a plot labelbar. The
        # orientation is stored in a variable hidden from Ngl by a leading
        # double underscore. Unfortunately Python's name mangling scheme will
        # convert this to _MapResources__lbOrientation, something Ngl will
        # find, unless a trailing underscore is added to the name. This 
        # variable is hidden from Ngl so that the property access can be used
        # instead. This allows the size of the labelbar to be changed
        # dynamically as the orientation changes.
        self.__lbOrientation__ = 'Horizontal'
        self.lbLabelFont = defaults['font']['axislabel']
        try:
            # Try to set the labelbar size and font height. This depends on
            # knowing the plot height in advance.
            self.pmLabelBarHeightF = 0.02 / self.vpHeightF
            self.lbLabelFontHeightF = defaults['fontheight']['axislabel'] * \
                    0.6 / self.vpWidthF
            self.pmLabelBarWidthF = 0.6
        except AttributeError:
            # If the plot height is not known then we can't set the labelbar
            # size, just carry on without doing it.
            pass
        # Also define the default format of labelbar labels.
        #self.lbLabelFormat = defaults['format']['labelbar']

    @property
    def lbOrientation(self):
        "Getter method for lbOrientation attribute."""
        return self.__lbOrientation__

    @lbOrientation.setter
    def lbOrientation(self, value):
        """Setter method for lbOrientation attribute.

        Sets the values of the pmLabelBarWidthF and pmLabelBarWidthF
        attributes appropriately for the value of the orientation.

        """
        self.__lbOrientation__ = value
        try:
            h = self.vpHeightF
            w = self.vpWidthF
            if value.lower() == 'vertical':
                self.pmLabelBarWidthF = 0.02 / w
                self.pmLabelBarHeightF = 0.6
            elif value.lower() == 'horizontal':
                self.pmLabelBarWidthF = 0.6
                self.pmLabelBarHeightF = 0.02 / h
            self.lbLabelFontHeightF = \
                        defaults['fontheight']['axislabel'] * 0.6 / w
        except AttributeError:
            pass

    @lbOrientation.deleter
    def lbOrientation(self):
        del self.__lbOrientation__
        

if __name__ == '__main__':
    pass

