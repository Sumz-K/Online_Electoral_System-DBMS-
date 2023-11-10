from flask import Flask, request,redirect,session, jsonify
import requests


app = Flask(__name__)
app.secret_key = "pass"

@app.route("/login_endpoint_client/<data>", methods=["POST","GET"])
def authtoken(data):
    return redirect(f"http://127.0.0.1:8080/take/{data}")

@app.route("/setsession",methods=["POST"])
def setss():
    data = request.get_json()
    print(data)
    return jsonify({'uri':"http://127.0.0.1:5000/login/API_key1"}),200



if __name__ == '__main__':
    app.run(debug=True, port=9000)
