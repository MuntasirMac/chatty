from pymongo import MongoClient
from bson import ObjectId
from decouple import config
from datetime import datetime
from werkzeug.security import generate_password_hash
from user import User

client = MongoClient(config('mongo_uri'))

chat_db = client.get_database(config('db'))
users_collection = chat_db.get_collection("users")
rooms_collection = chat_db.get_collection("rooms")
room_members_collection = chat_db.get_collection("room_members")

def save_user(username, email, password):
    password_hash = generate_password_hash(password)
    users_collection.insert_one({'_id': username, 'email': email, 'password': password_hash})

# save_user("mac", "mac@test.com", "test_pass")

def get_user(username):
    user_data = users_collection.find_one({'_id': username})
    return User(user_data['_id'], user_data['email'], user_data['password']) if user_data else None


def save_room(room_name, created_by):
    room_id = rooms_collection.insert_one(
        {'room_name': room_name, 'created_by': created_by, 'created_at': datetime.now()}
        ).inserted_id

    add_room_member(room_id, room_name, created_by, created_by, is_admin=True)

    return room_id


def update_room(room_id, room_name):
    pass


def get_room(room_id):
    rooms_collection.find_one({'_id': ObjectId(room_id)})


def add_room_member(room_id, room_name, username, added_by, is_room_admin=False):
    room_members_collection.insert_one({
        '_id': {
            'room_id': room_id,
            'username': username,
        },
        'room_name': room_name,
        'added_by': added_by,
        'added_at': datetime.now(),
        'is_room_admin': is_room_admin
    })


def add_room_members(room_id, room_name, usernames, added_by):
    room_members_collection.insert_many(
        [ {
        '_id': {
            'room_id': room_id,
            'username': username,
        },
        'room_name': room_name,
        'added_by': added_by,
        'added_at': datetime.now(),
        'is_room_admin': False
        } for username in usernames ]
    )


def remove_room_members(room_id, usernames):
    pass


def get_room_members(room_id):
    room_members_collection.find({'_id': ObjectId(room_id)})


def get_room_for_user(room_id):
    pass

