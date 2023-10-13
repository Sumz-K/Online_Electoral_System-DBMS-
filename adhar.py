##Throwaway

from urllib import request
from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
import random
app=Flask(__name__)
mysql_conn = mysql.connector.connect(
    host = "192.168.0.103",
    user = "ubuntu",
    password = "pass"
)






cursor = mysql_conn.cursor()
cursor.execute("use adhar;")
cursor.fetchall()

names=["Tejas A Kumar","Sumukh Kowndinya","Tarun Ramanujam","Thaleen CN","Saranya Rubini"]

dob=["2003-09-29","2003-12-07","2003-07-17","2003-04-12","1986-01-01"]

addr=["Banshankari","Talaghattapura","Girinagar","Malur","Coimbatore"]

state=["Karnataka","Karnataka","Karnataka","Karnataka","Tamil Nadu"]

uid=[random.randint(10000000,99999999) for i in range(5) ]

zip_code=[random.randint(100000,999999) for i in range(5) ]

ward=[random.randint(1000,9999) for i in range(5) ]

house=[random.randint(1,999) for i in range(5) ]

# cursor.execute('show databases')
# print(cursor.fetchall())

for i in range(5):
    query="INSERT INTO details VALUES (%s, %s, %s, %s,%s,%s,%s,%s);"
    values=(names[i],uid[i],dob[i],zip_code[i],ward[i],house[i],addr[i],state[i])

    cursor.execute(query,values)
    mysql_conn.commit()



