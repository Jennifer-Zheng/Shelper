from flask import Flask, jsonify, request
from flask.ext.pymongo import PyMongo

app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'hackrice17'
app.config['MONGO_URI'] = '<in the mlab>'

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
        output.append({'pid': p['_id'], 'name': p['name']})
    return jsonify({'result': output})

@app.route('/product', methods=['POST'])
def add_product():
    products = mongo.db.products
    name = request.json['name']
    pid = products.find_one({'name': name})
###################EXAMPLE CODE BELOW############################
@app.route('/endpoint', methods=['GET'])
def get_all_frameworks():
    framework = mongo.db.framework
    output = []
    for q in framework.find():
        output.append({'name': q['name'], 'language': q['language']})
    return jsonify({'result': output})

@app.route('/framework/<name>', methods=['GET'])
def get_one_framework(name):
    framework = mongo.db.framework

    q = framework.find_one({'name': name}) # one result

    if q:
        output = {'name': q['name'], 'language': q['language']}
    else:
        output = 'No Result Found'

    return jsonify({'result': output})


@app.route('/endpoint', methods=['POST'])
def add_framework():
    framework = mongo.db.framework
    name = request.json['name']
    language = request.json['language']

    framework_id = framework.insert({'name': name, 'language': language})
    new_framework = framework.find_one({'_id' : framework_id})
    output = {'name': new_framework['name'], 'language': new_framework['language']}
    return jsonify({'result': output})


if __name__ == '__main__':
    app.run(debug=True)
