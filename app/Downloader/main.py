#!/usr/bin/python3
import urllib3 as u

url = input("Enter your url you want to download: ")
print("Your url is: ", url)
http = u.PoolManager()
r = http.request('GET', url)
with open("data", "wb") as d:
    d.write(r.data)
