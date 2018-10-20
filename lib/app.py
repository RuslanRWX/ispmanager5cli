#!/usr/bin/env python
# Copyright (c) 2018 Ruslan Variushkin,  ruslan@host4.biz
# Version 0.0.2

#import sys
#sys.path.append("/usr/lib/python2.7/ispcli")
#from help_text import *
import argparse
#import main
#import ispmanagerclass

import ispcli

def main():
    parser = argparse.ArgumentParser(prog='ispcli', description=Help_desc,
                                     epilog=Hepl_epilog)
    parser.add_argument("--users",
                        help=Help_user_list, action='store_true' )
    parser.add_argument("-v", "--verbosity",
                        help="increase output verbosity",
                        action="count", default=0)
    parser.add_argument("--domains",
                        help=Help_user_domains, action='store_true')
    parser.add_argument("--webdomains",
                        help=Help_user_webdomains, action='store_true')
    parser.add_argument("--billing",
                        help=Help_billing, action='store_true')
    parser.add_argument("--emails",
                        help=Help_emails, action='store_true')
    parser.add_argument("--dbs",
                        help=Help_dbs, action='store_true')
    parser.add_argument("--dbs_users",
                        help=Help_dbs_users, action='store_true')
    parser.add_argument("--email_info",
                        help=Help_email_info)
    parser.add_argument("--user",
                        help=Help_user)
    parser.add_argument("--email",
                        help=Help_email, action='store_true')
    args = parser.parse_args()

    if args.users:
        query = ispcli.ispmanagerclass.http_query_isp("user")
        if args.verbosity >=1:
            names = ["user", "name"]
            return ispcli.main.load_data(names, query)
        elif args.users:
            names = ["name"]
            return main.load_data(names, query)
    elif args.domains:
        query = ispmanagerclass.http_query_isp("domain")
        names = ["user", "name"]
        return main.load_data(names, query)
    elif args.webdomains:
        query = ispmanagerclass.http_query_isp("webdomain")
        names = ["owner", "name", "docroot", "php",
                 "php_version", "cgi", "active", "ipaddr"]
        return main.load_data(names,query)
    elif args.billing:
        query = ispmanagerclass.Bill + "&func=user&out=xml"
        names = ["account_id","name","email"]
        return main.load_data(names, query)
    elif args.emails:
        query = ispmanagerclass.http_query_isp("email")
        names = ["owner","name","forward"]
        return main.load_data(names, query)
    elif args.dbs:
        query = ispmanagerclass.http_query_isp("db")
        names = ["owner","name","key"]
        return main.load_data(names, query)
    elif args.dbs_users:
        query = ispmanagerclass.http_query_isp("db")
        names = ["owner","name","key"]
        return main.load_db_data(names, query)
    elif args.email_info:
        query = ispmanagerclass.URL + "&elid=" + args.email_info + "&func=email.edit&out=xml"
        names = ["name","elid","note","passwd","forward"]
        return main.load_user_email(names, query)
    elif args.user:
        if args.email:
            names = ["owner", "name", "forward"]
            return main.load_email_setting(names,args.user)
    else:
        parser.print_help()
