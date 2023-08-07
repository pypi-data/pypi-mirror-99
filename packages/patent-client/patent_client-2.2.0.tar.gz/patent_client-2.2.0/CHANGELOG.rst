
Changelog
=========

2.1.3 (2020-11-12)
------------------
* Added support for USPTO's Full Text databases
* Added corresponding documentation

2.1.0 (2021-03-23)
------------------
* Add support for document downloads from the USPTO PEDS interface
* Fix flakey tests
* Update dependencies

2.0.3 (2020-10-14)
------------------
* Merge pull request ensuring that INPADOC produces consistent typing (PR #37)
* Update dev dependencies in Pipfile

2.0.2 (2020-04-13)
------------------
* Added foreign priority support back to PEDS API
* Revised and simplified documentation to match v.2, including using Sphinx Autodoc
* Added doctest support to documentation to confirm examples still work
* Added docstrings throughout
* Labeled some broken things as broken

2.0.1 (2020-03-12)
------------------
* Fixed problem where Inpadoc was indexing improperly

2.0.0 (2020-03-11)
------------------
* Major update with breaking API changes
* Refactored all API's to use requests_cache rather than custom caching scheme
* Uses Marshmallow for data validation, and memory-efficient dataclasses for all objects
* As part of the above, all API's now re-use the same requests.Session() object
* Deleted a ton of unnecessary code (Deleted code == debugged code)
* NOTE: Documentation not yet up-to-date. That is the next project

0.4.0 (2019-01-30)
------------------
* Renewed commitment to adhere to semantic versioning
* Added several new synthetic data attributes, including expiration date calculations
* General updates and improvements, including an overhaul of the base Manager and Model classes

0.2.3 (2018-11-02)
------------------
* Added parser for Inpadoc claims so they have an object repesentation

0.1.5 (2018-10-25)
------------------
* Massive refactor of OPS client

0.1.4 (2018-10-24)
------------------
* Support for USPTO Applications, Assignments, and PTAB documents
* Support for EPO Inpadoc and EPO Register
* Initial Installation and Getting Started Documentation

0.0.1 (2018-10-15)
------------------

* First release on PyPI.
* Support for EPO OPS (except Classification data)
