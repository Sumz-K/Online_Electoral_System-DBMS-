
from urllib import request
from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
app=Flask(__name__)
mysql_conn = mysql.connector.connect(
    host = "192.168.0.103",
    user = "ubuntu",
    password = "pass"
)






cursor = mysql_conn.cursor()
cursor.execute("use art_gallery;")

@app.route('/')
def index():
 
    cursor.execute("select * from art_order")
    data = cursor.fetchall()
    return render_template('index.html', data=data)

@app.route('/insert',methods=['GET','POST'])

def addrow():
    if request.method == 'POST':
        order_id = request.form.get('order_id', None)
        amount = request.form.get('amount', None)
        order_description = request.form.get('order_description', None)
        order_time = request.form.get('order_time', None)

       
        if order_id is None or amount is None or order_description is None or order_time is None:
            return "Error: Missing form fields."

        query = 'INSERT INTO art_order VALUES (%s, %s, %s, %s)'
        values = (order_id, amount, order_description, order_time)

        cursor.execute(query, values)
        mysql_conn.commit()
        return redirect(url_for('index'))

    return render_template('insert.html')


@app.route('/delete',methods=['GET','POST'])
def deleterow():
    if request.method == 'POST':
        id = request.form.get('del_order_id', None)
        
        print(id)
        if id is None:
            return "Error: Missing form fields."

        query = "DELETE from art_order where order_id=%s"

        cursor.execute(query, (id,))
        
        mysql_conn.commit()
        
        return redirect(url_for('index'))

    return render_template('delete.html')


if __name__ == '__main__':
    app.run(debug=True)
