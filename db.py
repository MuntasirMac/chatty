from pymongo import MongoClient
from decouple import config
from werkzeug.security import generate_password_hash

client = MongoClient(config('mongo_uri'))

chat_db = client.get_database(config('db'))
users_collection = chat_db.get_collection("users")

def save_user(username, email, password):
    password_hash = generate_password_hash(password)
    payload_to_insert = {
        '_id': username,
        'email': email,
        'password': password_hash
    }
    users_collection.insert_one(payload_to_insert)

save_user("mac", "mac@test.com", "test_pass")