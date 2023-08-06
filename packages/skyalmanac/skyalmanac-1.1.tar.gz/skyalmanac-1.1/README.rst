==============================
SkyAlmanac Project Description
==============================

.. |nbsp| unicode:: 0xA0
   :trim:

.. |emsp| unicode:: U+2003
   :trim:

This is the **PyPI edition** of `SkyAlmanac-Py3 <https://github.com/aendie/Skyalmanac-Py3>`_. Version numbering started from 1.0 as the previous well-tested versions that are on github since 2015 were never published in PyPI.

.. |smiley| image:: https://github.githubassets.com/images/icons/emoji/unicode/1f603.png
   :height: 24 px
   :width:  24 px

-----------------------------------------------------------------------------------------------------------------------
|emsp| |emsp| |emsp| |emsp| |emsp| |smiley| |emsp| **UT1 is the timescale now employed in the almanac** |emsp| |smiley|
-----------------------------------------------------------------------------------------------------------------------

Skyalmanac is a **Python 3** script that creates the daily pages of the Nautical Almanac.
The generated tables are needed for celestial navigation with a sextant.
Although you are strongly advised to purchase the official Nautical Almanac, this program will reproduce the tables with no warranty or guarantee of accuracy.

Two astronomical libraries are employed: `Skyfield <https://rhodesmill.org/skyfield/>`_ and `Ephem <https://rhodesmill.org/pyephem/>`_.
Ephem is only used for calculating twilight (actual, civil and nautical sunrise/sunset) and moonrise/moonset, as Ephem improves performance significantly with only a marginal loss of accuracy in the times stated above (that are rounded to the minute anyway).

Skyalmanac uses the Hipparcos catalog as its star database. If a current version Skyfield (>= 1.31) is used, you have two options (which one, you specify manually by editing *config.py*): 

* if "useIERS = False", the built-in UT1 tables in the installed version of Skyfield will be employed.
* if "useIERS = True", for optimal accuracy (especially for all GHA data), Earth orientation data from IERS (International Earth Rotation and Reference Systems Service) is downloaded and then used until it 'expires'. It expires after a chosen number of days (also specifiable in *config.py*). Note that IERS specifies the range of Earth Orientation Parameter (EOP) data currently as "from 2nd January 1973 to 15th May 2022". Refer to the `IERS web site <https://www.iers.org/IERS/EN/Home/home_node.html>`_ for current information.

If your Skyfield version is somewhat older (<= 1.30), Skyfield will have downloaded the older files it then used: *deltat.data, deltat.preds* and *Leap_Second.dat*, which are slightly less accurate than the IERS EOP data.

Software Requirements
=====================

|
| Astronomical computation is done by the free Ephem and Skyfield libraries.
| Typesetting is done typically by MiKTeX or TeX Live.
| These need to be installed:

* `python <https://www.python.org/downloads/>`_ >= 3.4 (the latest version is recommended)
* `skyfield <https://pypi.org/project/skyfield/>`__ >= v1.15 (see the `Skyfield Changelog <https://rhodesmill.org/skyfield/installation.html#changelog>`_)
* `pandas <https://pandas.pydata.org/>`_ >= 1.0 (to decode the Hipparcos catalog)
* `ephem <https://pypi.org/project/ephem/>`__ >= 3.7.6
* `MiKTeX <https://miktex.org/>`_ |nbsp| |nbsp| or |nbsp| |nbsp| `TeX Live <http://www.tug.org/texlive/>`_

Installation
============

Install a TeX/LaTeX program on your operating system so that 'pdflatex' is available.

Ensure that the `pip Python installer tool <https://pip.pypa.io/en/latest/installing.html>`_ is installed. 
Then ensure that old versions of PyEphem, Ephem and Skyalmanac are not installed before installing SkyAlmanac from PyPI::

  python -m pip uninstall pyephem ephem skyalmanac
  python -m pip install skyalmanac

Installing SkyAlmanac ensures that Ephem, Skyfield and Pandas (and their dependencies) are also installed. If previous versions of Skyalmanac were installed, consider upgrading Skyfield and Pandas::

  python -m pip install --upgrade skyfield pandas

Thereafter run it with::

  python -m skyalmanac

On a POSIX system (Linux or Mac OS), use ``python3`` instead of ``python`` in the commands above.

This PyPI edition also supports installing and running in a `venv <https://docs.python.org/3/library/venv.html>`_ virtual environment.
Finally check or change the settings in *config.py*.
It's location is printed immediately whenever Skyalmanac runs.

Guidelines for Linux & Mac OS
-----------------------------

Quote from `Chris Johnson <https://stackoverflow.com/users/763269/chris-johnson>`_:

It's best to not use the system-provided Python directly. Leave that one alone since the OS can change it in undesired ways.

The best practice is to configure your own Python version(s) and manage them on a per-project basis using ``venv`` (for Python 3). This eliminates all dependency on the system-provided Python version, and also isolates each project from other projects on the machine.

Each project can have a different Python point version if needed, and gets its own site_packages directory so pip-installed libraries can also have different versions by project. This approach is a major problem-avoider.

Troubleshooting
---------------

If using MiKTeX 21 or higher, executing 'option 5' (Increments and Corrections) will probably fail with::

    ! TeX capacity exceeded, sorry [main memory size=3000000].

To resolve this problem (assuming MiKTeX has been installed for all users),
open a Command Prompt as Administrator and enter: ::

    initexmf --admin --edit-config-file=pdflatex

This opens pdflatex.ini in Notepad. Add the following line: ::

    extra_mem_top = 1000000

and save the file. Problem solved. For more details look `here <https://tex.stackexchange.com/questions/438902/how-to-increase-memory-size-for-xelatex-in-miktex/438911#438911>`_.