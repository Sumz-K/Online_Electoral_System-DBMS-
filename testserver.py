from flask import Flask,request,jsonify,url_for,redirect,render_template

app=Flask(__name__)
@app.route("/otp", methods=['GET','POST'])
def otp():
    if request.method =='POST':
        n1 = request.form.get('digit1',0)
        n2 = request.form.get("digit2",0)
        n3 = request.form.get('digit3',0)
        n4 = request.form.get("digit4",0)
        print(n1+n2+n3+n4,type(n1))
        return jsonify({"good":"OTP"}),200
    return render_template("otp.html")
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