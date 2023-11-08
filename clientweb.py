from flask import Flask, redirect, url_for,render_template,request,make_response
app = Flask(__name__)
app.config['SESSION_COOKIE_NAME'] = None

@app.route("/")
def home():
    return render_template("index.html")

@app.route('/support')
def support():
    # Replace 'support_page_url' with the actual URL of your support page.
    return render_template("support.html")

@app.route('/vote', methods=["GET","POST"])
def vote():
    if request.method == "GET":
        cook = request.cookies.get("authcheck")
        print("cookie",cook)
        if cook == None:
            return redirect("http://127.0.0.1:5000/login/API_key1")
            
        if cook:
            return render_template("vote.html")
    if request.method == 'POST':
        data = request.get_json()
        resp = make_response(render_template("vote.html"))
        print(data['cookie'])
        resp.set_cookie("authcheck",data['cookie'],max_age=300)
        return resp
    
@app.route('/result')
def result():
    return render_template("result.html")
if __name__ == '__main__':
    app.run(debug=True,port=8080)
