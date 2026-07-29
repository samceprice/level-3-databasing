"""
"""
import sqlite3
import csv
import datetime

class main:
    # Setup databse
    def __init__ (self):
        self.connect = sqlite3.connect('Database.db')
        self.cursor = self.connect.cursor()

        self._remove_tables()
        self._create_tables()
        self._populate_tables_from_csv()

        self.connect.commit()
        self.connect.close()

    # Removes previously setup tables for rerunability
    def _remove_tables(self):
        self.cursor.execute("DROP TABLE IF EXISTS 'Students';")
        self.cursor.execute("DROP TABLE IF EXISTS 'Teachers';")
        self.cursor.execute("DROP TABLE IF EXISTS 'Enrollments';")
        self.cursor.execute("DROP TABLE IF EXISTS 'Courese';")
        self.cursor.execute("DROP TABLE IF EXISTS 'Classroom';")

    # Sets up all tables for the database
    def _create_tables(self):
        self.cursor.execute("""
            CREATE TABLE Students (
            student_id INTERGER NOT NULL PRIMARY KEY,
            first_name STRING NOT NULL,
            last_name STRING NOT NULL,
            date_of_birth STRING NOT NULL,
            email STRING NOT NULL
            );
        """)

        self.cursor.execute("""
            CREATE TABLE Teachers (
            teacher_id INTERGER NOT NULL PRIMARY KEY,
            first_name STRING NOT NULL,
            last_name STRING NOT NULL,
            department STRING NOT NULL,
            email STRING NOT NULL
            );
        """)

        self.cursor.execute("""
            CREATE TABLE Enrollments (
            enrollment_id INTERGER NOT NULL PRIMARY KEY,
            student_id INTERGER NOT NULL,
            course_id INTERGER NOT NULL,
            enrollment_date STRING NOT NULL,
            FOREIGN KEY (student_id) REFERENCES Student(student_id)
            FOREIGN KEY (course_id) REFERENCES Course(course_id)
            );
        """)

        self.cursor.execute("""
            CREATE TABLE Courese (
            course_id INTERGER NOT NULL PRIMARY KEY,
            course_name STRING NOT NULL,
            description STRING NOT NULL,
            credits INTERGER NOT NULL,
            classroom_id INTERGER NOT NULL,
            teacher_id INTERGER NOT NULL,
            FOREIGN KEY (classroom_id) REFERENCES Classroom(classroom_id)
            FOREIGN KEY (teacher_id) REFERENCES Teacher(teacher_id)
            );
        """)

        self.cursor.execute("""
            CREATE TABLE Classroom (
            classroom_id INTERGER NOT NULL PRIMARY KEY,
            room_number INTERGER NOT NULL,
            capacity INTERGER NOT NULL,
            building_name STRING NOT NULL
            );
        """)

    # Populates tables for the database with base data from csv files
    def _populate_tables_from_csv(self):
        self._import_csv('csv/classrooms_with_pk.csv', 'Classroom',
            ['classroom_id', 'room_number', 'capacity', 'building_name'])
        self._import_csv('csv/teachers_with_pk.csv', 'Teachers',
            ['teacher_id', 'first_name', 'last_name', 'department', 'email'])
        self._import_csv('csv/students_with_pk.csv', 'Students',
            ['student_id', 'first_name', 'last_name', 'date_of_birth', 'email'])
        self._import_csv('csv/courses_detailed_with_ids.csv', 'Courese',
            ['course_id', 'course_name', 'description', 'credits', 'classroom_id', 'teacher_id'])
        self._import_csv('csv/enrollments_with_pk.csv', 'Enrollments',
            ['enrollment_id', 'student_id', 'course_id', 'enrollment_date'])

    # Internal Funciton to import csv into a table from given data
    def _import_csv(self, csv_path, table_name, columns):
        # Read a CSV file and insert every row into the given table
        with open(csv_path, newline='', encoding='utf-8') as csv_file:
            reader = csv.DictReader(csv_file)
            rows = [tuple(row[column] for column in columns) for row in reader]
        placeholders = ', '.join('?' for _ in columns)
        column_list = ', '.join(columns)
        insert_sql = f"INSERT INTO {table_name} ({column_list}) VALUES ({placeholders});"
        self.cursor.executemany(insert_sql, rows)

    # Adds student to the Student table from inputed information
    def add_student(self):
        """ student_id INTERGER NOT NULL PRIMARY KEY,
            first_name STRING NOT NULL,
            last_name STRING NOT NULL,
            date_of_birth STRING NOT NULL,
            email STRING NOT NULL"""
        pass



    #Adds teacher to the Teacher table from inputed information
    def add_teacher(self):
        pass

    # Adds course to the Course table from inputed information
    def add_course(self):
        pass

    # Adds classroom to the Classroom table from inputed information
    def add_classroom(self):
        pass

    # Assigns student to a given course from inputed infomation
    def assign_student_to_course(self):
        pass

    # Assigns teacher to a given course from inputed infomation
    def assign_teacher_to_course(self):
        pass

    # Assigns classroom to a given course from inputed infomation
    def assign_classroom_to_course(self):
        pass

    # Search for a list of courses with the room and teacher based on a students name
    def search_course_by_student(self):
        pass

    # Search for a list of students based on a teachers name
    def search_student_by_teacher(self):
        pass

    # Gets user input as a string and checks for required characters present in input   
    def _get_string_input(self, prompt, required_characters = []):
        while True:
            user_input = input(prompt)
            if len(required_characters) >= 1:
                for character in required_characters:
                    if character not in user_input:
                        print ("invalid input")
                        continue

    # Gets user input as an interger and checks its within range
    def _get_int_input(self, prompt, minimum = None, maximum = None):
        while True:
            try: 
                user_input = int(input(prompt))

                # Checks if user input fits minimum and maximum values if provided and throws error if out of range
                if minimum is not None and maximum is not None:
                    if user_input >= minimum and user_input <= maximum:
                        return user_input
                    else: 
                        raise ValueError
                elif minimum is not None and  maximum is None:
                    if user_input >= minimum:
                        return user_input
                    else: 
                        raise ValueError
                elif maximum is not None and minimum is None:
                    if user_input <= maximum:
                        return user_input
                    else: 
                        raise ValueError
                else:
                    return user_input

            except ValueError:
                print ("Please enter a valid input")


    # Gets user input as a date and checks its a real date
    def _get_date_input(self, prompt):
        # return as yyyy-mm-dd
        while True:
            try:
                year = int(input("Enter year for " + prompt))
                month = int(input("Enter mother for " + prompt))
                day = int(input("Enter day for " + prompt))
                
                if self._is_valid_date(year, month, day):
                    return f"{year:04d}-{month:02d}-{day:02d}"
                else:
                    print("Enter a valid date")

            except ValueError:
               print ("please enter a valid date")

    # Checks if a date is valid
    def _is_valid_date (year, month, day):
        try:
            datetime.date(year, month, day)
            return True
        
        except ValueError:
            return False

def run():
    databse = main()
    

if __name__ == "__main__":
    run()