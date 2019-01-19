from flask import Flask, render_template
from flask_socketio import SocketIO, join_room, leave_room
from Database import Db
import flask-login

app = Flask(__name__)
app.config['SECRET_KEY'] = 'WRTGJOPIRUGOIQ34THLDCJNVXZas'
socketio = SocketIO(app)
users = Db();
count = 0


@app.route('/login', methods=['GET', 'POST'])
def login():
    next = get_redirect_target()
    if request.method == 'POST':
        # login code here
        return redirect_back('index')
    return render_template('index.html', next=next)


@app.route('/')
def sessions():
    return render_template('index.html')


@app.route('/chat')
def chat():
    return render_template('chat.html')


@socketio.on('connect', namespace='/chat')
def test_connect():
    socketio.emit('my response', {'data': 'Connected'})

@socketio.on('message', namespace='/chat')
def handle_message(message):
    print(message)
    socketio.emit('message', message)


@socketio.on('auth')
def handle_auth(data):

    if not data['username'] and not data['password']:
        socketio.emit('success', {'message': "Enter username and password"})
    else:

        username = data['username']
        password = data['password']
        # if username does not exist
        if not users.check_user(username):
            users.add_user(username, password)
            socketio.emit('success', {'message': "OK"})

        else:
            # if user enter valid password
            if users.check_password(username, password):
                socketio.emit('success', {'message': 'OK'})
                socketio.
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
