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
    print("message=", message)
    if message['message']:
        socketio.emit('message', message)
    # if message['message']:
    #     socketio.emit('message', message)
    try:
        if message['username'] and message['password']:
                if users.check_user(message['username']):
                    users.add_user(message['username'], message['password'])
    except KeyError:
        pass



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
