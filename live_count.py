#!/usr/env/bin python
#coding:utf-8

import base64
import hashlib
import hmac
import urllib2
from base64 import urlsafe_b64encode, urlsafe_b64decode
from urlparse import urlparse
import json
from info import accessKey
from info import secretKey
from info import hubName

AK = accessKey #账号的    AccessKey
SK = secretKey #账号的 SecretKey
HUb= hubName #直播的hub名字

def HTTP_CURL(function):
    def func(*agrs,**data):
      req = function(*agrs,**data)
      data  = urllib2.urlopen(req)
      return data
    return func
@HTTP_CURL
def getHTTPHeader(url,header = None,value=None):
    if value ==None:
        req =urllib2.Request(url)
    else:
        data =json.dumps(value)
        req = urllib2.Request(url,data)
    for (k,v) in header.items():
        req.add_header(k,v)
    return req

def urlsafe_base64_encode(data):

    ret = urlsafe_b64encode(b(data))
    return s(ret)


def urlsafe_base64_decode(data):
    ret = urlsafe_b64decode(s(data))
    return ret


def s(data):
    if isinstance(data, bytes):
        data = data.decode('utf-8')
    return data
def MACToken(AK,SK,URL,Conetnt,Body=None,Methon=None):
   PathData =urlparse(URL)
   pathdir =Methon+" "+ PathData.path
   if PathData.query != "":
       pathdir =pathdir +"?"+PathData.query

   pathdirHost =pathdir+"\nHost: "+PathData.netloc+"\n"
   pathdirContentType = pathdirHost+Conetnt+"\n\n"
   if Body!= None:
       pathdirContentType = pathdirContentType+Body
   Authdata = __hmac_sha1__(pathdirContentType,SK)
   AUTH="Qiniu "+AK+":"+Authdata
   return AUTH

def __hmac_sha1__(data, key):
    """
    hmac-sha1
    """
    hashed = hmac.new(key, data, hashlib.sha1)
    return base64.urlsafe_b64encode(hashed.digest())
def main():
   url="http://pili.qiniuapi.com/v2/hubs/hubname/stat/play"
   AUTH=MACToken(AK=AK,SK=SK,URL=url.replace("hubname",HUb),Conetnt="Content-Type: application/json",Methon="GET")
   myheader = {"Authorization": str(AUTH), "User-Agent": "Python-urllib/2.7", "Content-Type": "application/json"}
   data=getHTTPHeader( url=url.replace("hubname",HUb), header=myheader)
   print data.read()
if __name__ == '__main__':
    main()
