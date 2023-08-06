..
    :copyright: Copyright (c) 2013 Martin Pengelly-Phillips
    :license: See LICENSE.txt.

.. _release/migration:

***************
Migration notes
***************

This section will show more detailed information when relevant for switching to
a new version, such as when upgrading involves backwards incompatibilities.

.. _release/migration/2.0.0:

Migrating to 2.0.0
==================

From 2.0.0, Clique will only support Python 3. Earlier versions of Clique will
continue to work in Python 2, but will not receive any additional updates or
fixes.

As part of the move to Python 3, :ref:`patterns <assembly/patterns>` should be
specified as *raw strings* (prefixed with ``r``) to avoid warnings from Python
about invalid escape sequences. For example::

    >>> pattern = '\d'
    <stdin>:1: DeprecationWarning: invalid escape sequence \d
    >>> pattern = r'\d'

