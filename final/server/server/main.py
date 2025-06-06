from flask import Flask, jsonify
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
    
def decreaseQuantity(id):
    result = db.search(Query().id == id)
    if result:
        if result[0]["quantity"] > 0:
            db.update({"quantity": result[0]["quantity"] - 1}, Query().id == id)
            return True
        else:
            return False
    else:
        return None

# handles buying an item
@app.route("/buy", methods=['POST'])
def buy():
    quantity = getQuantity(1)

    if quantity == 0:
        return jsonify({"error": "Item out of stock"}), 404
    elif quantity is None:
        return jsonify({"error": "Item not found"}), 404
    
    decreaseQuantity(1)
    return jsonify({"message": "Item purchased successfully", "remaining_quantity": getQuantity(1)})

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

    return result