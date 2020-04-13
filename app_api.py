from io import open
import torch
import nltk
nltk.download('punkt')
from scipy import spatial

from models import InferSent


from flask import Flask   
from flask import request
from flask import jsonify        
from flask import render_template
import requests

app = Flask(__name__)


def convert(s):
    q=""
    for i in range (len(s)):
        if (s[i] >='a' and s[i]<='z')  or (s[i]>='A' and s[i]<='Z') or (s[i]>='0' and s[i]<='9' or s[i]==' '):
            q=q+s[i]
        
    return q







@app.route("/",methods=["GET","POST"])

def answer_the_question():
	print("***********************************************")

	#print(request.form)

	print("***********************************************")

	input_info = request.form['cont']
	#print(request.args['data'])
	question = request.form['question']
	#question = 'where are you.'
	#input_info = [['I am here.'],['fuck ooff']]
	print("___________________________________________________________")
	print(question)
	print(len(input_info))
	print("_________________________________________________________________")
	MODEL_PATH = 'encoder/infersent1.pkl'
	params_model = {'bsize': 64, 'word_emb_dim': 300, 'enc_lstm_dim': 2048,
                'pool_type': 'max', 'dpout_model': 0.0, 'version': 1}
	infersent = InferSent(params_model)
	infersent.load_state_dict(torch.load(MODEL_PATH))

	W2V_PATH = 'Glove/glove/glove.42B.300d.txt'
	infersent.set_w2v_path(W2V_PATH)

	sentences = []
	sentences.append(convert(question))
	li = input_info.split('.')
	for k in li:
		if len(k)>4 :
			k = convert(k)
			sentences.append(k)
	print("_____________________________________________________________________________")
	print(len(sentences))	
	print('__________________________________________________________________________')
	infersent.build_vocab(sentences, tokenize=True)

	dict_embeddings = {}
	for i in range(len(sentences)):
		try:
			dict_embeddings[sentences[i]] = infersent.encode([sentences[i]], tokenize=True)
		except:
			continue
    	#print(dict_embeddings[sentences[i]])
	li_of_dis = []
	for a2 in sentences:
		try:
			li_of_dis.append(spatial.distance.cosine(dict_embeddings[sentences[0]],dict_embeddings[a2]))
		except:
			li_of_dis.append(1.00)
	mini_d = 1
	x = 0
	print(li_of_dis)

	for i in range(1,len(li_of_dis)):
		if(li_of_dis[i]<mini_d and li_of_dis[i]>0.05):
			mini_d = li_of_dis[i]
			x = i

	ans_s = sentences[x]
	print("oooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo")
	if(x+3<len(sentences)):
		ans_s = ' '+sentences[x+1]+' '+sentences[x+2]+' '+sentences[x+3]

	return jsonify(ans=ans_s)


if __name__ == "__main__":
	app.run(port=8000)                 