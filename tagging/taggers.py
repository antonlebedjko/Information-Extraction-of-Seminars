import re

def names_to_string(file):
    names = ''
    for ch in file:
        names += ch
    return names

#tagging the end of event times. If we want to tag all time appereances in the text, we should run our endTimeTagger before startTimeTagger, they deppend from each other
def end_time_tagger(email):
    # converting string with a whole email to a list
    email_list = email.split('\n')
    # empty string to append a whole email with tags
    updated_email = ''
    pattern = re.compile('([ ]{0,1})([-]|(?:-|(?<=until)))([ ]{0,1})[0-9]{1,2}?\:[0-9][0-9][ ]{0,1}[am|AM|pm|PM|a.m|A.M|p.m|P.M|\n|\s]{0,3}')
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
                        end_time = end_time.strip()
                        if(end_time[0] == '-'):
                                end_time = end_time[1:]
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
        pattern = re.compile(r'((?<!<etime>)(\b([0-9]{1,2}(?::[0-9]{2}\s?(?:AM|PM|am|pm|a\.m|p\.m)|:[0-9]{2}|\s?(?:AM|PM|am|pm|a\.m|p\.m)))\b)(?!\<\/etime>))')
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
        email = '\n\n{}\n\n'.format(email.strip('\n'))
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
        pattern = re.compile(r'(?<=<paragraph>)([\d\D]*?)(?=\<\/paragraph>)')
        paragraphs_matches = pattern.finditer(email)
        sentence_pattern = re.compile(r'(([A-Z][^\.!?]*)(?=[\.!?]))')     
        for match in paragraphs_matches:
            paragraph = match.group()           
            if paragraph:                 
                sentences_matches = sentence_pattern.finditer(paragraph)
                for sentence_match in sentences_matches:                       
                        sentence = sentence_match.group()   
                        #to actually tag a sentences, not initials which may appear in a text
                        if(len(sentence)>3):                                     
                                email = email.replace(sentence, "<sentence>" + sentence + "</sentence>")
        return email.strip()
        

def speaker_tagger(email):
        # The logic is to search for Who field. If it exists, we extract only a proper name from it,
        # if it doesn't exist, we search for Dr. or Professor
        found_who = False
        pattern = re.compile(r'(?<=who:)(.*)(?=\n)', flags=re.IGNORECASE)
        speaker =''
        try:
                match = pattern.findall(email)
                #if there is a "Who:" field, it means that there should be a speaker after that
                if(len(match)>0):
                        speaker = match[0]
                        speaker = "".join(speaker.split(",")) #delete all commas
                        # split all words to a list, so we can extract only a name, not everything in case if there are more than 2 words in a sting
                        words = speaker.split()
                        if(len(words)>2):
                            male_names = open('names-male.txt', "r")
                            m_names = names_to_string(male_names)
                            male_names.close()
                            female_names = open('names-female.txt', "r")
                            f_names = names_to_string(female_names)
                            female_names.close()
                            for i in range(0, len(words)):
                                #if we see Dr or Professor plus there are two more words after
                                if(len(words) - i >=3 and (words[i] == 'Dr.' or words[i] == 'Professor')):
                                    speaker = words[i] + " " + words[i + 1] + " " + words[i+2]
                                    break;
                                #if first word is in names database, second one ends with dot (like Paul M.) and third word just exists    
                                elif (len(words) - i >=3 and (words[i] in m_names.lower().title() or words[i].lower().title() in f_names) and words[i+1].endswith('.')):
                                    speaker = words[i] + " " + words[i+1]+ " " + words[i+2]
                                    break;
                                #if we see proper name + another word
                                elif (len(words) - i >=2 and (words[i] in m_names.lower().title() or words[i].lower().title() in f_names)):
                                    speaker = words[i] + " " + words[i+1]
                                    break;
                        
                        #check for all appereances of the speaker in the whole email. If there are, we tag all of them
                        speaker = speaker.strip()
                        email = re.sub(speaker.strip(), "<speaker>" + speaker.strip() + "</speaker>", email)
                        found_who = True
                if not found_who:
                        #pattern for Dr. or Professor and two words after that
                        speaker_pattern = re.compile('Professor\s\w+\s\w+\.\s\w+|Professor\s\w+\s\w+|Dr\.\s\w+\s\w+\.\s\w+|Dr\.\s\w+\s\w+|Professor\sAssistant\s\w+\s\w+')
                        match = speaker_pattern.findall(email)
                        speaker = match[0]
                        if (len(match)>0):
                                if speaker:
                                        email = email.replace(speaker.strip(), "<speaker>" + speaker.strip() + "</speaker>")
                                        
      

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
        except:
                pass
        if not found_place:
                pattern = re.compile(r'(?<=where:)(.*)(?=\n)', flags=re.IGNORECASE)
                try:
                        match = pattern.findall(email, re.I)
                        #if there is a "Where:" field, it means we found a location
                        if(len(match)>0):
                                location = match[0]
                                found_place = True
                                #check for all appereances of the location in the whole email. If there are, we tag all of them
                                email = email.replace(location.strip(), "<location>" + location.strip() + "</location>")
                except:
                        pass

        return email.strip()
