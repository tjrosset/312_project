# import the Flask class from the flask module
from flask import Flask, render_template, redirect, url_for, request, session, send_from_directory
import pymongo
import bcrypt
from flask_socketio import SocketIO
import os
from werkzeug.utils import secure_filename


#client = pymongo.MongoClient("mongodb://localhost:27017/")
client = pymongo.MongoClient("mongo:27017")
db = client.get_database('total_records')
records = db.register

player = {
    "x_position": 100,
    "y_position": 100
}

loggedInPlayers ={}

player.update({"x_position": 200, "y_position": 200})
loggedInPlayers["Billy"] = player


# create the application object
app = Flask(__name__)
app.secret_key = "uyt$&%53dfJHJKru$%fg*()fit7d5"
socketio = SocketIO(app)

# base = os.path.dirname(os.path.abspath(__file__))
# app.config['UPLOAD_FOLDER'] = os.path.join(base,'uploads')
app.config['UPLOAD_FOLDER'] = './uploads'

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
        if user.find('&')!= -1 or user.find('<')!= -1 or user.find('>')!= -1:
            message = 'Username cannot contain these characters < > &'
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

@app.route('/uploads/<filename>')
def uploads(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],filename)


@app.route('/profile', methods=["GET","POST"])
def profile():
    if request.method == "POST":
        if 'email' in session:
            legal_extensions = {'png', 'jpg', 'jpeg'}
            
            message = "Changes Completed!"
            newemail = request.form.get("newemail")
            newpassword = request.form.get("newpassword")
            picture = request.form.get("picture")

            user = records.find_one({"email": session['email']})  

            userid = user["_id"]
            oldpassword = user['password']

            emailexists = records.find_one({"email": newemail})

            if emailexists:
                message += "Error Email already Exists!"
            elif newemail:
                newval = {"$set":{"email":newemail}} # query
                records.update_one({"email": session['email']},newval)
                message += "New Email Successful!"
                session['email'] = newemail

            if newpassword:
                if bcrypt.checkpw(newpassword.encode('utf8'), oldpassword):
                    message += "Error Old Password can't be the same as New Password!"
                elif newpassword:
                    hash = bcrypt.hashpw(newpassword.encode('utf-8'), bcrypt.gensalt())
                    newval = {"$set":{"password":hash}}
                    records.update_one({"email": session['email']},newval)
                    message += "New Password Successful!"

            if 'file' not in request.files:
                message += "No File Uploaded."

            elif request.files['file'].filename.rsplit('.',1)[1] in legal_extensions:
                file = request.files['file']
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))

                newval = {"$set":{"picture":filename}}
                records.update_one({"email": session['email']},newval)
                message += "Picture Upload Successful!"

            return render_template('profile.html', message=message)
        else:
            message = "Error"
            return render_template('profile.html', message=message)

    if 'email' in session:
        user =  records.find_one({"email": session['email']})  
        if user:
            username = user['name']
            ret = username
            ret = ret.replace('&','&amp')
            ret = ret.replace('>','&gt')
            ret = ret.replace('<','&lt')
            email = user['email']
            picture = user.get('picture')
            return render_template('profile.html', user=ret, email=email, picture=picture)
    
    message = "You're not logged In!"
    return render_template('profile.html',message = message)

@app.route('/game')
def game():
    if email.find('&') != -1:
        email.replace('&','&amp')

    if email.find('>') != -1:
        email.replace('>','&gt')

    if email.find('<') != -1:
        email.replace('<','&lt')

    return render_template('World.html', email=email)

@app.route('/logged_in')
def logged_in():
    if "email" in session:
        email = session["email"]
        userInfo = list(records.find({"email":email}))

        if(len(userInfo) == 0):
            session.pop("email", None)
            return redirect(url_for("login"))

        player = dict()
        player.update({"x_position": userInfo[0]["x_position"], "y_position": userInfo[0]["y_position"]})        
        loggedInPlayers[userInfo[0]["name"]] = player

        return render_template('World.html', name=userInfo[0]["name"])
    else:
        return redirect(url_for("login"))

@app.route("/logout", methods=["POST", "GET"])
def logout():
    if "email" in session:
        email = session["email"]
        session.pop("email", None)
        
        userInfo = list(records.find({"email":email}))
        records.update_one({"email": email },{ "$set":{"x_position": loggedInPlayers[userInfo[0]["name"]]["x_position"], "y_position": loggedInPlayers[userInfo[0]["name"]]["y_position"] } })
        userInfo = list(records.find({"email":email}))

        del loggedInPlayers[userInfo[0]["name"]]
        return render_template("logout.html")
    else:
        return render_template('index.html')

def SendAllPosition(position):
    if "email" in session:
        loggedInPlayers[position["name"]].update({"x_position": position["x_position"], "y_position": position["y_position"]})
        socketio.emit('allPositions', loggedInPlayers)

@socketio.on('SavedPosition')
def handle_my_custom_event():
    if "email" in session:
        socketio.emit('allPositions', loggedInPlayers)

@socketio.on('playerMoved')
def handle_my_custom_event(position):
    if "email" in session:
        SendAllPosition(position)
    #print('received new position: ' + str(position))

@socketio.on('allPositions')
def handle_my_custom_event(data):
    if "email" in session:
        emit('allPositions', data, broadcast=True)

@socketio.on('Message')
def handle_my_custom_event(json, methods=['GET', 'POST']):
    if "email" in session:
        socketio.emit('response', json)


 
#end of code to run it
if __name__ == "__main__":
    socketio.run(app, host='0.0.0.0', port=8000)
