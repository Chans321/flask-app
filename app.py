from flask import Flask   
from flask import request
from flask import jsonify        
from flask import render_template
from getLatestNews import send_news
from searchQuestion import get_all_data
import requests
from flask import Response

#from qa import answer_the_question
app = Flask(__name__)
import time            


titles=[] 

news=[]



list_of_states = requests.get("https://api.covid19india.org/state_district_wise.json").json().keys()

res={}
for i in list_of_states:
	res[i]=0

def event_stream(state):
	print(state)
	di = get_numbers()
	if(state!="None" and di[state]!=res[state]  ):
		yield "data: {}\n\n".format(di[state])
		res[state]=di[state]
		print("yooooooooooooooooooooo")
    

def get_numbers():
	a = requests.get("https://api.covid19india.org/state_district_wise.json").json()
	di = {}
	for state in list(a.keys()):
		di[state] = 0;
		for i in list(a[state]['districtData'].keys()):

			di[state] += a[state]['districtData'][i]['confirmed'] + a[state]['districtData'][i]['delta']['confirmed']

	return di





@app.route("/")
def hello():                 
    return  render_template('index.html',titles=titles, news=news)

@app.route("/getreply")
def reply_for_question():
	print(request.args['q'])
	print("***********************************************************************************************\n")
	data = get_all_data(request.args['q'])
	a=[]
	for i in data:
		s = '.'.join(i)
		a.append(s)
	cont = '.'.join(a)
	print(data)
	print("__________________________________________________________________________________________________")
	#ans = answer_the_question(equest.args['q'],data)
	payload = {'infor': '123','question':request.args['q'],'cont':cont}
	url = 'http://127.0.0.1:8000'
	print("herehttp://127.0.0.1:8000/eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee")
	print(len(data))
	ans = requests.post(url, data=payload).json()
	print("ssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssss")
	return jsonify(username="dedef",
                   text=ans['ans'],
                   id="34")


@app.route('/api/stream')
def stream():
	#print(request.q)
	print(request.args['q'])
	return Response(event_stream(request.args['q']), mimetype="text/event-stream")

if __name__ == "__main__":
    titles,news=send_news()  
    time.sleep(9.4)        
    app.run(threaded=True)                 