from flask import Flask, render_template, request, make_response
from flask_socketio import SocketIO, disconnect
from Database import Db
import uuid

app = Flask(__name__)
socketio = SocketIO(app)
users = Db()
active_users = []
user_count = 0


@app.route('/')
def sessions():
    session_id = str(uuid.uuid4())
    resp = make_response(render_template('index.html'))
    resp.set_cookie("session_id", session_id)
    return resp


@app.route('/chat')
def chat():
    return render_template('chat.html')


@socketio.on('isalive', namespace='/chat')
def handle_ping(data):
    print("received ping from: ", data['session_id'])
    active_users.append(data['session_id'])


@socketio.on('message', namespace='/chat')
def handle_message(message):
    print(message)
    if not message['session_id']:
        socketio.emit('message', {'user': 'SERVER', 'message': "Not authorized. You have to login."},
                      room=request.sid, namespace='/chat')
    if message['message'] == "/help":
        socketio.emit('message', {'user': 'SERVER', 'message': "Lol, trenger du hjelp?"},
                      room=request.sid, namespace='/chat')
    else:
        if message['message']:
            if "<" in message['message'] and ">" in message['message']:
                return

            if users.check_sid(message['user'], message['session_id']):
                socketio.emit('message', message, namespace='/chat')
            else:
                # reply "error" when not logged in
                socketio.emit('no-session', {'session': 'error'},
                              room=request.sid, namespace='/chat')


@socketio.on('auth')
def handle_auth(data):

    if not data['username'] and not data['password']:
        socketio.emit('success', {'message': "Enter username and password"}, room=request.sid)
    else:

        username = data['username']
        password = data['password']
        sid = data['session_id']
        # if username does not exist
        if not users.check_user(username):
            users.add_user(sid, username, password)
            socketio.emit('success', {'message': "OK"}, room=request.sid)

        else:
            # if user enter valid password
            if users.check_password(username, password):
                users.update_sid(username, sid)
                socketio.emit('success', {'message': 'OK'}, room=request.sid)
            else:
                # if user enter wrong password
                socketio.emit('success', {'message': "Wrong password"}, room=request.sid)


@socketio.on('connect', namespace='/chat')
def connect():
    global user_count
    user_count = len(users.list_users())

    socketio.emit('count', {'count': user_count}, namespace='/chat')
    socketio.emit('user-list', {'users': users.list_users()}, namespace='/chat')


@socketio.on('disconnect', namespace='/chat')
def disconnect():
    global user_count
    users.del_users(active_users)
    user_count = len(users.list_users())
    socketio.emit('user-list', {'users': users.list_users()}, namespace='/chat')
    socketio.emit('count', {'count': user_count}, namespace='/chat')


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=4000)
