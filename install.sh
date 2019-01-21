#!/bin/bash

if [ -f /etc/debian_version ]
then
    path="/usr/lib/python3/dist-packages/ispcli"
    apt install pip3-python -y
    pip install BeautifulTable
else
    path="/usr/lib/python3.6/site-packages/ispcli"
    yum install -y python36
    yum install -y python36-setuptools
    mkdir -P /usr/local/lib/python3.6/site-packages
    easy_install-3.6 pip
    pip install BeautifulTable
fi

mkdir /etc/ispcli

if [ -f /etc/ispcli/ispcli.conf ]
then
echo "Create backup for ispcli.conf"
cp /etc/ispcli/ispcli.conf  /etc/ispcli/ispcli.conf.back
fi
echo -y | cp ispcli.conf /etc/ispcli/

chmod 500 /etc/ispcli
chmod 500 /etc/ispcli/ispcli

cp ispcli.py /usr/sbin/ispcli 
chmod 500 /usr/sbin/ispcli
mkdir  $path
echo y | cp ispcli/help_text.py $path
echo y | cp ispcli/ispmanagerclass.py $path
echo y | cp ispcli/menu.py $path
echo y | cp  ispcli/main.py $path
echo y | cp ispcli/__init__.py $path

echo "Success!"
exit 0
