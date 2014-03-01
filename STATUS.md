Current stage (by Feb/March ??)
=========================

* ??

Possible themes for upcoming stages
===================================

* Read "Effective JavaScript", finish Django tutorial, finish Angular tutorial, read tastypie docs :)
* Add Spanish version of "I Can" statements (from Sonya), with means of retrieval
* Testcases
* New Django app: Interface for submitting materials for a LO (moves to repo after review/rework by approver)
* Refactor controllers.js
* Interface for submitting resources for a LO as well as voting up or flagging
* XML scheme/validation for repo data
* should teacher models specify separate base URLs for contributed resources vs. the repo? (TODO parent demo and sample code should use repo provider URL from class model)

Blatant bugs, even obvious at this early stage
==============================================

* need ASL in source files
* web app should cache server lookups for better performance
* individual items have ids for reuse with multiple objectives?  I dunno...  seems to imply performance hit, when instead the materials could be reused by some definitional mechanism
* no automated test cases, you moron; create course and objectives with fixed strings and go on from there
