import requests
from pymongo import MongoClient
from bson import ObjectId

client = MongoClient("mongodb://user:pass@ds149134.mlab.com:49134/hackrice17")
db = client['hackrice17']

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
    def __init__(self, idx, email, name, pwd, sid):
        self.id = idx
        self.email = email
        self.name = name
        self.pwd = pwd
        self.sid = sid

class Product:
    def __init__(self, idx, name, amz_link, cost):
        self.id = idx
        self.name = name
        self.amz_link = amz_link
        self.cost = cost

class Shelter:
    def __init__(self, idx, name, lat, lon, address):
       self.id = idx
       self.name = name
       self.lat = lat
       self.lon = lon
       self.address = address
       self.products = list()

    def add_product(self, product):
        products.append(product)

# fetch product info based on name and returns a Product
def make_product_using_name(name):
    name = name.strip(' \t\n\r()')
    # parse the data for a specific need based on keyword 'name'
    url = 'https://api.harveyneeds.org/api/v1/products?need=' + name
    result = requests.get(url)
    get_results = result.json()['products']
    # retrieve first result
    if len(get_results) == 0:
        result = db.products.insert_one(
            {
            'name': name,
            'amz_link': "www.amazon.com",
            'cost' : "-$1"
            }
        )
        p = Product(str(result.inserted_id), name, "www.amazon.com", "-$1")
    else:
        first_result =  get_results[0]
        # insert product to list of products in database and returns an unique id
        result = db.products.insert_one(
            {
            'name': name,
            'amz_link': first_result['detail_url'],
            'cost' : first_result['price']
            }
        )
        # create a Product from unique id and product info
        p = Product(str(result.inserted_id), name, first_result['detail_url'], first_result['price'] )
    return p

# adds the product to a shelter's list of products
def add_product_to_shelter(shelter, product):
    p = make_product_using_name(product)
    shelter.add_product(p)

# creates a list of dictionary values that map a product to the count requested
def map_prod_to_count(products_list):
    prod_with_count = []
    for product in products_list:
        prod_to_count = {
            'pid': product.id,
            'count': 1
        }
        prod_with_count.append(prod_to_count)
    return prod_with_count

def push_shelter_to_db(shelter):
    result = db.shelters.insert_one(
        {
        'name': shelter.name,
        'lat': shelter.lat,
        'lon': shelter.lon,
        'address': shelter.address,
        'products': map_prod_to_count(shelter.products)
        }
    )

# get Harvey shelter data
response = requests.get("https://api.harveyneeds.org/api/v1/shelters?county=harris")
# data in json format
data = response.json()

# get the list of all of the shelters from the data
shelters = data['shelters']

# go through and add shelters and their products to database
for s in shelters:
    name = s['shelter']
    address = s['address']
    lon = s['longitude']
    lat = s['latitude']
    products = s['needs']

    if not(products is None) and len(products) > 0:
        # create a Shelter with shelter info in API
        shelter = Shelter(-1, name, lat, lon, address)
        # add all of the needs into shelter's list of products
        for p in products:
            if not isinstance(p, str) or '(' in p or ')' in p:
                continue
            add_product_to_shelter(shelter, p)
        # push the Shelter to the database
        push_shelter_to_db(shelter)
    else:
        print(name)
