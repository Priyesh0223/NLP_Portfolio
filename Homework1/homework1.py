# Homework 1
# Priyesh Patel -PHP180002
# This Program reads in a csv file processes the text to be more standardized.
# Creating an object for each person with correction from the user.
# Outputting the final information for each person.


import pathlib
import sys
import re
import pickle

class Person:

    def __init__(self, last, first, mi, id, phone):
        # Inputs: Persons firstname, lastname, middle initial, ID, phone number
        # data Type: all strings
        self.last = last
        self.first = first
        self.mi = mi
        self.id = id
        self.phone = phone

    def display(self):
        # display a persons information with a format
        print('Employee id:',self.id)
        print('\t', self.first, self.mi, self.last)
        print('\t', self.phone, '\n')


def processData(data):
    # Input:  array of csv values for a person
    # data:   list of strings
    # return: dictionary of person objects created after processing

    persons = {}
    for person in data:
        #split a persons information into a array
        tokens = person.split(",");

        #process first and last name capitalize first character
        last = tokens[0].title()
        first = tokens[1].title()

        #process middle initial, if empty replace with "X"
        if tokens[2]:
            mi = tokens[2].title()
        else:
            mi = 'X' # if there isn't a middle name replace with "X"

        #process ID, if invalid ask user to input Corrected ID
        if re.match("^[A-Za-z]{2}[0-9]{4}$", tokens[3]):
            id = tokens[3]
        else:
            while not re.match("^[A-Za-z]{2}[0-9]{4}$", tokens[3]):
                print('ID invalid', tokens[3])
                print('ID is two letters followed by 4 digits.')
                print('Please enter a valid id:')
                tokens[3] = input()
                id = tokens[3].upper()

        #process phone number, check for proper formatting XXX-XXX-XXXX
        if re.match('^[0-9]{3}-[0-9]{3}-[0-9]{4}$', tokens[4]):
            phone = tokens[4]
        else:
            tokens[4] = re.sub(r'[^0-9]', '', tokens[4])
            phone = ''.join(tokens[4][:3]) + '-' + ''.join(tokens[4][3:6]) + '-' + ''.join(tokens[4][6:])
            while not re.match('^[0-9]{3}-[0-9]{3}-[0-9]{4}$', phone):
                print('Phone', phone, "is invalid")
                print('Enter phone number in form 123-456-7890')
                print('Enter phone number:')
                phone = input()

        #create person object and add the dictionary
        tempPerson = Person(last,first,mi,id,phone)
        if not tempPerson.id in persons.keys():
            persons[tempPerson.id] = tempPerson
        else:
            print("Error: ID exists in input file")

    #return processed people
    return persons

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # Check if user enter at least two arguments, if not display error and quit
    if len(sys.argv) < 2:
        print('Error: Please enter a filename as a system argument')
        quit()

    relativePath = sys.argv[1]
    with open(pathlib.Path.cwd().joinpath(relativePath), 'r') as file:
        text_in = file.read().splitlines()

    #get dictionary of employees
    employees = processData(text_in[1:])

    #pickle the employee
    pickle.dump(employees, open('employees.pickle', 'wb')) #write binary

    #read the pickle back in
    employees_in = pickle.load(open('employees.pickle', 'rb')) #read binary


    #Output the employees list
    print('\n\nEmployee List:\n')

    #display each person's information
    for emp_id in employees_in.keys():
        employees_in[emp_id].display()