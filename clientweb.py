from flask import Flask, redirect, url_for,render_template,request
app = Flask(__name__)
@app.route("/")
def home():
    return render_template("index.html")

@app.route('/support')
def support():
    # Replace 'support_page_url' with the actual URL of your support page.
    return render_template("support.html")

@app.route('/vote', methods=["GET","PSOT"])
def vote():
    if request.method == "GET":
        cook = request.cookies.get("session")
        if cook == None:
            return redirect("http://127.0.0.1:5000/login/API_key1")
        else:
            return render_template("vote.html")
    
@app.route('/result')
def result():
    return render_template("result.html")
if __name__ == '__main__':
    app.run(debug=True,port=8080)
