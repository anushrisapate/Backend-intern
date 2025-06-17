from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.config["MONGO_URI"] = os.getenv("MONGO_URI")
mongo = PyMongo(app)

db = mongo.db

from settlements import calculate_balances, calculate_settlements

@app.route('/')
def index():
    return "Split App Backend is Running!"

if __name__ == '__main__':
    app.run(debug=True)
