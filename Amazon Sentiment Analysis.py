import re

_author_ = 'Aman Chopra'
_description_ = 'Define methods to cleanData, classify reviews as negative or positive based on a trained model, and determine whether an inputted review is negative or positive.'
_puid_ = '0030974520'


def readAndDivideBySentiment(filename):
    pos_reviews = []
    neg_reviews = []

    file = open(filename, 'r')
    lines = file.read().split('\r\n')

    for line in lines:
        if line.endswith('0'):
            neg_reviews.append(line[0:line.rfind('\t')])
        elif line.endswith('1'):
            pos_reviews.append(line[0:line.rfind('\t')])

    return pos_reviews, neg_reviews


def cleanData(myData):
    cleanedData = []
    # print myData
    for data in myData:
        data = data.lower()

        data = re.sub(r"[^.\w\s'-]+", ' ', data)
        data = re.sub(r'(\w)\.+(\w)', r'\1 \2', data)
        data = re.sub(r'[.]', '', data)
        data = re.sub(r'(\w)-(\w)', r'\1\2', data)
        data = re.sub(r'-', ' ', data)

        data = re.sub(r"(\w)\d+$", r'\1 num ', data)
        data = re.sub(r'^\d+(\w)', r' num \1', data)
        data = re.sub(r'\s+\d+\s*\d*\s*\d*\s*', ' num ', data)
        data = re.sub(r'\s*\d+\s+', ' num ', data)
        data = re.sub(r'num\s+num\s+num\s+num\s+num\s+num\s+', ' num ', data)
        data = re.sub(r'num\s+num\s+num\s+num\s+', ' num ', data)
        data = re.sub(r'num\s+num', ' num ', data)

        data = re.sub(r"'{2,}", "'", data)
        data = re.sub(r'\s{2,}', ' ', data)
        data = re.sub(r'\s$', '', data)

        cleanedData.append(data)

    return cleanedData


def calculateUniqueWordsFreq(trainData, cutOff):
    word_list = []
    freq_data = {}

    for lines in trainData:
        word_list.extend(lines.split())

    for words in word_list:
        if words in freq_data:
            freq_data[words] += 1
        else:
            freq_data[words] = 1

    freq_list = freq_data.values()
    freq_list.sort()

    # file = open('aman.txt', 'w')
    #
    # for lines in trainData:
    #     file.write(lines + "\n")


    # print freq_list
    # print len(freq_data)

    for i in range(cutOff):
        for keys in freq_data.keys():
            if freq_data[keys] == freq_list[-(i + 1)]:
                del freq_data[keys]
                break

    return freq_data


def calculateClassProbability(posTrain, negTrain):
    total_reviews = float(len(posTrain) + len(negTrain))
    pos_reviews = len(posTrain)
    neg_reviews = len(negTrain)

    return pos_reviews/total_reviews, neg_reviews/total_reviews


def calculateScores(classProb, uniqueVocab, testData):
    test_scores = []
    total_freq = sum(uniqueVocab.values())
    # for values in uniqueVocab.values():
    #     total_freq += values

    freq_len_dict_sum = float(total_freq + len(uniqueVocab))

    for reviews in testData:
        score = 1
        for words in reviews.split():
            try:
                freq_word_in_dict = uniqueVocab[words]
            except KeyError:
                freq_word_in_dict = 0
            score *= ((freq_word_in_dict + 1) / freq_len_dict_sum)
        test_scores.append(classProb * score)
    return test_scores


def calculateAccuracy(positiveTestDataPositiveScores, positiveTestDataNegativeScores, negativeTestDataPositiveScores, negativeTestDataNegativeScores):
    tp = 0
    fp = 0
    tn = 0
    fn = 0

    for i in range(len(positiveTestDataPositiveScores)):
        if positiveTestDataPositiveScores[i] >= positiveTestDataNegativeScores[i]:
            tp += 1
        else:
            fn += 1

    for i in range(len(negativeTestDataPositiveScores)):
        if negativeTestDataNegativeScores[i] >= negativeTestDataPositiveScores[i]:
            tn += 1
        else:
            fp += 1

    return tp, fp, tn, fn


def demo(review):
    class_prob = calculateClassProbability(cleanData(readAndDivideBySentiment("TRAINING.txt")[0]),
                                           cleanData(readAndDivideBySentiment("TRAINING.txt")[1]))
    pos_training_rev_dict = calculateUniqueWordsFreq(cleanData(readAndDivideBySentiment("TRAINING.txt")[0]), 3)
    neg_training_rev_dict = calculateUniqueWordsFreq(cleanData(readAndDivideBySentiment("TRAINING.txt")[1]), 3)

    pos_score = calculateScores(class_prob[0], pos_training_rev_dict, cleanData([review]))
    neg_score = calculateScores(class_prob[1], neg_training_rev_dict, cleanData([review]))

    if pos_score > neg_score:
        return 1
    else:
        return -1


# def main():
#     pos_training_reviews = readAndDivideBySentiment('TRAINING.txt')[0]
#     neg_training_reviews = readAndDivideBySentiment('TRAINING.txt')[1]
#     pos_testing_reviews = readAndDivideBySentiment('TESTING.txt')[0]
#     neg_testing_reviews = readAndDivideBySentiment('TESTING.txt')[1]
#
#     cleaned_pos_training_reviews = cleanData(pos_training_reviews)
#     cleaned_neg_training_reviews = cleanData(neg_training_reviews)
#     cleaned_pos_testing_reviews = cleanData(pos_testing_reviews)
#     cleaned_neg_testing_reviews = cleanData(neg_testing_reviews)
#
#     pos_prob, neg_prob = calculateClassProbability(cleaned_pos_training_reviews, cleaned_neg_training_reviews)
#
#     # print '\033[1m' + 'List of raw positive TRAINING.txt reviews:', '\033[0m' + str(pos_training_reviews)
#     # print '\033[1m' + 'List of raw negative TRAINING.txt reviews:', '\033[0m' + str(neg_training_reviews)
#     # print '\033[1m' + 'List of raw positive TESTING.txt reviews:', '\033[0m' + str(pos_testing_reviews)
#     # print '\033[1m' + 'List of raw negative TESTING.txt reviews:', '\033[0m' + str(neg_testing_reviews)
#
#     # cutoff = raw_input('How many top-ranked frequency words would you like to remove: ')
#     #
#     # while True:
#     #     try:
#     #         pos_freq_dict = calculateUniqueWordsFreq(cleaned_pos_training_reviews, int(cutoff))
#     #         neg_freq_dict = calculateUniqueWordsFreq(cleaned_neg_training_reviews, int(cutoff))
#     #         break
#     #     except ValueError:
#     #         cutoff = raw_input(
#     #             'Please enter a valid integer! How many top-ranked frequency words would you like to remove: ')
#     #     except OverflowError:
#     #         cutoff = raw_input('Integer too large! How many top-ranked frequency words would you like to remove: ')
#
#     pos_freq_dict = calculateUniqueWordsFreq(cleaned_pos_training_reviews, 3)
#     neg_freq_dict = calculateUniqueWordsFreq(cleaned_neg_training_reviews, 3)
#
#     pos_data_pos_model = calculateScores(pos_prob, pos_freq_dict, cleaned_pos_testing_reviews)
#     neg_data_pos_model = calculateScores(pos_prob, pos_freq_dict, cleaned_neg_testing_reviews)
#     pos_data_neg_model = calculateScores(neg_prob, neg_freq_dict, cleaned_pos_testing_reviews)
#     neg_data_neg_model = calculateScores(neg_prob, neg_freq_dict, cleaned_neg_testing_reviews)
#     print pos_data_pos_model
#     print neg_data_pos_model
#     print pos_data_neg_model
#     print neg_data_neg_model
#
#     tp, fp, tn, fn = calculateAccuracy(pos_data_pos_model, pos_data_neg_model, neg_data_pos_model, neg_data_neg_model)
#     print tp, fp, tn, fn
#     # print pos_data_pos_model
#     # print neg_data_pos_model
#     # print pos_data_neg_model
#     # print neg_data_neg_model
#
#     while True:
#         review = raw_input('Please enter a review: ')
#         if demo(review) == 1:
#             print 'The review is positive!'
#         else:
#             print 'The review is negative!'
#         print
#
#
# if __name__ == '__main__':
#     main()


# readAndDivideBySentiment('TRAINING.txt')
# # print cleanData(readAndDivideBySentiment('TRAINING.txt')[1])
# print calculateUniqueWordsFreq(cleanData(readAndDivideBySentiment('TRAINING.txt')[1]), 3)
