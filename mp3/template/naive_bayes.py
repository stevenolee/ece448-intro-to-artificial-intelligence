# naive_bayes.py
# ---------------
# Licensing Information:  You are free to use or extend this projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to the University of Illinois at Urbana-Champaign
#
# Created by Justin Lizama (jlizama2@illinois.edu) on 09/28/2018

"""
This is the main entry point for MP4. You should only modify code
within this file -- the unrevised staff files will be used for all other
files and classes when code is run, so be careful to not modify anything else.
"""

import nltk 
import numpy as np
import math

LOWER_CASE = 1

def naiveBayes(train_set, train_labels, dev_set, smoothing_parameter, pos_prior):
    """
    train_set - List of list of words corresponding with each movie review
    example: suppose I had two reviews 'like this movie' and 'i fall asleep' in my training set
    Then train_set := [['like','this','movie'], ['i','fall','asleep']]

    train_labels - List of labels corresponding with train_set
    example: Suppose I had two reviews, first one was positive and second one was negative.
    Then train_labels := [1, 0]

    dev_set - List of list of words corresponding with each review that we are testing on
              It follows the same format as train_set

    smoothing_parameter - The smoothing parameter you provided with --laplace (1.0 by default)
    """
    # TODO: Write your code here
    number_of_classes = 2
    smoothing_parameter = 0.03

    total_pos = 0
    total_neg = 0
    positive = {}
    negative = {}
    # make bag of words
    word_count = {} 
    for index, data in enumerate(train_set): 
        for word in data: 
            if word not in word_count: 
                word_count[word] = 1
            else: 
                word_count[word] += 1
            if train_labels[index]:
                if word not in positive:
                    positive[word] = 1
                else:
                    positive[word] += 1
                total_pos += 1
            else:
                if word not in negative:
                    negative[word] = 1
                else:
                    negative[word] += 1
                total_neg += 1

    prob_pos = {}
    prob_neg = {}
    # calculate probabilities
    den = (smoothing_parameter * (number_of_classes + 1) + total_pos)
    smoothed = smoothing_parameter / den
    for word in word_count:
        if word in positive:
            prob_pos[word] = math.log((positive[word] + smoothing_parameter) / den)
        else:
            prob_pos[word] = smoothed

        if word in negative:
            prob_neg[word] = math.log((negative[word] + smoothing_parameter) / den)
        else: 
            prob_neg[word] = smoothed


    dev_labels = []
    for index, data in enumerate(dev_set):
        pos = math.log(pos_prior)
        neg = math.log(1 - pos_prior)
        for word in data:
            pos += prob_pos[word] if (word in prob_pos) else (smoothing_parameter) / (smoothing_parameter * (number_of_classes + 1) + len(positive))
            neg += prob_neg[word] if (word in prob_neg) else (smoothing_parameter) / (smoothing_parameter * (number_of_classes + 1) + len(negative))
        if (pos > neg):
            dev_labels.append(1)
        else:
            dev_labels.append(0)

    return dev_labels
