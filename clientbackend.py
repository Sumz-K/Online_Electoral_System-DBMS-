from flask import Flask, request

app = Flask(__name__)

@app.route("/login_endpoint_client", methods=["POST"])
def authtoken():
    authtok = request.get_json()
    print(authtok)
    return authtok

if __name__ == '__main__':
    app.run(debug=True, port=9000)
