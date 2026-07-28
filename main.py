"""
"""
import sqlite3
import csv

class main:
    # Setup databse
    def __init__ (self):
        connect = sqlite3.connect('Database.db')
        self.cursor = connect.cursor()

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
        """Read a CSV file and insert every row into the given table."""
        with open(csv_path, newline='', encoding='utf-8') as csv_file:
            reader = csv.DictReader(csv_file)
            rows = [tuple(row[column] for column in columns) for row in reader]

        placeholders = ', '.join('?' for _ in columns)
        column_list = ', '.join(columns)
        insert_sql = f"INSERT INTO {table_name} ({column_list}) VALUES ({placeholders});"
        self.cursor.executemany(insert_sql, rows)


    # Adds student to the Student table from inputed information
    def add_student(self):
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


def run():
    databse = main


if __name__ == "__main__":
    run()