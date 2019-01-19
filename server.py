from flask import Flask, render_template
from flask_socketio import SocketIO
from Database import Db

app = Flask(__name__)
app.config['SECRET_KEY'] = 'WRTGJOPIRUGOIQ34THLDCJNVXZas'
socketio = SocketIO(app)
users = Db();
count = 0


@app.route('/')
def sessions():
    return render_template('index.html')


@app.route('/chat')
def chat():
    return render_template('chat.html')


@socketio.on('message')
def handle_message(message):
    socketio.emit('success', {'message': message})


@socketio.on('auth')
def handle_auth(message):

    if not message['username'] and not message['password']:
        socketio.emit('success', {'message': "Enter username and password"})
    else:

        username = message['username']
        password = message['password']
        # if username does not exist
        if not users.check_user(username):
            users.add_user(username, password)
            socketio.emit('success', {'message': "OK"})

        else:
            # if user enter valid password
            if users.check_password(username, password):
                socketio.emit('success', {'message': 'OK'})
                # TODO: Deliver cookie with auth
            else:
                # if user enter wrong password
                users.add_user(username, password)
                socketio.emit('success', {'message': "Wrong password"})


@socketio.on('connect')
def connect():
    global count
    count += 1
    socketio.emit('count', {'count': count})


@socketio.on('disconnect')
def disconnect():
    global count
    count -= 1
    socketio.emit('count', {'count': count})


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=4000, debug=True)
