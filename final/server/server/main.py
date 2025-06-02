from flask import Flask
from tinydb import TinyDB, Query

db = TinyDB('db.json')  # fixed path: no leading slash unless it's absolute

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<h1>JOEL WANNNAAAA!</h1>"

@app.route("/in")
def inside():
    return "<h1>done!</h1>"

@app.route("/out/<int:id>")
def outside(id):
    result = db.search(Query().id == id)
    name = result[0]['name'] if result else "Not found"
    quantity = result[0]['quantity'] if result else "Not found"
    return f"<h1>name: {name}, quantity: {quantity}</h1>"
