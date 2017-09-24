from flask import Flask, jsonify, request
from flask.ext.pymongo import PyMongo
from bson import ObjectId

app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'hackrice17'
app.config['MONGO_URI'] = 'mongodb://user:pass@ds149134.mlab.com:49134/hackrice17'

mongo = PyMongo(app)

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

# donator side
# GET: /shelters
# output:
# {
#   'result':
#       [
#           { sid: shelter id, name: shelter name, latitude: latitude,
#            longitude: longitude, address: shelter address, products:
#            products in shelter },
#            ...
#       ]
# }
@app.route('/shelters', methods=['GET'])
def get_all_shelters():
    shelters = mongo.db.shelters
    output = []
    for s in shelters.find():
        output.append({'sid': str(s['_id']), 'name': s['name'], 'latitude': s['lat'],
        'longitude': s['lon'], 'address': s['address'], 'products': s['needs']})
    return jsonify({'result': output})

# GET: /<name>/productspecs
# output:
# {
#   'result':
#       {
#           pid: product id,
#           name: product name,
#           cost: product cost,
#           amz_link: product's amazon link
#       } <on success>
#       'INVALID UID' <on failure>
# }
@app.route('/<pid>/product_specs')
def get_product_specs(pid):
    product = mongo.db.products.find_one({'_id': pid})
    if product:
        output = {'pid': product['pid'], 'name': product['name'],
        'cost': product['cost'], 'amz_link': product['amz_link']}
    else:
        output = 'INVALID UID'
    return jsonify({'result': output})

# people in shelter side

# POST: /signup
# input:
# {
#   uid: user id,
#   email: user email,
#   name: user name,
#   pwd: user password,
#   shelter_name: shelter name
# }
# output:
# {
#   result: 'SIGN UP FAILED' <if id or email exists>
#           'SIGN UP SUCESS' <on success>
# }
@app.route('/signup', methods=['POST'])
def sign_up():
    users = mongo.db.users
    # fields
    _id = request.json['uid']
    email = request.json['email']
    # if the user id already exists
    if users.find_one({'_id': _id}) or users.find_one({'email': email}):
        return jsonify({'result': 'SIGN UP FAILED'})
    name = request.json['name']
    pwd = request.json['pwd']
    sid = mongo.db.shelter.find_one({'name': request.json['shelter_name']})
    framework.insert({'_id': _id, 'email': email, 'name': name, 'pwd': pwd, 'sid': sid})
    return jsonify({'result': 'SIGN UP SUCCESS'})

# GET: /<name>/userinfo
# output:
# {
#   'result':
#       {
#           uid: user id,
#           sid: shelter id
#       } <on success>
#       'INVALID UID' <on failure>
# }
@app.route('/<uid>/userinfo')
def get_user_shelter(uid):
    user = mongo.db.users.find_one({'_id': uid})
    if user:
        output = {'uid': uid, 'sid': user['sid']}
    else:
        output = 'INVALID UID'
    return jsonify({'result': output})


# GET: /products
# output:
# {
#   'result':
#       [
#           { uid: product id, name: product name },
#           ...
#       ]
# }
@app.route('/products', methods=['GET'])
def get_all_products():
    products = mongo.db.products
    output = []
    for p in products.find():
        output.append({'pid': str(p['_id']), 'name': p['name']})
    return jsonify({'result': output})

@app.route('/product', methods=['POST'])
def add_product():
    shelters = mongo.db.shelters
    products = mongo.db.products
    sid = request.json['sid']
    pid = request.json['pid']
    count = request.json['count']
    shelter = shelters.find_one({'_id': ObjectId(sid)})
    if not shelter:
        return jsonify({'result': 'FAILED'})
    prod = None
    for p in shelter['products']:
        if p['pid'] == pid:
            prod = p
            break
    if prod:
        prod['count'] = prod['count'] + count
    else:
        prod = dict()
        prod['pid'] = pid
        prod['count'] = count
        shelter['products'].append(prod)
    shelters.save(shelter)
    return jsonify({'result': 'SUCCESS'})


###################EXAMPLE CODE BELOW############################
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
