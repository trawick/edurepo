Three worst overall viability issues
====================================

1. no end user software (e.g., "My Classes" web app)
2. no complete course to use as good example (easiest fix: add materials to Alabama Grade 5 Science)
3. XXX

Three worst issues in teacher interface
=======================================

1. XXX
2. If no objectives can be found via web lookup, the add-objective-to-calendar form is useless.
3. when adding class, teacher can't see list of course ids based on current API provider; first determine API provider then proceed to form with list of courses by category?

Three worst issues in demo interface
====================================

1. Demo teacher/class has objectives that don't have any supporting materials in the repository.
   * currently adding more materials to a few of the objectives in Alabama Grade 5 Science
2. Errors or delays fetching asynchronously aren't reported well or at all.  The select boxes under Browse shouln't appear until we have something to select.
3. Ugly; needs to be Bootstrap-ed

Three worst issues for end users
================================

1. no end upser application ("My Edjectives")
2. Flashcards should indicate the type of question (e.g., "True or false?")
3. XXX

Three worst issues for developers
=================================

1. XXX
2. need model migration support (instead of using South, upgrade Django to 1.7)
3. XXX

Three worst issues for deployers
================================

1. Angular and Bootstrap are now loaded from CDN; zap from instructions/deployment scripts.
2. The Ansible inventory should be used to fill in template versions of the several required configuration files.
3. The Ansible deployment script should handle more of the setup steps, possibly with a small script that is run from the initial Ubuntu login.
4. Run pretend_teacher.sh immediately (instead of waiting for cron job) so that the demo works immediately.

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

* Follow updates to requests package to see when we can remove workarounds for issue 2192.
* Follow updates to requests package and Python 2.7.next to see when SNI will be supported and what, if any, needs to change in the edurepo code.
* Teacher forms should validate uniqueness instead of catching it in the view and slipping in an error message (must initialize forms with extra model data that they don't currently have)
* Improve formatting of resource view
* Minimize data transfer by link validator (e.g., grab just first 4-8K of document)
* Fix or hide noise from link validator cron job (e.g., invalid characters in some pages)
* edjective.org issue parsing some resources: Upgrade Python or use external HTML parser or just wait until setting up dedicated server with newer Ubuntu release
* websnapr or similar for more previews
* command-line "reference" clients:
  * test these automatically
  * current\_learning\_objectives.py: indicate when the specified class name is invalid
* Testcases for Angular app
* Improve interface for submitting resources for a LO
* might need ASL in source files
* caching of API calls somewhere
* individual items have ids for reuse with multiple objectives?  I dunno...  seems to imply performance hit, when instead the materials could be reused by some definitional mechanism
* no automated test cases for test clients or AngularJS app
