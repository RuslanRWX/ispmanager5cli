#!/bin/bash

lib_path="/usr/lib/python2.7/dist-packages/ispcli/"
mkdir /etc/ispcli
cp ispcli.conf /etc/ispcli/
chmod 500 /etc/ispcli 

cp ispcli.py /usr/sbin/ispcli 
chmod 500 /usr/sbin/ispcli
mkdir  $lib_path
echo y | cp ispcli/help_text.py $lib_path
echo y | cp ispcli/ispmanagerclass.py $lib_path
echo y | cp ispcli/menu.py $lib_path
echo -y | cp  ispcli/main.py $lib_path
echo -y | cp ispcli/__init__.py $lib_path

echo "Success!"
exit 0 
