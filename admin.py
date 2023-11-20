from time import time
from urllib import request
import threading
from flask import Flask, render_template, request, redirect, url_for,jsonify
import mysql.connector
import random
import time
import requests
import hashlib

import datetime

app=Flask(__name__)
mysql_conn = mysql.connector.connect(
    host = "10.20.202.132",
    user = "ubuntu",
    password = "pass"
)
app.config['SESSION_COOKIE_NAME'] = None
cursor = mysql_conn.cursor()
cursor.execute("use contestants;")
lst=[]
cursor.execute("select ward_num from candidate;")
lst=cursor.fetchall()
for i in range(len(lst)):
    lst[i]=lst[i][0]

lst=list(set(lst))
admins={"sumukh":"abc", "tejas":"xyz"}

@app.route("/adminlogin",methods=['GET','POST'])
def adminlogin():
    if request.method=='POST':
        username=request.form.get('user')
        passw=request.form.get('password')
        if username in admins and admins[username]==passw:
            return redirect(url_for("adminmain"))
    return render_template("adminlogin.html")

@app.route("/adminmain",methods=['GET','POST'])
def adminmain():
    return render_template("adminmain.html")

@app.route("/release_results",methods=['GET','POST'])
def release():
    if request.method=='POST':
        for i in lst:
            query=f"select c.name,co.name as const_name,political_party from candidate c join constituency co where c.ward_num=co.ward_num and c.ward_num={i} and votes=(select max(votes) from contestants.candidate where ward_num={i});"
            print("hello")
            cursor.execute(query)
            a=cursor.fetchall()
            name=a[0][0]
            party=a[0][2]
            ward_name=a[0][1]
            vals=(ward_name,party,name)
            print(a)
            query_new="insert into results values (%s,%s,%s)"
            cursor.execute(query_new,vals)
            mysql_conn.commit()
    return "Done"
@app.route("/deletecandidate",methods=['DELETE','POST'])
def deletecan():
    if request.method=='POST':
        cand_id=request.form.get("candidate_id")
        query="delete from candidate where candidate_id=(%s)"
        value=(cand_id,)
        cursor.execute(query,value)
        mysql_conn.commit()
        return f"Candidate with UID {cand_id} deleted",201
        









if __name__=='__main__':
    app.run(debug=True, port=7000)
