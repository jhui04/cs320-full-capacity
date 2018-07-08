fcapp
=====


**In the fcapp folder:** A minimally-working Django environment with mongo plugins.

<!--
To set up:
1. `source /usr/local/bin/virtualenvwrapper.sh`
2. `mkvirtualenv fcapp --python $(which python3)`
3. `pip install -r requirements.txt`
4. `cd fcapp; python manage.py runserver 0.0.0.0:8000`

After initial setup:
1. `source /usr/local/bin/virtualenvwrapper.sh`
2. `workon fcapp`
3. `cd fcapp; python manage.py runserver 0.0.0.0:8000`
-->

Environment Setup:
1. Install VirtualBox -- https://www.virtualbox.org/wiki/Downloads
2. Install Vagrant -- http://vagrantup.com/downloads.html
3. In the `cs320-full-capacity` folder, run `vagrant up`
4. To access the virtualized Linux box, run `vagrant ssh`

After initial setup, run:
1. `vagrant up`
2. `vagrant ssh`
3. `cd /vagrant`
4. `workon fcapp`
5. `cd fcapp`
6. Sync the local database with `python manage.py migrate`
7. To set up the Django admin user: `python manage.py createsuperuser` and create the account 'admin' 'admin'
8. To import the device information to the database: `python manage.py import_json -w -f ../umass-export-full.json`
9. To run the Django server: `python manage.py runserver 0.0.0.0:8080` 
10. Port 8080 will be forwarded to your local machine. To stop the Django server: `Ctrl-C`
11. To view the site, go to `http://localhost:8080` in your browser. This will give a TemplateNotFound page if the Angular stuff is not set up. Run `./frontend/storage-device-analytics/build_for_django.sh` to generate this. To view the API, go to `http://localhost:8080/api/`
11. You need to create a tenant relationship between your new user (admin, user id #1) and a "tenant" in the JSON (for example, "hpe"). So go to `http://localhost:8080/api/tenant/` and, at the bottom, fill out the HTML form with user id `1` and tenant id `hpe` and hit POST. This will mean that, when you're logged in as `admin` the site will know to display devices that are accessible to tenant `hpe`.
13. To log in, go to `http://localhost:8080/`. To log out, `http://localhost:8080/logout` 

To shut down Vagrant:
1. `exit` out of the current SSH session if you are still in it
2. `vagrant suspend`
3. To start the session back up, run `vagrant resume` next time instead of `vagrant up`.

**In the frontend/storage-device-analytics folder:** The Angular frontend application.

To install Angular/node dependencies, run `./angular_setup.sh`

To update the Angular application and have changes reflect in the Django dev server, run `./frontend/storage-device-analytics/build_for_django.sh`

**Tips:**
* Before you `git push`, run `git pull -r` (the `-r` is for 'rebase'), which ensures that merge conflicts/branch merges are minimized.
