from flask_socketio import SocketIO
from flask_socketio import send, emit, join_room, leave_room, disconnect
import startup

app = startup.get_app()
socketio = SocketIO(app)

#sends message to back end to be dipslayed
@socketio.on('message')
def handle_message(data):
    print('received message: ' , data)
    room = data['room']
    username = data['username']

    emit("message", data, broadcast=False, to=room)

#listens for events on socket and recieves them
@socketio.on('my event')
def handle_my_custom_event(json):
    print('received json: ' + str(json))


#allows user to join room
@socketio.on('join')
def on_join(data):
    username = data['username']
    print(username)
    room = data['room']
    print(room)
    join_room(room)
    value = str(username) + ' ' + 'entered'
    emit("message", {'data': value}, to=room)

#allows user to leave room
@socketio.on('leave')
def on_leave(data): 
    print('inside')
    username = data['username']
    room = data['room']
    leave_room(room)
    print(room)
    value = str(username) + ' ' + "left"
    emit("message", {'data': value}, to=room)



   

