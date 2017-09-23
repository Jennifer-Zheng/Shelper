import requests
from pymongo import MongoClient
from bson import ObjectId

client = MongoClient("mongodb://user:pass@ds149134.mlab.com:49134/hackrice17")
db = client.test

###### DATA MODEL
# User
# {
#     _id : user id,
#     email: user email,
#     name: user's name,
#     pwd: password,
#     sid: shelter id
# }
#
# Product
# {
#   _id: product id (auto-populated),
#   name: product name,
#   amz_link: amazon link,
#   cost: cost of product
# }
#
# Shelter
# {
#   _id: shelter id (auto-populated),
#   name: shelter name,
#   lat: latitude,
#   lon: longitude,
#   address: address,
#   products: [
#               { pid (product id): count },
#               ...
#             ]
# }
class User:
    def __init__(self, id, email, name, pwd, sid):
        self.id = id,
        self.email = email,
        self.name = name,
        self.pwd = pwd,
        self.sid = sid

class Product:
    def __init__(self, id, name, amz_link, cost):
        self.id = id,
        self.name = name,
        self.amz_link = amz_link,
        self.cost = cost

class Shelter
   def __init__(self, id, name, lat, lon, address, products):
       self.id = id,
       self.name = name,
       self.lat = lat,
       self.lon = lon
       self.address = address,
       self.products = []

    def add_product(self, product):
        products.append(product)


response = requests.get("https://api.harveyneeds.org/api/v1/shelters?county=harris")
data = response.json()

shelters = data['shelters']

def make_product_using_name(name):
    url = 'https://api.harveyneeds.org/api/v1/products?need=' + name
    result = requests.get(url)
    resulting_data = result.json()
    first_result = resulting_data['products'][0]
    result = db.products.insert_one(
        'name': name,
        'amz_link'= first_result['detail_url']
        'cost' = first_result['price']
    )
    p = Product(str(result.inserted_id), name, first_result['detail_url'], first_result['price'] )
    return p

def add_product_to_shelter(shelter, product):
    result = db.products.insert_one(
        {
            "name": product


        })

for s in shelters:
    name = s['shelter']
    address = s['address']
    lon = s['longitude']
    lat = s['latitude']
    products = s['needs']

    for p in products:
        parse_products(s, p)

    push_shelter_to_db(s)
