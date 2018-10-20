#!/bin/bash

lib_path = "/usr/lib/python2.7/ispcli/"
mkdir /etc/ispcli
cp ispcli.conf /etc/ispcli/
chmod 500 /etc/ispcli 

cp ispcli.py /usr/sbin/ispcli 
chmod 500 /usr/sbin/ispcli
mkdir -p $lib_path
cp lib/help_text.py $lib_path
cp lib/ispmanagerclass.py $lib_path
cp lib/app.py $lib_path
cp lib/main.py $lib_path
cp lib/__init__.py $lib_path

echo "Success!"
exit 0 
