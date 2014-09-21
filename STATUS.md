Three worst overall viability issues
====================================

1. lots of improvements needed to "My Edjectives"
2. no complete course to use as good example (easiest fix: add materials to Alabama Grade 5 Science)
3. XXX

Three worst issues in teacher interface
=======================================

1. XXX
2. If no objectives can be found via web lookup, the add-objective-to-calendar form is useless.
3. when adding class, teacher can't see list of course ids based on current API provider; first determine API provider then proceed to form with list of courses by category?

N worst issues in user interface
====================================


2. Errors or delays fetching asynchronously aren't reported well or at all.  The select boxes under Browse shouln't appear until we have something to select.
3. Ugly; needs to be Bootstrap-ed
3. Flashcard needs a shuffle feature
4. objective display needs nicer buttons
6. objective display needs to show a calendar
7. objective display shouldn't show same objective multiple times (if on calendar for multiple days)
8. objective display needs show/hide for different types of materials
9. objective display needs link to browsing of class
10. MyEdjectives shows objectives in order by date
11. objective display shows each type of material in its own box
12. MyEdjectives shows each objective in its own box
13. MyEdjectives lets range of dates be selected; by default, range is previous school day + this school day + next school day
14. refresh on flashcard screen should take you to somewhere meaningful

Three worst issues for developers
=================================

1. XXX
2. need model migration support (instead of using South, upgrade Django to 1.7)
3. XXX

Three worst issues for deployers
================================

1. XXX
2. XXX
3. The Ansible deployment script should handle more of the setup steps, possibly with a small script that is run from the initial Ubuntu login.

Possible themes for upcoming stages
===================================

* Import Common Core high school math course definitions
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
