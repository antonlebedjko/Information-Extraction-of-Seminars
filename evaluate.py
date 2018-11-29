import re
from tagging import main
test_tagged_email_file = open('test_tagged/303.txt', "r")
#helper function to convert a file with an email to a string
def email_to_string(email_file):
        email = ''
        for ch in email_file:
                email+= ch
        return email

def extract(email, starting_tag, closing_tag):      
        set_of_matches = set()
        pattern = re.compile(starting_tag + '(.*?)' + closing_tag)
        stimes_matches = pattern.finditer(email)
        for match in stimes_matches:
            stime = match.group(1)          
            if stime:                 
                set_of_matches.add(stime)
        return set_of_matches

def remove_tags(email, starting_tag, closing_tag):
         email = email.replace(starting_tag, "")
         email = email.replace(closing_tag, "")
         return email      

def evaluate(testing_set, tagged_by_me_set):
        true_positive = len(testing_set & tagged_by_me_set)  # taggs correctly identified
        false_positive = len(tagged_by_me_set - testing_set) # taggs incorrecty labeled as taggs
        false_negative = len(testing_set - tagged_by_me_set) # taggs incorrectly labeled as not taggs
        print("My true pos: ", true_positive)
        print("My false pos: ", false_positive)
        print("My false neg:", false_negative)
        if(true_positive>0):
            precision = float(true_positive) / float(true_positive + false_positive)
            recall = float(true_positive) / float(true_positive + false_negative)
            fscore = float((2 * float(precision) * float(recall)) / float(precision + recall))
            return (precision, recall, fscore)
        else:
            return (0,0,0)

def mainEvaluate():
    initial_email = email_to_string(test_tagged_email_file)
    test_tagged_email_file.close()
    test_set = extract(initial_email, '<stime>', '</stime')
    tagged_set = extract(main(), '<stime>', '</stime')
    print("Test taggs: ",test_set)
    print("Tagged by me: ", tagged_set)
    print("Evaluation: ", evaluate(test_set, tagged_set ))
mainEvaluate()
