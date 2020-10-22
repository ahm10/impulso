import bs4 as bs  
import urllib.request  
import re  
import spacy
nlp = spacy.load('en_core_web_sm')

from spacy.matcher import Matcher
from spacy.matcher import PhraseMatcher

scrapped_data = urllib.request.urlopen('https://en.wikipedia.org/wiki/Artificial_intelligence')  
article = scrapped_data .read()

parsed_article = bs.BeautifulSoup(article,'lxml')

paragraphs = parsed_article.find_all('p')

article_text = ""

for p in paragraphs:  
    article_text += p.text
    
    
processed_article = article_text.lower()  
processed_article = re.sub('[^a-zA-Z]', ' ', processed_article )  
processed_article = re.sub(r'\s+', ' ', processed_article)


phrase_matcher = PhraseMatcher(nlp.vocab)

phrases = ['machine learning', 'robots', 'intelligent agents']

patterns = [nlp(text) for text in phrases]

matchername = 'tags_extractor1'

phrase_matcher.add(matchername, None, *patterns)

sentence = nlp (processed_article)

matched_phrases = phrase_matcher(sentence)

for match_id, start, end in matched_phrases:
    string_id = nlp.vocab.strings[match_id]  
    span = sentence[start:end]                   
    print(match_id, string_id, start, end, span.text)

