import re
untagged_email_file = open('seminars_untagged/untagged/301.txt', "r")


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


#taging time using regular expression
def timeTagger(email_list):
        #empty string to append a whole email with tags
        updated_email = ''
        pattern = re.compile(r'\b([0-9]{1,2}(?::[0-9]{2}\s?(?:AM|PM|am|pm|a\.m|p\.m)|:[0-9]{2}|\s?(?:AM|PM|am|pm|a\.m|p\.m)))\b')
        for line in email_list:
                if(not "PostedBy" in line):                                      
                        matches = pattern.finditer((line))
                        #to check if there are any time patterns in a line
                        condition = (len(list(matches))==0)
                        if (condition):
                                updated_email += line + '\n'
                        else:
                                matches = pattern.finditer((line))
                                for match in matches:                                       
                                        line = line[0:match.start()] + "<stime>" + line[match.start():match.end()] + "</stime>" + line[match.end():]
                                        updated_email += line +'\n'
                else :
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
      email_with_paragraphs = paragraphsTagger(initial_email)
      email_with_paragraphs_to_list = email_with_paragraphs.split('\n')
      email_with_times = timeTagger(email_with_paragraphs_to_list)
      print(email_with_times)

main()








"""

def main():
        email_list = emailToList(untagged_email_file)
        text = timeTagger(email_list)
        #print(timeTagger(email_list))
        print(email_list)
        #print(paragraphsTagger(text))
        tagged_times = timeTagger(email_list)
        tagged_email = open("tagged_email.txt", "w")
        for c in tagged_times:
                tagged_email.write(c)


        tagged_email.close()

"""



















"""

from os import listdir
from os.path import isfile, join


mypath = "seminars_untagged/untagged/"
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
corpus = nltk.corpus.reader.plaintext.PlaintextCorpusReader(mypath, onlyfiles)
all_text = corpus.raw()
print(all_text)"""
