from io import open
import torch
import nltk
nltk.download('punkt')
from scipy import spatial

from models import InferSent



def answer_the_question(question,input_info):
	MODEL_PATH = 'encoder/infersent1.pkl'
	params_model = {'bsize': 64, 'word_emb_dim': 300, 'enc_lstm_dim': 2048,
                'pool_type': 'max', 'dpout_model': 0.0, 'version': 1}
	infersent = InferSent(params_model)
	infersent.load_state_dict(torch.load(MODEL_PATH))

	W2V_PATH = 'Glove/glove/glove.42B.300d.txt'
	infersent.set_w2v_path(W2V_PATH)

	sentences = []
	sentences.append(question)
	for i in input_info:
		for j in i:
			li = j.split('.')
			for k in li:
				if len(k)>4 :
					sentences.append(k)
		
	print(sentences)	
	infersent.build_vocab(sentences, tokenize=True)

	dict_embeddings = {}
	for i in range(len(sentences)):
		dict_embeddings[sentences[i]] = infersent.encode([sentences[i]], tokenize=True)
    	#print(dict_embeddings[sentences[i]])
	li_of_dis = []
	for a2 in sentences:
		li_of_dis.append(spatial.distance.cosine(dict_embeddings[sentences[0]],dict_embeddings[a2]))
	mini_d = 1
	x = 0
	print(li_of_dis)
	for i in range(1,len(li_of_dis)):
		if(li_of_dis[i]<mini_d):
			mini_d = li_of_dis[i]
			x = i

	return sentences[x]





    
	

