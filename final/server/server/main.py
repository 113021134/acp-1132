from flask import Flask, jsonify, request, redirect, url_for, make_response
from flask_cors import CORS, cross_origin
from tinydb import TinyDB, Query
from webScrape import getPrice
db = TinyDB('db.json')
cartdb = TinyDB('cart.json')
ratingsdb = TinyDB('ratings.json')
accountdb = TinyDB('accounts.json')

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

def getQuantity(id):
    result = db.search(doc_id=id)
    if result:
        return result[0]["quantity"]
    else:
        return None
    
def decreaseQuantity(id, quantity_to_reduce):
    result = db.search(doc_id=id)
    if result:
        if result[0]["quantity"] >= quantity_to_reduce:
            db.update({"quantity": result[0]["quantity"] - quantity_to_reduce}, doc_id=id)
            return True
        else:
            return False
    else:
        return None

# * CRUD items
# handles buying an item
@app.route("/buy", methods=['POST'])
def buy():
    datas = request.get_json()
    productId = data.get('productId')
    requested_quantity = data.get('quantity')

    for data in datas:
        print(data)
        
    # Validate input
    # if not productId or not requested_quantity:
    #     return jsonify({"error": "Missing productId or quantity in request"}), 400
    # if not isinstance(productId, int) or not isinstance(requested_quantity, int):
    #     return jsonify({"error": "productId and quantity must be integers"}), 400
    # if requested_quantity <= 0:
    #     return jsonify({"error": "Quantity must be greater than 0"}), 400

    # # Check current stock
    # current_quantity = getQuantity(productId)
    # if current_quantity is None:
    #     return jsonify({"error": "Item not found"}), 404
    # if current_quantity < requested_quantity:
    #     return jsonify({"error": "Insufficient stock"}), 400
    
    # # Process purchase
    # success = decreaseQuantity(productId, requested_quantity)
    # if success:
    #     return jsonify({"message": "Item purchased successfully", "remaining_quantity": getQuantity(productId)})
    # else:
    #     return jsonify({"error": "Failed to process purchase"}), 500

# getting the quantity of an item by its ID
@app.route("/quantity/<int:id>")
def quantity(id):
    result = getQuantity(id)
    if result is not None:
        return jsonify({"id": id, "quantity": result})
    else:
        return jsonify({"error": "Item not found"}), 404
    
# getting an item by its ID
@app.route("/item/<int:id>", methods=["GET"])
@cross_origin()
def item(id):
    result = db.get(doc_id=id)

    if result:
        return jsonify({
            "id": id,
            "name": result["name"],
            "quantity": result["quantity"]
        })
    else:
        return jsonify({"error": "Item not found"}), 404
    
# * price comparison
@app.route("/compare-price/<string:perfume_name>")
def comparePrice(perfume_name):
    result = getPrice(perfume_name)
    return jsonify(result)

# * CART
@app.route("/increase-quantity", methods=["POST"])
def increaseQuantity():
    data = request.form
    productId = data.get('productId')
    quantity = data.get('quantity')

    if not productId or not quantity:
        return jsonify({"error": "Missing productId or quantity in request"}), 400
    
    if not isinstance(productId, int) or not isinstance(quantity, int):
        return jsonify({"error": "productId and quantity must be integers"}), 400
    
    if quantity <= 0:
        return jsonify({"error": "Quantity must be greater than 0"}), 400

    result = db.search(doc_id=productId)
    
    if result:
        new_quantity = result[0]["quantity"] + quantity
        db.update({"quantity": new_quantity}, doc_id=productId)
        return jsonify({"message": "Quantity updated successfully", "new_quantity": new_quantity}), 200
    else:
        return jsonify({"error": "Item not found"}), 404

@app.route("/delete-cart", methods=["POST"])
def deleteCart():
    data = request.form
    productId = data.get('productId')

    if not productId:
        return jsonify({"error": "Missing productId in request"}), 400
    
    ip = request.remote_addr
    cartdb.remove((Query().id == productId) & (Query().ip == ip)) # FIXME query.id pake doc_id=

    return jsonify({"message": "Item removed from cart successfully"}), 200

@app.route("/add-to-cart", methods=["POST"])
def addcart():
    data = request.form
    productId = data.get('productId')
    quantity = data.get('quantity')

    print(productId, quantity)

    if not productId or not quantity:
        return jsonify({"error": "Missing productId or quantity in request"}), 400
    
    cartdb.insert({
        "id": productId,
        "quantity": quantity,
        "ip": request.remote_addr
    })

    return redirect(request.referrer) # to home page
    # return jsonify({"message": "Item added to cart successfully"}), 200
    # return jsonify({'ip': request.remote_addr}), 200

@app.route("/cart", methods=["GET"])
def getCart():
    userId = request.args.get('userId')
    cart_items = cartdb.search(Query().userId == userId)

    if not cart_items:
        return jsonify({"message": "Cart is empty"}), 200
    
    items = []
    for item in cart_items:
        product = db.get(doc_id=item["id"])
        print(product)
        if product:
            items.append({
                "id": item["id"],
                "name": product["name"],
                "brand": product['brand'],
                "price": product['price'],
                "image": product["image"],
                "quantity": item["quantity"]
            })
    
    return jsonify(items), 200

# TODO ON CHECK OUT SEND EMAIL and delete cart


# * RATINGS
@app.route("/rating", methods=['POST'])
def insertRating():
    data = request.get_json()
    productId = data['productId']
    comment = data['comment']
    star = data['rating']
    userId = data['userId']

    print(data)

    account = accountdb.get(doc_id=userId)
    if not account:
        return jsonify({"message": "user with id not found"}), 400

    product = db.get(doc_id=productId)
    if not product:
        return jsonify({"message": "product with id not found"}), 400
    
    ratingsdb.insert({
        "productId": str(productId),
        "comment": comment,
        "stars": star,
        "userName": account['name']
    })

    return jsonify({"message": "nice"}), 201


@app.route("/rating/<string:productId>")
def getRatings(productId):
    ratings = ratingsdb.search(Query().productId == productId)

    result = []
    for rating in ratings:
        if rating:
            result.append({
                "userId": rating['userName'],
                "star": rating['stars'],
                "comment": rating['comment']
            })
    return jsonify(result), 200

@app.route("/rating/overall/<string:productId>")
def getOverallRatings(productId): #TODO benerin html shop data-produt-id ngga sesuai db.json
    try:
        ratings = ratingsdb.search(Query().productId == productId)
        if not ratings:
            return jsonify({"ratings": 0})
        
        ratingsArr = [int(item.get("stars", 0)) for item in ratings]
        overall = sum(ratingsArr) / len(ratingsArr) if ratingsArr else 0
        return jsonify({"ratings": overall})
    except Exception as e:
        print("Error in getOverallRatings:", e)
        return jsonify({"ratings": 0}), 500


# * ACCOUNTS
@app.route("/register", methods=['POST'])
def createAccount():
    data = request.form
    email = data.get('email')
    password = data.get('password')
    confirmpassword = data.get('confirm-password')
    name = data.get('name')

    if password != confirmpassword:
        return jsonify({"message": "confimr password is not the same"}), 400

    accountdb.insert({
        "email": email,
        "password": password,
        "name": name
    })
    return jsonify({"message": "account created successfully"}), 201

@app.route("/login", methods=['POST'])
def login():
    data = data = request.form
    email = data.get('email')
    password = data.get('password')

    account = accountdb.get(Query().email == email)
    
    if not account:
        return jsonify({"message": "not nice"}), 400

    if account['password'] == password:
        resp = make_response("Cookie set!")
        resp.set_cookie('userId', str(account.doc_id), max_age=36000)
        return resp

    return jsonify({"message": "not nice"}), 400