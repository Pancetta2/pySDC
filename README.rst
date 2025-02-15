Welcome to pySDC!
=================

The `pySDC` project is a Python implementation of the spectral deferred correction (SDC) approach and its flavors,
esp. the multilevel extension MLSDC and PFASST. It is intended for rapid prototyping and educational purposes.
New ideas like e.g. sweepers or predictors can be tested and first toy problems can be easily implemented.


Features
--------

- Variants of SDC: explicit, implicit, IMEX, multi-implicit, Verlet, multi-level, diagonal, multi-step
- Variants of PFASST: virtual parallel or MPI-based parallel, classical of multigrid perspective
- 8 tutorials: from setting up a first collocation problem to SDC, PFASST and advanced topics
- Projects: many documented projects with defined and tested outcomes
- Many different examples, collocation types, data types already implemented
- Works with `FEniCS <https://fenicsproject.org/>`_, `mpi4py-fft <https://mpi4py-fft.readthedocs.io/en/latest/>`_ and `PETSc <http://www.mcs.anl.gov/petsc/>`_ (through `petsc4py <https://bitbucket.org/petsc/petsc4py>`_)
- Continuous integration via `Github Actions <https://github.com/Parallel-in-Time/pySDC/actions>`__
- Fully compatible with Python 3.6 - 3.9


Getting started
---------------

The code is hosted on GitHub, see `https://github.com/Parallel-in-Time/pySDC <https://github.com/Parallel-in-Time/pySDC>`_, and PyPI, see `https://pypi.python.org/pypi/pySDC <https://pypi.python.org/pypi/pySDC>`_.
Use

.. code-block:: bash

   pip install pySDC

to get the latest stable release including the core dependencies.
Note that this will omit some of the more complex packages not required for the core functionality of `pySDC`, e.g. `mpi4py`, `fenics` and `petsc4py` (see below).
All requirements are listed in the files `requirements.txt <https://github.com/Parallel-in-Time/pySDC/blob/master/requirements.txt>`_ .
To work with the source files, checkout the code from Github and install the dependencies e.g. by using a `conda <https://conda.io/en/latest/>`_ environment and

.. code-block:: bash

   conda install -c conda-forge --file requirements.txt

To check your installation, run

.. code-block:: bash

   pytest pySDC/tests

You may need to update your ``PYTHONPATH`` by running

.. code-block:: bash

   export PYTHONPATH=$PYTHONPATH:/path/to/pySDC/root/folder

in particular if you want to run any of the playgrounds, projects or tutorials.
All ``import`` statements there assume that the `pySDC`'s base directory is part of ``PYTHONPATH``.

Note: When installing `mpi4py`, `fenics` and `petsc4py`, make sure they use the same MPI installation (e.g. MPICH3).
You can achieve this e.g. by

.. code-block:: bash

   conda install -c conda-forge mpich petsc4py mpi4py fenics

Most of the code is tested automatically using `Github Actions <https://github.com/Parallel-in-Time/pySDC/actions>`__, so
a working version of the installation process can always be found in the `ci_pipeline.yml <https://github.com/Parallel-in-Time/pySDC/blob/master/.github/workflows/ci_pipeline.yml>`_ file.
This workflow can be run locally using `act <https://github.com/nektos/act>`_ by

.. code-block:: bash

   act --env CONDA=/usr/share/miniconda -j ci

See also `this page <https://github.com/lmmx/devnotes/wiki/Running-GitHub-CI-locally-with-nektos-act-(Docker)-in-LXC>`_ for details on how to run workflows depending on miniconda locally.

For many examples, `LaTeX` is used for the plots, i.e. a decent installation of this is needed in order to run the tests.
When using `fenics` or `petsc4py`, a C++ compiler is required (although installation may go through at first).

For more details on `pySDC`, check out `http://www.parallel-in-time.org/pySDC <http://www.parallel-in-time.org/pySDC>`_.


How to cite
-----------

If you use pySDC or parts of it for your work, great! Let us know if we can help you with this. Also, we would greatly appreciate a citation of `this paper <https://doi.org/10.1145/3310410>`_:

   Robert Speck, **Algorithm 997: pySDC - Prototyping Spectral Deferred Corrections**, 
   ACM Transactions on Mathematical Software (TOMS), Volume 45 Issue 3, August 2019,
   `https://doi.org/10.1145/3310410 <https://doi.org/10.1145/3310410>`_

The current software release can be cited using Zenodo: |zenodo|

.. |zenodo| image:: https://zenodo.org/badge/26165004.svg
   :target: https://zenodo.org/badge/latestdoi/26165004

Acknowledgements
----------------

This project has received funding from the `European High-Performance Computing Joint Undertaking <https://eurohpc-ju.europa.eu/>`_  (JU) under grant agreement No 955701 (`TIME-X <https://www.time-x-eurohpc.eu/>`_).
The JU receives support from the European Union’s Horizon 2020 research and innovation programme and Belgium, France, Germany, and Switzerland.
This project also received funding from the `German Federal Ministry of Education and Research <https://www.bmbf.de/bmbf/en/home/home_node.html>`_ (BMBF) grant 16HPC047.

.. image:: docs/source/logo/Time-X.png
   :width: 20%

.. image:: docs/source/logo/EU.png
   :width: 15%

.. image:: docs/source/logo/BMBF.jpg
   :width: 20%
