############################################################
# CMPSC 442: Homework 5
############################################################

student_name = "Angelo Kwak"

############################################################
# Imports
############################################################

import string
import math
import random

############################################################
# Section 1: Markov Models
############################################################

def tokenize(text):
    tokens = []
    for i in text.strip():
        if i in string.punctuation:
            text = text.replace(i, ' %s ' % i)
    tokens = text.split()
           
    return tokens

def ngrams(n, tokens):
    #Add end to list of tokens since it only appears once
    tokens.append('<END>')
    ngrams = []
    #check first if n = 1
    if n == 1:
        context = ()
        for i in tokens:
            ngrams.append((context, i))
    #n is > 1
    else:
        temp = []
        #add all needed <START> to temp list
        for x in range(n-1):
            temp.append('<START>')

        for a in tokens:
            #create tuple out of current temp list
            context = tuple(temp)
            #add ngram tupple to answer list
            ngrams.append((context,a))
            temp.pop(0) #remove the value currently at the front of the temp list
            temp.append(a) #add the current token to the end of the temp list
            
    return ngrams
            
class NgramModel(object):

    def __init__(self, n):
        self.n = n
        #dictionary to hold the internal counts of each Ngram
        self.model_counts = {}

    def update(self, sentence): 
        tokens = tokenize(sentence) #tokenize the input sentence
        model_ngrams = ngrams(self.n, tokens) #calculate ngrams for the tokens
        #for all ngrams, create dictionary containing counts
        for i in model_ngrams:
            if i in self.model_counts.keys(): #if ngram already exists as a key, increment the count
                self.model_counts[i] += 1
            else: #create new dictionary pair
                self.model_counts[i] = 1

    def prob(self, context, token):
        #if Ngram DNE
        if (context, token) not in self.model_counts.keys():
            return 0.0
        #get the count for the given ngram
        ngram_count = self.model_counts[(context, token)]
        ngram_total = 0
        #for all ngrams with the same context, sum counts
        for i,j in self.model_counts.keys(): 
            if i == context:
                ngram_total += self.model_counts[(i,j)]

        return ngram_count/ngram_total

    def random_token(self, context):
        random_num = random.random()
        tokens = []
        p_sum = 0
        #get all tokens that have the given context
        for i,j in self.model_counts.keys(): 
            if i == context:
                tokens.append(j)
        #sort tokens in lexicographic order
        tokens = sorted(set(tokens))
        
        for token in tokens:
            #calculate probability of the token given the context
            prob = self.prob(context, token)
            #if the sum of probabilities < random number < (sum of probs + prob of token)
            if p_sum < random_num < (p_sum + prob):
                    return token
            #add calculated probability to the sum variable
            p_sum += prob             

    def random_text(self, token_count):
        text = ''

        if self.n == 1:
            context = ()
            for i in range(token_count):
                token = self.random_token(context)
                text += token + ' '
        else:
            temp = []
            #add all needed <START> to temp list
            for x in range(self.n-1):
                temp.append('<START>')
            #for all tokens
            for i in range(token_count):
                context = tuple(temp)
                token = self.random_token(context) #find random token based on current context
                text += token + ' ' #add the found random token to text string

                if token == '<END>':
                    temp = []
                    for x in range(self.n-1):
                        temp.append('<START>')
                else:
                    temp.pop(0) #remove the value currently at the front of the temp list
                    temp.append(token) #add the current token to the end of the temp list
                
        return text.strip()
                
    def perplexity(self, sentence):
        tokens = tokenize(sentence)
        grams = ngrams(self.n, tokens)
        perp = 0
        probs = []
        
        #for all ngrams, calculate their probabilities
        for i,j in grams:
            probs.append(self.prob(i,j))
        #for all probabilities, add the log
        for p in probs:
            perp += (-math.log(p))
        #return the "unlogged" value
        return math.exp(perp/len(grams))
            

def create_ngram_model(n, path):
    #open file at given path
    file = open(path)
    #create model for file
    file_ngram_model = NgramModel(n)
    #update model with every line from the file
    for i in file:
        file_ngram_model.update(i)
        
    return file_ngram_model

############################################################
# Section 2: Feedback
############################################################

feedback_question_1 = """
I spent approximately 12 hours on this assignment.
"""

feedback_question_2 = """
I found creating the random text function to be most challenging.
"""

feedback_question_3 = """
Overall I enjoyed the assignment.
"""
