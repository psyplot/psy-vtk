"""plotters module of the psy-vtk psyplot plugin

This module defines the plotters for the psy-vtk package. It should import
all requirements and define the formatoptions and plotters that are specified
in the :mod:`psy_vtk.plugin` module.
"""
from psyplot.plotter import Formatoption, Plotter, BEFOREPLOTTING
from psy_simple.plotters import CMap, Bounds, convert_radian
import numpy as np
import pyvista as pv
from pyvista import examples


# -----------------------------------------------------------------------------
# ---------------------------- Formatoptions ----------------------------------
# -----------------------------------------------------------------------------


class DataGrid(Formatoption):

    connections = ['plot']

    priority = BEFOREPLOTTING

    name = 'Show the datagrid'

    default = False

    def validate(self, value):
        return bool(value)

    def update(self, value):
        self.plot._plot_kws['show_edges'] = value


class GlobePlot(Formatoption):

    default = True

    plot_fmt = True

    group = 'plotting'

    priority = BEFOREPLOTTING

    dependencies = ['cmap', 'bounds']

    name = 'Plotter for the data'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._plot_kws = {}
        self.actor = None

    @property
    def xcoord(self):
        """The x coordinate :class:`xarray.Variable`"""
        return self.decoder.get_x(self.data, coords=self.data.coords)

    @property
    def ycoord(self):
        """The y coordinate :class:`xarray.Variable`"""
        return self.decoder.get_y(self.data, coords=self.data.coords)

    @property
    def cell_nodes_x(self):
        """The unstructured x-boundaries with shape (N, m) where m > 2"""
        decoder = self.decoder
        xcoord = self.xcoord
        data = self.data
        xbounds = decoder.get_cell_node_coord(
            data, coords=data.coords, axis='x')
        if self.plotter.convert_radian:
            xbounds = convert_radian(xbounds, xcoord, xbounds)
        return xbounds.values

    @property
    def cell_nodes_y(self):
        """The unstructured y-boundaries with shape (N, m) where m > 2"""
        decoder = self.decoder
        ycoord = self.ycoord
        data = self.data
        ybounds = decoder.get_cell_node_coord(
            data, coords=data.coords, axis='y')
        if self.plotter.convert_radian:
            ybounds = convert_radian(ybounds, ycoord, ybounds)
        return ybounds.values

    def update(self, value):
        pass

    def make_plot(self):
        if self.actor is not None:
            self.ax.remove_actor(self.actor)
        globe = examples.load_globe()
        lat = self.cell_nodes_y
        lon = self.cell_nodes_x
        height = globe.points[:, -1].max() - 10

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
            self._ax = pv.Plotter()
        return self._ax

    @ax.setter
    def ax(self, value):
        self._ax = value

    def start_update(self, draw=False, *args, **kwargs):
        # set draw=False always (we do not use matplotlib!)
        return super().start_update(False, *args, **kwargs)
