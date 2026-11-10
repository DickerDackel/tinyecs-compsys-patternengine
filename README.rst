tinyecs-compsys-patternengine
=============================

These are components and systems for tinyecs together with the `patternengine`_.

.. _patternengine: https://github.com/dickerdackel/patternengine/

Synopsis
--------

This package relies on registered component IDs from ``tinyecs-compsys-base``.
It should not be used standalone, but instead be automatically detected and
registered with the top level ``tinyecs.compsys`` package.

.. code:: python

   import tinyecs.compsys as cs

   cs.register()

Usage
-----

Start with the `tinyecs docs`_, followed by the `patternengine docs`_

.. _tinyecs docs: https://tinyecs.readthedocs.io/en/latest/
.. _patternengine docs: https://patternengine.readthedocs.io/en/latest/

Then check the API docs.

Installation
------------

It's up to you, if you install the currently provided ``compsys`` packages from
``tinyecs`` by using

.. code:: console

   pip install tinyecs[base,patternengine]

or include them by adding specific dependencies:

.. code:: console

   pip install tinyecs
   pip install tinyecs-compsys
   pip install tinyecs-compsys-patternengine

Support / Contributing
----------------------

Issues can be opened on `github issues`_

.. _github issues: https://github.com/dickerdackel/tinyecs-compsys-patternengine/issues


License
-------

This software is provided under the MIT license.

See LICENSE file for details.
