from flask import Flask, request,redirect,session, jsonify
import requests
import mysql.connector
import json
app = Flask(__name__)
app.secret_key = "pass"
mysql_conn = mysql.connector.connect(
    host = "192.168.0.107",
    user = "ubuntu",
    password = "pass"
)

cursor = mysql_conn.cursor()
cursor.execute("use contestants;")
cursor.execute("select voting_status from voted where user_id = 26252155")
print(cursor.fetchall())