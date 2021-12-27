import flask
from flask import Flask,render_template,request,redirect
from flask import app
import re
app=Flask(__name__)

@app.route("/",methods=['GET','POST'])
def home():
    if request.method=='POST':
        return redirect('/add_data')
    return render_template('admin_login.html')

@app.route('/add_data')
def add_data():
    return render_template('add_data.html')

@app.route("/Player_details")
def Pdetails():
    return render_template('display.html')
app.run(debug=True)