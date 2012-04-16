"""Example plot modification.

Add a resource to control an institution name appearing in the lower
right corner of a plot.

"""
import numpy as np
import Ngl

from nglextras.modification import PlotModifier, ModificationManager


class InstitutionName(PlotModifier):

    # This class add the resource name "nglxInstitutionNameOn" which
    # turns on or off the plotting of the name of an institution name
    # in the lower right corner of the plot.
    resource_names = ["nglxInstitutionNameOn"]

    def preplot(self, *args):
        """
        Determine if the 'nglxInsitutionNameOn' resource is set to True.

        """
        # Retrieve all resource variables. Some plot types take two resources
        # variables as input.
        resource_vars = list()
        for arg in args:
            if isinstance(arg, Ngl.Resources):
                resource_vars.append(arg)
        # Decide if the institution name should be drawn or not.
        self._draw_institution_name = False
        for res in resource_vars:
            if getattr(res, "nglxInstitutionNameOn", False):
                self._draw_institution_name = True

    def postplot(self, wks, plot):
        """Draw the institution name."""
        if not self._draw_institution_name:
            # Return early if no modification is required.
            return
        # Create resources for the text itself and the annotation.
        txres = Ngl.Resources()
        txres.nglDraw = False
        txres.txFontColor = "red"
        anres = Ngl.Resources()
        anres.amSide = "Right"
        anres.amJust = "BottomRight"
        anres.amOrthogonalPosF = .46
        anres.amParallelPosF = -.46
        # Create the text and attach it to the plot as an annotation.
        text = Ngl.text_ndc(wks, "NglExtras", 0., 0., txres)
        anno = Ngl.add_annotation(plot, text, anres)


if __name__ == "__main__":

    # Add an instance of our modifier to the modification manager.
    ModificationManager.addModifiers(InstitutionName())

    # Wrap the Ngl function xy to create a modified version that
    # accepts our nglxInstitutionNameOn resource.
    xymod = ModificationManager(Ngl.xy)

    # Create a workstation.
    wkres = Ngl.Resources()
    wks = Ngl.open_wks("png", "plotmod_example", wkres)

    # Create a set of resources that turn on the institution name.
    res = Ngl.Resources()
    res.tiMainString = "res.nglxInstitutionNameOn=False (default)"

    x = np.arange(-np.pi, np.pi, np.pi/100.)
    y = np.sin(x)
    
    # Plot y=sin(x) with the instutution name turned off.
    plot = xymod(wks, x, y, res)

    # Plot y=sin(x) with the institution name turned on.
    res.nglxInstitutionNameOn = True
    res.tiMainString = "res.nglxInstitutionNameOn=True"
    plot = xymod(wks, x, y, res)

    Ngl.end()

