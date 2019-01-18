from flask import Flask, render_template
from flask_socketio import SocketIO

app = Flask(__name__)
app.config['SECRET_KEY'] = 'WRTGJOPIRUGOIQ34THLDCJNVXZas'
socketio = SocketIO(app)


@app.route('/')
def sessions():
    return render_template('index.html')


@socketio.on('message')
def handle_message(message):
    # ('received message: ', message['user'], message['message'])
    if message['message']:
        socketio.emit('message', message)


count = 0


@socketio.on('connect')
def connect():
    global count
    count += 1
    print("count=", count)
    socketio.emit('count', {'count': count})


@socketio.on('disconnect')
def disconnect():
    global count
    count -= 1
    print("count=", count)
    socketio.emit('count', {'count': count})


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=4000)
