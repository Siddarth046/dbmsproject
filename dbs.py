from os import name
import flask
from flask import Flask,render_template,request,redirect,url_for,session
#import MySQLdb.cursors
from flask_mysqldb import MySQL
import re
app = Flask(__name__)


app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='newuser'
app.config['MYSQL_PASSWORD']='realme3pro'
app.config['MYSQL_DB']='cricket'

mysql=MySQL(app)
@app.route("/")
def f1():
    return render_template('home.html')

@app.route("/contacts")
def f2():
    return render_template('Contact_Us.html')

@app.route("/details")
def f3():
    return render_template('details.html')

@app.route("/login",methods=['GET','POST'])
def f4():
    if request.method=='POST':
        userDeatils=request.form
        Username=userDeatils['name']
        Password=userDeatils['password']
        # Username=request.form('name')
        # Password=request.form('password')
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO accounts(username,password) VALUES (%s, %s)", (Username, Password))
        mysql.connection.commit()
        cur.close()
        return redirect('/')
    return render_template('login.html')

@app.route("/Player_details")
def f5():
    return render_template('display.html')
    
app.run(debug=True)
from flask import Flask,render_template,request,redirect
from flask_mysqldb import MySQL
import MySQLdb.cursors

app = Flask(__name__)
