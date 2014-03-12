Current stage (by March 12)
=========================

* Resource submission
  * DONE Glue Resource to LearningObjective
  * DONE Browse categories, then courses, then objectives
  * DONE Submit resource for objective
  * TODO Create ResourceSubmission records as appropriate
  * TODO Use user's browser to validate URL
    * Is this really practical?
  * TODO Implement server-side script to validate URLs in database
    * Use table for URL verification/ban with last-verified date?
    * Same URL could be used for multiple objectives and/or courses
  * TODO websnapr or similar
    * Have preview for YouTube videos now, but it needs to be fixed to correctly choose http/https...
    * At least grab title, possibly store in URL verification table

Possible themes for upcoming stages
===================================

* Implement resource upvoting/flagging
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
* web app should cache server lookups for better performance
* individual items have ids for reuse with multiple objectives?  I dunno...  seems to imply performance hit, when instead the materials could be reused by some definitional mechanism
* no automated test cases, you moron; create course and objectives with fixed strings and go on from there
