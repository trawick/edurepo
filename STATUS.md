Current stage (by Feb 26)
=========================

Easy odds and ends:

* DONE Add "Reference View" and "Quick and Dirty Demonstration" tags to different screens where appropriate to rationalize the ugliness.
* TODO Resource model: need inappropriate-flag-counter field and exploitation in clients
* DONE Customize Django admin for easier use
* DONE ~~Create~~ Improve reference views of repo data

Possible themes for upcoming stages
===================================

* Read "Effective JavaScript", finish Django tutorial, finish Angular tutorial, read tastypie docs :)
* Add Spanish version of some "I Can" statements or other materials, with means of retrieval
* Testcases
* Get Sonya to translate "I Can" statements into Spanish; support language preference on API
* New Django app: Interface for submitting materials for a LO (moves to repo after review/rework by approver) (needs social sign-in)
* Refactor controllers.js
* Social sign-in for submitting/voting/flagging resources
* Interface for submitting resources for a LO (needs social sign-in)
* Resource model: need creator id field (needs social sign-in)
* XML scheme/validation for repo data
* should teacher models specify separate base URLs for contributed resources vs. the repo? (TODO parent demo and sample code should use repo provider URL from class model)

Blatant bugs, even obvious at this early stage
==============================================

* need ASL in source files
* web app should cache server lookups for better performance
* individual items have ids for reuse with multiple objectives?  I dunno...  seems to imply performance hit, when instead the materials could be reused by some definitional mechanism
* no automated test cases, you moron; create course and objectives with fixed strings and go on from there
