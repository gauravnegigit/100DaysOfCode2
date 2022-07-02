import nltk
import pickle
nltk.download('punkt')
from nltk.stem.lancaster import LancasterStemmer

import numpy as np 
import tflearn 
import tensorflow as tf 
import random 
import json

# since I was working on google colab so I have uplaoded the files using the following syntax

from google.colab import files
uploaded = files.upload()

stemmer = LancasterStemmer()

with open('intents (4).json') as file :
  data = json.load(file)
print(data["intents"])

key = 0

try :  # make some error in the try block while running for the first time and then remove the error while running for second or third time as the model will be saved in the first time .
  with open("data.pickle" , "rb") as f :
    words , labels, training , output = pickle.load(f)
  
  key = 1

except : 

  words = []
  labels = []
  doc_x , doc_y = [] , []

  for intent in data['intents'] :
    for pattern in intent['patterns'] :
      wrds = nltk.word_tokenize(pattern)
      words.extend(wrds)
      doc_x.append(wrds)
      doc_y.append(intent['tag'])

    if intent['tag'] not in labels :
      labels.append(intent['tag'])

  words = [stemmer.stem(w.lower()) for w in words if w != '?']
  words = sorted(list(set(words)))

  labels = sorted(labels)

  training = []
  output = []

  out_empty = [0 for _ in range(len(labels))]

  for x , doc in enumerate(doc_x) :
    bag = []

    wrds = [stemmer.stem(w) for w in doc]

    for w in words :
      if w in wrds :
        bag.append(1)
      else :
        bag.append(0)
    
    output_row = out_empty[:]
    output_row[labels.index(doc_y[x])] = 1

    training.append(bag)
    output.append(output_row)

  training = np.array(training)
  output = np.array(output)

  with open("data.pickle" , "wb") as f :
    pickle.dump((words , labels , training , output) , f)

tf.compat.v1.reset_default_graph()    #tf.reset_deafult_graph() function is deprecated 

net = tflearn.input_data(shape = [None , len(training[0])])
net = tflearn.fully_connected(net , 8)
net = tflearn.fully_connected(net , 8)
net = tflearn.fully_connected(net , len(output[0]) , activation = 'softmax')
net = tflearn.regression(net)

model = tflearn.DNN(net)

if key == 1 :
  model.load("model.tflearn")
else :
  model.fit(training , output , n_epoch = 1000 , batch_size = 8 , show_metric = True)
  model.save("model.tflearn")


def bag_of_words(s , words):
  bag = [0 for _ in range(len(words))]

  s_words = nltk.word_tokenize(s)
  s_words = [stemmer.stem(word.lower()) for word in s_words]

  for se in s_words :
    for i , w in enumerate(words):
      if w == se :
        bag[i] = 1

  return np.array(bag)

def chat():
  print("Start talking iwth the bot !")

  while True :
    inp = input("User input : ")

    if inp.lower() == "quit":
      print("Thanks for your time !")
      break 

    results = model.predict([bag_of_words(inp , words)])[0]
    results_index = np.argmax(results)

    if results[results_index] > 0.5 :
      tag = labels[results_index]
      

      for tg in data['intents'] :
        if tg['tag'] == tag :
          responses = tg['responses']
      
      print(random.choice(responses))


    else :
      print("i didn't get that ! ")
        


chat()
