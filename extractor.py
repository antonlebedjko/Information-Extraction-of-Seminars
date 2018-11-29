import re
from taggers import end_time_tagger, start_time_tagger, paragraphs_tagger, sentences_tagger, speaker_tagger, location_tagger
tagged_email_file = open('test_tagged/301.txt', "r")
#helper function to convert a file with an email to a string
def email_to_string(email_file):
        email = ''
        for ch in email_file:
                email+= ch
        return email

def extract(email):      
        pattern = re.compile('\<stime\>(.*?)\</stime\>')
        stimes_matches = pattern.finditer(email)
        for match in stimes_matches:
            stime = match.group(1)          
            if stime:                 
                print("stime: " + stime)
                

def main():
    initial_email = email_to_string(tagged_email_file)
    tagged_email_file.close()
    print(extract(initial_email))
main()
