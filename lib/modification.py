"""modifications system for Ngl plots"""
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


from copy import copy

import Ngl


class PlotModifier(object):
    """Base class for plot modification objects.

    All modifiers should inherit from this object to ensure that the
    required methods exist.

    """

    # List of special resources that this modifier handles. These would
    # be any resources that Ngl will not recognize.
    resource_names = list()

    def preplot(self, *args):
        """Method called before a plot is created.
        
        This method recieves the full argument list to the plotting
        function which may be modified. Generally this method should
        parse the resource list for resource names it is associated
        with and take some action on these. Returns None.

        """
        pass

    def postplot(self, wks, plot):
        """method called after a plot is created.

        This method receives the workstation and the plot object.
        Modifications can then be applied to the plot. Returns None.

        """
        pass


class ModificationManager(object):
    """A decorator class for applying plot modifiers.
    
    The class methods addModifiers and setModifiers should be used to
    define the modifications that will be applied.
    
    """

    # Class variable defining the modifiers that are currently active.
    modifiers = list()

    @classmethod
    def addModifiers(cls, *modifiers):
        """Add modifiers to all modification managers.

        Argument:
        *modifiers -- PlotModification objects.

        """
        for m in modifiers:
            cls.modifiers.append(m)

    @classmethod
    def setModifiers(cls, modifiers):
        """Set the modifiers used for all modification managers.

        Argument:
        modifiers -- List/tuple etc. of PlotModifier objects.

        """
        cls.modifiers = modifiers

    def __init__(self, ngl_plot_func):
        """Initialize a ModificationManager.

        Argument:
        ngl_plot_func -- An Ngl plotting function to be modified.

        """
        self.f = ngl_plot_func

    def __call__(self, *args):
        """Ngl graphics function with modifications applied."""
        # Make a local copy of the resources arguments, preventing them
        # from being modified in the calling namespace. These copied (and
        # possibly modified) are used only inside this method.
        res = list()
        for i, arg in enumerate(args):
            if isinstance(arg, Ngl.Resources):
                res.append((copy(arg), i))
        # Form the new argument list containing copies of the resource
        # variables. We alse need to intercept nglDraw and nglFrame at the top
        # level, making sure they are turned off while modifications are
        # applied. After modifications we can check if drawing and frame
        # advancing was requested and do so then.
        new_args = list(args)
        draw_on = frame_on = False
        for r, i in res:
            draw_on = getattr(r, 'nglDraw', True)
            frame_on = getattr(r, 'nglFrame', True)
            if draw_on:
                setattr(r, 'nglDraw', False)
            if frame_on:
                setattr(r, 'nglFrame', False)
            new_args[i] = r
        # Call the modifier pre-plot methods.
        special_resources = list()
        for modifier in self.modifiers:
            # Run the preplot method of each modifier.
            modifier.preplot(*new_args)
            special_resources += modifier.resource_names
        # Go back and remove all special resources from resource variables
        # before they are passed to the Ngl plotting routine.
        for r, i in res:
            for resource_name in special_resources:
                try:
                    delattr(r, resource_name)
                except AttributeError:
                    pass
        # Make the plot.
        plot = self.f(*new_args)
        # Call the modifier post-plot methods.
        wks = args[0]
        for modifier in self.modifiers:
            modifier.postplot(wks, plot)
        # Check if the plot should be drawn and the frame advanced. Do so now
        # if required.
        if draw_on:
            Ngl.draw(plot)
        if frame_on:
            Ngl.frame(wks)
        # Return the modified plot.
        return plot

    def __repr__(self):
        return self.f.__repr__()

    def __get__(self, obj, objtype):
        return functools.partial(self.__call__, obj)

    __doc__ = property(lambda self:self.f.__doc__)
    __module__ = property(lambda self:self.f.__module__)
    __name__ = property(lambda self:self.f.__name__)


if __name__ == '__main__':
    pass

