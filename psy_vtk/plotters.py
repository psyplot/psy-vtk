"""plotters module of the psy-vtk psyplot plugin

This module defines the plotters for the psy-vtk package. It should import
all requirements and define the formatoptions and plotters that are specified
in the :mod:`psy_vtk.plugin` module.
"""
from psyplot.plotter import Formatoption, Plotter


# -----------------------------------------------------------------------------
# ---------------------------- Formatoptions ----------------------------------
# -----------------------------------------------------------------------------


class MyNewFormatoption(Formatoption):

    def update(self, value):
        # hooray
        pass


# -----------------------------------------------------------------------------
# ------------------------------ Plotters -------------------------------------
# -----------------------------------------------------------------------------


class MyPlotter(Plotter):

    _rcparams_string = ['plotter.psy_vtk.']

    my_fmt = MyNewFormatoption('my_fmt')
