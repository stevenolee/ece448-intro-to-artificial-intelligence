"""
This is the main entry point for MP4. You should only modify code
within this file -- the unrevised staff files will be used for all other
files and classes when code is run, so be careful to not modify anything else.
"""
import math


def baseline(train, test):
    '''
    TODO: implement the baseline algorithm.
    input:  training data (list of sentences, with tags on the words)
            test data (list of sentences, no tags on the words)
    output: list of sentences, each sentence is a list of (word,tag) pairs.
            E.g., [[(word1, tag1), (word2, tag2)], [(word3, tag3), (word4, tag4)]]
    '''

    # initialize map
    map = {
        train[0][0][0] : {train[0][0][1] : 0}
    }
    map_baseline = {}
    prediction = []

    # train
    for sentence in train:
        for words in sentence:
            word = words[0]
            tag = words[1]
            if word in map:
                if tag in map[word]:
                    map[word][tag] += 1
                else:
                    map[word][tag] = 1
            else:
                map[word] = {tag : 1}

    # modify map
    for word in map:
        max = 0
        tag = ''
        for pos in map[word]:
            if map[word][pos] > max:
                tag = pos
                max = map[word][pos]
        map_baseline[word] = tag

    # test
    for sentence in test:
        list = []
        for word in sentence:
            if word in map_baseline:
                pos = map_baseline[word]
            else:
                pos = 'NOUN'
            list.append((word, pos))
        prediction.append(list)


    return prediction


def viterbi(train, test):
    '''
    TODO: implement the Viterbi algorithm.
    input:  training data (list of sentences, with tags on the words)
            test data (list of sentences, no tags on the words)
    output: list of sentences with tags on the words
            E.g., [[(word1, tag1), (word2, tag2)], [(word3, tag3), (word4, tag4)]]
    '''
    tagset = []
    for sentence in train:
        for word in sentence:
            if word[1] not in tagset:
                tagset.append(word[1])

    smoothing_parameter = .00001

    map = {
        train[0][0][0] : {train[0][0][1] : 0}
    }
    emissions = {
        train[0][0][1] : {train[0][0][0] : 0}
    }
    prediction = []
    tag_pairs = {
        train[0][0][1] : {train[0][1][1] : 0}
    }
    tags = {}
    start_count = {}
    tag_word = {}
    words_appear_once = {}
    
    total_words = 0
    # train
    for sentence in train:
        prev_tag = ''
        for words in sentence:
            total_words += 1
            word = words[0]
            tag = words[1]
            tags[tag] = tags.get(tag, 0) + 1
            tag_word[tag] = tag_word.get(tag, 0) + 1
            if word in words_appear_once:
                words_appear_once[word] = False
            else:
                words_appear_once[word] = tag
            if word in map:
                if tag in map[word]:
                    map[word][tag] += 1
                else:
                    map[word][tag] = 1
            else:
                map[word] = {tag : 1}

            if prev_tag is '':
                start_count[tag] = start_count.get(tag, 0) + 1
            else:
                if prev_tag in tag_pairs:
                    tag_pairs[prev_tag][tag] = tag_pairs[prev_tag].get(tag, 0) + 1 
                else:
                    tag_pairs[prev_tag] = {tag : 1}
            prev_tag = tag
            # fill out emissions
            if tag in emissions:
                if word in emissions[tag]:
                    emissions[tag][word] += 1
                else: 
                    emissions[tag][word] = 1
            else:
                emissions[tag] = {word : 1}

    hapax_tag_probabilities = {}
    len_words_appear_once = len(words_appear_once)
    # calculate probabilities for the hapax words
    for word in words_appear_once:
        if words_appear_once[word] is False:
            len_words_appear_once -= 1
        else:
            hapax_tag_probabilities[words_appear_once[word]] = hapax_tag_probabilities.get(words_appear_once[word], 0) + 1

    for key in hapax_tag_probabilities:
            hapax_tag_probabilities[key] = (hapax_tag_probabilities[key] / len_words_appear_once)
            
    for tag in tagset:
        if tag not in hapax_tag_probabilities:
            hapax_tag_probabilities[tag] = smoothing_parameter / (smoothing_parameter * (len(tagset) + 1) + len_words_appear_once)

    # laplace smoothing denominator 
    den = (smoothing_parameter * (len(tagset) + 1) + len(train))

    #initial probabilities
    initial_prob = {}
    for tag in tagset:
        # if tag == 'START':
            # initial_prob[tag] = math.log((smoothing_parameter) / den)
        # else:
            # initial_prob[tag] = math.log((start_count.get(tag, 0) + smoothing_parameter) / den)
            initial_prob[tag] = math.log((tag_word[tag]/total_words + smoothing_parameter) / den)

    print(initial_prob)

    # transition probabilities
    transition_prob = {}
    for tag1 in tagset:
        for tag2 in tagset:
            pair = (tag1, tag2)
            # transition_prob[pair] = math.log((tag_pairs.get(pair, 0) + smoothing_parameter) / den)
            transition_prob[pair] = math.log((tag_pairs[tag1].get(tag2, 0) + smoothing_parameter) / (smoothing_parameter * (len(tagset) + 1) + len(tag_pairs[tag1])))

    # emission probabilities
    emission_prob = {}
    for tag in emissions:
        for word in emissions[tag]:
            scaled_smoothing_parameter = smoothing_parameter * hapax_tag_probabilities[tag]
            # separating changing part of the denominator from den variable
            # emission_prob[(tag, word)] = math.log(((emissions[tag].get(word)) + smoothing_parameter ) / (den + tag_word[tag]))
            # emission_prob[(tag, word)] = math.log(((emissions[tag].get(word)) + smoothing_parameter ) / (smoothing_parameter * (len(tagset) + 1) + tag_word[tag]))
            emission_prob[(tag, word)] = math.log(((emissions[tag].get(word)) + scaled_smoothing_parameter ) / (scaled_smoothing_parameter * (len(tagset) + 1) + tag_word[tag]))

    for sentence in test:
        # build trellis

        trellis = []
        initial = False
        for word in sentence:
            arr = {}
            for tag1 in tagset:
                # val = math.log((smoothing_parameter ) / (smoothing_parameter * (len(tagset) + 1) + tag_word[tag1]))
                if word == "START":
                    prob = (initial_prob[tag1] + emission_prob.get((tag1, word), \
                            math.log(((smoothing_parameter * hapax_tag_probabilities[tag1]) / (smoothing_parameter * hapax_tag_probabilities[tag1] * (len(tagset) + 1) + tag_word[tag1])))) \
                            )
                    arr[tag1] = (prob, None)
                    # print(word, tag1, prob)

                elif initial:
                    prob = (initial_prob[tag1] + emission_prob.get((tag1, word), \
                        # math.log(smoothing_parameter / (den + tag_word[tag2]))) 
                        # math.log(((hapax_tag_probabilities[tag2] * smoothing_parameter ) / (hapax_tag_probabilities[tag2] * smoothing_parameter * (len(tagset) + 1) + tag_word[tag2])))) \
                        math.log(((smoothing_parameter * hapax_tag_probabilities[tag1]) / (smoothing_parameter * hapax_tag_probabilities[tag1] * (len(tagset) + 1) + tag_word[tag1])))) \
                        # val)
                        )
                    arr[tag1] = (prob, "START")
                    # print(word, tag1, prob)
                else:
                    curr_max = -math.inf
                    prev_tag = ''
                    temp = trellis[-1] if len(trellis) >= 1 else trellis[0]
                    for tag2 in temp:
                        prob = temp[tag2][0] + transition_prob[(tag2, tag1)] + emission_prob.get((tag1, word), \
                            #  math.log(smoothing_parameter / (den + tag_word[tag2]))
                            # math.log(((hapax_tag_probabilities[tag2] * smoothing_parameter ) / (hapax_tag_probabilities[tag2] * smoothing_parameter * (len(tagset) + 1) + tag_word[tag2]))) \
                            math.log(((smoothing_parameter * hapax_tag_probabilities[tag1]) / (smoothing_parameter * hapax_tag_probabilities[tag1] * (len(tagset) + 1) + tag_word[tag2]))) \
                            # val
                            )
                        if prob > curr_max:
                            curr_max = prob
                            prev_tag = tag2
                    arr[tag1] = (curr_max, prev_tag)
                    # print(word, tag1, prob)

            initial = True if word == 'START' else False
            trellis.append(arr)
        # print("done_________")
        # backtrace trellis
        backtrace_arr = []
        # find greatest of last word
        curr_index = len(trellis) - 1
        tag_dict = trellis[curr_index]
        max_prob = tag_dict['NOUN'][0]
        max_tag = 'NOUN'
        parent_tag = tag_dict['NOUN'][1]
        for key in tag_dict:
            if tag_dict[key][0] > max_prob:
                max_prob = tag_dict[key][0]
                parent_tag = tag_dict[key][1]
                max_tag = key
        index = -1
        while len(backtrace_arr) != len(sentence):
            backtrace_arr.insert(0, (sentence[index], max_tag))
            max_tag = trellis[index][max_tag][1]
            index -= 1
        prediction.append(backtrace_arr)

    return prediction
