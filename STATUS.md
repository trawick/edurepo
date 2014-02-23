Current stage (by Feb 24)
=========================

Model fixes, implement demo of traversing a course description (access from author page)

* TODO Teacher class def should have a place for non-default api providers urls
* TODO Materials in repo must be labelled by language (or universal for some).
* TODO Resource model needs date-added field to allow sorting by new[+popular]
* TODO add "I can" model, linked to learning objective
* TODO script to populate teacher and resource db with a few entries
* TODO create demo on curiculum designer page showing traversal of different types of information

Possible themes for upcoming stages
===================================

* XML scheme for course definition
* Model for multiple choice questions (exploit in demo)

Blatant bugs, even obvious at this early stage
==============================================

* need ASL in source files
* web app should cache server lookups for better performance
* individual items have ids for reuse with multiple objectives?  I dunno...  seems to imply performance hit, when the materials could be reused by some definitional mechanism
* no automated test cases, you moron; create course and objectives with fixed strings and go on from there
