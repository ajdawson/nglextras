nglextras
=========

This is a collection of tools used in conjunction with [PyNGL](http://http://www.pyngl.ucar.edu). The tools were developed out of personal need, but it is hoped that they may be useful to the wider PyNGL user community.


Description
-----------

The package contains a variety of tools to aid plotting. These include a generic mechanism for adding resources to a plot method (e.g., make Ngl.contour_map recognize left and right string resources); a system for setting and managing default values for things like fonts, font sizes etc.; and custom resource classes to make creating plots just the way you want them with no hassle.

The generic tools currently consist of:

* `PlotModifier`: Allows arbitrary modifications to Ngl plotting routines without having to edit their source code. An example of use is the included `NglStrings` modifier in the package, which allows any plotting routine to accept resources for setting and controlling the appearance of left right and center strings.

* `ModificationManager`: Manage the application of plot modifiers.


Notes
-----

* Currently the defaults system is rather crude, but functional. This could easily be improved on.


Installation
------------

    sudo python setup.py install

to install system-wide, or to install in a specific place

    python setup.py install --intall-lib=/PATH/TO/INSTALL/DIR

