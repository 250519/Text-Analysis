#!/usr/bin/env python
# coding: utf-8

# In[79]:


import nltk
nltk.download('punkt')
import nltk
from nltk.corpus import stopwords
nltk.download('stopwords')
import re
import nltk
from nltk.tokenize import word_tokenize
nltk.download('punkt')
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import requests


# # Data Extraction
# 
# import pandas as pd
# import numpy as np
# from bs4 import BeautifulSoup
# import requests
# 
# data=pd.read_excel('/Users/harshshivhare/Downloads/Input.xlsx')
# data=pd.DataFrame(data)
# urls=data['URL'].tolist()
# urls_id=data['URL_ID'].tolist()
# for name,url in zip(urls_id,urls):
# 
#     text=requests.get(url).text
#     soup = BeautifulSoup(text,'lxml')
# 
#     title_element = soup.find('h1', class_='entry-title')
#     # print(title_element)
#     if title_element:
#         title = (title_element.text.strip())
#     else:
#         title = "Title not found"
# 
#     textt_element = soup.find('div', class_='td-post-content tagdiv-type')
#     if textt_element:
#         textt = textt_element.text.strip()
#     else:
#         textt = "Text not found"
# 
#     with open(f'project/{name}.txt','w') as f:
#         f.write(f"title - {title.strip()}\n")
#         f.write(f"Text - {textt}")
# 
# 

# # Data Analysis

# In[98]:


df=pd.read_excel('/Users/harshshivhare/Downloads/Input.xlsx')


# In[75]:


stopwords_file=['/Users/harshshivhare/Downloads/StopWords/StopWords_Auditor.txt','/Users/harshshivhare/Downloads/StopWords/StopWords_Currencies.txt','/Users/harshshivhare/Downloads/StopWords/StopWords_DatesandNumbers.txt','/Users/harshshivhare/Downloads/StopWords/StopWords_Generic.txt','/Users/harshshivhare/Downloads/StopWords/StopWords_GenericLong.txt','/Users/harshshivhare/Downloads/StopWords/StopWords_Geographic.txt','/Users/harshshivhare/Downloads/StopWords/StopWords_Names.txt']
stopwords1=[]
for file in stopwords_file:
    
    with open(file,'r',encoding='ascii',errors='replace') as file:
        data1=file.read()
        stopwords1.append(data1)
        
with open('/Users/harshshivhare/Downloads/MasterDictionary/positive-words.txt', 'r') as file:
    # Read the entire contents of the file
    positive_words = file.read()
#     print(positive_words)
with open('/Users/harshshivhare/Downloads/MasterDictionary/negative-words.txt', 'r',errors='replace') as file:
    # Read the entire contents of the file
    negative_words = file.read()
#     print(negative_words)    
        


# In[74]:


def rem_stopwords(text,stopwords):
    data_clean=[]
    for word in text.split():
        if word.lower() not in stopwords1:
            data_clean.append(word)
    data_clean= " ".join(data_clean)      
            
    return data_clean


# In[3]:


def count_positive(positive_words,text):
    text=text.split()
    positive_score=0
    for words in text:
        if words.lower() in positive_words:
            positive_score+=1
            
    return positive_score


# In[4]:


def count_negative(negative_words,text):
    text=text.split()
    negative_score=0
    for words in text:
        if words.lower() in negative_words:
            negative_score+=1
            
    return negative_score


# In[6]:


def polarity_score(positive_score,negative_score):
    polarity_score = (positive_score - negative_score)/ ((positive_score + negative_score) + 0.000001)
    return polarity_score


# In[121]:


def subjectivity(positive_score,negative_score,data_clean):
    Total_words=len(data_clean)
    subjectivity_score1 = (positive_score + negative_score)/ ((Total_words) + 0.000001)
    return subjectivity_score1


# In[58]:


def Total_words1(text):
    sentences = nltk.sent_tokenize(text)
    total_words = 0
    for sentence in sentences:
        words = word_tokenize(sentence)
        total_words += len(words)
    return total_words


# In[63]:


def avg_sentence_len1(text,total_words):
    sentences = nltk.sent_tokenize(text)
    avg_sentence_len=total_words/len(sentences)
    return avg_sentence_len


# In[13]:


def count_syllables(word):
    vowels = "aeiouy"
    num_vowels = sum(1 for char in word if char.lower() in vowels)
    num_diphthongs = sum(1 for diphthong in ['ai', 'au', 'ei', 'eu', 'oi', 'ou'] if diphthong in word.lower())
    num_vowels -= num_diphthongs
#     exception given in the question
    exception=sum(1 for words in word[-2:]) 
    num_vowels-=exception
    return  num_vowels


# In[64]:


def avg_no_of_words_per_sent1(Total_words):
    sentences = nltk.sent_tokenize(text)
    avg_sentence_len=total_words/len(sentences)
    return avg_sentence_len
    


# In[66]:


def count_complex_words1(text):
    words = nltk.word_tokenize(text)
    complex_words = [word for word in words if count_syllables(word) > 2]
    return len(complex_words)


# In[70]:


def percentage_complex_words1(complex_words,Total_words):
    percentage_complex_words=complex_words/Total_words
    return percentage_complex_words


# In[77]:


def fog_index1(avg_sentence_len,percentage_complex_words):
    Fog_Index = 0.4 * (avg_sentence_len + percentage_complex_words)
    return Fog_Index
    
    


# In[82]:


def remove_stopwords(text):
    stop_words = set(stopwords.words('english'))
    words = text.split()
    filtered_words = [word for word in words if word.lower() not in stop_words]
    data_clean_again=' '.join(filtered_words)
    return clean_text(data_clean_again)

def clean_text(text):
    pattern = re.compile(r'[^a-zA-Z0-9\s]')
    # Replace non-alphanumeric characters with an empty string
    cleaned_text = pattern.sub('', text)
    return cleaned_text


# In[39]:


def word_count_clean(text):
    cleaned_textt=remove_stopwords(text)
    return len(cleaned_textt)
    


# In[24]:


def count_specific_pronoun(text):
    from collections import Counter
    
    specific_pronouns = ['i', 'we', 'my', 'ours', 'us']
    
    pattern = re.compile(r'\b(?:i|we|my|ours|us)\b', re.IGNORECASE)
    
    # Find all matches in the text
    matches = pattern.findall(text)
    
    # Count the occurrences of each pronoun
    pronoun_counts = Counter(match.lower() for match in matches if match.lower() != 'us' or (match.islower() and match == 'us'))
    
    # Calculate total number of specific personal pronouns
    total_pronouns = sum(pronoun_counts.values())
    
    return total_pronouns


# In[89]:


def count_characters_in_words(text):
    """Count the number of characters in each word in the text."""
    words = text.split()
    sum=0
    for word in words:
        sum+=len(word)
        
    return sum
def avg_word_len1(word_count,total_clean_text):
    count_character_word=count_characters_in_words(total_clean_text)
    avg_word_len=count_character_word/word_count
    return avg_word_len


# In[ ]:


POSITIVE_SCORE=[]
NEGATIVE_SCORE=[]
POLARITY_SCORE=[]
SUBJECTIVITY_SCORE=[]
AVG_SENTENCE_LENGTH=[]
PERCENTAGE_OF_COMPLEX_WORDS=[]
FOG_INDEX=[]
AVG_NUMBER_OF_WORDS_PER_SENTENCE=[]
COMPLEX_WORD_COUNT=[]
WORD_COUNT=[]
SYLLABLE_PER_WORD=[]
PERSONAL_PRONOUNS=[]
AVG_WORD_LENGTH=[]


# # Applying Data Extraction and Analysis simultaneously

# In[ ]:



data=pd.read_excel('/Users/harshshivhare/Downloads/Input.xlsx')
data=pd.DataFrame(data)
urls=data['URL'].tolist()
# urls_id=data['URL_ID'].tolist()
for url in urls:

    text=requests.get(url).text
    soup = BeautifulSoup(text,'lxml')

    title_element = soup.find('h1', class_='entry-title')
    # print(title_element)
    if title_element:
        title = (title_element.text.strip())
    else:
        title = "Title not found"

    textt_element = soup.find('div', class_='td-post-content tagdiv-type')
    if textt_element:
        textt = textt_element.text.strip()
    else:
        textt = "Text not found"
        
    data=title+textt
    data_clean=rem_stopwords(data,stopwords1)

    positive_score=count_positive(positive_words,data)
    POSITIVE_SCORE.append(positive_score)

    negative_score=count_negative(negative_words,data)
    NEGATIVE_SCORE.append(negative_score)

    Polarity_Score=polarity_score(positive_score,negative_score)
    POLARITY_SCORE.append(Polarity_Score)

    subjectivity_score=subjectivity(positive_score,negative_score,data_clean)
    SUBJECTIVITY_SCORE.append(subjectivity_score)

    Total_words=Total_words1(data)
    avg_sentence_len=avg_sentence_len1(data,Total_words)
    AVG_SENTENCE_LENGTH.append(avg_sentence_len)

    count_syllable=count_syllables(data)
    SYLLABLE_PER_WORD.append(count_syllable)

    count_complex_words=count_complex_words1(data)
    COMPLEX_WORD_COUNT.append(count_complex_words)

    avg_number_words_per_sentences=avg_sentence_len1(data,Total_words)
    AVG_NUMBER_OF_WORDS_PER_SENTENCE.append(avg_number_words_per_sentences)

    percentage_complex_words=percentage_complex_words1(count_complex_words,Total_words)
    PERCENTAGE_OF_COMPLEX_WORDS.append(percentage_complex_words)

    fog_index=fog_index1(avg_sentence_len,percentage_complex_words)
    FOG_INDEX.append(fog_index)

    total_clean_text=remove_stopwords(data)
    word_count=word_count_clean(data)
    WORD_COUNT.append(word_count)

    personal_pronoun=count_specific_pronoun(data)
    PERSONAL_PRONOUNS.append(personal_pronoun)

    avg_word_len=avg_word_len1(word_count,total_clean_text)
    AVG_WORD_LENGTH.append(avg_word_len)
    


# In[ ]:


df['POSITIVE_SCORE']=POSITIVE_SCORE
df['NEGATIVE_SCORE']=NEGATIVE_SCORE
df['POLARITY_SCORE']=POLARITY_SCORE
df['SUBJECTIVITY_SCORE']=SUBJECTIVITY_SCORE
df['AVG_SENTENCE_LENGTH']=AVG_SENTENCE_LENGTH
df['PERCENTAGE_OF_COMPLEX_WORDS']=PERCENTAGE_OF_COMPLEX_WORDS
df['FOG_INDEX']=FOG_INDEX
df['AVG_NUMBER_OF_WORDS_PER_SENTENCE']=AVG_NUMBER_OF_WORDS_PER_SENTENCE
df['COMPLEX_WORD_COUNT']=COMPLEX_WORD_COUNT
df['WORD_COUNT']=WORD_COUNT
df['SYLLABLE_PER_WORD']=SYLLABLE_PER_WORD
df['PERSONAL_PRONOUNS']=PERSONAL_PRONOUNS
df['AVG_WORD_LENGTH']=AVG_WORD_LENGTH


# In[ ]:


df=pd.read_excel('/Users/harshshivhare/Downloads/Input.xlsx')


# In[126]:


df


# In[127]:


output_file = 'output.xlsx'
df.to_excel(output_file)


# In[ ]:




