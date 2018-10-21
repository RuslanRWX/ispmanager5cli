#!/usr/bin/env python
# Version 0.0.2
from xml.dom import minidom
import ConfigParser
import urllib2
from urllib2 import urlopen
global URL_IPS
global User_IPS
global Pass_ISP

Conf_file = "/etc/ispcli/ispcli.conf"
config = ConfigParser.ConfigParser()
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





def request_http(query):
    result = urllib2.Request(query, headers=hdr)
    return minidom.parse(urlopen(result))

def request_http_xmltodict(query):
    import xmltodict
    result = urllib2.Request(query, headers=hdr)
    return xmltodict.parse(urlopen(result).read())

def http_query_isp(func):
    add = "&func="+ func +"&out=xml"
    return url_isp + add



class list_data():
    def __init__(self, values):
        self.values = values

    def fetch_data(self, xmldoc):
        data=[]
        for node in xmldoc.getElementsByTagName('elem'):
            account={}
            for attr in self.values:
                for var in node.getElementsByTagName(attr):
                    account.update({attr:var.firstChild.nodeValue.encode("utf-8")})
            data.append(account)
        return data

    def list(self, query):
        return self.fetch_data(request_http(query))

    def db_user(self, key):
        query = url_isp+ "&func=db.users&out=xml&elid="+key
        users=[]
        for name in self.fetch_data(request_http(query)):
            users.append(name["name"])
        return users

    def dbs_users(self, query):
        full_data=[]
        for data in self.fetch_data(request_http(query)):
            array={}
            name = self.db_user(data["key"])
            array.update({"owner":data["owner"],
                          "db_name": data["name"],
                          "db_user": name })
            full_data.append(array)
        return full_data

    def user_email(self, query):
        array={}
        doc=request_http_xmltodict(query)
        for key in self.values:
            value = doc["doc"][key]
            if value:
                array.update({key: value.encode("utf-8")})
        return [array]
