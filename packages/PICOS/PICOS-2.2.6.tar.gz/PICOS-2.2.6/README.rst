Introduction
============

PICOS is a user friendly Python API to several conic and integer programming
solvers, very much like `YALMIP <https://yalmip.github.io/>`_ or
`CVX <http://cvxr.com/cvx/>`_ under `MATLAB <http://www.mathworks.com/>`_.

PICOS allows you to enter a mathematical optimization problem as a **high level
model**, with painless support for **(complex) vector and matrix variables** and
**multidemensional algebra**. Your model will be transformed to the standard
form understood by an appropriate solver that is available at runtime. This
makes your application **portable** as users have the choice between several
commercial and open source solvers.

Features
--------

PICOS supports the following solvers and problem types. To use a solver, you
need to seperately install it along with the Python interface listed here.

.. _GPL-3: https://www.gnu.org/licenses/gpl-3.0.html
.. _MIT: https://opensource.org/licenses/MIT
.. _ZIB: https://scip.zib.de/academic.txt

.. list-table::
    :header-rows: 1

    * - | Solver
        |
      - | Python
        | interface
      - | `LP <https://en.wikipedia.org/wiki/Linear_programming>`_
        |
      - | `SOCP <https://en.wikipedia.org/wiki/Second-order_cone_programming>`_,
        | `QCQP <https://en.wikipedia.org/wiki/Quadratically_constrained_quadratic_program>`_
      - | `SDP <https://en.wikipedia.org/wiki/Semidefinite_programming>`_
        |
      - | `EXP <https://docs.mosek.com/modeling-cookbook/expo.html>`_
        |
      - | `MIP <https://en.wikipedia.org/wiki/Integer_programming>`_
        |
      - | License
        |
    * - `CPLEX <https://www.ibm.com/analytics/cplex-optimizer>`_
      - included
      - Yes
      - Yes
      -
      -
      - Yes
      - non-free
    * - `CVXOPT <https://cvxopt.org/>`_
      - native
      - Yes
      - Yes
      - Yes
      - `GP <https://en.wikipedia.org/wiki/Geometric_programming>`_
      -
      - `GPL-3`_
    * - `ECOS <https://github.com/embotech/ecos>`_
      - `ecos-python <https://github.com/embotech/ecos-python>`_
      - Yes
      - Yes
      -
      - Yes
      - Yes
      - `GPL-3`_
    * - `GLPK <https://www.gnu.org/software/glpk/>`_
      - `swiglpk <https://github.com/biosustain/swiglpk>`_
      - Yes
      -
      -
      -
      - Yes
      - `GPL-3`_
    * - `Gurobi <http://www.gurobi.com/products/gurobi-optimizer>`_
      - included
      - Yes
      - Yes
      -
      -
      - Yes
      - non-free
    * - `MOSEK <https://www.mosek.com/>`_
      - included
      - Yes
      - Yes
      - Yes
      - WIP
      - Yes
      - non-free
    * - `SCIP <http://scip.zib.de/>`_
      - `PySCIPOpt <https://github.com/SCIP-Interfaces/PySCIPOpt/>`_
      - Yes
      - Yes
      -
      -
      - Yes
      - `ZIB`_/`MIT`_
    * - `SMCP <http://smcp.readthedocs.io/en/latest/>`_
      - native
      -
      -
      - Yes
      -
      -
      - `GPL-3`_

.. rubric:: Example

This is what it looks like to solve a multidimensional mixed integer program
with PICOS:

>>> import picos
>>> P = picos.Problem()
>>> x = picos.IntegerVariable("x", 2)
>>> P.add_constraint(2*x <= 11)
<2×1 Affine Constraint: 2·x ≤ [11]>
>>> P.set_objective("max", picos.sum(x))
>>> P.solve(solver="glpk")  # Optional: Use GLPK as backend.
<feasible primal solution (claimed optimal) from glpk>
>>> P.value
10.0
>>> print(x)
[ 5.00e+00]
[ 5.00e+00]

You can head to the
`tutorial <https://picos-api.gitlab.io/picos/tutorial.html>`_ for more examples.

Installation
------------

As of release 2.2, PICOS requires **Python 3.4** or later.

.. rubric:: Via pip

If you are using `pip <https://pypi.org/project/pip/>`_ you can run
``pip install picos`` to get the latest version.

.. rubric:: Via Anaconda

If you are using `Anaconda <https://anaconda.org/>`_ you can run
``conda install -c picos picos`` to get the latest version.

.. rubric:: Via your system's package manager

.. list-table::
    :header-rows: 1
    :stub-columns: 1

    * - Distribution
      - Latest release
      - Latest version
    * - Arch Linux
      - `python-picos <https://aur.archlinux.org/packages/python-picos/>`__
      - `python-picos-git <https://aur.archlinux.org/packages/python-picos-git/>`__

If you are packaging PICOS for additional systems, please let us know.

.. rubric:: From source

The PICOS source code can be found on `GitLab
<https://gitlab.com/picos-api/picos>`_. There are only two dependencies:

- `NumPy <https://numpy.org/>`_
- `CVXOPT`_

Documentation
-------------

The full documentation can be browsed `online
<https://picos-api.gitlab.io/picos/>`__ or downloaded `in PDF form
<https://picos-api.gitlab.io/picos/picos.pdf>`__.

Credits
-------

.. rubric:: Developers

- `Guillaume Sagnol <http://page.math.tu-berlin.de/~sagnol/>`_ has started work
  on PICOS in 2012.
- `Maximilian Stahlberg <about:blank>`_ is extending and co-maintaining PICOS
  since 2017.

.. rubric:: Contributors

For an up-to-date list of all code contributors, please refer to the
`contributors page <https://gitlab.com/picos-api/picos/-/graphs/master>`_.
Should a reference from before 2019 be unclear, you can refer to the
`old contributors page <https://github.com/gsagnol/picos/graphs/contributors>`_
on GitHub as well.

License
-------

PICOS is free and open source software and available to you under the terms of
the `GNU GPL v3 <https://gitlab.com/picos-api/picos/raw/master/LICENSE.txt>`_.
