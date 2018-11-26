# Copyright (c) 2018 Ruslan Variushkin,  ruslan@host4.biz


from beautifultable import BeautifulTable
from .ispmanagerclass import *
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
    data = list_data(names)
#    print query
#    print data.list(query)
 #   domains =getattr(data, func)()
    return print_data(data.list(query), names)

def load_db_data(names, query):
    data = list_data(names)
    head = ["owner","db_name","db_user"]
    return print_data(data.dbs_users(query), head)

def load_user_email(head, query):
    data = list_data(head)
    return print_data(data.user_email(query), head)

def load_email_setting(names, user):
    query = http_query_isp("email")
    data = list_data(names)
    api_result = data.list(query)
    head = ["name", "elid", "note", "passwd", "forward"]
    full_data = []
    for api_data in api_result:
        if api_data["owner"] == user:
            data = list_data(head)
            query = url_isp + "&elid=" + api_data["name"] + "&func=email.edit&out=xml"
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
                if "note" not in setting: setting["note"] = ""
                if "forward" not in setting: setting["forward"] = ""
                #print "user="+setting["elid"].replace("@", " ")+" passwd="+setting["passwd"] \
                #+" note: " + str(setting["note"]) \
                #+" forward: " + setting["forward"]
                print " user="+ str(setting["elid"].split("@")[0]) \
                      +" domain="+ str(setting["elid"].split("@")[1]) \
                      +" pass="+ str(setting["passwd"]) \
                      +" forward=" + str(setting["forward"]) \
                      +" note="+ str(setting["note"].replace(" ", "%20"))


def load_get_user_email(head, user_isp):
    account=bill_account(user_isp)
    if account:
        email=bill_user(account, "email")
        id=bill_user(account, "id")
        data=[{"ID":id,"Client":account.encode("utf-8"), "Email":email}]
        return print_data(data, head)
    else:
        print "Shared hosting service is off"
        return

