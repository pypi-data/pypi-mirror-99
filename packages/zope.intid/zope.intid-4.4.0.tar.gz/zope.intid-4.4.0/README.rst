================
 ``zope.intid``
================

.. image:: https://img.shields.io/pypi/v/zope.intid.svg
        :target: https://pypi.org/project/zope.intid/
        :alt: Latest release

.. image:: https://img.shields.io/pypi/pyversions/zope.intid.svg
        :target: https://pypi.org/project/zope.intid/
        :alt: Supported Python versions

.. image:: https://travis-ci.com/zopefoundation/zope.intid.svg?branch=master
        :target: https://travis-ci.com/zopefoundation/zope.intid

.. image:: https://readthedocs.org/projects/zopeintid/badge/?version=latest
         :target: http://zopeintid.readthedocs.io/en/latest/?badge=latest
         :alt: Documentation Status

.. image:: https://coveralls.io/repos/github/zopefoundation/zope.intid/badge.svg?branch=master
        :target: https://coveralls.io/github/zopefoundation/zope.intid?branch=master
        :alt: Code Coverage


This package provides an API to create integer ids for any object. Later
objects can be looked up by their id as well. This functionality is commonly
used in situations where dealing with objects is undesirable, such as in
search indices or any code that needs an easy hash of an object.

Documentation is hosted at http://zopeintid.readthedocs.io
