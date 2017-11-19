import re
import string
import numpy as np

niceEmojis = [u'\U0001f44D', u'\U0001f44f', u'\U0001f603', u'\U0001f600', u'\U0001f64f', u'\U0001f618', u'\U0001f60A', u'\U0001f601', u'\U0000270c']
badEmojis = [u'\U0001f622', u'\U0001f62d', u'\U0001f621', u'\U0001f615', u'\U0001f623', u'\U0001f614', u'\U0001f44e', u'\U0001f620', u'\U0001f611', u'\U0001f616', u'\U0001f625', u'\U0001f629']
def preprocess(data, stopWords = [], extractEmojis = True, forTraining = True):
	finalData = []
	for i in range(len(data)):
		if (forTraining):
			comment = data[i][0]
		else : comment = data[i]
		comment = subDots(comment)
		comment = comment.translate(None, string.punctuation)
		if (extractEmojis):
			for emoji in niceEmojis:
				if emoji in unicode(comment, "utf-8"): 
					comment = comment + " testnicemoji"
					break
			for emoji in badEmojis:
				if emoji in unicode(comment, "utf-8"):
					comment = comment + " testbademoji"
					break
		comment = unicode(comment, "utf-8")
		comment = removeNewlines(comment)
		# print(comment)
		original = data[i][0] if forTraining else data[i]
		if (hasUpperCaseWord(comment)): comment = comment + " testcaps"
		comment = comment.lower().strip(" \t\n\r")
		if (hasEllipsis(original)): comment = comment + " testret"
		if (hasStar(original)): comment = comment + " teststar"
		if (hasMultiQuestionMark(original)): comment = comment + " testduploq"
		elif (hasSingleQuestionMark(original)): comment = comment + " testq"
		if (hasMultiExclamationMark(original)): comment = comment + " testduploexcl"
		elif (hasSingleExclamationMark(original)): comment = comment + " testexcl"
		if (forTraining): 
			finalData.append((comment, data[i][1],  data[i][-1]))
		else : finalData.append(comment)
	finalData = filterStopWords(finalData, stopWords, removeNumerals = True, forTraining = forTraining)
	return finalData


def hasUpperCaseWord(text):
	for word in text.split(" "):
		if (len(word) >= 2 and not(re.search("\d+", text)) and word.upper() == word): 
			return True 
	return False

def hasEllipsis(text):
	return re.search("\.\.+", text)

def hasStar(text):
	return re.search("\*", text)

def hasMultiExclamationMark(text):
	return re.search("!!+", text)

def hasMultiQuestionMark(text):
	return re.search("\?\?+", text)

def hasSingleExclamationMark(text):
	return re.search("!", text)

def hasSingleQuestionMark(text):
	return re.search("\?", text)

def removeNumbers(text):
	return re.sub(r"\d+", "", text)

def removeNewlines(text):
	return re.sub(r"\n+", " ", text)

def subDots(text):
	return re.sub(r"(\w+)[\-\.\,\(\)]{1}(\w+)", r"\1 \2", text)


def mostFrequentWords(corpus):
	words = {}
	for document in corpus:
		docWords = document.split(" ")
		for word in docWords:
			if word in words:
				words[word] = words[word] + 1
			else : words[word] = 1
	return words

def filterStopWords(data, stopWords, removeNumerals = False, forTraining = True):
	filteredDocuments = []
	for i in range(len(data)):
		if (forTraining):
			document = data[i][0].split(" ")
		else : document = data[i].split(" ")
		filteredDoc = " ".join([word for word in document if word not in stopWords])
		if (removeNumerals) : filteredDoc = removeNumbers(filteredDoc)
		if (forTraining):
			filteredDocuments.append((filteredDoc, data[i][1], data[i][-1]))
		else : filteredDocuments.append(filteredDoc)
	return filteredDocuments