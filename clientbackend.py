from flask import Flask, request
import requests


app = Flask(__name__)
app.config['SESSION_COOKIE_NAME'] = None
@app.route("/login_endpoint_client", methods=["POST"])
def authtoken():
    authtok = request.get_json()
    print(authtok)
    data = {"cookie":"value"}
    resp  = requests.post("http://127.0.0.1:8080/vote", json=data)
    print(resp.text)
    return authtok

if __name__ == '__main__':
    app.run(debug=True, port=9000)
