Three worst overall viability issues
====================================

1. no end user software (e.g., "My Classes" web app)
   * currently looking at a small script that fetches materials for current objectives and passes it to Anki
2. no complete course to use as good example (easiest fix: add materials to Alabama Grade 5 Science)
3. XXX

Three worst issues in teacher interface
=======================================

0. SSL is used for the API endpoint if a class is added via https (okay); Python 2.x SSL to edjective.org
fails BECAUSE THERE IS NO FREAKING SNI SUPPORT!!!!!!!!!!!  The API endpoint has to be manually edited to
disable SSL.
1. If no objectives can be found via web lookup, the add-objective-to-calendar form is useless.
2. when adding class, teacher can't see list of course ids based on current API provider; first determine API provider then proceed to form with list of courses by category?
3. After adding a class, the teacher is taken back to the main screen.  They should be taken to the dashboard for that class.

Three worst issues in demo interface
====================================

1. Demo teacher/class has objectives that don't have any supporting materials in the repository.
   * currently adding more materials to a few of the objectives in Alabama Grade 5 Science
2. Errors or delays fetching asynchronously aren't reported well or at all.  The select boxes under Browse shouln't appear until we have something to select.
3. Ugly; needs to be Bootstrap-ed

Three worst issues for developers
=================================

1. XXX
2. need VM for testing deployment
3. XXX

Three worst issues for deployers
================================

1. The Ansible deployment script should handle more of the setup process.
2. XXX
3. XXX

Possible themes for upcoming stages
===================================

* Use requests instead of urllib2 for eventual SNI support with 2.7.future
* Import Common Core high school math course definitions
* Bootstrap-ify Angular app
* Improve user interface for resource browsing and commenting
* Course needs short form of description
* Add Spanish version of "I Can" statements (from Sonya), with means of retrieval
* New Django app: Interface for submitting materials for a LO (moves to repo after review/rework by approver)
* XML scheme/validation for repo data

Bugs of interest
================

* Teacher forms should validate uniqueness instead of catching it in the view and slipping in an error message (must initialize forms with extra model data that they don't currently have)
* Improve formatting of resource view
* Minimize data transfer by link validator (e.g., grab just first 4-8K of document)
* Fix or hide noise from link validator cron job (e.g., invalid characters in some pages)
* edjective.org issue parsing some resources: Upgrade Python or use external HTML parser or just wait until setting up dedicated server with newer Ubuntu release
* websnapr or similar for more previews
* command-line "reference" clients:
  * test these automatically
  * current\_learning\_objectives.py: indicate when the specified class name is invalid
* handle API failures in Angular webapp
* Read "Effective JavaScript", finish Django tutorial, finish Angular tutorial, read tastypie docs :)
* Testcases for Angular app
* Improve interface for submitting resources for a LO
* might need ASL in source files
* caching of API calls somewhere
* individual items have ids for reuse with multiple objectives?  I dunno...  seems to imply performance hit, when instead the materials could be reused by some definitional mechanism
* no automated test cases for test clients or AngularJS app
