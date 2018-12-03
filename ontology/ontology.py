'''What this class do, is: we open the tagged email, we delete stime, etime, speaker because these don't contain any information that can be relevent for ontology.
After that, we delete any other tags, but not what it's inside them. We tokenize an email. We delete any non words in an email.
We remove any words that have only 1 or 2 chars in them. We remove the stop words (like the, an, a...). After we cleaned everything, what is no needed,
we find the most 25 poplar ords in an email.

'''
from nltk import word_tokenize
from nltk.corpus import stopwords
import re
import collections
from nltk.stem import WordNetLemmatizer
from itertools import chain
from nltk.corpus import wordnet
number_of_most_accured_words = 25

#to remove speakers, stimes, etimes, that will not give any right information for ontology. This method also removed the tags associated with them
def remove_between_tags(email, starting_tag, closing_tag):
    pattern = re.compile(starting_tag + '([\d\D]*?)' + closing_tag)
    matches = pattern.finditer(email)
    for match in matches:             
            found = match.group()
            if found:
                email = email.replace(found, "")
    return email

#to delete the tags from the email
def delete_tags(email, starting_tag, closing_tag):
    pattern = re.compile(starting_tag)
    matches = pattern.finditer(email)
    for match in matches:             
            found = match.group()
            if found:
                email = email.replace(found, "")
    pattern2 = re.compile(closing_tag)
    matches2 = pattern2.finditer(email)
    for match in matches2:             
            found = match.group()
            if found:
                email = email.replace(found, "")
    return email

def email_to_string(email_file):
        email = ''
        for ch in email_file:
                email+= ch
        return email

def ontology_on_one_email(file_name):
    email_file = open('../tagged_by_my_code/' + str(file_name)+ '.txt', "r")
    email = email_to_string(email_file)
    email = email.lower()
    email_file.close()
    email = remove_between_tags(email, '<stime>', '</stime>') #we don't need to now stime for ontology, so we can remove it
    email = remove_between_tags(email, '<etime>', '</etime>') #we don't need to now etime for ontology, so we can remove it
    email = remove_between_tags(email, '<speaker>', '</speaker>') #we don't need to now speaker for ontology, so we can remove it
    email = delete_tags(email, '<paragraph>', '</paragraph>')
    email = delete_tags(email, '<sentence>', '</sentence>')
    email = delete_tags(email, '<location>', '</location>')
    word_list = word_tokenize(email)
    word_list =[re.sub(r'[^A-Za-z0-9]+', '', x) for x in word_list]
    word_list = [x for x in word_list if not any(c.isdigit() for c in x)] #delete all the words with digits
    word_list = [y for y in word_list if y]#removes all the empty strings
    word_list = [z for z in word_list if len(z)>2] #removes all strings which have only 1 or 2 chars
    filtered_word_list = word_list[:] #make a copy of the word_list
    for word in word_list: # iterate over word_list
      if word in stopwords.words('english'): 
        filtered_word_list.remove(word) # remove word from filtered_word_list if it is a stopword
    counter = collections.Counter(filtered_word_list)

    most_accured_words = counter.most_common()[:number_of_most_accured_words]
    most_accured_words_after_lemmatizer = []
    lemmatizer = WordNetLemmatizer()
    #applying lemmatizer on all most popular words
    for i in range (0, number_of_most_accured_words):
        popular_word = most_accured_words[i][0]
        lemmatized_word = lemmatizer.lemmatize(popular_word)
        most_accured_words_after_lemmatizer.append(lemmatized_word )
        #print('original word: ', popular_word, "           lemmatized word: ", lemmatized_word)

    list_of_all_synonims_of_most_popular_words = []    
    for i in range (0, number_of_most_accured_words):    
        synonyms = wordnet.synsets(most_accured_words_after_lemmatizer[i])
        lemmas = set(chain.from_iterable([word.lemma_names() for word in synonyms]))
        lemmas = list(lemmas) #convert set to list
        #to put all values to a list, not a sublists to a list
        for word in lemmas:
            list_of_all_synonims_of_most_popular_words.append(word)
        #print(lemmas)

    print(list_of_all_synonims_of_most_popular_words)

ontology_on_one_email('301')


