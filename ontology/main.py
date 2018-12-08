'''
What this class does, is: is opens all the emails which have been tagged by
taggers written by me. It uses the ontology class which does ontology for one email,
but it runs methods from it on all of the emails here. In the end, it prints the
ontology results for all of the departments.
'''
from ontology import *

def main():
    Computer_Science = []
    Biology = []
    Chemistry = []
    Electronics = []
    Physics = []
    Politics = []
    Languages = []
    Performing_Arts = []
    Finance = []
    all_departments = {'Science & Enginnering School': {'Computer Science':[], 'Biology':[], 'Chemistry':[], 'Electronics': [], 'Physics':[]}
                       ,'Arts School': {'Politics':[], 'Languages':[], 'Performing Arts':[]}
                       ,'Business School':{'Finance':[]}
                       ,'Other':{'Other' : []}
                       }
    for i in range(301, 486):
        department = ontology_on_one_email(str(i))
        if(department == 'Computer Science'):
            all_departments['Science & Enginnering School']['Computer Science'].append(str(i)+'.txt')
        elif(department == 'Biology'):
            all_departments['Science & Enginnering School']['Biology'].append(str(i)+'.txt')
        elif(department == 'Chemistry'):
            all_departments['Science & Enginnering School']['Chemistry'].append(str(i)+'.txt')
        elif(department == 'Electronics'):
            all_departments['Science & Enginnering School']['Electronics'].append(str(i)+'.txt')
        elif(department == 'Physics'):
            all_departments['Arts School']['Physics'].append(str(i)+'.txt')
        elif(department == 'Politics'):
            all_departments['Arts School']['Politics'].append(str(i)+'.txt')
        elif(department == 'Languages'):
            all_departments['Arts School']['Languages'].append(str(i)+'.txt')
        elif(department == 'Performing Arts'):
            all_departments['Arts School']['Performing Arts'].append(str(i)+'.txt')
        elif(department == 'Finance'):
            all_departments['Business School']['Finance'].append(str(i)+'.txt')
        elif(department == 'Other'):
            all_departments['Other']['Other'].append(str(i)+'.txt')
            

    for school in all_departments:
        print(school, ": ")
        print()
        for department in all_departments[school]:
            print("           ", department, ":    ")
            print()
            for file in all_departments[school][department]:
                print("                               ",file)
            print()
main()

