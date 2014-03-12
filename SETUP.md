Configuration and setup for the Django app
==========================================

PostgreSQL on Ubuntu:


```
sudo apt-get install postgresql libpq-dev
sudo su - postgres
  createdb djangoedurepo
  createuser -P
    ("n" to last three questions)
  psql
    grant all privileges on database djangoedurepo to NEWUSER;
    \q
```

In order to run tests, run this additional command under psql so that the test version of the database can be created by the PostgreSQL user:

```
alter user NEWUSER createdb;
```


Create settings.cfg for Django app in src/edurepo directory

```
# generate a new secret:
#   >>> from django.utils.crypto import get_random_string
#   >>> chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
#   >>> get_random_string(50, chars)

[secret]
key=    (whatever)

[debugging]
# should be True or False
DEBUG=False
TEMPLATE_DEBUG=False

[deployment]
# should be comma-delimited list of acceptable hostnames
ALLOWED_HOSTS=*
set_static_root=True
# set this to location where /static from Django app will be copied
STATIC_ROOT=/home/whatever/edurepo-static/
# set this to location where Django app is mounted (blank for /)
MOUNTED_AT=

[database]
NAME=djangoedurepo
USER=   (whatever)
PASSWORD=   (whatever)
```

Python environment:

System python: 

```
  sudo apt-get install python-pip
  sudo pip install virtualenv
```

Local python environment:

```
  cd edurepo (root of git checkout)
  mkdir envs
  virtualenv envs/edurepo
  . envs/edurepo/bin/activate
  cd src
  pip install -r requirements.txt
```

---

bunch of crap with /home/trawick/edurepo-static and django command to put stuff there

* python manage.py collectstatic

httpd.conf
==========

```
WSGIDaemonProcess edurepo \
    home=/home/trawick/git/edurepo/src/edurepo \
    python-path=/home/trawick/git/edurepo/src/edurepo:/home/trawick/git/edurepo/envs/edurepo/lib/python2.6/site-packages

<VirtualHost *:80>
  WSGIProcessGroup edurepo
  include conf/conf.d/foo.include
</VirtualHost>

<VirtualHost *:443>
  WSGIProcessGroup edurepo
  (SSL configuration)
  include conf/conf.d/foo.include
</VirtualHost>
```

foo.include
===========

```
# included in SSL and non-SSL vhosts

ErrorLog logs/edjective.org.errors
LogLevel info

ServerName edjective.org
DocumentRoot /home/trawick/git/edurepo/src/webapp/

<Directory />
    Require all denied
    AllowOverride None
</Directory>

<Directory /home/trawick/git/edurepo/src/webapp/>
    Options Indexes FollowSymlinks
    AllowOverride None
    Require all granted
</Directory>

WSGIScriptAlias /ed/ /home/trawick/git/edurepo/src/edurepo/edurepo/wsgi.py/

Alias /static/ /home/trawick/edurepo-static/

<Directory /home/trawick/git/edurepo/src/edurepo>
    <Files wsgi.py>
        Require all granted
    </Files>
</Directory>

<Location /ed/admin/>
    Require ssl
</Location>

<Directory /home/trawick/edurepo-static>
    Require all granted
</Directory>
```

Configuration and setup of the AngularJS web app
================================================

Create file src/webapp/resources/config.json with something like the following
to configure the API endpoint:

```
{"base_api_url" : "http://edjective.org/ed/"}
```

On a development system, the setting would typically be:

```
{"base_api_url" : "http://127.0.0.1:8000/"}
```

Angular for webapp:

```
cd edurepo/src/webapp/
mkdir lib
cd lib
unzip /path/to/angular-1.2.13.zip
ln -s angular-1.2.13 angular
```

Bootstrap for webapp:

```
cd /scratch
unzip /path/to/bootstrap.zip (2.3.2)
cd bootstrap/css
cp bootstrap* /path/to/edurepo/src/webapp/css/
```

When picking up software updates
================================

* Restart httpd
* pip install -r requirements.txt
* manage.py collectstatic
* manage.py syncdb   OR POSSIBLY starting over with new data (below)

When dropping tables
====================

E.g., table south_migrationhistory...

```
sudo su - postgres
psql
\c djangoedurepo
drop table south_migrationhistory;
DROP TABLE
djangoedurepo=# \q
```

Starting over with new data
===========================

**Yo!  Save teachers and resources data first!**

```
python manage.py sqlclear teachers resources repo | python manage.py dbshell
python manage.py syncdb
python repo/import.py ../../samples/ import
(edit teachers/fixtures/sample.json to fix URL)
python manage.py loaddata teachers/fixtures/sample.json
python manage.py loaddata resources/fixtures/sample.json
```
