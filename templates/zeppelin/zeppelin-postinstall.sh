#!/bin/bash
set -ex

wget http://mirror.klaus-uwe.me/apache/zeppelin/zeppelin-0.7.3/zeppelin-0.7.3-bin-all.tgz
tar -xzf zeppelin-0.7.3-bin-all.tgz
rm zeppelin*.tgz
mv zeppelin*/ zeppelin
mv zeppelin/conf/zeppelin-env.sh.template zeppelin/conf/zeppelin-env.sh
echo 'export SPARK_HOME="/opt/spark"' >> zeppelin/conf/zeppelin-env.sh

sudo mv zeppelin /opt/zeppelin
sudo chown -R linux:linux /opt/zeppelin
sudo cp zeppelin.service /usr/lib/systemd/system/
sudo htpasswd -c /etc/nginx/htpasswd zeppelin
sudo systemctl start zeppelin
sudo systemctl enable zeppelin
