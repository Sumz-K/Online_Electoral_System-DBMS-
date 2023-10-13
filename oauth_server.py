from time import time
from urllib import request

from flask import Flask, render_template, request, redirect, url_for,jsonify
import mysql.connector
import random
import time
import json
import hashlib

import datetime

app=Flask(__name__)
mysql_conn = mysql.connector.connect(
    host = "192.168.0.103",
    user = "ubuntu",
    password = "pass"
)
cursor = mysql_conn.cursor()
cursor.execute("use adhar;")

#App id, UID, time(current time)
#Populate the other table 'token' : ID---> UID from details
#Function will generate hash 
#Time goes to access in tokens table

@app.route('/approval',methods=['GET','POST'])
def gettokens():
    data=request.get_json()
    cur_time=datetime.datetime.strptime(data["time"], '%Y-%m-%d %H:%M:%S.%f')
    #print(cur_time[0:19])
    uid=data["UID"]
    cur_time1 = str(cur_time)
    h=hashlib.sha256()
    h.update((cur_time1+uid).encode())
    
    hashed=h.hexdigest()
   
    query="insert into sessions values(%s,%s,%s,%s)"
    dynamic_ttl = cur_time + datetime.timedelta(minutes=10)
    dynamic_ttl = str(dynamic_ttl)[:19]
    values=(hashed,cur_time,dynamic_ttl,uid)
    cursor.execute(query,values)
    mysql_conn.commit()
    
    dummy_dict={"A":"B"}
    return jsonify(dummy_dict),200

@app.route("/toapp",methods=['GET','POST'])
def timetolive():
    # uid=123
    # ttl=Query
    # if ttl>0 return flag
    # else return "redirect"

    data=request.get_json()
    uid=data["uid"]
    query=f"select ttl from sessions where id={uid}"
    cursor.execute(query)
    time_str=(cursor.fetchall()[0][0])
    
    if datetime.datetime.now()<time_str:
        valid={"Status":"Active"}
        return valid,200
    else:
        invalid={"Status":"Invalid"}
        return invalid,302
    # dummy={"A":"B"}
    # return dummy
    
    

if __name__ == '__main__':
    app.run(debug=True)
