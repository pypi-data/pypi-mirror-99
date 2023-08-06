from gensim.models import KeyedVectors
import nltk
import numpy as np
import pandas as pd


class TextFeature:

	LEXICON_NAMES = ['nrc0']

	def __init__(self, word2vec_model='', lexicon_nrc0='', w2v_binary=True, w2v_unicode_errors='strict', w2v_datatype=np.float32):
		# Decide to use word2vec as feature or not
		if word2vec_model:
			self.word2vec = KeyedVectors.load_word2vec_format(fname=word2vec_model,binary=w2v_binary,unicode_errors=w2v_unicode_errors,datatype=w2v_datatype)

		self.lexicon = {}
		# Decide to use NRCv0.92 lexicon as feature or not
		if lexicon_nrc0:
			self.lexicon['nrc0'] = pd.read_csv(lexicon_nrc0, engine='c', encoding='utf-8', index_col=0).T.to_dict('list')

	def text_w2v(self, word_tokens):
		"""
		Turns text to vector
		:param word_tokens: (Array of String) words of text
		:return: average vector of all words
		"""

		# Return false if word2vec model is not loaded
		try:
			vocab = self.word2vec.vocab
		except Exception as e:
			print('This instance of class doesn\'t use word2vec')
			return False
		# calculate average of vectors for each word that exists in both text and word2vec model. Other words are ignored
		vector_sum = np.array([0] * self.word2vec.vector_size)
		number_of_words = 0
		for word in word_tokens:
			if word in vocab:
				vector_sum = vector_sum + self.word2vec[word]
				number_of_words = number_of_words + 1
		# If there is at least 1 word in text return the result
		if number_of_words == 0:
			return False
		return vector_sum/number_of_words

	def text_l2v(self, word_tokens, lexicon_name, vector_size):
		"""
		Turns text to lexicon vector
		:param word_tokens: (Array of String) words of text
		:param lexicon_name: (String)
		:param vector_size: (Int) usable feature size of lexicon for each word
		:return: average lexicon vector of all words
		"""

		# Return false if lexicon is not loaded
		try:
			lexicon = self.lexicon[lexicon_name]
		except Exception as e:
			print('This instance of class doesn\'t use ' + lexicon_name)
			return False
		# calculate average of vectors for each word that exists in both text and lexicon. Other words are ignored
		vector_sum = np.array([0] * vector_size)
		number_of_words = 0
		stemmer = nltk.stem.PorterStemmer()
		for word in word_tokens:
			word = stemmer.stem(word)
			if word in lexicon:
				vector_sum = vector_sum + np.array(lexicon[word][0:vector_size])
				number_of_words = number_of_words + 1
		# If there is at least 1 word in text return the result
		if number_of_words == 0:
			return False
		return vector_sum / number_of_words
