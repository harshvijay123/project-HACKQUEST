
#imports
import nltk
from nltk.stem.lancaster import LancasterStemmer
import numpy
import tensorflow
import tflearn
import random
import pickle
import json



def train():
    global stemmer,data,words,labels,training,output
    stemmer = LancasterStemmer()


    with open("intents.json") as file:
        data = json.load(file)


    try:
        file=open('reporter.bin','rb')
        changes=pickle.load(file)
        if changes:
            print(1/0)
        else:
            with open('data.pickle','rb') as f:
                words,labels,training,output=pickle.load(f)

    except:
    
        words = []
        labels = []
        docs_x = []
        docs_y = []

        for intent in data['intents']:
            for pattern in intent["patterns"]:
                wrds = nltk.word_tokenize(pattern)
                words.extend(wrds)
                docs_x.append(wrds)
                docs_y.append(intent['tag'])

            if intent['tag'] not in labels:
                labels.append(intent['tag'])


        words=[stemmer.stem(w.lower()) for w in words]
        words=sorted(list(set(words)))

        training = []
        output = []

        out_empty = [0 for _ in range(len(labels))]

        for x,doc in enumerate(docs_x):
            bag = []
            wrds = [stemmer.stem(w) for w in doc if w!='?']

            for w in words:
                if w in wrds:
                    bag.append(1)
                else:
                    bag.append(0)


            output_row=out_empty[:]
            output_row[labels.index(docs_y[x])]=1

            training.append(bag)
            output.append(output_row)

        training = numpy.array(training)
        output = numpy.array(output)

        with open('data.pickle','wb') as f:
            pickle.dump((words,labels,training,output),f)



        

    tensorflow.reset_default_graph()

    net = tflearn.input_data(shape=[None,len(training[0])])
    net = tflearn.fully_connected(net,8)
    net = tflearn.fully_connected(net,8)
    net = tflearn.fully_connected(net,len(output[0]),activation='softmax')
    net = tflearn.regression(net)

    global model
    model = tflearn.DNN(net)

    try:
        if not changes:
            model.load('model.tflearn')
        else:
            print(1/0)
    except:
        model.fit(training,output,n_epoch=1000,batch_size=8,show_metric=False)
        model.save('model.tflearn')








def bag_of_words(s,words):
    bag=[0 for _ in range(len(words))]
    s_words=nltk.word_tokenize(s)
    s_words=[stemmer.stem(word.lower()) for word in s_words]

    for se in s_words:
        for i,w in enumerate(words):
            if w==se:
                bag[i]=1

    return numpy.array(bag)


def chat(msg):
    global words,model,labels
    results=model.predict([bag_of_words(msg,words)])[0]
    result_index=numpy.argmax(results)
    tag=labels[result_index]

    if results[result_index]>0.7:
        for tg in data['intents']:
            if tg['tag']==tag:
                responses=tg['responses']
                return random.choice(responses)
    else:
        return 'i do not understand'




if __name__=='__main__':
    train()
    print(chat('hello help me '))
    input()
