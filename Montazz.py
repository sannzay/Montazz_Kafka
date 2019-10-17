from flask import Flask, render_template, session, redirect, request, url_for
from pymongo import MongoClient
from ProducerKafka import video_emitter

app = Flask(__name__)

client = MongoClient()
db = client.registration


@app.route('/')
def index():
    if 'username' in session:
        return render_template("home.html", users=session['username'])
    return render_template("index.html")


@app.route('/signUp', methods=["POST"])
def signUp():
    name = str(request.form["fullname"])
    password = str(request.form["password"])
    email = str(request.form["email"])
    post = {
        "username": name,
        "password": password,
        "useremail": email
    }
    collection = db.users
    ids = collection.insert_one(post).inserted_id
    return redirect(url_for('index'))


@app.route('/SignUp')
def SignUp():
    return render_template("SignUp.html")


@app.route('/signOut', methods=["POST"])
def signOut():
    session.pop('username')
    return redirect(url_for('index'))


@app.route('/check', methods=["POST"])
def check():
    email = str(request.form["email-id"])
    password = str(request.form["passkey"])
    collection = db.users
    users = collection.find_one({"useremail": email})
    if users:
        if password == users["password"]:
            session['username'] = users['username']
            return redirect(url_for('index'))
        else:
            return 'user not available'
    else:
        return 'user not available'


@app.route('/file', methods=["POST"])
def file():
    if 'username' in session:
        return render_template("FileUpload.html", name=session['username'])
    return render_template("index.html")


@app.route('/produce', methods=["POST"])
def produce():
    if 'username' in session:
        
        video_emitter()
        return render_template('FinishUpload.html')
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.secret_key = 'mysecretkey'
    app.run()
