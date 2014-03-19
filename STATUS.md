Current stage (by March 20)
===========================

* DONE Teacher defines a class they are teaching
* TODO unit tests for new code
* TODO set up on edjective.org
* TODO save/restore code

Possible themes for upcoming stages
===================================

* Navigation for Django views/forms showing login status
* Teacher maintains the learning objective calendar for a class
* Improve user interface for resource browsing and commenting
* Course needs short form of description
* Add Spanish version of "I Can" statements (from Sonya), with means of retrieval
* New Django app: Interface for submitting materials for a LO (moves to repo after review/rework by approver)
* XML scheme/validation for repo data

Bugs of interest
================

* Minimize data transfer by link validator (e.g., grab just first 4-8K of document)
* edjective.org issue parsing some resources: Upgrade Python or use external HTML parser or just wait until setting up dedicated server with newer Ubuntu release
* websnapr or similar for more previews
* command-line "reference" clients:
  * test these automatically
  * current\_learning\_objectives.py: indicate when the specified class name is invalid
* handle API failures in Angular webapp
* Read "Effective JavaScript", finish Django tutorial, finish Angular tutorial, read tastypie docs :)
* More testcases
* Refactor controllers.js
* Improve interface for submitting resources for a LO

Blatant bugs, even obvious at this early stage
==============================================

* need ASL in source files
* caching of API calls somewhere
* individual items have ids for reuse with multiple objectives?  I dunno...  seems to imply performance hit, when instead the materials could be reused by some definitional mechanism
* no automated test cases for API, test clients, or AngularJS app, and poor test coverage in general
