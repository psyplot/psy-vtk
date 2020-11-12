"""plotters module of the psy-vtk psyplot plugin

This module defines the plotters for the psy-vtk package. It should import
all requirements and define the formatoptions and plotters that are specified
in the :mod:`psy_vtk.plugin` module.
"""
from psyplot.plotter import Formatoption, Plotter, BEFOREPLOTTING
import psyplot
from psy_simple.plotters import CMap, Bounds, Plot2D
import numpy as np
import pyvista as pv
from pyvista import examples


# -----------------------------------------------------------------------------
# ---------------------------- Formatoptions ----------------------------------
# -----------------------------------------------------------------------------


if psyplot.with_gui:
    from pyvistaqt import BackgroundPlotter as PlotterClass
else:
    PlotterClass = pv.Plotter


class DataGrid(Formatoption):

    connections = ['plot']

    priority = BEFOREPLOTTING

    name = 'Show the datagrid'

    default = False

    def validate(self, value):
        return bool(value)

    def update(self, value):
        self.plot._plot_kws['show_edges'] = value


class GlobePlot(Plot2D):

    default = True

    priority = BEFOREPLOTTING

    dependencies = ['cmap', 'bounds']

    def validate(self, value):
        return bool(value)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._plot_kws = {}
        self.actor = None

    def update(self, value):
        pass

    def make_plot(self):
        if self.actor is not None:
            self.ax.remove_actor(self.actor)
        globe = examples.load_globe()
        lat = self.cell_nodes_y
        lon = self.cell_nodes_x
        height = globe.points[:, -1].max() - 10

        if lat.ndim > 2:
            lat = lat.reshape((-1, lat.shape[-1]))
            lon = lon.reshape((-1, lon.shape[-1]))

        # transform lon, lat into cartesian coordinates
        x = height * np.cos(lat*np.pi/180)*np.cos(lon*np.pi/180)
        y = height * np.cos(lat*np.pi/180)*np.sin(lon*np.pi/180)
        z = height * np.sin(lat*np.pi/180)

        # put the vertices together
        vertices = np.vstack([x.ravel(), y.ravel(), z.ravel()]).T

        # compute the faces
        nv = x.shape[1]
        faces = np.hstack([[nv] + list(range(i, i+nv))
                           for i in range(0, vertices.shape[0], nv)])

        # create the polygon
        poly = pv.PolyData(vertices, faces)
        kws = self._plot_kws.copy()
        arr = self.data.values.ravel()
        norm = self.bounds.norm

        arr = norm.boundaries[norm(arr)]

        if self.value:
            kws['scalars'] = arr

        kws['cmap'] = cmap = self.cmap.get_cmap(arr)
        kws['n_colors'] = cmap.N

        self.actor = self.ax.add_mesh(poly, **kws)

# -----------------------------------------------------------------------------
# ------------------------------ Plotters -------------------------------------
# -----------------------------------------------------------------------------


class GlobePlotter(Plotter):

    _rcparams_string = ['plotter.plot2d.', 'plotter.psy_vtk.']

    convert_radian = True

    datagrid = DataGrid('datagrid')
    cmap = CMap('cmap')
    bounds = Bounds('bounds')
    plot = GlobePlot('plot')

    @property
    def ax(self):
        """Axes instance of the plot"""
        if self._ax is None:
            self._ax = PlotterClass()
        return self._ax

    @ax.setter
    def ax(self, value):
        self._ax = value

    def start_update(self, draw=False, *args, **kwargs):
        # set draw=False always (we do not use matplotlib!)
        return super().start_update(False, *args, **kwargs)
