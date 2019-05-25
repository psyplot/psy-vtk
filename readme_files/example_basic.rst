
Basic proof of concept for psy-vtk
==================================

This notebook just tests the visualization of geo-referenced data using
psy-vtk and a rectilinear netCDF file (see `the psyplot
docs <https://psyplot.readthedocs.io/en/latest/getting_started.html>`__
if you want to see how it looks with matplotlib)

.. code:: ipython3

    import psyplot.project as psy
    import psy_vtk.plotters as pvtk






.. code:: ipython3

    %matplotlib inline

.. code:: ipython3

    ds = psy.open_dataset('demo.nc')
    ds




.. parsed-literal::

    <xarray.Dataset>
    Dimensions:  (lat: 96, lev: 4, lon: 192, time: 5)
    Coordinates:
      * lon      (lon) float64 0.0 1.875 3.75 5.625 7.5 ... 352.5 354.4 356.2 358.1
      * lat      (lat) float64 88.57 86.72 84.86 83.0 ... -83.0 -84.86 -86.72 -88.57
      * lev      (lev) float64 1e+05 8.5e+04 5e+04 2e+04
      * time     (time) datetime64[ns] 1979-01-31T18:00:00 ... 1979-05-31T18:00:00
    Data variables:
        t2m      (time, lev, lat, lon) float32 ...
        u        (time, lev, lat, lon) float32 ...
        v        (time, lev, lat, lon) float32 ...
    Attributes:
        CDI:          Climate Data Interface version 1.6.8 (http://mpimet.mpg.de/...
        Conventions:  CF-1.4
        history:      Mon Aug 17 22:51:40 2015: cdo -r copy test-t2m-u-v.nc test-...
        title:        Test file
        CDO:          Climate Data Operators version 1.6.8rc2 (http://mpimet.mpg....



.. code:: ipython3

    data = ds.psy.t2m[0, 0]

.. code:: ipython3

    globe_plot = pvtk.GlobePlotter(data)
    disp = globe_plot.ax.show()
    disp



.. image:: readme_files/example_basic_files/example_basic_5_0.png


.. code:: ipython3

    globe_plot.update(datagrid=True, cmap='viridis')
    disp



.. image:: readme_files/example_basic_files/example_basic_6_0.png

