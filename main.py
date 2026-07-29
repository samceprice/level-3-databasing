"""
"""
import sqlite3
import csv
import re
import datetime

class Database:
    # Setup databse
    def __init__ (self):
        self.connect = sqlite3.connect('Database.db')
        self.cursor = self.connect.cursor()

        self._remove_tables()
        self._create_tables()
        self._populate_tables_from_csv()

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

    # Add data into a given table table
    def _add_into_table(self, table, columns: list, data: list):
        column_names = ", ".join(columns)
        placeholders = ", ".join(["?"] * len(data))
        query = f"INSERT INTO {table} ({column_names}) VALUES ({placeholders})"
        self.cursor.execute(query, data)

    # Gets user input as a string and checks for required characters present in input   
    def _get_string_input(self, prompt):
        while True:
            user_input = input(prompt).strip()
            if len(user_input) <= 0:
                print("Please enter a non blank input")
                continue            
            return user_input

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

    # Gets user input for an email and checks it matches email syntax
    def _get_email_input(self, prompt):
        while True:
            user_input = input(prompt)
            if self._is_valid_email(user_input):
                return user_input
            else:
                print("Please enter a valid email")

    # Checks if a given email matches corect email syntax
    def _is_valid_email(email):
        # Syntax patern of an email   
        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    
        # Use fullmatch to ensure email matches syntax and trailing characters aren't accepted
        if re.fullmatch(pattern, email):
            return True
        return False

    # Gets user input for a date and checks its a real date
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
    
    # Adds student to the Student table from inputed information
    def add_student(self):
        self._add_into_table(
            "Students",
            ["first_name", "last_name", "date_of_birth", "email"],
            [
                self._get_string_input("Enter the students first name: ").title(),
                self._get_string_input("Enter the students last name: ").title(),
                self._get_date_input("students date of birth: "),
                self._get_email_input("Enter the students email: ")
            ] 
        )

    #Adds teacher to the Teacher table from inputed information
    def add_teacher(self):
        self._add_into_table(
            "Teachers",
            ["first_name", "last_name", "department", "email"],
            [
                self._get_string_input("Enter the teachers first name: ").title(),
                self._get_string_input("Enter the teachers last name: ").title(),
                self._get_string_input("Enter the teachers department: ").title(),
                self._get_email_input("Enter the teachers email: ")
            ]
        )

    # Adds course to the Course table from inputed information
    def add_course(self):
        self._add_into_table(
            "Course",
            ["course_name", "description", "credits", "classroom_id", "teacher_id"],
            [
                self._get_string_input("Enter the name of the course: "),
                self._get_string_input("Enter the description of the course: "),
                self._get_int_input("Enter the number of credits for the course: ", minimum = 0),
                self._get_int_input("Enter the classroom id for the course: ", minimum = 0),
                self._get_int_input("senter the teacher id for the course: ", minimum = 0)
            ]
        )

    # Adds classroom to the Classroom table from inputed information
    def add_classroom(self):
        """
            classroom_id INTERGER NOT NULL PRIMARY KEY,
            room_number INTERGER NOT NULL,
            capacity INTERGER NOT NULL,
            building_name STRING NOT NULL
        """
        self._add_into_table(
            "Classroom",
            ["room_number", "capacity", "building_name"],
            [
                self._get_int_input("Enter the room number for the classroom: ", minimum = 1),
                self._get_int_input("Enter the capacity for the classroom: ", minimum = 1),
                self._get_string_input("Enter the name of the building for the classroom: ")
            ]
        )

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


def run():
    databse = Database()
    databse.connect.commit()
    databse.connect.close()
    

if __name__ == "__main__":
    run()
    