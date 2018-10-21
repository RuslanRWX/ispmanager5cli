#!/bin/bash

lib_path="/usr/local/lib/python2.7/dist-packages/ispcli"
mkdir /etc/ispcli
cp ispcli.conf /etc/ispcli/
chmod 500 /etc/ispcli 

cp ispcli.py /usr/sbin/ispcli 
chmod 500 /usr/sbin/ispcli
mkdir  $lib_path
echo y | cp lib/help_text.py $lib_path
echo y | cp lib/ispmanagerclass.py $lib_path
echo y | cp lib/app.py $lib_path
echo -y | cp  lib/main.py $lib_path
echo -y | cp lib/ $lib_path

echo "Success!"
exit 0 
