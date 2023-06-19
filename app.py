from flask import Flask, redirect, render_template, request, url_for
from flask_login import current_user, login_user, login_manager, LoginManager, login_required, logout_user
from flask_socketio import SocketIO, join_room
# from db import get_user, save_user, save_room, add_room_member, add_room_members, remove_room_members
from db import *

app = Flask(__name__)
app.secret_key = "test secret key"
socketio = SocketIO(app)
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)


@app.route('/')
def home():
    return render_template("index.html")


@app.route('/login', methods=['GET', 'POST'])
def login():

    if current_user.is_authenticated:
        return redirect(url_for('home'))
    message = ''
    if request.method == 'POST':
        username = request.form.get('username')
        password_input = request.form.get('password')
        user = get_user(username)

        if user and user.check_password(password_input):
            login_user(user)
            return redirect(url_for('home'))
        else:
            message = 'Failed to login!'

    return render_template('login.html', message=message)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    message = ''
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        try:
            save_user(username, email, password)
            return redirect(url_for('home'))
        except:
            message = "User already exists!"

    return render_template('signup.html', message=message)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/create-room/', methods=['GET', 'POST'])
@login_required
def create_room():

    if request.method == 'POST':
        room_name = request.form.get('room_name')
        usernames = [username.strip() for username in request.form.get('members').split(',')]

        if len(room_name) and len(usernames):
            room_id = save_room(room_name, current_user.username)
            if current_user.username in usernames:
                usernames.remove(current_user.username)

    return render_template('create_room.html')


@app.route('/chat')
@login_required
def chat():
    username = request.args.get('username')
    room = request.args.get('room')

    if username and room:
        print(username, room)
        return render_template("chat.html", username=username, room=room)
    # else:
    #     return redirect(url_for('home'))


@socketio.on('send_message')
def handle_send_message_event(data):
    app.logger.info(f"{data['username']} has sent message to the room {data['room']}: {data['message']}")
    socketio.emit('receive_message', data, room=data['room'])


@socketio.on('join_room')
def handle_join_room_event(data):
    app.logger.info(f"{data['username']} has joined the room {data['room']}")
    join_room(data['room'])
    socketio.emit('join_room_announcement', data)


@login_manager.user_loader
def load_user(username):
    return get_user(username)


if __name__ == '__main__':
    socketio.run(app, debug=True)