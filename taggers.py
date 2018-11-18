import re
untagged_email_file = open('seminars_untagged/untagged/315.txt', "r")


def emailToString(email_file):
        email = ''
        for ch in email_file:
                email+= ch
        return email

def emailToList(email):
        email_list = []
        for line in email:
                words = line.rstrip()
                email_list = email_list + [words]
        
        #email.close()
        return email_list

#tagging the end of event times. If we want to tag all time appereances in the text, we should run our endTimeTagger before startTimeTagger, they deppend from each other
def endTimeTagger(email_list):
    # converting string with a whole email to list
    email_list = email_list.split('\n')
    # empty string to append a whole email with tags
    updated_email = ''
    # different patterns, need to evaluate to choose the best one in the end
    pattern = re.compile(r'\b([0-9]{1,2}(?::[0-9]{2}\s?(?:AM|PM|am|pm|a\.m|p\.m)|:[0-9]{2}|\s?(?:AM|PM|am|pm|a\.m|p\.m)))\b')
    pattern = re.compile('[ ]([-]|(?:-|until))[ ][0-9][0-9]?\:[0-9][0-9][ ][am|AM|pm|PM|a.m|A.M|p.m|P.M]{2,3}')
    for line in email_list:
        if (not "PostedBy" in line):
            matches = pattern.finditer((line))
            # to check if there are any time patterns in a line
            condition = (len(list(matches)) == 0)
            if (condition):
                updated_email += line + '\n'
            else:
                matches = pattern.finditer((line))
                start = 0
                end = 0
                for match in matches:
                    matchStart = match.start() + start
                    matchEnd = match.end() + end
                    line = line[0:matchStart] + "<etime>" + line[matchStart:matchEnd] + "</etime>" + line[matchEnd:]
                    start += 15 #if we have more than one match in out matches array, we need to update the next match starting index, because we appended extra characters to the string
                    end += 22 #same with the match end index
                updated_email += line + '\n'
        else:
            updated_email += line + '\n'
    return updated_email

#tagging the start of event times or just any other times in the email, which potentially should also be the starting times. Before calling this method, we should call endTimeTagger, otherwise we will tag the <etime> as <stime>
def startTimeTagger(email_list):
        #converting string with a whole email to list
        email_list = email_list.split('\n')
        #empty string to append a whole email with tags
        updated_email = ''
        #different patterns, need to evaluate to choose the best one in the end
        pattern = re.compile('([0-9][0-9]?\:[0-9][0-9][ ][am|AM|pm|PM|a.m|A.M|p.m|P.M]{2,3})(?!\<\/etime)')
        pattern = re.compile(r'(\b([0-9]{1,2}(?::[0-9]{2}\s?(?:AM|PM|am|pm|a\.m|p\.m)|:[0-9]{2}|\s?(?:AM|PM|am|pm|a\.m|p\.m)))\b)(?!\<\/etime)')
        pattern = re.compile('([0-9]{1,2}?\:[0-9][0-9][ ][am|AM|pm|PM|a.m|A.M|p.m|P.M]{2,3})(?!\<\/etime)')
        pattern = re.compile(r'(\[0-9]+:[0-9][0-9]|[0-9]+:[0-9][0-9] +[APap]\.?[mM])(?!\<\/etime)')
        for line in email_list:
                if(not "PostedBy" in line):                                      
                        matches = pattern.finditer((line))
                        #to check if there are any time patterns in a line
                        condition = (len(list(matches))==0)
                        # to check if there are any time patterns in a line
                        if (condition):
                                updated_email += line + '\n'
                        else:
                                matches = pattern.finditer((line))
                                start = 0
                                end = 0
                                for match in matches:
                                    matchStart = match.start() + start
                                    matchEnd = match.end() + end
                                    line = line[0:matchStart] + "<stime>" + line[matchStart:matchEnd] + "</stime>" + line[matchEnd:]
                                    start += 15  # if we have more than one match in out matches array, we need to update the next match starting index, because we appended extra characters to the string
                                    end += 22  # same with the match end index
                                updated_email += line +'\n'
                else:
                       updated_email += line + '\n'
        return updated_email



#taging paragraphs using regular expression. It expects string as an input
def paragraphsTagger(text):
        text = '\n\n{}\n\n'.format(text.strip('\n'))
        pattern = re.compile(r'(?<=\n\n)(?:(?:\s*\b.+\b:(?:.|\s)+?)|(\s{0,4}[A-Za-z0-9](?:.|\n)+?\s*))(?=\n\n)')
        matches = pattern.finditer((text))
        for match in matches:
            paragraph = match.group(1)
            if paragraph:
                text = text.replace(paragraph, "<paragraph>" + paragraph + "</paragraph>")
        return text.strip()




def main():
        initial_email = emailToString(untagged_email_file)
        untagged_email_file.close()
        emailAfterEndTimeTagger = endTimeTagger(initial_email)
        print(startTimeTagger(emailAfterEndTimeTagger))


main()
























"""

from os import listdir
from os.path import isfile, join


mypath = "seminars_untagged/untagged/"
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
corpus = nltk.corpus.reader.plaintext.PlaintextCorpusReader(mypath, onlyfiles)
all_text = corpus.raw()
print(all_text)"""
