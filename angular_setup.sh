cd /vagrant/frontend/storage-device-analytics
touch package-lock.json
rm package-lock.json
mkdir -p node_modules/foo
rm -rf node_modules
cp -r /vagrant/frontend/storage-device-analytics /tmp/
cd /tmp/storage-device-analytics
curl -sL https://deb.nodesource.com/setup_8.x | sudo -E bash -
sudo apt-get install -y nodejs

sudo npm install --no-bin-links
cp -r /tmp/storage-device-analytics /vagrant/frontend