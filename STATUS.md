Current stage
=============

Deploy what is working now on edjective.org.

* TODO Split up settings.py following "Two Scoops..." to keep deployment secret key out of source code
* TODO Switch to Postgresql on dev system
* TODO Set up Postgresql on server
* TODO Have settings for API endpoint in webapp
* TODO Have settings for API endpoint in sample clients
* TODO git checkout on server
* TODO Set up SSL on server (self-signed cert is okay)
* TODO Deploy Django app via mod_wsgi; httpd: /admin requires SSL, which in turn requires client auth; everything else is okay but allows only GET/HEAD/OPTIONS, / redirects to /webapp/ for now

Blatant bugs, even obvious at this early stage
==============================================

* web app should cache server lookups for better performance
* resource model needs date-added field to allow sorting by new[+popular]
* no automated test cases, you moron; create course and objectives with fixed strings and go on from there
