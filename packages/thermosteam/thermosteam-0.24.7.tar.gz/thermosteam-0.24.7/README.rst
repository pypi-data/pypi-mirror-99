====================================================
Thermosteam: BioSTEAM's Premier Thermodynamic Engine 
====================================================

.. image:: http://img.shields.io/pypi/v/thermosteam.svg?style=flat
   :target: https://pypi.python.org/pypi/thermosteam
   :alt: Version_status
.. image:: http://img.shields.io/badge/docs-latest-brightgreen.svg?style=flat
   :target: https://thermosteam.readthedocs.io/en/latest/
   :alt: Documentation
.. image:: https://img.shields.io/pypi/pyversions/thermosteam.svg
   :target: https://pypi.python.org/pypi/thermosteam
   :alt: Supported_versions
.. image:: http://img.shields.io/badge/license-UIUC-blue.svg?style=flat
   :target: https://github.com/BioSTEAMDevelopmentGroup/thermosteam/blob/master/LICENSE.txt
   :alt: license
.. image:: https://coveralls.io/repos/github/BioSTEAMDevelopmentGroup/thermosteam/badge.svg?branch=master
   :target: https://coveralls.io/github/BioSTEAMDevelopmentGroup/thermosteam?branch=master
   :alt: Coverage
.. image:: https://travis-ci.com/BioSTEAMDevelopmentGroup/thermosteam.svg?branch=master
   :target: https://travis-ci.com/BioSTEAMDevelopmentGroup/thermosteam
.. image:: https://joss.theoj.org/papers/10.21105/joss.02814/status.svg
   :target: https://doi.org/10.21105/joss.02814

.. contents::

What is Thermosteam?
--------------------

Thermosteam is a standalone thermodynamic engine capable of estimating mixture 
properties, solving thermodynamic phase equilibria, and modeling stoichiometric 
reactions. Thermosteam builds upon `chemicals <https://github.com/CalebBell/chemicals>`_, 
the chemical properties component of the Chemical Engineering Design Library, 
with a robust and flexible framework that facilitates the creation of property packages.  
`The Biorefinery Simulation and Techno-Economic Analysis Modules (BioSTEAM) <https://biosteam.readthedocs.io/en/latest/>`_ 
is dependent on thermosteam for the simulation of unit operations.

Installation
------------

Get the latest version of Thermosteam from `PyPI <https://pypi.python.org/pypi/thermosteam/>`_.
If you have an installation of Python with pip, simple install it with::

    $ pip install thermosteam

To get the git version and install it, run::

    $ git clone --depth 100 git://github.com/BioSTEAMDevelopmentGroup/thermosteam
    $ cd thermosteam
    $ pip install .

We use the `depth` option to clone only the last 100 commits. Thermosteam has a 
long history, so cloning the whole repository (without using the depth option)
may take over 30 min.

Documentation
-------------

Thermosteam's documentation is available on the web:

    http://thermosteam.readthedocs.io/

Bug reports
-----------

To report bugs, please use the thermosteam's Bug Tracker at:

    https://github.com/BioSTEAMDevelopmentGroup/thermosteam


License information
-------------------

See ``LICENSE.txt`` for information on the terms & conditions for usage
of this software, and a DISCLAIMER OF ALL WARRANTIES.

Although not required by the thermosteam license, if it is convenient for you,
please cite Thermosteam if used in your work. Please also consider contributing
any changes you make back, and benefit the community.


Citation
--------

To cite Thermosteam in publications use::

    Cortés-Peña, Y., (2020). Thermosteam: BioSTEAM’s Premier Thermodynamic Engine. 
    Journal of Open Source Software, 5(56), 2814. https://doi.org/10.21105/joss.02814
