#!/usr/bin/python2

import urllib2
import re

ip_list = []

def enter_url():
  url = raw_input("Enter the url you want to crawl")
  return url

def set_header():
  ua = "'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.1 Safari/537.36'"
  headers = {'User-Agent': ua, 'Referer': "http://www.google.com"}
  return headers

def get_web_page(url):
  try:
    headers = set_header()
    req = urllib2.Request(url, None, headers)
    res = urllib2.urlopen(req, timeout = 3)
    web_page = res.read()
  except Exception, e:
    print str(e)
    print "Error web page"
    web_page = ''
  finally:
    res.close()
  return web_page

def resolve_web_page(web_page):
  print "web_page: %s" % (web_page)
  try:
    table = re.findall(r"<tbody>(.*?)</tbody>", web_page, re.S)
    a_ip_list = re.findall(r"<td>(\d+\.\d+\.\d+\.\d+)</td>", table[0], re.S)
    a_port_list = re.findall(r"<td>(\d{2,5})</td>", table[0], re.S)
  except Exception, e:
    print str(e)
    print "Error in resolving web page"
    a_ip_list = []
    a_port_list = []
  a_ip_port_list = []
  print "Megre ip and port into a list"
  for item in range(0, len(a_ip_list)):
    a_ip_port_list.append(a_ip_list[item] + ":" + a_port_list[item])
  return a_ip_port_list

def crawl(url):
  web_page = get_web_page(url) 
  global ip_list
  ip_list += resolve_web_page(web_page)
  return ip_list

if __name__ == '__main__':
  url = "https://www.sslproxies.org/"
  for ip in crawl(url):
    print ip
  

