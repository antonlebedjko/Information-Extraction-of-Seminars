import re
untagged_email_file = open('../seminars_untagged/untagged/301.txt', "r")
email_list = []
for line in untagged_email_file:
        words = line.rstrip()
        email_list = email_list + [words]
untagged_email_file.close()

for words in email_list:
    pattern = re.compile(r'\b([0-9]{1,2}(?::[0-9]{2}\s?(?:AM|PM|am|pm|a\.m|p\.m)|:[0-9]{2}|\s?(?:AM|PM|am|pm|a\.m|p\.m)))\b')
    matches = pattern.finditer((words))
    for match in matches:
        print(match.start(), match.end(), match.group())


