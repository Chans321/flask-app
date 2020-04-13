import requests


payload = {'cont': "corona is a disease.It is a pandemic.It is a festival.",'question':"hey there"}
url = 'http://127.0.0.1:8000'
print("herehttp://127.0.0.1:8000/eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee")
ans = requests.post(url,data=payload)
print(ans.json())
