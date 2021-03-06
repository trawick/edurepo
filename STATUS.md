BASICALLY BROKEN
================

1. XXX

Three worst overall viability issues
====================================

1. XXX
1. lots of improvements needed to "My Edjectives" (see user interface issues below)
1. no complete course to use as good example (easiest fix: add materials to Alabama Grade 5 Science)

Three worst issues in teacher interface
=======================================

1. XXX
2. If no objectives can be found via web lookup, the add-objective-to-calendar form is useless.
3. when adding class, teacher can't see list of course ids based on current API provider; first determine API provider then proceed to form with list of courses by category?

N worst issues in user interface
====================================

1. Ugly; needs to be pretty :)
1. resource upvote/downvote need different views/URLs, and shouldn't let user change the resource
1. resource submission shouldn't let user change the objective
1. Flashcard needs a shuffle feature
1. MyEdjectives lets range of dates be selected; by default, range is previous school day + this school day + next school day
1. objective display needs link to browsing of class
1. objective display needs to show a calendar
1. objective display shows each type of material in its own box
1. Errors or delays fetching asynchronously aren't reported well or at all.  The select boxes under Browse shouln't appear until we have something to select.

Three worst issues for developers
=================================

1. XXX
2. XXX
3. XXX

Three worst issues for deployers
================================

1. master .conf files for non-Ubuntu-httpd deployment not properly maintained
2. deploy with mod\_proxy_*cgi to avoid intersection with httpd dependencies and app dependencies (e.g., OpenSSL version when upgrading front-end web stack)
3. The Ansible deployment script should handle more of the setup steps, possibly with a small script that is run from the initial Ubuntu login.

Possible themes for upcoming stages
===================================

* Import Common Core high school math course definitions
* Course needs short form of description
* Add Spanish version of "I Can" statements (from Sonya), with means of retrieval
* New Django app: Interface for submitting materials for a LO (moves to repo after review/rework by approver)
* XML scheme/validation for repo data

Bugs of interest
================

* resources/fixtures/sample.json is out of date; meanwhile, the resources should be exportable in a share-able format so that, for example, someone can use the course definition files and set of resources for those objectives with some other system
* Follow updates to requests package to see when we can remove workarounds for issue 2192.  (4.0.1 is now available.)
* Follow updates to requests package and Python 2.7.next to see when SNI will be supported and what, if any, needs to change in the edurepo code.
* Teacher forms should validate uniqueness instead of catching it in the view and slipping in an error message (must initialize forms with extra model data that they don't currently have)
* Improve formatting of resource view in Django application
* Minimize data transfer by link validator (e.g., grab just first 4-8K of document)
* websnapr or similar for more previews
* command-line "reference" clients:
  * test these automatically
  * current\_learning\_objectives.py: indicate when the specified class name is invalid
* Testcases for Angular app
* might need ASL in source files
* caching of API calls somewhere
* individual items have ids for reuse with multiple objectives?  I dunno...  seems to imply performance hit, when instead the materials could be reused by some definitional mechanism
* no automated test cases for test clients or AngularJS app
* redirect production http requests to https; too confusing to hit admin over http and get bogus message, and probably want https for other requests anyway
