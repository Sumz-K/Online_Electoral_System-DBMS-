import requests
import datetime
#data={"time":str(datetime.datetime.now()),"UID":"26252155"}

#a=requests.post("http://127.0.0.1:5000/approval",json=data)

# new_data={"uid":"26252155"}
# b=requests.post("http://127.0.0.1:5000/toapp",json=new_data)
# print(b.text)

info_data={"token":"3a68a01ab2fa54a8482fcaa71d9514e81e2573c06468885b334379a44d6f5fb1"}
c=requests.post("http://127.0.0.1:9000/login_endpoint_client",json=info_data)
print(c.text)

#print(a.text)