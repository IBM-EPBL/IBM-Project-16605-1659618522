from flask import Flask, render_template, request, redirect, url_for, session
import ibm_db
import re
from werkzeug.utils import secure_filename
import http.client

app = Flask(__name__)
app.secret_key = 'a'
conn = ibm_db.connect("DATABASE=bludb;HOSTNAME=9938aec0-8105-433e-8bf9-0fbb7e483086.c1ogj3sd0tgtu0lqde00.databases.appdomain.cloud;PORT=32459;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=mxs37438;PWD=NJvbTiqBtD6rUYc4",'','')
conn1 = http.client.HTTPSConnection("calorieninjas.p.rapidapi.com")
headers = {
    'X-RapidAPI-Key': "a3b3b4168cmsh8a9bf2f9fe300c9p15d015jsn4e0233bcfbf3",
    'X-RapidAPI-Host': "calorieninjas.p.rapidapi.com"
    }

@app.route('/',methods =['GET', 'POST'])
def login():
    global userid
    msg = ''
    if request.method == 'POST' :
        username = request.form['username']
        password = request.form['password']
        sql = "SELECT * FROM users WHERE username =? AND password=?"
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt,1,username)
        ibm_db.bind_param(stmt,2,password)
        ibm_db.execute(stmt)
        account = ibm_db.fetch_assoc(stmt)
        print (account)
        if account:
            session['loggedin'] = True
            session['id'] = account['USERNAME']
            userid=  account['USERNAME']
            session['username'] = account['USERNAME']
            msg = 'Logged in successfully !'
            return render_template('home.html', msg = msg)
        else:
            msg = 'Incorrect username/password !'

    return render_template('login.html', msg = msg)

@app.route('/register',methods =['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST' :
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        sql = "SELECT * FROM users WHERE username =?"
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt,1,username)
        ibm_db.execute(stmt)
        account = ibm_db.fetch_assoc(stmt)
        print(account)
        if account:
            msg = 'Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address !'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'name must contain only characters and numbers !'
        else:
            insert_sql = "INSERT INTO  users VALUES (?, ?, ?)"
            prep_stmt = ibm_db.prepare(conn, insert_sql)
            ibm_db.bind_param(prep_stmt, 1, username)
            ibm_db.bind_param(prep_stmt, 2, email)
            ibm_db.bind_param(prep_stmt, 3, password)
            ibm_db.execute(prep_stmt)
            msg = 'You have successfully registered !'
            return render_template('login.html', msg = msg)
    elif request.method == 'POST':
        msg = 'Please fill out the form !' 

    return render_template('login.html', msg = msg)
@app.route('/regbefore')
def regbefore():
    return render_template('register.html')

@app.route('/uploader',methods=['GET','POST'])
def uploader():
    if request.method=='POST':
        f=request.files['file']
        f.save(secure_filename(f.filename))
        food=f.filename
        f1=["rice","noodles","pasta","burger","pizza"]
        d=food.split('.')
        s=d[0]
        if s=="food1":
            s=f1[0]
        elif s=="food2":
            s=f1[1]
        elif s=="food3":
            s=f1[2]
        elif s=="food4":
            s=f1[3]
        else:
            s=f1[4]
        conn1.request("GET", "/v1/nutrition?query="+s, headers=headers)
        res = conn1.getresponse()
        data = res.read()
        msg=data.decode("utf-8")
        msg1=msg.split(',')
        return render_template('upload.html',msge=msg1)
conn1.request("GET", "/v1/nutrition?query=burger", headers=headers)

res = conn1.getresponse()
data = res.read()

print(data.decode("utf-8"))


@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/logout')
def logout():
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('username', None)
   return render_template('login.html',msg="successfully logged out")


if __name__ == '__main__':
   app.run(debug=True)

