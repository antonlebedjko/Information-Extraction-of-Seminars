import re
untagged_email_file = open('seminars_untagged/untagged/306.txt', "r")

#helper function to convert a file with an email to a string
def emailToString(email_file):
        email = ''
        for ch in email_file:
                email+= ch
        return email


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
                #because we append to the same string, if we have several matches at the same time, we need to track how many characters we have already appended before that. So, we increase start and end everytime when we add the new tags
                start = 0
                end = 0
                for match in matches:
                    match_start = match.start() + start
                    match_end = match.end() + end
                    line = line[0:match_start] + "<etime>" + line[match_start:match_end] + "</etime>" + line[match_end:]
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
                                #because we append to the same string, if we have several matches at the same time, we need to track how many characters we have already appended before that. So, we increase start and end everytime when we add the new tags
                                start = 0
                                end = 0
                                for match in matches:
                                    match_start = match.start() + start
                                    match_end = match.end() + end
                                    line = line[0:match_start] + "<stime>" + line[match_start:match_end ] + "</stime>" + line[match_end :]
                                    start += 15  # if we have more than one match in out matches array, we need to update the next match starting index, because we appended extra characters to the string
                                    end += 22  # same with the match end index
                                updated_email += line +'\n'
                else:
                       updated_email += line + '\n'
        return updated_email


#taging paragraphs using regular expression. It expects string as an input
def paragraphsTagger(email):
        pattern = re.compile(r'(?<=\n\n)(?:(?:\s*\b.+\b:(?:.|\s)+?)|(\s{0,4}[A-Za-z0-9](?:.|\n)+?\s*))(?=\n\n)')
        matches = pattern.finditer(email)
        for match in matches:
            paragraph = match.group(1)
            if paragraph:
                email = email.replace(paragraph, "<paragraph>" + paragraph + "</paragraph>")
        return email.strip()


#tagging sentences using regular expressions. This function depends on a paragraphsTagger(text) function, because it first of all searches for any paragraphs in an email
def sentencesTagger(email):       
        #pattern to find the paragraphs, because we have sentences inside them
        pattern = re.compile(r'(?<=\<paragraph\>)(?:(?:\s*\b.+\b:(?:.|\s)+?)|(\s{0,4}[A-Za-z0-9](?:.|\n)+?\s*))(?=\<\/paragraph\>)')
        paragraphs_matches = pattern.finditer(email)
        for match in paragraphs_matches:
            paragraph = match.group(1)
            if paragraph:                
                #pattern for finding the sentences in a paragraph
                sentence_pattern = re.compile(r'([A-Z][^\.!?]*[\.!?])')
                sentences_matches = sentence_pattern.finditer(paragraph)
                for sentence_match in sentences_matches:
                        sentence = sentence_match.group()                     
                        email = email.replace(sentence, "<sentence>" + sentence + "</sentence>")
        return email.strip()
        

def main():
        initial_email = emailToString(untagged_email_file)
        untagged_email_file.close()
        emailAfterParagraphTagger = paragraphsTagger(initial_email)
        emailAfterSentencesTagger = sentencesTagger(emailAfterParagraphTagger)
        emailAfterEndTimeTagger = endTimeTagger(emailAfterSentencesTagger)
        emailAfterStartTimeTagger = startTimeTagger(emailAfterEndTimeTagger)
        print(emailAfterStartTimeTagger)

main()
