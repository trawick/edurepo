Current stage (by March 13)
=========================

* DONE Get server-side script running at intervals on edjective.org with reporting going somewhere useful
* DONE Fix redirect issue with http://www.livescience.com/22367-digestive-system.html
* TODO Purge resources that have not been retrievable for a while
* TODO Annotate resource display in browse app with hints from ResourceVerification table, such as title, link status, and hints based on content-type
* TODO Put notice on resource submission form that resources can be removed later based on availability and appropriateness

Possible themes for upcoming stages
===================================

* Minimize data transfer by link validator (e.g., grab just first 4-8K of document)
* edjective.org issue parsing some resources: Upgrade Python or use external HTML parser or just wait until setting up dedicated server with newer Ubuntu release
* Implement resource upvoting/flagging
* websnapr or similar for more previews
* Course needs short form of description
* command-line "reference" clients:
  * test these automatically
  * current\_learning\_objectives.py: indicate when the specified class name is invalid
* handle API failures in Angular webapp
* Read "Effective JavaScript", finish Django tutorial, finish Angular tutorial, read tastypie docs :)
* Add Spanish version of "I Can" statements (from Sonya), with means of retrieval
* More testcases
* New Django app: Interface for submitting materials for a LO (moves to repo after review/rework by approver)
* Refactor controllers.js
* Improve interface for submitting resources for a LO
* Allow voting up or flagging a resource
* XML scheme/validation for repo data

Blatant bugs, even obvious at this early stage
==============================================

* need ASL in source files
* caching of API calls somewhere
* individual items have ids for reuse with multiple objectives?  I dunno...  seems to imply performance hit, when instead the materials could be reused by some definitional mechanism
* no automated test cases for API, test clients, or AngularJS app, and poor test coverage in general
