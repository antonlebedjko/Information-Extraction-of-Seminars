import re

def email_to_string(email_file):
        email = ''
        for ch in email_file:
                email+= ch
        return email

def extract(email, starting_tag, closing_tag):      
        set_of_matches = set()
        pattern = re.compile(starting_tag + '([\d\D]*?)' + closing_tag)
        matches = pattern.finditer(email)       
        for match in matches:             
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


def evaluate_one_email(test_email_file, tagged_by_me_email):
    test_tagged_email_file = open(test_email_file, "r")
    initial_email = email_to_string(test_tagged_email_file)
    test_tagged_email_file.close()
    tagged_by_me_email_file = open(tagged_by_me_email, "r")
    my_email = email_to_string(tagged_by_me_email_file)
    tagged_by_me_email_file.close()
    array_of_opening_tags = ['<stime>', '<etime>', '<speaker>', '<location>', '<sentence>', '<paragraph>']
    array_of_closing_tags = ['</stime>', '</etime>', '</speaker>', '</location>', '</sentence>', '</paragraph>']
    for i in range(0, len(array_of_opening_tags)):
        test_set = extract(initial_email, array_of_opening_tags[i], array_of_closing_tags[i])
        tagged_by_me_set = extract(my_email, array_of_opening_tags[i], array_of_closing_tags[i])
        print("Test taggs: ",test_set)
        print("Tagged by me: ", tagged_by_me_set)
        initial_email = remove_tags(initial_email, array_of_opening_tags[i], array_of_closing_tags[i])
        my_email = remove_tags(my_email, array_of_opening_tags[i], array_of_closing_tags[i])        
        print("Evaluation: ", evaluate(test_set, tagged_by_me_set ))

evaluate_one_email('test_tagged/301.txt', 'tagged_by_my_code/301.txt')