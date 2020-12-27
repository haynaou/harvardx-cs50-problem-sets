from cs50 import SQL
import sys

def main():

    # Check command line arguments
    if len(sys.argv) != 2:
        print('./Usage: roster.py house')
        exit()

    house = sys.argv[1]

    # Set database connection
    db = SQL("sqlite:///students.db")

    # Query the students table in the students.db database for all of the students in the specified house.
    students = query_students(db, house)

    # Print out each student’s full name and birth year
    # formatted as, e.g., Harry James Potter, born 1980 or Luna Lovegood, born 1981
    for student in students:
        print_student(student)


def query_students(db, house):
    ''' Function that queries students full name and year of birth by house'''

    # Students should be ordered by last name. For students with the same last name, they should be ordered by first name.
    query = '''SELECT first, middle, last, birth FROM students WHERE house = ? COLLATE NOCASE ORDER BY last, first'''
    students = db.execute(query, house)
    return students


def print_student(student):
    ''' Function that prints single student'''
    if student['middle'] == None:
        print(f"{student['first']} {student['last']}, born {student['birth']}")
    else:
        print(f"{student['first']} {student['middle']} {student['last']}, born {student['birth']}")


main()