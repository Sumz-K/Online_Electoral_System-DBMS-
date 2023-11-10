from urllib import request
from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
import random
app=Flask(__name__)
mysql_conn = mysql.connector.connect(
    host = "192.168.0.107",
    user = "ubuntu",
    password = "pass"
)






cursor = mysql_conn.cursor()
cursor.execute("use adhar;")
cursor.fetchall()

names=["RV Iyer","Kushal Raghuveer","Karthik K","Ali Hussain","Miguel Diaz"]

dob=["1975-01-11","2003-11-11","2003-09-07","1998-05-05","2002-01-01"]

addr=["Coimbatore","Banashankari","Kathriguppe","Dsouza nagar","Leeraj"]

state=["Tamil Nadu","Karnataka","Karnataka","Karnataka","Madhya Pradesh"]

uid=[random.randint(10000000,99999999) for i in range(5) ]

zip_code=[random.randint(100000,999999) for i in range(5) ]

ward=[6553,9669,1121,1121,300]

house=[random.randint(1,999) for i in range(5) ]

# cursor.execute('show databases')
# print(cursor.fetchall())

for i in range(5):
    query="INSERT INTO details VALUES (%s, %s, %s, %s,%s,%s,%s,%s);"
    values=(names[i],uid[i],dob[i],zip_code[i],ward[i],house[i],addr[i],state[i])

    cursor.execute(query,values)
    mysql_conn.commit()