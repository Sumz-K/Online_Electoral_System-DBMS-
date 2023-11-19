from flask import Flask, request,redirect,session, jsonify
import requests
import mysql.connector
import json
import hashlib
from datetime import datetime,timedelta
app = Flask(__name__)
app.secret_key = "pass"
mysql_conn = mysql.connector.connect(
    host = "10.20.205.52",
    user = "ubuntu",
    password = "pass"
)
cursor = mysql_conn.cursor()
cursor.execute("use contestants;")

@app.route("/login_endpoint_client/<data>", methods=["POST","GET"])
def authtoken(data):
    #data_obj=json.loads(data)
    
    json_string = data.replace("'", "\"")
    #print(json_string)
    json_data=json.loads(json_string)
    ward_num=(json_data['ward_no'])

    query=f"select name,political_party,candidate_id from candidate where ward_num={ward_num};"
    cursor.execute(query)
    res=cursor.fetchall()
    #print(res)
    cursor.execute(f"select voting_status from voted where user_id = {json_data['uid']}")
    ret = cursor.fetchall()
    ttl = datetime.now()+timedelta(minutes=3)
    cookie = hashlib.sha256((str(json_data['uid'])+str(ttl)).encode('utf-8')).hexdigest()
    
    if len(ret)==0:
        # we should send a cookie 
        cursor.execute("LOCK tables voted write, cookie_jar write")
        insert_voted_query = "INSERT INTO voted (user_id, voting_status) VALUES (%s, 'no')"
        cursor.execute(insert_voted_query, (json_data['uid'],))

        insert_cookie_query = "INSERT INTO cookie_jar (cookie, userid, ttl) VALUES (%s, %s, %s)"
        cursor.execute(insert_cookie_query, (cookie, json_data['uid'], ttl))
        cursor.execute("UNLOCK tables")
        data_dict = {name: [party,ids] for name, party,ids in res}
        data_dict["cookie"] = cookie
        final_str = json.dumps(data_dict)
        print((final_str))
        return redirect(f"http://127.0.0.1:8080/take/{final_str}")
    elif ret[0][0] == 'no':
        # send a cookie 
        cursor.execute("LOCK tables cookie_jar write")
        insert_cookie_query = "INSERT INTO cookie_jar (cookie, userid, ttl) VALUES (%s, %s, %s)"
        cursor.execute(insert_cookie_query, (cookie, json_data['uid'], ttl))
        cursor.execute("UNLOCK tables")
        data_dict = {name: [party,ids] for name, party,ids in res}
        data_dict["cookie"] = cookie
        final_str = json.dumps(data_dict)
        print((final_str))
        return redirect(f"http://127.0.0.1:8080/take/{final_str}")
    else:
        data_dict = {'cookie':cookie}
        final_str = json.dumps(data_dict)
        print((final_str))
        return redirect(f"http://127.0.0.1:8080/red-casted/{final_str}")


@app.route("/retrieve",methods=["POST"])
def retrieve():
    data = request.get_json()
    val = data['cookie']
    cursor.callproc('checkstatus', (val,))
    for result in cursor.stored_results():
        rows = result.fetchall()
        for row in rows:
            status = row
    print(status)
    if status[0] == 'no':
        return jsonify({'status':"not voted",}),200
    else:
        return jsonify({"status":'Yes','cookie':val}),200
    
    
@app.route("/writevote", methods=["POST"])
def write():
    data = request.get_json()
    query = "select userid from cookie_jar where cookie = %s"
    cursor.execute(query,(data['cookie'],))
    uid = cursor.fetchall()
    uid = uid[0][0]
    cursor.execute("lock tables voted write,candidate write")
    update_query = "UPDATE voted SET voting_status = %s WHERE user_id = %s"
    cursor.execute(update_query, ("yes", uid))
    cid = eval(data['candidate'])
    update_query = "UPDATE candidate SET votes = votes+1 WHERE candidate_id = %s"
    cursor.execute(update_query, (cid[1],))
    mysql_conn.commit()
    cursor.execute("unlock tables")
    return jsonify({"status":"OK"}),200





@app.route("/setsession",methods=["POST"])
def setss():
    data = requests.get_json()
    print(data)
    return jsonify({'uri':"http://127.0.0.1:5000/login/API_key1"}),200

@app.route("/showresult",methods=['GET','POST'])
def showres():
    cursor.execute("select * from results;")
    return cursor.fetchall()




if __name__ == '__main__':
    app.run(debug=True, port=9000)
