Three worst overall viability issues
====================================

1. no end user software (e.g., "My Classes" web app)
2. dedicated, real deployment (dedicated server, SSL certificate, etc.)
3. no complete course to use as good example (add reference materials to Alabama Grade 5 Science)

Three worst issues in teacher interface
=======================================

1. XXX
2. XXX
3. XXX

Three worst issues in demo interface
====================================

1. Demo teacher/class has objectives that don't have any supporting materials in the repository.
2. Ugly; needs to be Bootstrap-ed
3. XXX

Possible themes for upcoming stages
===================================

* Import Common Core high school math course definitions
* Bootstrap-ify Angular app
* Improve user interface for resource browsing and commenting
* Course needs short form of description
* Add Spanish version of "I Can" statements (from Sonya), with means of retrieval
* New Django app: Interface for submitting materials for a LO (moves to repo after review/rework by approver)
* XML scheme/validation for repo data

Bugs of interest
================

* dates in dashboard URLs have different formats than dates in add/remove objective URLs
* Improve formatting of resource view
* Minimize data transfer by link validator (e.g., grab just first 4-8K of document)
* Fix or hide noise from link validator cron job (e.g., invalid characters in some pages)
* edjective.org issue parsing some resources: Upgrade Python or use external HTML parser or just wait until setting up dedicated server with newer Ubuntu release
* websnapr or similar for more previews
* command-line "reference" clients:
  * test these automatically
  * current\_learning\_objectives.py: indicate when the specified class name is invalid
* handle API failures in Angular webapp
* Read "Effective JavaScript", finish Django tutorial, finish Angular tutorial, read tastypie docs :)
* More testcases
* Improve interface for submitting resources for a LO

Blatant bugs, even obvious at this early stage
==============================================

* need ASL in source files
* caching of API calls somewhere
* individual items have ids for reuse with multiple objectives?  I dunno...  seems to imply performance hit, when instead the materials could be reused by some definitional mechanism
* no automated test cases for API, test clients, or AngularJS app, and poor test coverage in general
