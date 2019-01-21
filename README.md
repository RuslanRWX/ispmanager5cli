# ISPManager5Cli
ispcli is a simple command line interface client for ISPManager 5.
The script uses API of ISPManager 5 and ISPBilling 5, therefore can be installed on your workstation or an ISPmanager5 server as well.

Ability:
 - list of users
 - list of webdomains
 - list of billing users
 - list of emails
 - list of databases
 - list of databases and passwords 
 - list of domain emails 
 - list of webscripts


install

```
git clone https://github.com/ruslansvs2/ispmanager5cli.git

./install.sh

```

configuration

```
cd /etc/ispcli/
```

Use vim or other command line editor

```
vim ispcli.conf
```

print help out

```
ispcli -h

usage: ispcli [-h] [--users] [-v] [--domains] [--webdomains] [--billing]
              [--emails] [--dbs] [--dbs_users] [--email_info EMAIL_INFO]
              [--user USER] [--email] [--get_user_email GET_USER_EMAIL]
              [--web_script_packages WEB_SCRIPT_PACKAGES] [--web_scripts] [-V]

ispcli works with ispmanager5 through API

optional arguments:
  -h, --help            show this help message and exit
  --users               list all of users
  -v, --verbosity       increase output verbosity
  --domains             Domains list
  --webdomains          List of webdomains and their configurations
  --billing             Billing information, users and emails
  --emails              List of accounts' emails
  --dbs                 List of databases
  --dbs_users           List of databases and users of databases
  --email_info EMAIL_INFO
                        Email settings
  --user USER           Specify username
  --email               List of setting of emails
  --get_user_email GET_USER_EMAIL
                        Get user's email
  --web_script_packages WEB_SCRIPT_PACKAGES
                        List of script packages, example --web_script_packages
                        WordPress
  --web_scripts         List of web-scripts
  -V, --version         Show version

Thanks for using
```

Example of using

```
 ispcli --web
+------------------+-----------------------------+-----------------------------------+-----+-----------------+------+--------+---------------+
|      owner       |            name             |              docroot              | php |   php_version   | cgi  | active | ipaddr        |
+------------------+-----------------------------+-----------------------------------+-----+-----------------+------+--------+---------------+
|      test1       |   test.io                   |     www/test.io                   | on  | 5.4.16 (native) |  on  |  off   | 127.0.0.1     |
+------------------+-----------------------------+-----------------------------------+-----+-----------------+------+--------+---------------+
|      test2       |   test2.org                 |     www/test3.org                 | on  | 5.4.16 (native) |  on  |  off   | 127.0.0.1     |

```



