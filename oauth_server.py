from time import time
from urllib import request
import threading
from flask import Flask, render_template, request, redirect, url_for,jsonify
import mysql.connector
import random
import time
import json
import hashlib

import datetime

app=Flask(__name__)
mysql_conn = mysql.connector.connect(
    host = "192.168.0.104",
    user = "ubuntu",
    password = "pass"
)
cursor = mysql_conn.cursor()
cursor.execute("use adhar;")



def remove():
    thread_cursor = mysql_conn.cursor()
    thread_cursor.execute("USE adhar;")
    while True:
        
        thread_cursor.execute("LOCK TABLES otp write")
        try:
            current = datetime.datetime.now()
            thread_cursor.execute(f"DELETE FROM otp WHERE ttl < '{current}'")
            mysql_conn.commit()
        except mysql.connector.Error as err:
            # Handle errors, print or log them as needed
            print(f"Error: {err}")
            mysql_conn.rollback()
        finally:
            thread_cursor.execute("UNLOCK Tables")
        time.sleep(1)

t = threading.Thread(target=remove)
t.daemon = True
t.start()

@app.route("/login",methods=['GET','POST'])
def login():
    if request.method == 'POST':
        data = request.form.get("uid",None)
        cursor.execute("")

    









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
    print(uid)
    q = "select * from details where uid = %s;"
    v = (uid,)
    cursor.execute(q,v)
    see = cursor.fetchall()
    print(see)
    if len(see) != 0:
        cur_time1 = str(cur_time)
        h=hashlib.sha256()
        h.update((cur_time1+uid).encode())
    
        hashed=h.hexdigest()
   
        query="insert into sessions values(%s,%s,%s,%s)"
        dynamic_ttl = cur_time + datetime.timedelta(minutes=3)
        dynamic_ttl = str(dynamic_ttl)[:19]
        values=(hashed,cur_time,dynamic_ttl,uid)
        cursor.execute(query,values)
        mysql_conn.commit()
        query = 'insert into otp values(%s,%s,%s)'
        values = (uid,random.randint(1000,9999),str(cur_time+datetime.timedelta(minutes=3))[:19])
        cursor.execute(query,values)
        mysql_conn.commit()
        dummy_dict={"status":"yes"}
        return jsonify(dummy_dict),200
    else:
        ret = {"status":"no"}
        return jsonify(ret),200
    
def compare(lst):
    for i in range (len(lst)):
        lst[i]=lst[i][0]

@app.route("/check-otp",methods=['GET',"POST"])
def otp_check():
    data=request.get_json()
    print(data)
    cur_time=datetime.datetime.strptime(data["time"], '%Y-%m-%d %H:%M:%S.%f')
    #print(cur_time[0:19])
    uid=data["uid"]
    query = 'select code from otp where id = %s'
    val = (uid,)
    cursor.execute(query,val)
    val = cursor.fetchall()
    compare(val)
    print(val,type(val[0]))

    if int(data['otp']) in val:
        return jsonify({"status":"accepted"}),200

    return jsonify({"status":"rejected"}),200

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
    cur_time=datetime.datetime.now()
    if datetime.datetime.now()<time_str:
        valid={"Status":"Active"}
        return valid,200
    else:

        invalid={"Status":"Invalid"}
        query=f"delete from sessions where ttl<{cur_time}"
        return invalid,302
    # dummy={"A":"B"}
    # return dummy
    
@app.route("/fetch",methods=['GET','POST'])

def getinfo():
    data=request.get_json()
    tkn=data["token"]
    print(tkn)
    query=f"""
    SELECT d.name, d.zip, d.ward_no
    FROM details d
    WHERE EXISTS (SELECT id FROM sessions 
    WHERE id = d.uid AND token = '{tkn}');
    """
    #query_dummy = f"select id from sessions where token='{tkn}';"
    cursor.execute(query)
    
    return (cursor.fetchall()),200
    

    


    

if __name__ == '__main__':
    app.run(debug=True, port=8000)