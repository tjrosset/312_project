from flask import Flask,render_template,redirect,url_for,request
app = Flask(__name__)

@app.route('/template')
def template():
    return render_template("template.html")

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/login')
def login():
    return render_template("login.html")

if __name__ == '__main__':
    app.run()