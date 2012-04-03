"""additional/modified plotting functions for Ngl"""
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


import warnings
from copy import copy

import numpy as np
import Ngl

from defaults import ngldefaults as defaults
from modification import ModificationManager as ModMan
from modifiers import NglStrings


# Define plotting functions in this namespace with the same names as the Ngl
# plotting functions. These versions have modifications applied using a
# ModificationManager object. The modification applied allows the use of the
# NCL-style 'gsn' strings. Note that  we are re-defining the built-in 'map'
# here.
ModMan.addModifiers(NglStrings())
xy = ModMan(Ngl.xy)
y = ModMan(Ngl.y)
map = ModMan(Ngl.map)
contour = ModMan(Ngl.contour)
contour_map = ModMan(Ngl.contour_map)
streamline = ModMan(Ngl.streamline)
streamline_map = ModMan(Ngl.streamline_map)
streamline_scalar = ModMan(Ngl.streamline_scalar)
streamline_scalar_map = ModMan(Ngl.streamline_scalar_map)
vector = ModMan(Ngl.vector)
vector_map = ModMan(Ngl.vector_map)
vector_scalar = ModMan(Ngl.vector_scalar)
vector_scalar_map = ModMan(Ngl.vector_scalar_map)


# New plotting functions.
def histogram(wks, data, res):
    """Plot a histogram.

    The NumPy histogram function is used to define the histogram.

    Arguments:
    wks -- Ngl wrokstation.
    data -- 1D array of data to construct a histogram from.
    res -- Ngl resources variable. Valid resources are:
        
    """
    # Define a function to compute bar locations.
    def bar_position(x, y, dx, ymin, bar_width_perc):
        """Compute the coordinates required to draw a specified bar."""
        dxp = dx * bar_width_perc
        xbar = np.array([x, x+dxp, x+dxp, x, x])
        ybar = np.array([ymin, ymin, y, y, ymin])
        return xbar, ybar
    # Make a local copy of resources so they can be modified.
    res = copy(res)
    # Intercept and turn off draw and frame resources. These will be applied
    # if necessary once the histogram has been constructed.
    frame_on = getattr(res, 'nglFrame', True)
    draw_on = getattr(res, 'nglDraw', True)
    res.nglFrame = False
    res.nglDraw = False
    # Set default values of special resources that will not be recognised by 
    # Ngl.
    resdefaults = {
            'nglHistogramBarWidthPercent': 1.,
            'nglHistogramBinIntervals': None,
            'nglHistogramNumberOfBins': 10,
            'nglxHistogramRange': None,
            'nglxHistogramBarColor': 0,
            'nglxHistogramBarOutlineColor': 1,
            'nglxHistogramDensity': True,
    }
    # Record the values of the special resources, and remove them from the
    # resource list.
    specialres = dict()
    for resname in resdefaults.keys():
        specialres[resname] = getattr(res, resname, resdefaults[resname])
        try:
            delattr(res, resname)
        except AttributeError:
            pass
    # Work out the values of histogram parameters.
    nbins = specialres['nglHistogramBinIntervals'] or \
            specialres['nglHistogramNumberOfBins']
    hrange = specialres['nglxHistogramRange']
    density = specialres['nglxHistogramDensity']
    # Compute the histogram with the NumPy routine.
    hist, binedges = np.histogram(data, bins=nbins, range=hrange, density=density)
    dx = binedges[1] - binedges[0]
    ymin = 0.
    # Draw up to three bars, the first and last and the tallest, if they are
    # different. This sets up the plot correctly. The user specified plotting
    # resources are respected during this process. The lines drawn here will
    # be covered by the histogram.
    xdum, ydum = list(), list()
    xbar, ybar = bar_position(binedges[0], hist[0], dx, ymin,      # first bar
            specialres['nglHistogramBarWidthPercent'])
    xdum.append(xbar)
    ydum.append(ybar)
    if nbins > 1:
        xbar, ybar = bar_position(binedges[-2], hist[-1], dx, ymin,    # last bar
                specialres['nglHistogramBarWidthPercent'])
        xdum.append(xbar)
        ydum.append(ybar)
    i = np.argmax(hist)
    if i not in (0, nbins-1):
        xbar, ybar = bar_position(binedges[i], hist[i], dx, ymin,    # tallest bar
                specialres['nglHistogramBarWidthPercent'])
        xdum.append(xbar)
        ydum.append(ybar)
    plot = xy(wks, np.array(xdum), np.array(ydum), res)
    # Create resources for shading the bars and drawing outlines around them.
    fillres = Ngl.Resources()
    fillres.gsFillColor = specialres['nglxHistogramBarColor']
    lineres = Ngl.Resources()
    lineres.gsLineColor = specialres['nglxHistogramBarOutlineColor']
    # Draw the bars and their outlines.
    plot._histbars = list()
    plot._histlines = list()
    for bar in xrange(nbins):
        xbar, ybar = bar_position(binedges[bar], hist[bar], dx, ymin,
                specialres['nglHistogramBarWidthPercent'])
        plot._histbars.append(Ngl.add_polygon(wks, plot, xbar, ybar, fillres))
        plot._histlines.append(Ngl.add_polyline(wks, plot, xbar, ybar, lineres))
    # Apply drawing and frame advancing if they were specified in the input
    # resources.
    if draw_on:
        Ngl.draw(plot)
    if frame_on:
        Ngl.frame(plot)
    # Return a plot identifier.
    return plot


class PanelPlot(object):
    """Create panel plots from individual plots."""

    def __init__(self, warnings=False, debug=False):
        """
        Create a panel plot object.

        Optional arguments:
        warnings -- If True warnings will be used when a non-fatal but
            unexpected event occurs. An example of when a warning would
            be issued is if the users specifies 3 panels but provides 4
            plots and therefore only 3 can be drawn. If False no warnings
            are generated. Defaults to False.
        debug -- If True debugging output will be printed to stderr. If
            False no debugging output is produced. Defaults to False.

        """
        self._warnings_on = warnings
        self._debug_on = debug

    def __call__(self, wks, plots, dims, res=None):
        """Panel a collection of plots.
        
        Arguments:
        wks -- An Ngl workstation to plot onto.
        plots -- A collection of plots to put together into a panel
            plot.
        dims -- Dimensions of the panel plot. It should be specified as
            (rows, cols) or, if the panel resource 'nglPanelRowSpec' is
            set to True, as (cols0, cols1, cols2) where each entry
            is a row and its value specifies the number of columns in
            the row.
        res -- An Ngl resources object. The following resources are
            understood:

            'nglPanelRowSpec'
            'nglPanelCenter'
            'nglPanelScalePlotIndex'
            'nglPanelTop'
            'nglPanelLeft'
            'nglPanelRight'
            'nglPanelXF'
            'nglPanelYF'
            'nglPanelXWhiteSpacePercent'
            'nglPanelYWhiteSpacePercent'
            'nglPanelTitleString'
            'nglPanelTitleFont'
            'nglPanelTitleFontheightF'
            'nglPanelTitleFontColor'
            'nglPanelTitleOffsetXF'
            'nglPanelTitleOffsetYF'
            'nglPanelFigureStrings'            X not implemented
            'nglPanelLabelBar'                 X not implemented
            'nglPanelDebug'
       
        """
        # Get the unified panel specification. These details can be used to
        # produce the panel plot independently of the user's choice of panel
        # specification format.
        self.number_rows, self.number_columns, self.row_spec, \
                self.number_panels = self._get_panel_spec(dims, res)
        # Get the number of plots that can actually be plotted. We cannot plot
        # more plots than panels that are defined.
        self.number_plots = self._get_number_plots(plots)
        # Retrieve the width and height of the plots from the plot objects.
        # Only one plot is considered and the others assumed to be the same
        # size. Unless otherwise specified, the plot this information comes
        # from will be the first plot.
        self.plot_width, self.plot_height = \
                self._get_plot_dimensions(plots, res)
        # Compute the space to be left between plots. This consists of a base
        # size plus an offset. The offset can be user specified via the
        # resources variable.
        self.delta_x, self.delta_y = self._get_plot_spacing(res)
        # Compute the total width of the panel plot.
        self.total_width = self.number_columns * self.plot_width + \
                (self.number_columns - 1) * self.delta_x
        # Compute the top and left coordinates of the panel plot.
        self.panel_x0, self.panel_center_x = self._get_panel_xcoord(res)
        self.panel_y0 = self._get_panel_ycoord(res)
        # Work out where to draw each of the plots.
        self.plot_coordinates = self._get_plot_coords(res)
        # Draw each plot on the workstation.
        self._draw_plots(plots, res)
        # Draw panel labels if required.
        self._draw_panel_labels(wks, res)
        # Draw a main title if required.
        self._draw_main_title(wks, res)
        # Finish the panelling by advancing the frame unless requested not to.
        if getattr(res, 'nglPanelFrame', True):
            Ngl.frame(wks)

    def _draw_plots(self, plots, res):
        """Draw the provided plots."""
        for plot in xrange(self.number_plots):
            # It is OK for a plot to be None, it will just be skipped. This
            # allows the user to have a lot of control over their panel plot.
            if plots[plot] is not None:
                # Set the position of the plot.
                res_pos = Ngl.Resources()
                res_pos.vpXF, res_pos.vpYF = self.plot_coordinates[plot]
                Ngl.set_values(plots[plot], res_pos)
                # Draw to plot.
                Ngl.draw(plots[plot])

    def _draw_main_title(self, wks, res):
        """Draw a title string above the panel plot."""
        # A panel title is specified using the panel resources.
        ngl_panel_title_string = getattr(res, 'nglPanelTitleString', None)
        if ngl_panel_title_string is not None:
            # If a panel title is requested then it first needs to be parsed
            # for newlines. This allows a multi-line title to be properly
            # centered automatically.
            panel_titles = reversed(
                    [p.strip() for p in ngl_panel_title_string.split('\n')])
            # Create resources for displaying the text.
            txres = Ngl.Resources()
            txres.txFontHeightF = getattr(res, 'nglPanelTitleFontHeightF',
                    defaults['fontheight']['title'])
            txres.txFont = getattr(res, 'nglPanelTitleFont', 
                    defaults['font']['title'])
            txres.txJust = 'BottomCenter'
            # Work out the center coordinate of the title, this is the same
            # for each line of a multi-line title.
            title_x = self.panel_center_x + getattr(res,
                    'nglPanelTitleOffsetXF', 0.)
            for i, t in enumerate(panel_titles):
                # For each line of a multi-line title (just one for a single
                # line title) work out the y coordinate and then draw the text
                # on the workstation.
                title_y = self.panel_y0 + 0.04 + \
                        (i+ (i * 0.5)) * txres.txFontHeightF
                Ngl.text_ndc(wks, t, title_x, title_y, txres)

    def _draw_panel_labels(self, wks, res):
        ngl_panel_figure_strings = getattr(res, 'nglPanelFigureStrings', None)
        if ngl_panel_figure_strings is not None:
            txres = Ngl.Resources()
            txres.txFontHeightF = getattr(res,
                    'nglPanelFigureStringsFontHeightF',
                    defaults['fontheight']['ngl'])
            txres.txFontColor = getattr(res,
                    'nglPanelFigureStringsFontColor', 1)
            txres.txFont = getattr(res,
                    'nglPanelFigureStringsFont',
                    defaults['font']['labels'])
            txres.txJust = 'BottomRight'
            for plot in self.number_plots:
                plot_x, plot_y = self.plot_positions[plot]
                label_x = plot_x - 0.03
                label_y = plot_y + 0.03
                Ngl.text_ndc(wks, ngl_panel_figure_strings[plot], label_x,
                        label_y, txres)

    def _get_panel_spec(self, dims, res):
        """Generate a panel row specification and useful information."""
        is_row_spec = getattr(res, 'nglPanelRowSpec', False)
        if is_row_spec:
            # The given dimensions are in 'row spec' format, where each entry
            # in the dimensions array specifies the number of plots on that
            # row.
            for row_spec in dims:
                # Check the validity of each row specification, the number
                # must be positive.
                if row_spec < 1:
                    raise ValueError('a positive number of plots is required')
            # The row spec is as given by the dimensions so just store it.
            row_spec = dims
            # Also store the number of panels requested, and the number of
            # rows and columns. The number of columns is the maximum of all
            # the rows.
            npanels = sum(dims)
            nrows = len(dims)
            ncols = max(dims)
        else:
            # The given dimensions specify a grid as [rows, columns]. We need
            # to construct a corresponding row spec so that only one method
            # needs to be considered throughout this code.
            if len(dims) != 2:
                # Check that the dimension specification is a valid grid.
                raise ValuError('invalid dimension')
            # Store the number of rows and columns in the grid.
            nrows, ncols = dims
            npanels = nrows * ncols
            # Construct an equivalent 'row spec' format specification for the
            # grid.
            row_spec = [ncols] * nrows
        return (nrows, ncols, row_spec, npanels)

    def _get_number_plots(self, plots):
        """Get the number of plots that can actually be panelled."""
        nplots = len(plots)
        if nplots > self.number_panels:
            nplots = self.number_panels
            if self._warnings_on:
                warnings.warn('more plots than defined panels, truncating')
        return nplots

    def _get_plot_dimensions(self, plots, res):
        """Get the dimensions of the plots to be panelled."""
        # Select the index of the plot to get the size from.
        base_plot = getattr(res, 'nglPanelScalePlotIndex', 0)
        pwidth = Ngl.get_float(plots[base_plot], 'vpWidthF')
        pheight = Ngl.get_float(plots[base_plot], 'vpHeightF')
        return pwidth, pheight

    def _get_plot_spacing(self, res):
        """Work out the spacing between individual panels."""
        base_x = 0.04
        offset_x = getattr(res, 'nglPanelXWhiteSpacePercent', 0.) / \
                100. * self.plot_width
        base_y = 0.05
        offset_y = getattr(res, 'nglPanelYWhiteSpacePercent', 0.) / \
                100. * self.plot_height
        return (base_x + offset_x, base_y + offset_y)

    def _get_panel_xcoord(self, res):
        """Generate the x coordinate of the left edge of the panel."""
        ngl_panel_x = getattr(res, 'nglPanelXF', None)
        ngl_panel_left = getattr(res, 'nglPanelLeft', 0.)
        ngl_panel_right = getattr(res, 'nglPanelRight', 1.)
        if ngl_panel_x is None:
            # The x coordinate of the left edge is not explicitly defined, so
            # we should try to center the plot in the middle of the available
            # workstation. The available workstation is defined by the user.
            panel_center_x = (ngl_panel_left + ngl_panel_right) / 2.
            ngl_panel_x = panel_center_x - 0.5 * self.total_width
            if ngl_panel_x < ngl_panel_left:
                if self.warnings_on:
                    warnings.warn(
                           'panel is too wide for available workstation area')
        else:
            # If ngl_panel_x is defined we use all the space to the right that
            # is available to us.
            panel_center_x = ngl_panel_x + 0.5 * self.total_width
        return ngl_panel_x, panel_center_x

    def _get_panel_ycoord(self, res):
        """Generate the y coordinate of the top edge of the panel."""
        ngl_panel_y = getattr(res, 'nglPanelYF', None)
        ngl_panel_top = getattr(res, 'nglPanelTop', 1.)
        ngl_panel_bottom = getattr(res, 'nglPanelBottom', 0.)
        if ngl_panel_y is None:
            # The y coordinate of the top edge is not explicitly defined, so
            # we pick a default offset from the top of the available
            # workstation.
            ngl_panel_y = ngl_panel_top - 0.07
            if ngl_panel_y > 1:
                if self._warnings_on:
                    warnings.warn(
                          'panel is placed off the bottom of the workstation')
        return ngl_panel_y

    def _get_plot_coords(self, res):
        """
        Generate the coordinates of the top left corner of each  plot.
        
        """
        # How short rows are position can be user specified.
        ngl_panel_center = getattr(res, 'nglPanelCenter', True)
        # Create empty lists for the x and y coordinates.
        xpos, ypos = list(), list()
        # Use the row specification to determine the positions of each plot.
        panel_counter = 0
        for row in xrange(self.number_rows):
            ncols = self.row_spec[row]
            for col in xrange(ncols):
                panel_counter += 1
                if panel_counter > self.number_plots:
                    # If there are no more plots there is no point working out
                    # any more plot positions so we just stop early.
                    break
                # Compute the x coordinate of the plot.
                if ngl_panel_center and ncols < self.number_columns:
                    # The panel is on a short row and centering is required.
                    width = ncols * self.plot_width + \
                            (ncols - 1) * self.delta_x
                    x0 = self.panel_center_x - 0.5 * width
                    xpos.append(x0 + col * (self.plot_width + self.delta_x))
                else:
                    # The panel is on a full row or no centering is required.
                    xpos.append(self.panel_x0 + \
                            col * (self.plot_width + self.delta_x))
                # Compute the y coordinate of the plot.
                ypos.append(self.panel_y0 - \
                        row * (self.plot_height + self.delta_y))
        # Return a list of (x, y) coordinate pairs, one for each plot.
        return zip(xpos, ypos)


if __name__ == '__main__':
    pass

