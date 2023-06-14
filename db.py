from pymongo import MongoClient
from werkzeug.security import generate_password_hash

client = MongoClient("url will be provided after getting the cluster")

chat_db = client.get_database("will be generated")
users_collection = chat_db.get_collection("will be provided after setting the cluster")

def save_user(username, email, password):
    password_hash = generate_password_hash(password)
    payload_to_insert = {
        '_id': username,
        'email': email,
        'password': password_hash
    }
    users_collection.insert_one(payload_to_insert)