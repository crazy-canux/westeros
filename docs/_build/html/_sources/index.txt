.. westeros documentation master file, created by
   sphinx-quickstart on Thu Nov  3 00:47:47 2016.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

========
westeros
========

Test Automation build with robot framework and unittest.

=====
Usage
=====

Use source code::

    $ git clone https://github.com/crazy-canux/westeros.git
    $ cd westeros
    $ python setup.py install

==============
The User Guide
==============

Create the AUC for the business::

    $ cd westeros/auc
    $ mkdir <auc-category-name>
    $ cd <auc-category-name>
    $ vim manager.py
    $ mkdir <auc-sub-name>
    $ cd <auc-sub-name>
    $ vim auc.py

Create the KEYWORDS for workflows::

    $ cd westeros/keywords
    $ vim <keywords_category>_workflow.py

Create workflow in robot file::

    $ cd westeros/examples
    $ vim westeros.robot

Modify configuration for workflow::

    $ cd westeros/etc
    $ vim global.yaml
    $ vim shared.yaml



.. toctree::
   :maxdepth: 2


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

