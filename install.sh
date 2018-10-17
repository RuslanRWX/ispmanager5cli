#!/bin/bash


mkdir /etc/ispcli
cp ispcli.conf /etc/ispcli/
chmod 500 /etc/ispcli 

cp ispcli.py /usr/sbin/ispcli 
chmod 500 /usr/sbin/ispcli
mkdir -p /usr/lib/python2.7/ispcli
cp lib/help_text.py /usr/lib/python2.7/ispcli/
cp lib/ispmanagerclass.py /usr/lib/python2.7/ispcli/

echo "Success!"
exit 0 
