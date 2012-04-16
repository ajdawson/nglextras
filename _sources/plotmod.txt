Plot modification system
========================

One of the most useful features of :py:mod:`nglextras` is the plot modification system. This allows you to create extra resources that affect plotting behaviour, and have these recognised by :py:mod:`Ngl` plotting functions without modifying their code.

The idea behind this system is simple: to be able to create arbitrary modifications to plotting functions, which can be combined in a way the user chooses. 


Plot modifications
------------------

Plot modifications work by automatically wrapping plotting functions with code that performs the modifications. It is of course possible to write function wrappers that apply custom modifications to plots. However, using this system is more flexible as the same modifications can be re-used for multiple plotting functions and also combined with other modifications..

A plot modification consists of an instance of a class derived from :py:class:`nglextras.modification.PlotModifier`. The :py:class:`~nglextras.modification.PlotMofifier` class has the following form:

  .. autoclass:: nglextras.modification.PlotModifier
     :members: resource_names, preplot, postplot
     :undoc-members:
     :noindex:

The class variable :py:attr:`~nglextras.modification.PlotModifier.resource_names` is a list which must include the names of all the special resources defined by the modifier. This allows these special resource names to be removed from the resource list before being passed to :py:mod:`Ngl` plotting functions.

The methods :py:meth:`~nglextras.modification.PlotModifier.preplot` and :py:meth:`~nglextras.modification.PlotModifier.postplot` should be overridden so as to produce the required modifications. Typically :py:meth:`~nglextras.modification.PlotModifier.preplot` will look for resource variables, and parse them to determine which features of the current modification are required. The actual modifications are then made to the plot in :py:meth:`~nglextras.modification.PlotModifier.postplot`.


Applying modifications
----------------------

Modifications are applied to plotting functions via the :py:class:`nglextras.modification.ModificationManager` decorator class. The class method :py:meth:`~nglextras.modification.ModificationManager.addModifiers` is called with an instance the :py:class:`~nglextras.modification.PlotMofifier` to be applied:

  .. code-block:: python

     ModificationManager.addModifier(MyPlotModifier())
     
An instance of the :py:class:`~nglextras.modification.ModificationManager` class can then be created with an Ngl plotting function as the argument to its constructor. This will add all the modifications known to the :py:class:`~nglextras.modification.ModificationManager` to the plotting function:

  .. code-block:: python

     contour_map_mod = ModificationManager(Ngl.contour_map)


Example
-------

The following example creates a plot modifier that adds an annotation to the lower right corner of the plot. This annotation could be the name of your institution or research group etc.:

.. literalinclude:: codeexamples/plotmod_example.py

which produces the following plots:

.. image:: plotexamples/plotmod_example_instoff.png
   :width: 400

.. image:: plotexamples/plotmod_example_inston.png
   :width: 400
