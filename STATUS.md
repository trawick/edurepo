Current stage (by March 12)
=========================

* Resource submission
  * TODO Glue Resource to LearningObjective
  * TODO Browse categories, then courses, then objectives
  * TODO Submit resource for objective
  * TODO Use user's browser to validate URL
  * TODO Implement server-side script to validate URLs in database
  * TODO websnapr or similar

Possible themes for upcoming stages
===================================

* command-line "reference" clients:
  * test these automatically
  * current\_learning\_objectives.py: indicate when the specified class name is invalid
* @login_required doesn't redirect to the proper URL
* handle API failures in Angular webapp
* Read "Effective JavaScript", finish Django tutorial, finish Angular tutorial, read tastypie docs :)
* Add Spanish version of "I Can" statements (from Sonya), with means of retrieval
* Testcases
* New Django app: Interface for submitting materials for a LO (moves to repo after review/rework by approver)
* Refactor controllers.js
* Improve interface for submitting resources for a LO
* Allow voting up or flagging a resource
* XML scheme/validation for repo data
* should teacher models specify separate base URLs for contributed resources vs. the repo? (TODO parent demo and sample code should use repo provider URL from class model)
  * this is a pain...  forgetting about teachers for a moment, when you submit an external resource to an instance of the resources app it must know what instance of the repo app contains the learning objectives; why not just require that external resources for an objective are necessarily maintained together with the repo, so Resource::objective is ForeignKey and everything is simplified; getting back to teachers, one base API URL stored with the teacher is sufficient for accessing both the repo and submitted external resources

Blatant bugs, even obvious at this early stage
==============================================

* need ASL in source files
* web app should cache server lookups for better performance
* individual items have ids for reuse with multiple objectives?  I dunno...  seems to imply performance hit, when instead the materials could be reused by some definitional mechanism
* no automated test cases, you moron; create course and objectives with fixed strings and go on from there
