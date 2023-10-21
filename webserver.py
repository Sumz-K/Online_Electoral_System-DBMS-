from flask import Flask,request,jsonify,url_for,redirect,render_template,make_response
import requests
import datetime
import json
app=Flask(__name__)

@app.route("/otp", methods=['GET','POST'])
def otp():
    uid = request.cookies.get('username') 
    print("hello")
    print(uid)
    if uid is None:
            redirect(url_for("login_page"))
            return "failed"

    if request.method =='POST':
        
        n1 = request.form.get('digit1',0)
        n2 = request.form.get("digit2",0)
        n3 = request.form.get('digit3',0)
        n4 = request.form.get("digit4",0)
        opt = n1+n2+n3+n4
        
       
        
        
        if len(opt)==4:
            data = {"otp" :opt,
                "time" : str(datetime.datetime.now()),
                'uid' : uid}
            print(data)
            resp = requests.post("http://127.0.0.1:8000/check-otp",json=data)
            response = resp.json()
            if response['status'] == "accepted":
                return jsonify({"status":"OTP accepted"}),200
            else:
                return render_template("otp.html",error=" Invalid OTP")
    return render_template("otp.html")


@app.route("/login",methods=['GET','POST'])
def login_page():
    user_id=""
    if request.method == "POST":
        data = request.form.get("uid",None)
        user_id=data

        if data != None:
            data = {"UID":data,
                    'time':str(datetime.datetime.now())}
            resp = requests.post("http://127.0.0.1:8000/approval",json=data)
            print(resp.json())
            response = resp.json()
            if response['status'] == "yes":
                resp = make_response(redirect(url_for("otp"))) 
                resp.set_cookie('username', data["UID"])
               
                redirect(url_for("otp"))
                print(requests.get(f"http://127.0.0.1:8000/printotp/{user_id}"))
                return resp
            else:
                return render_template("login.html",error=" Invalid User ID")
                
            
            
    return render_template("login.html",)


@app.route("/server",methods=["GET","POST"])
def func():
    if request.method == 'POST':
        # this takes in name in html
        data = request.form.get("uid",None)
        print(data)
        return redirect(url_for("otp"))

    return jsonify({"error":"Invalid method"}),405

if __name__ == '__main__':
    app.run(debug=True)