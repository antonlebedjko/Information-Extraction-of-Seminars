from taggers import end_time_tagger, start_time_tagger, paragraphs_tagger, sentences_tagger, speaker_tagger, location_tagger
#untagged_email_file = open('seminars_untagged/untagged/303.txt', "r")
#helper function to convert a file with an email to a string
def email_to_string(email_file):
        email = ''
        for ch in email_file:
                email+= ch
        return email

def tag_one_email(email_file):
        untagged_email_file = open(email_file, "r")
        #untagged_email_file = open('seminars_untagged/untagged/303.txt', "r")
        initial_email = email_to_string(untagged_email_file)
        untagged_email_file.close()       
        email_after_paragraph_tagger = paragraphs_tagger(initial_email)
        email_after_sentences_tagger = sentences_tagger(email_after_paragraph_tagger)
        email_after_end_time_tagger = end_time_tagger(email_after_sentences_tagger)        
        email_after_start_time_tagger = start_time_tagger(email_after_end_time_tagger)
        email_after_speaker_tagger = speaker_tagger(email_after_start_time_tagger)
        email_after_location_tagger = location_tagger(email_after_speaker_tagger)
        return email_after_location_tagger

def tag_all_emails():
        for i in range(321, 327):
                out = open('tagged_by_my_code/' +str(i) + '.txt', "w")
                out.write(tag_one_email('seminars_untagged/untagged/' +str(i) + '.txt'))
                out.close()
print(tag_all_emails())