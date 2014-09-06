Python version
==============

It has been tested a lot with Python 2.6, but Python 2.7 is currently used.
The `group_writable_file_handler` in `settings.py` might only work with 2.7,
so be careful out there.

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
ALLOWED\_HOSTS=*
set_static_root=True
# set this to location where /static from Django app will be copied
STATIC_ROOT=/home/whatever/edurepo-static/
# set this to location where Django app is mounted (blank for /)
MOUNTED_AT=

[database]
NAME=djangoedurepo
USER=   (whatever)
PASSWORD=   (whatever)

[logging]
DIRECTORY=/path/where/Django-logs-are-created
GLOBAL_LEVEL=INFO
```

Python environment:

System python: 

```
  sudo apt-get install python-pip
  sudo pip install virtualenv
```

Local python environment:

(This is handled by the Ansible deploy script.)

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

(This is handled by the Ansible deploy script.)

```
python manage.py collectstatic
```

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
    Options FollowSymlinks
    Require all denied
    AllowOverride None
</Directory>

<Directory /home/trawick/git/edurepo/src/webapp/>
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

(These steps are handled by the Ansible deploy script.)

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
python repo/import_xml.py ../../samples/ import
(edit teachers/fixtures/sample.json to fix URL)
python manage.py loaddata teachers/fixtures/sample.json
python manage.py loaddata resources/fixtures/sample.json
```

Adding a single course
======================

In this example, NC-HSM-III is imported:

```
python repo/import_xml.py ../../samples/M/NC-HSM-III.xml check
python repo/import_xml.py ../../samples/M/NC-HSM-III.xml import
```

Removing a single course
========================
```
python repo/remove.py COURSE-ID check
python repo/delete.py COURSE-ID delete
```

This will display any objectives that will be removed, but it will also remove related I-Can statements, glossary items, and anything else in the repository.

Fixing the admin password
=========================

```
./manage.py changepassword <admin-user-id>
```

Dumping current data
====================

```
./manage.py dumpdata --indent=4 > ~/edurepo-2014-MM-DD.json
```

Testing
=======

```
./manage.py test
```

Of course.  But that won't test everything, as we need to have an API provider live and set the API endpoint with the TEST\_PROVIDER environment variable.  First run the normal Django application then run tests like this:

```
export TEST_PROVIDER=http://127.0.0.1:8000/
./manage.py test
```

Fixing PostgreSQL user password
===============================
```
$ sudo -u postgres psql postgres
psql (9.1.13)
Type "help" for help.

postgres=# ALTER USER djangoedurepo PASSWORD 'NewPassword';
ALTER ROLE
postgres=# \q
$
```

Setting up a log directory
==========================

Create a directory somewhere to store Django logs, such as /var/log/django-edurepo.

Create a group with the managing user AND the daemon user in it.  (The daemon user
will be the normal log writer; the managing user may run commands interactively
or via cron, which need to write to the log directory.)

```
# usermod -a -G LOGGING-GROUP DAEMON-USER
# usermod -a -G LOGGING-GROUP MANAGING_USER
```

Deploying with Ansible
======================

Currently the playbook itself must be customized.  For support of deploying on machines with differing requirements, the differences need to be extracted.

After activating a `virtualenv` with Ansible installed:

```
$ cd src/ansible
$ ansible-playbook deploy.yml -i inventory
```

Check `deploy.yml` for details.  In particular, note the overlay directory that must be created manually, and which corresponds to the manual steps described above which create files in the edurepo checkout.

Starting from zero
==================

Initial manual setup
--------------------

Create an Ubuntu 14.04 Server VM:

* A 32-bit image with 1 CPU and 2GB of RAM is fine.
* Create a user to manage edurepo.  This will be referred to as "managing-user" in subsequent
instructions.
* Use visudo to add a line like the following to the end of the sudo config:
```
managing-user ALL=(ALL) NOPASSWD: ALL
```
(The user must be able to run commands as root or as the Postgresql user without a password prompt.)
* Enable sshd:
```
sudo apt-get install openssh-server
```
* Put your client's public key in the `/home/managing-user/.ssh/authorized_keys` file on the server,
creating `.ssh` (with permissions 0700) or `authorized_keys` (with permissions 0600) as necessary.
* ssh from the system to github.com to populate the host key (or git checkout from playbook will fail)

Automatic setup and deploy
--------------------------

1. Look at the Ansible inventory file in `src/ansible/hosts_sample` and create a version for your system.
2. Create a virtualenv for running Ansible (`virtualenv /path/to/env` followed by `pip install ansible`).
3. With that virtualenv activated:
```
$ ansible-playbook -i /path/to/hosts deploy.yml
```

Manual creation of Django superuser
-----------------------------------

After running the deploy script, log in to the remove server and create a Django superuser:
```
$ cd /home/managing-user/git/edurepo
$ . envs/edurepo/bin/activate
$ cd src/edurepo
$ python manage.py createsuperuser
Username: superman
Email address: superman@example.com
Password:
Password (again):
Superuser created successfully.
```
