import re
array_of_opening_tags = ['<stime>', '<etime>', '<speaker>', '<location>', '<sentence>', '<paragraph>']
array_of_closing_tags = ['</stime>', '</etime>', '</speaker>', '</location>', '</sentence>', '</paragraph>']
tags_counter = [0, 0, 0, 0, 0, 0]   # if a tag appears in an email, we increase counter by 1
# when we will go through each email, we will add new precision, recall_sum and f_measure to their sums,
# so we can devide them after by the counter of each tag and get the average from all emails
precision_sum = [0, 0, 0, 0, 0, 0]
recall_sum = [0, 0, 0, 0, 0, 0]
f_measure_sum = [0, 0, 0, 0, 0, 0]

def email_to_string(email_file):
        email = ''
        for ch in email_file:
                email+= ch
        return email

#this method extracts everything in an email what is between particlurar tag and puts all the matches to the set
def extract(email, starting_tag, closing_tag):
        set_of_matches = set()
        pattern = re.compile(starting_tag + '([\d\D]*?)' + closing_tag)
        matches = pattern.finditer(email)       
        for match in matches:             
            found = match.group(1)
            if found:
                set_of_matches.add(found)
        return set_of_matches

# one we extracted something from between the tags, we can remove the tags and return updated email without these tags
def remove_tags(email, starting_tag, closing_tag):
         email = email.replace(starting_tag, "")
         email = email.replace(closing_tag, "")
         return email      

# to get precision, recall, fscore for one particulat tag from one email
def evaluate(testing_set, tagged_by_me_set):
        true_positive = len(testing_set & tagged_by_me_set)  # taggs correctly identified
        false_positive = len(tagged_by_me_set - testing_set) # taggs incorrecty labeled as taggs
        false_negative = len(testing_set - tagged_by_me_set) # taggs incorrectly labeled as not taggs
        if(true_positive>0):
            precision = float(true_positive) / float(true_positive + false_positive)
            recall = float(true_positive) / float(true_positive + false_negative)
            fscore = float((2 * float(precision) * float(recall)) / float(precision + recall))
            return (precision, recall, fscore)
        else:
            return (0,0,0)

def evaluation_on_one_email(initial_email, email_tagged_by_my_code):
    for i in range(0, len(array_of_opening_tags)):
        test_set = extract(initial_email, array_of_opening_tags[i], array_of_closing_tags[i])
        tagged_by_me_set = extract(email_tagged_by_my_code, array_of_opening_tags[i], array_of_closing_tags[i])
        if(len(test_set) > 0):
            tags_counter[i]+=1
        initial_email = remove_tags(initial_email, array_of_opening_tags[i], array_of_closing_tags[i])
        email_tagged_by_my_code = remove_tags(email_tagged_by_my_code, array_of_opening_tags[i], array_of_closing_tags[i])
        evaluated = evaluate(test_set, tagged_by_me_set)
        precision_sum[i] += evaluated[0]
        recall_sum[i]+= evaluated[1]
        f_measure_sum[i]+=evaluated[2]
    return precision_sum, recall_sum, f_measure_sum

def evaluation_on_all_emails():
    for i in range(301, 324):
        test_tagged_email_file = open('test_tagged/'+str(i)+'.txt', "r")
        initial_email = email_to_string(test_tagged_email_file)
        test_tagged_email_file.close()
        tagged_by_me_email_file = open('tagged_by_my_code/' + str(i)+'.txt', "r")
        email_tagged_by_my_code = email_to_string(tagged_by_me_email_file)
        tagged_by_me_email_file.close()
        evaluation_on_one_email(initial_email, email_tagged_by_my_code)


evaluation_on_all_emails()
print("Tag             Precision       Recall       F Measure")
print("------------------------------------------------------")
for i in range(0,len(array_of_opening_tags)):
    tag_to_string = array_of_opening_tags[i][1:len(array_of_opening_tags[i]) - 1]
    print tag_to_string + (10 - len(tag_to_string)) * " ",
    print "      ", round(precision_sum[i]/tags_counter[i], 4),
    print "      ", round(recall_sum[i]/tags_counter[i], 4),
    print "      ", round(f_measure_sum[i]/tags_counter[i], 4)