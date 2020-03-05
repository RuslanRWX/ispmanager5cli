# Copyright (c) 2018 Ruslan Variushkin,  ruslan@host4.biz

from xml.dom import minidom
import configparser
import urllib.request, urllib.error, urllib.parse
from urllib.request import urlopen
import ssl

global URL_IPS
global User_IPS
global Pass_ISP

Conf_file = "/etc/ispcli/ispcli.conf"
config = configparser.ConfigParser()
config.read(Conf_file)

hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}

url_isp = config.get('main', 'URL_IPS') + \
      "/ispmgr?authinfo=" \
      + config.get('main', 'User_IPS') + \
        ":" + config.get('main','Pass_ISP')
url_bill = config.get('main','BillURL') + \
       "/billmgr?authinfo=" + \
       config.get('main', 'UserBill') \
       + ":" + config.get('main','PassBill')

#if INSECURE:
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

def request_http(query, insecure):
    result = urllib.request.Request(query, headers=hdr)
    if insecure:
        return minidom.parse(urlopen(result, context=ctx))
    else:
        return minidom.parse(urlopen(result))

def request_http_xmltodict(query, insecure):
    import xmltodict
    result = urllib.request.Request(query, headers=hdr)
    if insecure:
        return xmltodict.parse(urlopen(result, context=ctx).read())
    else:
        return xmltodict.parse(urlopen(result).read())

def http_query_isp(func):
    add = "&func="+ func +"&out=xml"
    return url_isp + add



class list_data():
    def __init__(self, values, *args):
        self.values = values
        for var in args:
            self.insecure = var.insecure

    def fetch_data(self, xmldoc):
        data=[]
        for node in xmldoc.getElementsByTagName('elem'):
            account={}
            for attr in self.values:
                for var in node.getElementsByTagName(attr):
                    account.update({attr:var.firstChild.nodeValue})
            data.append(account)
        return data

    def list(self, query):
        return self.fetch_data(request_http(query, self.insecure))

    def db_user(self, key):
        query = url_isp+ "&func=db.users&out=xml&elid="+key
        users=[]
        for name in self.fetch_data(request_http(query, self.insecure)):
            users.append(name["name"])
        return users

    def dbs_users(self, query):
        full_data=[]
        for data in self.fetch_data(request_http(query, self.insecure)):
            array={}
            name = self.db_user(data["key"])
            array.update({"owner":data["owner"],
                          "db_name": data["name"],
                          "db_user": name })
            full_data.append(array)
        return full_data

    def user_email(self, query):
        array={}
        doc=request_http_xmltodict(query, self.insecure)
        for key in self.values:
            value = doc["doc"][key]
            if value:
                array.update({key: value})
        return [array]




def bill_account(user, *args):
    query = url_bill + "&func=vhost&out=xml"
    doc=request_http(query, *args)
    for node in doc.getElementsByTagName('elem'):
        for usernameBill in node.getElementsByTagName('username'):
                    if usernameBill.firstChild.nodeValue == user:
                        for account in node.getElementsByTagName('account'):
                            return account.firstChild.nodeValue

def bill_user(account,search, *args):
    query = url_bill + "&func=user&out=xml"
    doc=request_http(query, *args)
    for node in doc.getElementsByTagName('elem'):
        for accountBill in node.getElementsByTagName('account'):
            if accountBill.firstChild.nodeValue == account:
                for value in node.getElementsByTagName(search):
                    return  value.firstChild.nodeValue


#query = url_bill + "&func=user&out=xml"
#        URLBILL = urlBill + "/billmgr?authinfo=" + \
#            userbill + ":" + passbill + "&func=vhost&out=xml"
#        res = urlopen(URLBILL)
#        xmldoc = minidom.parse(res)
#        for node in xmldoc.getElementsByTagName('elem'):
#            for usernameBill in node.getElementsByTagName('username'):
#                if usernameBill.firstChild.nodeValue == user:
#                    for account in node.getElementsByTagName('account'):
#                        return account.firstChild.nodeValue
