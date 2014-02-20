Current stage (by Feb 21)
=========================

Better demo webapp...

* TODO small image as replacement for "Front page" link
* TODO get Ksenija to choose better colors for bars on front page
* TODO clean up and simplify text everywhere
* TODO on parent demo, load resources for current learning objective
* TODO on parent demo, load sample problems for current learning objective
* TODO create demo on curiculum designer page showing traversal of different types of information
* TODO fix overlap of text on small screen
* TODO find out why text color isn't black

Possible themes for upcoming stages
===================================

* add "I can" model, linked to learning objective, then add demo of traversing a course description to the curiculum page


Blatant bugs, even obvious at this early stage
==============================================

* need ASL in source files
* web app should cache server lookups for better performance
* resource model needs date-added field to allow sorting by new[+popular]
* individual items have ids for reuse with multiple objectives?  I dunno...  seems to imply performance hit, when the materials could be reused by some definitional mechanism
* no automated test cases, you moron; create course and objectives with fixed strings and go on from there
