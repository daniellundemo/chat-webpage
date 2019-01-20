from flask import Flask, render_template, request
from flask_socketio import SocketIO
from Database import Db

app = Flask(__name__)
app.config['SECRET_KEY'] = 'WRTGJOPIRUGOIQ34THLDCJNVXZas'
socketio = SocketIO(app)
users = Db();
clients = []
count = 0


@app.route('/')
def sessions():
    return render_template('index.html')


@app.route('/chat')
def chat():
    return render_template('chat.html')


@socketio.on('message', namespace='/chat')
def handle_message(message):
    print("clientid:", request.namespace, request.sid)
    print(message)
    print(type(users.list_users()))
    if message['message'] == "/help":
        socketio.emit('message', {'user': 'SERVER', 'message': "Lol, trenger du hjelp?"},
                      room=request.sid, namespace='/chat')
    else:
        socketio.emit('message', message, namespace='/chat')


@socketio.on('auth')
def handle_auth(data):

    if not data['username'] and not data['password']:
        socketio.emit('success', {'message': "Enter username and password"}, room=request.sid)
    else:

        username = data['username']
        password = data['password']
        # if username does not exist
        if not users.check_user(username):
            users.add_user(username, password)
            socketio.emit('success', {'message': "OK"}, room=request.sid)

        else:
            # if user enter valid password
            if users.check_password(username, password):
                socketio.emit('success', {'message': 'OK'}, room=request.sid)
                # TODO: Deliver cookie with auth
            else:
                # if user enter wrong password
                users.add_user(username, password)
                socketio.emit('success', {'message': "Wrong password"}, room=request.sid)


@socketio.on('connect', namespace='/chat')
def connect():
    global count
    count = len(users.list_users())
    socketio.emit('count', {'count': count}, namespace='/chat')

    socketio.emit('user-list', {'users': users.list_users()}, namespace='/chat')


@socketio.on('disconnect', namespace='/chat')
def disconnect():
    global count
    count = len(users.list_users())
    socketio.emit('count', {'count': count}, namespace='/chat')

    socketio.emit('user-list', {'users': users.list_users()}, namespace='/chat')


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=4000, debug=True)
