import requests
import datetime
data={"time":str(datetime.datetime.now()),"UID":"26252155"}

a=requests.post("http://127.0.0.1:5000/approval",json=data)

new_data={"uid":"26252155"}
b=requests.post("http://127.0.0.1:5000/toapp",json=new_data)
print(b.text)

# print(a.text)