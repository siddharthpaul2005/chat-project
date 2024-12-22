from flask import Flask,render_template,request
from flask_socketio import SocketIO, emit
import random

# create the class and the instance (⓿_⓿)

app = Flask (__name__)        # the app
socketio = SocketIO(app)    #inctance 

#python dictionary to store all the users . Kay is the socketID and username is avatarUrl

users = {}


#if domeone visits this place then th index.html will be rendered
@app.route('/')
def index():
         return render_template('index.html')

# we are listening to connection events ( this is for the when the user connects)
@socketio.on("connect")
def handel_connet():
        username = f"User_{random.randint(1000,9999)}"
        gender =  random.choice(["girl","boy"])
        avatar_url = f" https://avatar.iran.liara.run/public/{gender}?username={username} "

        users[request.sid] = {"username": username, "avatar":avatar_url}

        emit("user_joined", {"username":username,"avatar":avatar_url},broadcast=True)
        emit("set_username", {"username":username})
#for the dissconnect events ✍️(◔◡◔)
@socketio.on("disconnect")
def handle_disconnect():
    user = users.pop(request.sid, None)
    if user:
      emit("user_left", {"username":user["username"]},broadcast=True)
# sending meassages homie
@socketio.on("send_message")
def handle_message(data):
    user = users.get(request.sid)
    if user:
        emit("new_message", {
            "username":user["username"],
            "avatar":user["avatar"],
            "message":data["message"]
        }, broadcast=True)
# skibidy skibidy skibidy skibidy skibidy skibidy gyat gyat gyat gyat suss suss ankur is suss
@socketio.on("update_username")
def handle_update_username(data):
    old_username = users[request.sid]["username"]
    new_username = data["username"]
    users[request.sid]["username"] = new_username

    emit("username_updated", {
        "old_username":old_username,
        "new_username":new_username
    }, broadcast=True)

if __name__ == "__main__":  
        socketio.run(app)   #to initialise the socket and flask in out application
        socketio.run(app, debug=True)