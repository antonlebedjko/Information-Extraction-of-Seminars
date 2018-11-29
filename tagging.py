from taggers import end_time_tagger, start_time_tagger, paragraphs_tagger, sentences_tagger, speaker_tagger, location_tagger
untagged_email_file = open('seminars_untagged/untagged/301.txt', "r")
#helper function to convert a file with an email to a string
def email_to_string(email_file):
        email = ''
        for ch in email_file:
                email+= ch
        return email

def main():
        initial_email = email_to_string(untagged_email_file)
        untagged_email_file.close()       
        email_after_paragraph_tagger = paragraphs_tagger(initial_email)
        email_after_sentences_tagger = sentences_tagger(email_after_paragraph_tagger)
        email_after_end_time_tagger = end_time_tagger(email_after_sentences_tagger)        
        email_after_start_time_tagger = start_time_tagger(email_after_end_time_tagger)
        email_after_speaker_tagger = speaker_tagger(email_after_start_time_tagger)
        email_after_location_tagger = location_tagger(email_after_speaker_tagger)
        print(email_after_location_tagger)

main()
