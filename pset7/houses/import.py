from cs50 import SQL
import csv 
import sys 

def main():
    ''' Function that reads data from csv and write it to database'''

    # Check command line arguments
    if len(sys.argv) != 2:
        print('./Usage: import.py characters.csv')
        exit()
    
    # Set database connection
    db = SQL("sqlite:///students.db")
    
    # Open CSV
    file = sys.argv[1]
    with open(file) as students:
        reader = csv.DictReader(students)
        for row in reader:
            # Parse student
            student = parse_student(row)
            
            # Insert the student into the students.db 
            row_id = insert_student(db, student)
            # print(f'inserted student with id = {row_id}')
        
    
def parse_student(row):
    ''' Function that parses student info and returns dict'''
    student = {}
    
    name_parts = row['name'].split(' ')
    if len(name_parts) == 2:
        student['first'] = name_parts[0]
        student['middle'] = None
        student['last'] = name_parts[1]
    elif len(name_parts) == 3:
        student['first'] = name_parts[0]
        student['middle'] = name_parts[1]
        student['last'] = name_parts[2]
    
    student['house'] = row['house']
    student['birth'] = int(row['birth'])
    
    return student


def insert_student(db, student):
    '''Function that inserts student into students database'''
    
    query = '''INSERT INTO students(first,middle,last,house,birth) VALUES(?,?,?,?,?)'''
    return db.execute(query, student['first'], student['middle'], student['last'], student['house'], student['birth'])
    
    
main()