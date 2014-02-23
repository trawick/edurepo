Current stage (by Feb 24)
=========================

Model fixes, implement demo of traversing a course description (access from author page)

* DONE Teacher class def should have a place for non-default api providers urls
* DONE Materials in repo have optional language label
* DONE script to populate teacher and resource db with a few entries
* DONE Resource model needs date-added field to allow sorting by new[+popular]
* DONE add "I can" model, linked to learning objective
* DONE courses in samples provide "I Can" statements
* TODO Parent demo finds applicable "I can" statements.
* TODO create demo on curriculum designer page showing traversal of different types of information
* TODO parent demo and sample code should use repo provider URL from class model

Possible themes for upcoming stages
===================================

* Customize Django admin for easier use
* Create reference views of repo data
* XML scheme/validation for repo data
* Model for multiple choice questions (exploit in demo)
* Add Spanish version of some "I Can" statements or other materials, with means of retrieval

Blatant bugs, even obvious at this early stage
==============================================

* need ASL in source files
* web app should cache server lookups for better performance
* individual items have ids for reuse with multiple objectives?  I dunno...  seems to imply performance hit, when the materials could be reused by some definitional mechanism
* no automated test cases, you moron; create course and objectives with fixed strings and go on from there
