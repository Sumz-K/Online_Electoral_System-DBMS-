import re
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
        cookie = data_dict.pop("cookie")
        pairs = list(data_dict.items())
        print(pairs)
        plain_string = ', '.join(f"{name}: {party}" for name, party in data_dict.items())
        session['cookie'] = cookie
        session['cookie_count'] = 1
        session['data_sent']=pairs
        print(val)
        return redirect(url_for('castyourvote'))



@app.route("/castyourvote")
def castyourvote():
        if "cookie" in session or request.cookies.get("authcheck"):
            print("lets see if cookie is there or not ====>",'cookie' in session)
            if 'cookie' in session:
                print(session['data_sent'],session['cookie'])
                resp = make_response(render_template("vote.html",data=session['data_sent']))
                resp.set_cookie("authcheck",session['cookie'],max_age=300)
                session.pop('cookie')
            else:
                response = requests.post("http://127.0.0.1:9000/retrieve",json={'cookie':request.cookies.get("authcheck")})
                response = response.json()
                if response['status'] == "not voted":
                    return render_template("vote.html",data=session['data_sent'])
                else:
                    return redirect(f'/red-casted/{str(dict({"cookie":response["cookie"]}))}')
            return resp
        else:
             return redirect(url_for("vote"))


@app.route("/red-casted/<jai>")
def red_casted(jai):
    dictt = eval(jai)
    print(dictt)
    session['cookie'] = dictt['cookie']
    return redirect(url_for("casted"))


@app.route("/casted")
def casted():
    # all the users can acces this page 
    if 'cookie' in session:
        resp = make_response(render_template("voted.html"))
        resp.set_cookie("authcheck",session['cookie'],max_age=300)
        session.pop("cookie")
        return resp
    else:
         return render_template("voted.html")

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
                return redirect(url_for('castyourvote'))
    
@app.route("/submit_vote", methods=["POST"])
def submit_vote():
    data = request.form.get('voted_contestant')
    cook = request.cookies.get("authcheck")
    data_to_be_sent = {
         "cookie":cook,
         'candidate': data
    }
    resp = requests.post("http://127.0.0.1:9000/writevote",json=data_to_be_sent)
    if resp.json()['status'] == 'OK':
         return redirect(url_for('casted'))
    return (resp.text)


import json

def array_to_json(array):
  """Converts a 2D array to a 2D JSON object."""
  json_array = []
  for row in array:
    json_row = []
    for element in row:
      json_row.append(element)
    json_array.append(json_row)
  return json.dumps(json_array)
@app.route('/result')
def result():
    res=requests.post("http://127.0.0.1:9000/showresult",json={})
    r=res.text
    r=eval(r)
        
    return render_template("showres.html",data=r)
if __name__ == '__main__':
    app.run(debug=True,port=8080)
