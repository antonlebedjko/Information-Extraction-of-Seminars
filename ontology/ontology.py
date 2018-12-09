'''What this class do, is: it opens the tagged email, deletes stime, etime, speaker,
because these don't contain any information that can be relevent for ontology.
After that, it deletes any other tags which are left, but not what it's inside them.
We tokenize an email. We remove the stop words (like the, an, a...).
We remove any words that have only 1 or 2 chars in them. After we cleaned everything, 
what is no needed,we lemmatize an email and find the most 25 poplar words in an email (in case if email,
doen't have 25 words, we will take as many as we can). We use wordnet to get all
the synonims of these 25 post popular words. After we have a lot of synonims, we
compare and count them with a specific words for each department, which are in our
ontology tree.
'''

from nltk import word_tokenize
from nltk.corpus import stopwords
import re
import collections
import operator
from nltk.stem import WordNetLemmatizer
from itertools import chain
from nltk.corpus import wordnet
from ontology_tree  import my_ontology_tree


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
    number_of_most_accured_words = 25
    email_file = open('../tagging/tagged_by_my_code/' + str(file_name)+ '.txt', "r")
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
    
    lemmatizer = WordNetLemmatizer()
    list_of_all_lemmatized_words = []
    #applying lemmatizer on the proper words
    for i in range (0, len(filtered_word_list)):
        word = filtered_word_list[i]
        lemmatized_word = lemmatizer.lemmatize(word)
        list_of_all_lemmatized_words.append(lemmatized_word)
    counter = collections.Counter(list_of_all_lemmatized_words)
    # if statement that checks if we actually can take so many elements as we specify
    # in number_of_most_accured_words value, because some emails can be very short
    if(len(list_of_all_lemmatized_words)>number_of_most_accured_words):
        most_accured_words = counter.most_common()[:number_of_most_accured_words] #returns a bunch of most popular words
    else:
        most_accured_words = counter.most_common()[:len(list_of_all_lemmatized_words)]
        number_of_most_accured_words = len(list_of_all_lemmatized_words)
    list_of_all_synonims_of_most_popular_words = []    
    #applying lemas to get all synonims of most popular words
    for i in range (0, number_of_most_accured_words):
        try:
            synonyms = wordnet.synsets(most_accured_words[i][0])
        except IndexError:
            pass
        lemmas = set(chain.from_iterable([word.lemma_names() for word in synonyms]))
        lemmas = list(lemmas) #convert set to list
        #to put all values to a list, not a sublists to a list
        for word in lemmas:
            list_of_all_synonims_of_most_popular_words.append(word)
    #print(list_of_all_synonims_of_most_popular_words)
    counter = {'Computer Science':0, 'Biology':0, 'Chemistry':0, 'Electronics': 0, 'Physics':0, 'Politics':0, 'Languages':0, 'Performing Arts':0, 'Finance':0}
    #comparing all the words if they belong to different departments and icrease a counter every time when there is a match
    for school in my_ontology_tree:
        for department in my_ontology_tree[school]:
            number_of_matches = set(my_ontology_tree[school][department]) & set(list_of_all_synonims_of_most_popular_words) 
            counter[department]+=len(number_of_matches)
    # result_department will be our final answer. It will return department with the most matches
    result_department = max(counter.items(), key=operator.itemgetter(1))[0]
    # if there are no matches
    if(counter[result_department] == 0):
        result_department = "Other"
    return result_department


