import re


untagged_email_file = open('seminars_untagged/untagged/301.txt', "r")

email_list = []
for line in untagged_email_file:
        words = line.rstrip()
        email_list = email_list + [words]
        
untagged_email_file.close()

def timeTagger(email_list):
        updated_email = ''
        pattern = re.compile(r'\b([0-9]{1,2}(?::[0-9]{2}\s?(?:AM|PM|am|pm|a\.m|p\.m)|:[0-9]{2}|\s?(?:AM|PM|am|pm|a\.m|p\.m)))\b')
        for line in email_list:
                if(not "PostedBy" in line):                                      
                        matches = pattern.finditer((line))
                        "print(len(list(matches))==1)"
                        "koroche zaceni, otkomentj strochku sverhu i poprobuj zapustitj programmu. Esli eto stroka zakomenchina, to v nachjale teksta mozno uvidetj tagi tipa <stime>, no esli otkomentitj, to boljshe ne rabotaet. Kak? ;DDD"
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

print(timeTagger(email_list))




"""print(email_list)"""


































"""

from os import listdir
from os.path import isfile, join


mypath = "seminars_untagged/untagged/"
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
corpus = nltk.corpus.reader.plaintext.PlaintextCorpusReader(mypath, onlyfiles)
all_text = corpus.raw()
print(all_text)"""
