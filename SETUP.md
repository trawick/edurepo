Setting up a test or production machine from zero
=================================================

Ubuntu Linux and Ansible are currently required.

You need to be familiar with Linux system administration and Python "virtual environments" in order to install the software.  Most of the necessary steps will be shown explicitly, but you may not be able to identify when an error occurs without any background information.

Initial manual setup
--------------------

### VM

Create an Ubuntu 14.04 Server VM:

* A 32-bit image with 1 CPU and 2GB of RAM is fine.
* Using the user id created during installation, create the user `edurepo` to manage edurepo:
```
$ sudo useradd -m edurepo -s /bin/bash
$ sudo passwd edurepo
Enter new UNIX password:
Retype new UNIX password:
passwd: password updated successfully
```
* Use visudo to add a line like the following to the end of the sudo config:
```
edurepo ALL=(ALL) NOPASSWD: ALL
```
(This allows the user to be able to run commands as `root` or as the Postgresql user without
a password prompt.)
* Enable sshd:
```
$ sudo apt-get install openssh-server
```
* Put your client's public key in the `/home/edurepo/.ssh/authorized_keys` file on the server,
creating `.ssh` (with permissions 0700) or `authorized_keys` (with permissions 0600) as necessary.
Also, ensure that it has the proper ownership:
```
$ sudo chown -R edurepo:edurepo /home/edurepo/.ssh
```
* Log in as user `edurepo` and ssh to github.com to populate the host key:
```
$ ssh github.com
The authenticity of host 'github.com (XXX)' can't be established.
RSA key fingerprint is YYYYY.
Are you sure you want to continue connecting (yes/no)? yes
Warning: Permanently added 'github.com,XXX' (RSA) to the list of known hosts.
Permission denied (publickey).
```
(You'll need to verify Github's RSA key fingerprint (YYYYY above) manually, such as by checking the Github documentation; be sure to use an https connection to minimize the chance of accessing a malicious page.)

### Configuration files

Several configuration files have to be created within a certain directory
structure on the managing system; the top directory in the structure is referred
to as `rootdir` in the following documentation.  This configuration should be
kept out of public repositories as it will contain private information.
(Consider filesystem encryption and appropriate backup strategies.)

#### `rootdir/ansible/hosts`

Refer to the example in `git-edurepo/src/ansible/hosts.sample` for instructions.

The path to this file will be passed to the `ansible-playbook` command when deploying.

#### `rootdir/git-edurepo/src/edurepo/settings.cfg`

Refer to `git-edurepo/src/ansible/settings.cfg.sample` for instructions.  In many cases, only the secret key needs to be set.

#### `rootdir/ubuntu-apache24/edurepo-vhost.conf`

Refer to `git-edurepo/src/ansible/edurepo-vhost.conf.sample` for an example.  In many cases this won't have to be modified.

Automatic setup and deploy
--------------------------

1. Create a virtualenv for running Ansible:

  ```
  $ virtualenv /path/to/env
  $ . /path/to/env/bin/activate
  $ pip install ansible
  ```
2. With that virtualenv activated:

  ```
  $ cd /path/to/git-edurepo/src/ansible
  $ ansible-playbook -i rootdir/ansible/hosts deploy.yml
  ```

Manual creation of Django superuser
-----------------------------------

After running the deploy script, log in to the remote server as user `edurepo` and create a Django superuser:
```
$ cd /home/edurepo/git/edurepo
$ . envs/edurepo/bin/activate
$ cd src/edurepo
$ python manage.py createsuperuser
Username: superman
Email address: superman@example.com
Password:
Password (again):
Superuser created successfully.
```

Setup e-mail address for cron job output
----------------------------------------

Edit the crontab with `crontab -e` and add a line like the following to the top:

```
MAILTO=you@example.com
```

(with a working e-mail address, of course.)

Reports on issues with web resource submissions will be sent to that address.

Archiving data
--------------

A very simple mechanism to dump tables in gzipped, JSON format is provided
in `src/edurepo/backup.sh`.  The deploy script runs this nightly and saves
it to the `backup` folder in the managing user's home directory.  The last
10 backups will be retained in that location, and older backups will be
deleted.  Separate logic must be required for moving the backups off-site.

Archival can be disabled by setting `nightly_archive=no` in the Ansible
inventory file (`hosts`).

This script dumps the tables at the Django layer.  It will be more efficient
to manage this at the database layer.

Developer instructions
======================

The Ansible playbook described under the deployment instructions above covers installation of
required packages so look there for such requirements.

Although a developer setup is much simpler, you can get an overview of what is required by looking at the Ansible playbook for deployment (`src/ansible/deploy.yml`).

Python version
--------------

It has been tested a lot with Python 2.6, but Python 2.7 is currently used.
The `group_writable_file_handler` in `settings.py` might only work with 2.7,
so be careful out there.

Configuration and setup for the Django app
------------------------------------------

### PostgreSQL on Ubuntu:

You likely have your own methodology for PostgreSQL administration, and won't choose to follow the instructions below.  You need to create a database (named in `setup.cfg`) and
create a new PostgreSQL user or use an existing one for use by the Django application.

```
sudo su - postgres
  createdb djangoedurepo
  createuser -P
    ("n" to last three questions)
  psql
    grant all privileges on database djangoedurepo to NEWUSER;
    \q
```

In order to run tests, run this additional command under `psql` so that the test version of the database can be created by the PostgreSQL user:

```
alter user NEWUSER createdb;
```

### settings.cfg

Create settings.cfg for the Django app in the `src/edurepo` directory.  See `settings.cfg.sample` for instructions.

For development, you'll want these particular values:

```
DEBUG=True
TEMPLATE_DEBUG=True
set_static_root=False
```


### Local python environment


```
  cd edurepo (root of git checkout)
  mkdir envs
  virtualenv envs/edurepo
  . envs/edurepo/bin/activate
  cd src
  pip install -r requirements.txt
```


### Configuration and setup of the AngularJS web app

Create the file `src/webapp/resources/config.json` with something like the following
to configure the API endpoint to point to your development server:

```
{"base_api_url" : "http://127.0.0.1:8000/"}
```

You need a web server to serve the files under `/webapp` in a development environment; it is not served by Django's `runserver`.

When picking up software updates
--------------------------------

* pip install -r requirements.txt
* manage.py collectstatic
* manage.py syncdb   OR POSSIBLY starting over with new data (below)

Testing
-------

You'll need to have an API provider live (e.g., run `manage.py runserver` in the background) and point to it with the TEST_PROVIDER environment variable while running tests:

```
export TEST_PROVIDER=http://127.0.0.1:8000/
./manage.py test
```

Various administration hints
============================

When dropping tables
--------------------

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
---------------------------

**If this is a production server, you probably don't want to do this.  First
consider what you need to save and restore.**

```
python manage.py sqlclear teachers resources repo | python manage.py dbshell
python manage.py syncdb
python repo/import_xml.py ../../samples/ import
(edit teachers/fixtures/sample.json to fix URL)
python manage.py loaddata teachers/fixtures/sample.json
python manage.py loaddata resources/fixtures/sample.json
```

### Or with the Ansible deploy playbook

Run these commands from the `git/edurepo/src/edurepo` directory before running
he deploy playbook:

```
python manage.py sqlclear teachers resources repo | python manage.py dbshell
rm ../../data-imported
```

(The `data-imported` file is the flag that indicates that data needs to be
reloaded.)

Adding a single course
----------------------

In this example, NC-HSM-III is imported:

```
python repo/import_xml.py ../../samples/M/NC-HSM-III.xml check
python repo/import_xml.py ../../samples/M/NC-HSM-III.xml import
```

Removing a single course
------------------------

```
python repo/remove.py COURSE-ID check
python repo/delete.py COURSE-ID delete
```

This will display any objectives that will be removed, but it will also remove related I-Can statements, glossary items, and anything else in the repository.

Fixing the admin password
-------------------------

```
./manage.py changepassword <admin-user-id>
```

Dumping current data
--------------------

```
./manage.py dumpdata --indent=4 > ~/edurepo-2014-MM-DD.json
```

Saving and restoring data for a single app
------------------------------------------

```
python manage.py dumpdata --indent 2 resource > ~/edurepo-resource-2014-xx-yy.json
```


Fixing PostgreSQL user password
-------------------------------

```
$ sudo -u postgres psql postgres
psql (9.1.13)
Type "help" for help.

postgres=# ALTER USER djangoedurepo PASSWORD 'NewPassword';
ALTER ROLE
postgres=# \q
$
```

