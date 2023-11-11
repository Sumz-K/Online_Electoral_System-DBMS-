from flask import Flask, redirect, url_for,render_template,request,make_response,session,jsonify
import requests
app = Flask(__name__)
app.secret_key = "P@$$c0de"
import json
@app.route("/")
def home():
    return render_template("index.html")

@app.route('/support')
def support():
    # Replace 'support_page_url' with the actual URL of your support page.
    return render_template("support.html")


@app.route("/take/<val>")
def postvote(val):
        data_dict=eval(val)
        pairs = list(data_dict.items())
        print(pairs)
        plain_string = ', '.join(f"{name}: {party}" for name, party in data_dict.items())
        session['cookie'] = "check cookie"
        session['cookie_count'] = 1
        session['data_sent']=pairs
        print(val)
        return redirect(url_for('castyourvote'))



@app.route("/castyourvote")
def castyourvote():
        if "cookie" in session or request.cookies.get("authcheck"):
            if 'cookie' in session:
                print(session['data_sent'])
                resp = make_response(render_template("vote.html",data=session['data_sent']))
                resp.set_cookie("authcheck",session['cookie'],max_age=300)
                session.pop('cookie')
            else:
                response = requests.post("http://127.0.0.1:9000/retrieve",json={'cookie':request.cookies.get("authcheck")})
                if response['status'] == "not voted":
                    return render_template("vote.html",data=session['data_sent'])
                else:
                    return redirect(f'/casted/{response["cookie"]}')
            return resp
        else:
             return redirect(url_for("vote"))


@app.route("/casted/<jai>")
def casted(jai):
    resp = make_response(render_template("voted.html"))
    resp.set_cookie("authcheck",jai)
    return resp

@app.route('/vote', methods=["GET","POST"])
def vote():
    if request.method == "GET":
        cook = request.cookies.get("authcheck")
        print("cookie",cook)
        if cook == None:
                resp = requests.post("http://127.0.0.1:9000/setsession",json={"a":"b"})
                print(resp)
                return redirect(resp.json().get("uri"))
                
        if cook:
                session['cookie'] = cook
                return redirect(url_for('castyourvote'))
    


@app.route('/result')
def result():
    return render_template("result.html")
if __name__ == '__main__':
    app.run(debug=True,port=8080)
