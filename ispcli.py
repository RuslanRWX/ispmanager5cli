#!/usr/bin/env python
# Copyright (c) 2018 Ruslan Variushkin,  ruslan@host4.biz
# Version 0.0.2


import sys
sys.path.append("/usr/lib/python2.7/ispcli")
from beautifultable import BeautifulTable
from help_text import *
import argparse
import ispmanagerclass
table = BeautifulTable(max_width=300)


def print_data(domains, names):
    table.column_headers = names
    for domain in domains:
        data=[]
        for key in names:
            try:
                local_data = domain[key]
            except:
                domain[key] = "None"
                local_data = domain[key]
            data.append(local_data)
        table.column_alignments[key] = BeautifulTable.ALIGN_LEFT
        table.append_row([ x for x in data])
    print (table)


def load_data(names, query):
    data = ispmanagerclass.list_data(names)
 #   domains =getattr(data, func)()
    return print_data(data.list(query), names)


def load_db_data(names, query):
    data = ispmanagerclass.list_data(names)
    head = ["owner","db_name","db_user"]
    return print_data(data.dbs_users(query), head)

def load_user_email(head, query):
    data = ispmanagerclass.list_data(head)
    return print_data(data.user_email(query), head)

def load_email_setting(names, user):
    query = ispmanagerclass.http_query_isp("email")
    data = ispmanagerclass.list_data(names)
    api_result = data.list(query)
    head = ["name", "elid", "note", "passwd", "forward"]
    full_data = []
    for api_data in api_result:
        if api_data["owner"] == user:
            data = ispmanagerclass.list_data(head)
            query = ispmanagerclass.URL + "&elid=" + api_data["name"] + "&func=email.edit&out=xml"
            #print (str(api_data["owner"])+" "+str(api_data["name"]))
            setting_info_by_user = data.user_email(query)
            array={}

            for setting in setting_info_by_user:
            #    for key in head:
            #        value = setting[key]
            #        if key:
            #            array.update(({key: value}))
            #    full_data.append(array)
            #print full_data
                if "note" not in setting: setting["note"] = "None"
                if "forward" not in setting: setting["forward"] = "Note"
                #print "user="+setting["elid"].replace("@", " ")+" passwd="+setting["passwd"] \
                #+" note: " + str(setting["note"]) \
                #+" forward: " + setting["forward"]
                print " user="+ str(setting["elid"].split("@")[0]) \
                      +" domain="+ str(setting["elid"].split("@")[1]) \
                      +" passwd="+ str(setting["passwd"]) \
                      +" note=" + str(setting["note"]) \
                      +" forward=" + str(setting["forward"])



            #query = ispmanagerclass.URL + "&elid=" + args.email_info + "&func=email.edit&out=xml"
            #names = ["name", "elid", "note", "passwd", "forward"]
            #return load_user_email(names, query)


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
        query = ispmanagerclass.http_query_isp("user")
        if args.verbosity >=1:
            names = ["user", "name"]
            return load_data(names, query)
        elif args.users:
            names = ["name"]
            return load_data(names, query)
    elif args.domains:
        query = ispmanagerclass.http_query_isp("domain")
        names = ["user", "name"]
        return load_data(names, query)
    elif args.webdomains:
        query = ispmanagerclass.http_query_isp("webdomain")
        names = ["owner", "name", "docroot", "php",
                 "php_version", "cgi", "active", "ipaddr"]
        return load_data(names,query)
    elif args.billing:
        query = ispmanagerclass.Bill + "&func=user&out=xml"
        names = ["account_id","name","email"]
        return load_data(names, query)
    elif args.emails:
        query = ispmanagerclass.http_query_isp("email")
        names = ["owner","name","forward"]
        return load_data(names, query)
    elif args.dbs:
        query = ispmanagerclass.http_query_isp("db")
        names = ["owner","name","key"]
        return load_data(names, query)
    elif args.dbs_users:
        query = ispmanagerclass.http_query_isp("db")
        names = ["owner","name","key"]
        return load_db_data(names, query)
    elif args.email_info:
        query = ispmanagerclass.URL + "&elid=" + args.email_info + "&func=email.edit&out=xml"
        names = ["name","elid","note","passwd","forward"]
        return load_user_email(names, query)
    elif args.user:
        if args.email:
            names = ["owner", "name", "forward"]
            return load_email_setting(names,args.user)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()

