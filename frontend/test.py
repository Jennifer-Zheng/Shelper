from pymongo import MongoClient
import requests
import os

client = MongoClient('mongodb://user:pass@ds149134.mlab.com:49134/hackrice17')
db = client['hackrice17']

url = 'http://0.0.0.0:8080/shelters'
result = requests.get(url)
json= result.json()

print (json)
