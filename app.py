from flask import Flask
import sys
import os
import pickle
from preproc import *
from sklearn.svm import LinearSVC as svm
from sklearn.linear_model import LogisticRegression as lr
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
app = Flask(__name__)

classifier = None
countVectorizer = None
tfIdfTransformer = None
worstFeats = None

@app.route('/<comment>')
def homepage(comment=None):
	data = [comment.encode("utf-8")]
	data = preprocess(data, forTraining = False)
	data = filterStopWords(data, worstFeats, forTraining = False)

	data = countVectorizer.transform(data)
	data = tfIdfTransformer.transform(data)

	predictions = classifier.predict(data)
	return(comment + " - " + predictions[0])

if __name__ == '__main__':
	f = open("classifier.p", "rb")
	classifier = pickle.load(f)
	f.close()

	# transform words into numbers
	f = open("countVectorizer.p", "rb")
	countVectorizer = pickle.load(f)
	f.close()

	f = open("tfIdfTransformer.p", "rb")
	tfIdfTransformer = pickle.load(f)
	f.close()

	# list of ignored words
	f = open("worstFeats.p", "rb")
	worstFeats = pickle.load(f)
	f.close()

	print("Classifier loaded")
	app.run(debug=True, use_reloader=True)