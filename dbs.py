from os import name
from MySQLdb.cursors import Cursor
import flask
from flask import Flask,render_template,request,redirect,url_for,session
from flask_mysqldb import MySQL
#import MySQLdb.cursors
import re
app = Flask(__name__)

app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']='GDSiddu@3858'
app.config['MYSQL_DB']='mydatabase'
mysql=MySQL(app)
@app.route("/")
def f1():
    return render_template('home.html')

@app.route("/contacts")
def f2():
    return render_template('Contact_Us.html')

@app.route("/rankings")
def f3():
    return render_template('Batting_rankings.html')

@app.route("/odi")
def odi():
    return render_template('odi_ranking.html')

@app.route("/t20")
def t20():
    return render_template('t20_ranking.html')

@app.route("/B_rankings")
def branking():
    return render_template('bowling_ranking.html')

@app.route("/B_odi")
def b_odi():
    return render_template('B_odi.html')

@app.route("/B_t20")
def b_t20():
    return render_template('B_t20.html')


@app.route("/login",methods=['GET','POST'])
def f4():
    msg=''
    if request.method=='POST' and 'username' in request.form and 'password' in request.form:
        req=request.form
        username=req['username']
        password=req['password']
        cursor=mysql.connection.cursor()
        cursor.execute('select * from sign_up where username=%s and password=%s',(username,password,))
        account=cursor.fetchone()
        if account:
            msg='Logged in successfully'
            return redirect('/')
        else:
            msg='Incorrect username/password'
    return render_template('login.html',msg=msg)

@app.route("/admin-login",methods=['GET','POST'])
def admin_login():
    msg=''
    if request.method=='POST' and 'username' in request.form and 'password' in request.form:
        req=request.form
        username=req['username']
        password=req['password']
        cursor=mysql.connection.cursor()
        cursor.execute('select * from sign_up where username=%s and password=%s',(username,password,))
        account=cursor.fetchone()
        if account:
            msg='Logged in successfully'
            return redirect('/add_data')
        else:
            msg='Incorrect username/password'
    return render_template('admin_login.html',msg=msg)

@app.route('/add_data')
def add_data():
    return render_template('add_data.html')

@app.route("/Player_details")
def f5():
    return render_template('display.html')
    
@app.route("/sign-up",methods=['GET','POST'])
def sign_up(): 
    msg=''
    if request.method=='POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        req=request.form
        username=req['username']
        password=req['password']
        email=req['email']
        cursor=mysql.connection.cursor()
        cursor.execute('select * from sign_up where username=%s',(username,))
        account=cursor.fetchone()
        if account:
            msg='Account already exist'
        # elif not re.match(r'[^@]+@[^@]+\.[^@]+',email):
        #     msg='Invalid email'
        # elif not re.match(r'[A-Za-z0-9]+',username):
        #     msg='Username contains only letters and numbers'
        # elif not username or not password or not email:
        #     msg='Please fill out the form not entered'
        else:
            cursor.execute("INSERT INTO sign_up(username,password,email) VALUES (%s, %s,%s)",(username,password,email))
            mysql.connection.commit()
            msg='Successfully registerd'
            cursor.close()
            return redirect('/')
    elif request.method=='POST':
        msg='Please fill out the form hg'
    return render_template('sign_up.html',msg=msg)

app.run(debug=True)
