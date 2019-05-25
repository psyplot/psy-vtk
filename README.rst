===============================
psy-vtk: VTK plugin for psyplot
===============================

This  proof of concept shows the principal functionality for using vtk inside
the psyplot visualization framework. We use the functionality of psyplot and
combine it with the wonderful vtk interface by pyvista_ [1]_.

You can run some example use cases interactively on mybinder.org: |binder|

.. note::

    This package is in the development mode and it will take several months
    until it is ready for general usage. But we are looking for contributions
    and/or feedback. Just raise a new issue or post your comment in
    `#1`_


.. _pyvista: https://docs.pyvista.org
.. _#1: https://github.com/Chilipp/psy-vtk/issues/1

.. |binder| image:: https://mybinder.org/badge_logo.svg
    :target: https://mybinder.org/v2/gh/Chilipp/psy-vtk/master?filepath=examples/

.. include:: readme_files/example_basic.rst

References
==========
.. [1] Sullivan et al., (2019). PyVista: 3D plotting and mesh analysis through a streamlined interface for the Visualization Toolkit (VTK). Journal of Open Source Software, 4(37), 1450, https://doi.org/10.21105/joss.01450
