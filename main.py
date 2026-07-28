"""
"""
import sqlite3
import csv

class main:
    def __init__ (self):
        connect = sqlite3.connect('Database.db')
        self.cursor = connect.cursor()

        self.cursor.execute("DROP TABLE IF EXISTS 'Students';")
        self.cursor.execute("DROP TABLE IF EXISTS 'Teachers';")
        self.cursor.execute("DROP TABLE IF EXISTS 'Enrollments';")
        self.cursor.execute("DROP TABLE IF EXISTS 'Courese';")
        self.cursor.execute("DROP TABLE IF EXISTS 'Classroom';")

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

    def add_student(self):
        pass

    def add_teacher(self):
        pass

    def add_course(self):
        pass

    def add_classroom(self):
        pass

    def assign_student_to_course(self):
        pass

    def assign_teacher_to_course(self):
        pass

    def assign_classroom_to_course(self):
        pass

    def run(self):
        pass

if __name__ == "__main__":
    program = main()
    program.run()