"""
"""
import sqlite3
import csv
import re
import datetime


class Database:
    # Setup databse
    def __init__(self):
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
        self.cursor.execute("DROP TABLE IF EXISTS 'Course';")
        self.cursor.execute("DROP TABLE IF EXISTS 'Classroom';")

    # Sets up all tables for the database
    def _create_tables(self):
        self.cursor.execute("""
            CREATE TABLE Students (
            student_id INTEGER NOT NULL PRIMARY KEY,
            first_name STRING NOT NULL,
            last_name STRING NOT NULL,
            date_of_birth STRING NOT NULL,
            email STRING NOT NULL
            );
        """)

        self.cursor.execute("""
            CREATE TABLE Teachers (
            teacher_id INTEGER NOT NULL PRIMARY KEY,
            first_name STRING NOT NULL,
            last_name STRING NOT NULL,
            department STRING NOT NULL,
            email STRING NOT NULL
            );
        """)

        self.cursor.execute("""
            CREATE TABLE Enrollments (
            enrollment_id INTEGER NOT NULL PRIMARY KEY,
            student_id INTEGER NOT NULL,
            course_id INTEGER NOT NULL,
            enrollment_date STRING NOT NULL,
            FOREIGN KEY (student_id) REFERENCES Student(student_id),
            FOREIGN KEY (course_id) REFERENCES Course(course_id)
            );
        """)

        self.cursor.execute("""
            CREATE TABLE Course (
            course_id INTEGER NOT NULL PRIMARY KEY,
            course_name STRING NOT NULL,
            description STRING NOT NULL,
            credits INTEGER NOT NULL,
            classroom_id INTEGER NOT NULL,
            teacher_id INTEGER NOT NULL,
            FOREIGN KEY (classroom_id) REFERENCES Classroom(classroom_id),
            FOREIGN KEY (teacher_id) REFERENCES Teacher(teacher_id)
            );
        """)

        self.cursor.execute("""
            CREATE TABLE Classroom (
            classroom_id INTEGER NOT NULL PRIMARY KEY,
            room_number INTEGER NOT NULL,
            capacity INTEGER NOT NULL,
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
        self._import_csv('csv/courses_detailed_with_ids.csv', 'Course',
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

    # Changes a data point in a column at the point of the given id
    def _change_data_in_table(self, table, column, id, data):
        self.cursor.execute(
            f"UPDATE {table} SET {column} = ? WHERE rowid = ?",
            (data, id)
        )

    # Gets primary key from a 
    def _query_primary_key(self, table, search_columns, text_queries, operator):
        # Checks if a single value has been passed in for the colums instead of a list and converts it to a list
        if not isinstance(search_columns, list):
            search_columns = [search_columns]
        # Checks if a single value has been passed in for the text queries instead of a list and converts it to a list
        if not isinstance(text_queries, list):
            text_queries = [text_queries]

        # Check that columns and values have the same lenth
        if len(search_columns) != len(text_queries):
            raise ValueError("Number of search columns must match number of query values")

        # Sets conditions
        conditions = f" {operator} ".join([f"{column} = ?" for column in search_columns])
        query = f"SELECT rowid FROM {table} WHERE {conditions}"
        self.cursor.execute(query, tuple(text_queries))

        results = self.cursor.fetchall()

        # Checks for a single result
        if len(results) == 1:
            return results[0][0]

        # Checks for multiple results and settles them
        elif len(results) > 1:
            print("Multiple results have been found:")
            for result in results:
                print(f"    {result[0]}")

            while True:
                result_to_use = self._get_int_input(
                    "Enter the id that you would like to proceed with: ",
                    minimum=0
                )

                if (result_to_use,) in results:
                    return result_to_use
                else:
                    print("Please enter an id from the given results")

        #  Fallback if no results found
        else:
            return None

    # Gets user input as a string and checks for required characters present in input   
    def _get_string_input(self, prompt):
        while True:
            user_input = input(prompt).strip()
            if len(user_input) <= 0:
                print("Please enter a non blank input")
                continue            
            return user_input

    # Gets user input as an integer and checks its within range
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
    def _is_valid_email(self, email):
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
                month = int(input("Enter month for " + prompt))
                day = int(input("Enter day for " + prompt))
                
                if self._is_valid_date(year, month, day):
                    return f"{year:04d}-{month:02d}-{day:02d}"
                else:
                    print("Enter a valid date")

            except ValueError:
               print ("please enter a valid date")

    # Checks if a date is valid
    def _is_valid_date(self, year, month, day):
        try:
            datetime.date(year, month, day)
            return True
        
        except ValueError:
            return False

    # Gets the id of a student from the first and last name
    def _get_student_id(self):
        while True:
            student_id = self._query_primary_key(
                "Students",
                ["first_name", "last_name"],
                [
                    self._get_string_input("Please enter the first name of the student to search: ").title(),
                    self._get_string_input("Please enter the last name of the student to search: ").title()
                ],
                "AND" 
            )
            if student_id is not None:
                return student_id
            else:
                print("No student with that name found please try a name that is in the database")

    # Gets the id of a teacher from the first and last name
    def _get_teacher_id(self):
        while True:
            teacher_id = self._query_primary_key(
                "Teachers",
                ["first_name", "last_name"],
                [
                    self._get_string_input("Please enter the first name of the teacher to search: ").title(),
                    self._get_string_input("Please enter the last name of the teacher to search: ").title()
                ],
                "AND"                
            )
            if teacher_id is not None:
                return teacher_id
            else:
                print("No teacher with that name found please try a name that is in the database")

    # gets the id of a course from its name
    def _get_course_id(self):
        while True:
            course_id = self._query_primary_key(
                "Course",
                "course_name",
                self._get_string_input("Enter the name of the course to search for: ").title(),
                "AND"
            )
            if course_id is not None:
                return course_id
            else:
                print("No course with that name found please enter a course name that is in the database")

    # Gets the id of a classroom from its room number
    def _get_classroom_id(self):
        while True:
            classroom_id = self._query_primary_key(
                "Classroom",
                "room_number",
                self._get_int_input("Enter the room number of the classroom to search: "),
                "AND"
            )
            if classroom_id is not None:
                return classroom_id
            else:
                print("No classroom with that room number found please enter a room number that is in the database")

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
                self._get_string_input("Enter the name of the course: ").title(),
                self._get_string_input("Enter the description of the course: "),
                self._get_int_input("Enter the number of credits for the course: ", minimum = 0),
                self._get_classroom_id(),
                self._get_teacher_id()
            ]
        )

    # Adds classroom to the Classroom table from inputed information
    def add_classroom(self):
        self._add_into_table(
            "Classroom",
            ["room_number", "capacity", "building_name"],
            [
                self._get_int_input("Enter the room number for the classroom: ", minimum = 1),
                self._get_int_input("Enter the capacity for the classroom: ", minimum = 1),
                self._get_string_input("Enter the name of the building for the classroom: ").title()
            ]
        )

    # Assigns student to a given course from inputed infomation
    def assign_student_to_course(self):
        self._add_into_table(
            "Enrollments",
            ["student_id", "course_id", "enrollment_date"],
            [
                self._get_student_id(),
                self._get_course_id(),
                self._get_date_input("enrollment date: ")
            ]
        )

    # Assigns teacher to a given course from inputed infomation
    def assign_teacher_to_course(self):
        self._change_data_in_table(
            "Course",
            "teacher_id",
            self._get_course_id(),
            self._get_teacher_id()
        )

    # Assigns classroom to a given course from inputed infomation
    def assign_classroom_to_course(self):
        self._change_data_in_table(
            "Course",
            "classroom_id",
            self._get_course_id(),
            self._get_classroom_id()
        )

    # Search for a list of courses with the room and teacher based on a students name
    def search_course_by_student(self):
        student_id = self._get_student_id()

        self.cursor.execute("""
            SELECT Course.course_name
            FROM Enrollments
            JOIN Course ON Enrollments.course_id = Course.course_id
            WHERE Enrollments.student_id = ?
        """, (student_id,))

        courses = self.cursor.fetchall()

        if courses:
            print("\nThe selected student takes the following courses:")
            for course in courses:
                print(f" - {course[0]}")
        else:
            print("The selected student is not enrolled in any courses.")
        
    # Search for a list of students based on a teachers name
    def search_student_by_teacher(self):
        teacher_id = self._get_teacher_id()

        self.cursor.execute("""
            SELECT Students.first_name, Students.last_name
            FROM Enrollments
            JOIN Students on Enrollments.student_id = Students.student_id 
            JOIN Course on Enrollments.course_id = Course.course_id
            WHERE Course.teacher_id = ?
        """, (teacher_id,))

        students = list(set(self.cursor.fetchall()))

        if students:
            print("\nThe selected teacher teaches the following students:")
            for student in students:
                print(f" - {student[0]} {student[1]}")
        else:
            print("The selected teacher does not teach any students.")

    # Save and exit
    def save_and_exit(self):
        self.connect.commit()
        self.connect.close()
        exit()


def run():
    database = Database()
    menu = {
        "add classroom" : "database.add_classroom()",
        "add course" : "database.add_course()",
        "add student" : "database.add_student()",
        "add teacher" : "database.add_teacher()",
        "assign classroom to course" : "database.assign_classroom_to_course()",
        "assign student to course" : "database.assign_student_to_course()",
        "assign teacher to course" : "database.assign_teacher_to_course()",
        "search course by student" : "database.search_course_by_student()",
        "search student by teacher" : "database.search_student_by_teacher()",
        "save and exit" : "database.save_and_exit()",
        "exit" : "exit()"
    }

    while True:    
        print("Menu:")
        for item in menu.keys():
            print(f"  {str(list(menu.keys()).index(item) + 1)}) {item}")   

        while True:
            to_run = input("\nEnter the function to run: ")

            if to_run == "":
                print("Please enter a valid function to run")
            elif to_run in list(menu.keys()):
                print(f"running - {menu[to_run]}")
                eval(menu[to_run])
            elif to_run.isdecimal():
                if int(to_run) > 0 and int(to_run) <= len(menu):
                    to_run = list(menu.keys())[int(to_run)-1]
                    print(f"running - {menu[to_run]}")
                    eval(menu[to_run])
                else:
                    print("Please enter a valid function to run")
            else:
                print ("Please enter a valid function to run")
    

if __name__ == "__main__":
    run()
    