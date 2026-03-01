import requests
url='http://127.0.0.1:5000/predict'
files={'xray': open(r'D:\overflow\OsteoAI\dataset\train\Normal\Normal 1.png','rb')}
data={'name':'Jane Doe','age':'45','sex':'Female','height':'160','weight':'55','phone':'555-1234','email':'jane@example.com'}
resp=requests.post(url,data=data,files=files)
print(resp.status_code)
print(len(resp.text))
print(resp.text[:200])
