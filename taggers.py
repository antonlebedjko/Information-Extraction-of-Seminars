import re
untagged_email_file = open('seminars_untagged/untagged/333.txt', "r")

#tagging the end of event times. If we want to tag all time appereances in the text, we should run our endTimeTagger before startTimeTagger, they deppend from each other
def end_time_tagger(email):
    # converting string with a whole email to a list
    email_list = email.split('\n')
    # empty string to append a whole email with tags
    updated_email = ''
    # different patterns, need to evaluate to choose the best one in the end
    pattern = re.compile(r'\b([0-9]{1,2}(?::[0-9]{2}\s?(?:AM|PM|am|pm|a\.m|p\.m)|:[0-9]{2}|\s?(?:AM|PM|am|pm|a\.m|p\.m)))\b')
    pattern = re.compile('[ ]([-]|(?:-|until))[ ][0-9][0-9]?\:[0-9][0-9][ ][am|AM|pm|PM|a.m|A.M|p\.m\.|p.m|P.M]{2,3}')
    pattern = re.compile('([ ]{0,1})([-]|(?:-|(?<=until)))([ ]{0,1})[0-9][0-9]?\:[0-9][0-9][ ][am|AM|pm|PM|a.m|A.M|p.m|P.M|]{2,3}')
    #<etime>- 5:00 PM</etime> need to fix this problem with minus
    for line in email_list:
        if (not "PostedBy" in line):
            matches = pattern.finditer((line))
            # to check if there are any time patterns in a line
            condition = (len(list(matches)) == 0)
            if (condition):
                updated_email += line + '\n'
            else:
                matches = pattern.finditer((line))
                for match in matches:
                    end_time = match.group()
                    if end_time:
                        line = line.replace(end_time.strip(), "<etime>" + end_time.strip() + "</etime>")
                updated_email += line + '\n'
        else:
            updated_email += line + '\n'
    return updated_email


#tagging the start of event times or just any other times in the email, which potentially should also be the starting times.
#Before calling this method, we should call endTimeTagger, otherwise we will tag the <etime> as <stime>, because out pattern checks first of all which times are not already tagged as <etime>
def start_time_tagger(email):
        #converting string with a whole email to a list
        email_list = email.split('\n')
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
                                for match in matches:
                                    start_time = match.group()
                                    line = line.replace(start_time.strip(), "<stime>" + start_time.strip() + "</stime>")
                                updated_email += line +'\n'
                else:
                       updated_email += line + '\n'
        return updated_email


#taging paragraphs using regular expression. It expects string as an input
def paragraphs_tagger(email):
        pattern = re.compile(r'(?<=\n\n)(?:(?:\s*\b.+\b:(?:.|\s)+?)|(\s{0,4}[A-Za-z0-9](?:.|\n)+?\s*))(?=\n\n)')
        matches = pattern.finditer(email)
        for match in matches:
            paragraph = match.group(1)         
            if paragraph:
                email = email.replace(paragraph, "<paragraph>" + paragraph + "</paragraph>")
        return email.strip()


#tagging sentences using regular expressions. This function depends on a paragraphsTagger(text) function, because it first of all searches for any paragraphs in an email
def sentences_tagger(email):       
        #pattern to find the paragraphs, because we have sentences inside them
        pattern = re.compile(r'(?<=\<paragraph\>)(?:(?:\s*\b.+\b:(?:.|\s)+?)|(\s{0,4}[A-Za-z0-9](?:.|\n)+?\s*))(?=\<\/paragraph\>)')
        paragraphs_matches = pattern.finditer(email)
        sentence_pattern = re.compile(r'(([A-Z][^\.!?]*)(?=[\.!?]))')
        for match in paragraphs_matches:
            paragraph = match.group(1)           
            if paragraph:                 
                sentences_matches = sentence_pattern.finditer(paragraph)
                for sentence_match in sentences_matches:                       
                        sentence = sentence_match.group()   
                        #to actually tag a sentences, not initials which may appear in a text
                        if(len(sentence)>3):                                         
                                email = email.replace(sentence, "<sentence>" + sentence + "</sentence>")
        return email.strip()
        

def speaker_tagger(email):
        #to check if we can get a speaker from the "Who:"" field, if it exists in an email. 
        #If it does, we will tag it as a speaker and will search for all of the appearences of the same speaker in the whole email and will tag them as well.
        #If it doesn't we will use the POS and wiki to try to find the speaker in an email
        found_who = False
        pattern = re.compile(r'(?<=who:)(.*)(?=\n)', flags=re.IGNORECASE)
        try:
                match = pattern.findall(email)
                #if there is a "Who:" field, it means we found a speaker
                if(len(match)>0):
                        speaker = match[0]                       
                        found_who = True
                        #check for all appereances of the speaker in the whole email. If there are, we tag all of them
                        email = re.sub(speaker.strip(), "<speaker>" + speaker.strip() + "</speaker>", email)
                if not found_who:
                        #Use POS and wiki here
                        print("no2")
        except:
                pass
        return email.strip()


def location_tagger(email):
        #to check if we can get a location from the "Place:"" field, if it exists in an email. 
        #If it does, we will tag it as a location and will search for all of the appearences of the same location in the whole email and will tag them as well.
        #If it doesn't we will use the POS and wiki to try to find the location in an email
        found_place = False
        pattern = re.compile(r'(?<=place:)(.*)(?=\n)', flags=re.IGNORECASE)
        try:
                match = pattern.findall(email, re.I)
                #if there is a "Place:" field, it means we found a location
                if(len(match)>0):
                        location = match[0]
                        found_place = True
                        #check for all appereances of the location in the whole email. If there are, we tag all of them
                        email = email.replace(location.strip(), "<location>" + location.strip() + "</location>")
                if not found_place:
                        #Use POS and wiki here
                        print("no")
        except:
                pass
        return email.strip()
