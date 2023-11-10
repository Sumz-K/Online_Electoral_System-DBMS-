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
app.config['SESSION_COOKIE_NAME'] = None
cursor = mysql_conn.cursor()
cursor.execute("use contestants;")

@app.route("/login_endpoint_client/<data>", methods=["POST","GET"])
def authtoken(data):
    #data_obj=json.loads(data)
    
    json_string = data.replace("'", "\"")
    #print(json_string)
    json_data=json.loads(json_string)
    ward_num=(json_data['ward_no'])

    query=f"select name,political_party from candidate where ward_num={ward_num};"
    cursor.execute(query)
    res=cursor.fetchall()
    #print(res)
    data_dict = {name: party for name, party in res}
    final_str = json.dumps(data_dict)
    print((final_str))


    return redirect(f"http://127.0.0.1:8080/take/{final_str}")

@app.route("/retrieve",methods=["POST"])
def retrieve():
    data = request.get_json()
    val = data['cookie']
    



@app.route("/setsession",methods=["POST"])
def setss():
    data = request.get_json()
    print(data)
    return jsonify({'uri':"http://127.0.0.1:5000/login/API_key1"}),200



if __name__ == '__main__':
    app.run(debug=True, port=9000)
