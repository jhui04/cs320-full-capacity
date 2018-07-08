#!/bin/bash
set -e

echo Starting Vagrant provision script as `whoami`


echo cd to /vagrant...
cd /vagrant

echo Installing packages...

apt-get update
apt-get install -y python3-pip virtualenv virtualenvwrapper mongodb

echo Enabling mongodb
systemctl enable mongodb
systemctl start mongodb

echo Setting up virtualenv

sudo -i -u vagrant bash -c "
	cd /vagrant &&
	source /usr/share/virtualenvwrapper/virtualenvwrapper.sh &&
	mkvirtualenv fcapp --python=$(which python3) &&
	workon fcapp &&
	pip install -r requirements.txt &&
	chmod +x ./angular_setup.sh &&
	dos2unix ./angular_setup.sh &&
	./angular_setup.sh
"

echo ====================================
echo Vagrant should be provisioned.
echo Reconnect to the Vagrant machine with:
echo 
echo vagrant ssh
echo 
echo Then, once inside the virtual machine, in order
echo to get into the virtualenv you need to run:
echo 
echo cd /vagrant
echo workon fcapp
echo 
echo to be placed in the virtualenv.
echo To run the Django server, then run:
echo 
echo cd fcapp
echo python ./manage.py runserver 0.0.0.0:8080
echo
echo ====================================
