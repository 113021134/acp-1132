from flask import Flask, jsonify, request
from tinydb import TinyDB, Query
from webScrape import getPrice
db = TinyDB('db.json')

app = Flask(__name__)

def getQuantity(id):
    result = db.search(Query().id == id)
    if result:
        return result[0]["quantity"]
    else:
        return None
    
def decreaseQuantity(id, quantity_to_reduce):
    result = db.search(Query().id == id)
    if result:
        if result[0]["quantity"] >= quantity_to_reduce:
            db.update({"quantity": result[0]["quantity"] - quantity_to_reduce}, Query().id == id)
            return True
        else:
            return False
    else:
        return None

# handles buying an item
@app.route("/buy", methods=['POST'])
def buy():
    data = request.get_json()
    productId = data.get('productId')
    requested_quantity = data.get('quantity')

    # Validate input
    if not productId or not requested_quantity:
        return jsonify({"error": "Missing productId or quantity in request"}), 400
    if not isinstance(productId, int) or not isinstance(requested_quantity, int):
        return jsonify({"error": "productId and quantity must be integers"}), 400
    if requested_quantity <= 0:
        return jsonify({"error": "Quantity must be greater than 0"}), 400

    # Check current stock
    current_quantity = getQuantity(productId)
    if current_quantity is None:
        return jsonify({"error": "Item not found"}), 404
    if current_quantity < requested_quantity:
        return jsonify({"error": "Insufficient stock"}), 400
    
    # Process purchase
    success = decreaseQuantity(productId, requested_quantity)
    if success:
        return jsonify({"message": "Item purchased successfully", "remaining_quantity": getQuantity(productId)})
    else:
        return jsonify({"error": "Failed to process purchase"}), 500

# getting the quantity of an item by its ID
@app.route("/quantity/<int:id>")
def quantity(id):
    result = getQuantity(id)
    if result is not None:
        return jsonify({"id": id, "quantity": result})
    else:
        return jsonify({"error": "Item not found"}), 404
    
# getting an item by its ID
@app.route("/item/<int:id>")
def item(id):
    result = db.search(Query().id == id)
    if result:
        return jsonify({
            "id": result[0]["id"],
            "name": result[0]["name"],
            "quantity": result[0]["quantity"]
        })
    else:
        return jsonify({"error": "Item not found"}), 404
    
@app.route("/compare-price/<string:perfume_name>")
def comparePrice(perfume_name):
    result = getPrice(perfume_name)
    return jsonify(result)