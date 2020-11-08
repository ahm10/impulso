# importing libraries 
import nltk 
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize, sent_tokenize 
from summarizer import Summarizer



def sentencizer(text):
    doc = nlp(text)

    sents_list = []
    for sent in doc.sents:
        sents_list.append(sent.text)

    return sents_list

def cleanup(text):
    processed = text.lower()  
    processed = re.sub('[^a-zA-Z]', ' ', processed )  
    processed= re.sub(r'\s+', ' ', processed)

    return processed
    
def summarise(text): 
    # Tokenizing the text 
    stopWords = set(stopwords.words("english")) 
    words = word_tokenize(text) 

    # Creating a frequency table to keep the 
    # score of each word 

    freqTable = dict() 
    for word in words: 
        word = word.lower() 
        if word in stopWords: 
            continue
        if word in freqTable: 
            freqTable[word] += 1
        else: 
            freqTable[word] = 1

    # Creating a dictionary to keep the score 
    # of each sentence 
    sentences = sent_tokenize(text) 
    sentenceValue = dict() 

    for sentence in sentences: 
        for word, freq in freqTable.items(): 
            if word in sentence.lower(): 
                if sentence in sentenceValue: 
                    sentenceValue[sentence] += freq 
                else: 
                    sentenceValue[sentence] = freq 



    sumValues = 0
    for sentence in sentenceValue: 
        sumValues += sentenceValue[sentence] 

    # Average value of a sentence from the original text 

    average = int(sumValues / len(sentenceValue)) 

    # Storing sentences into our summary. 
    summary = '' 
    for sentence in sentences: 
        if (sentence in sentenceValue) and (sentenceValue[sentence] > (0.5 * average)): 
            summary += " " + sentence 


    # print(len(text))
    # print("-----------")
    # print(len(summary)) 

    # print(summary)

    return summary

 
def summarise1(txt):

    model = Summarizer()
    return model(txt)
    
    

# text = '''Machine learning (ML) is the study of computer algorithms that improve automatically through experience.[1] It is seen as a subset of artificial intelligence. Machine learning algorithms build a model based on sample data, known as "training data", in order to make predictions or decisions without being explicitly programmed to do so.[2] Machine learning algorithms are used in a wide variety of applications, such as email filtering and computer vision, where it is difficult or infeasible to develop conventional algorithms to perform the needed tasks.

# A subset of machine learning is closely related to computational statistics, which focuses on making predictions using computers; but not all machine learning is statistical learning. The study of mathematical optimization delivers methods, theory and application domains to the field of machine learning. Data mining is a related field of study, focusing on exploratory data analysis through unsupervised learning.[4][5] In its application across business problems, machine learning is also referred to as predictive analytics.'''

# import time

# print(text)

# start = time.time()

# res1 = summarise(text)

# end = time.time()
# print("-----NLTK----")
# print("time : ", end - start)
# print("-----o/p-----")
# print(res1)

# start = time.time()

# res2 = summarise1(text)

# end = time.time()
# print("-----BERT----")
# print("time : ", end - start)
# print("-----o/p-----")
# print(res2)