Current stage
=============

Deploy what is working now on edjective.org.

* DONE Split up settings.py following "Two Scoops..." to keep deployment secret key out of source code (did it differently!)
* DONE Switch to Postgresql on dev system
* DONE Set up Postgresql on server
* DONE Have settings for API endpoint in webapp
* DONE Have settings for API endpoint in sample clients
* DONE git checkout on server
* DONE Set up SSL on server (self-signed cert is okay)
* DONE Deploy Django app via mod_wsgi; httpd: /admin requires SSL, which in turn requires client auth; everything else is okay but allows only GET/HEAD/OPTIONS, / redirects to /webapp/ for now

Blatant bugs, even obvious at this early stage
==============================================

* need ASL in source files
* web app should cache server lookups for better performance
* resource model needs date-added field to allow sorting by new[+popular]
* individual items have ids for reuse with multiple objectives?  I dunno...  seems to imply performance hit, when the materials could be reused by some definitional mechanism
* no automated test cases, you moron; create course and objectives with fixed strings and go on from there
