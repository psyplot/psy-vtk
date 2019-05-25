"""Setup file for plugin psy-vtk

This file is used to install the package to your python distribution.
Installation goes simply via::

    python setup.py install
"""

from setuptools import setup, find_packages


setup(name='psy-vtk',
      version='0.0.1.dev0',
      description='VTK plugin for psyplot',
      keywords='visualization psyplot',
      license="GPLv3",
      packages=find_packages(exclude=['docs', 'tests*', 'examples']),
      url='https://github.com/Chilipp/psyplot',
      author='Philipp Sommer',
      author_email='philipp.sommer@unil.ch',
      install_requires=[
          'psyplot',
          'pyvista',
      ],
#      entry_points={'psyplot': ['plugin=psy_vtk.plugin']},
      zip_safe=False)
