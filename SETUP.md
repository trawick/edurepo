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
ALLOWED_HOSTS=edjective.org

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

look through httpd config in detail for all the crap

---

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
* manage.py syncdb
* manage.py collectstatic

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
