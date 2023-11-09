from flask import Flask, render_template, request, redirect, url_for,make_response

app=Flask(__name__)

@app.route("/")
def home():
    return "check the url"
if __name__ == '__main__':
    app.run(debug=True,port=15000)