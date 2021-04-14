# import the Flask class from the flask module
from flask import Flask, render_template, redirect, url_for, request, session
import pymongo
import bcrypt
from flask_socketio import SocketIO


client = pymongo.MongoClient("mongodb://localhost:27017/")
#client = pymongo.MongoClient("mongo:27017")
db = client.get_database('total_records')
records = db.register

player = {
    "name": "",
    "x_position": 100,
    "y_position": 100
}

loggedInPlayers ={
    "players": []
}

player.update({"name": "Billy", "x_position": 200, "y_position": 200})
loggedInPlayers["players"].append(player)


# create the application object
app = Flask(__name__)
app.secret_key = "uyt$&%53dfJHJKru$%fg*()fit7d5"
socketio = SocketIO(app)

@app.route("/", methods=['post', 'get'])
def index():
    message = ''
    if "email" in session:
        return redirect(url_for("logged_in"))
    if request.method == "POST":
        user = request.form.get("fullname")
        email = request.form.get("email")
        
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")
        
        user_found = records.find_one({"name": user})
        email_found = records.find_one({"email": email})
        if user_found:
            message = 'There already is a user by that name'
            return render_template('index.html', message=message)
        if email_found:
            message = 'This email already exists in database'
            return render_template('index.html', message=message)
        if password1 != password2:
            message = 'Passwords should match!'
            return render_template('index.html', message=message)
        else:
            hashed = bcrypt.hashpw(password2.encode('utf-8'), bcrypt.gensalt())
            user_input = {'name': user, 'email': email, 'password': hashed, 'x_position': 100, 'y_position': 100}
            records.insert_one(user_input)
            
            user_data = records.find_one({"email": email})
            new_email = user_data['email']
   
            return redirect(url_for("logged_in"))
    return render_template('index.html')

@app.route("/login", methods=["POST", "GET"])
def login():
    message = 'Please login to your account'
    if "email" in session:
        return redirect(url_for("logged_in"))

    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

       
        email_found = records.find_one({"email": email})
        if email_found:
            email_val = email_found['email']
            passwordcheck = email_found['password']
            
            if bcrypt.checkpw(password.encode('utf-8'), passwordcheck):
                session["email"] = email_val
                return redirect(url_for('logged_in'))
            else:
                if "email" in session:
                    return redirect(url_for("logged_in"))
                message = 'Wrong password'
                return render_template('login.html', message=message)
        else:
            message = 'Email not found'
            return render_template('login.html', message=message)
    return render_template('login.html', message=message)

@app.route('/game')
def game():
    return render_template('World.html', email=email)

@app.route('/logged_in')
def logged_in():
    if "email" in session:
        email = session["email"]
        userInfo = list(records.find({"email":email}))
        return render_template('World.html', name=userInfo[0]["name"])
    else:
        return redirect(url_for("login"))

@app.route("/logout", methods=["POST", "GET"])
def logout():
    if "email" in session:
        session.pop("email", None)
        return render_template("logout.html")
    else:
        return render_template('index.html')

def SendAllPosition():
    socketio.emit('allPositions', loggedInPlayers["players"])

@socketio.on('playerMoved')
def handle_my_custom_event(position):
    SendAllPosition()
    #print('received new position: ' + str(position))

@socketio.on('allPositions')
def handle_my_custom_event(data):
    emit('allPositions', data, broadcast=True)


 
#end of code to run it
if __name__ == "__main__":
    socketio.run(app, host='0.0.0.0', port=8000)
