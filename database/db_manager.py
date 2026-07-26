import sqlite3

DATABASE = "database/exam.db"


class DatabaseManager:

    def __init__(self):
        self.connection = sqlite3.connect(DATABASE)
        self.conn = self.connection  
        self.cursor = self.connection.cursor()

    def create_table(self):

        self.cursor.execute("""

        CREATE TABLE IF NOT EXISTS students(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            name TEXT NOT NULL,

            roll TEXT UNIQUE,

            department TEXT,

            semester TEXT,

            email TEXT,

            phone TEXT,

            gender TEXT

        )

        """)
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS exam_results(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            roll TEXT,

            name TEXT,

            exam_date TEXT,

            duration TEXT,

            violations INTEGER,

            status TEXT,

            report_path TEXT

        )
        """)
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS questions(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question TEXT,
            option1 TEXT,
            option2 TEXT,
            option3 TEXT,
            option4 TEXT,
            answer TEXT
        )
        """)
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS student_answers(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            roll TEXT,

            question_id INTEGER,

            selected_answer TEXT,

            correct_answer TEXT,

            is_correct INTEGER

        )
        """)
        self.connection.commit()

    def insert_student(
        self,
        name,
        roll,
        department,
        semester,
        email,
        phone,
        gender
    ):

        self.cursor.execute("""

        INSERT INTO students(

            name,

            roll,

            department,

            semester,

            email,

            phone,

            gender

        )

        VALUES(?,?,?,?,?,?,?)

        """,

        (

            name,

            roll,

            department,

            semester,

            email,

            phone,

            gender

        ))

        self.connection.commit()

    def get_students(self):

        self.cursor.execute("SELECT * FROM students")

        return self.cursor.fetchall()

    def close(self):

        self.connection.close()
    def update_student(
        self,
        name,
        roll,
        department,
        semester,
        email,
        phone,
        gender
    ):

        self.cursor.execute("""
            UPDATE students
            SET
                name=?,
                department=?,
                semester=?,
                email=?,
                phone=?,
                gender=?
            WHERE roll=?
        """,
        (
            name,
            department,
            semester,
            email,
            phone,
            gender,
            roll
        ))

        self.connection.commit()
        self.cursor.execute("SELECT * FROM students WHERE roll=?", (roll,))
        print(self.cursor.fetchone())
    def delete_student(self, roll):

        self.cursor.execute(
            "DELETE FROM students WHERE roll=?",
            (roll,)
        )

        self.connection.commit()

    def search_student(self, roll):

        self.cursor.execute(
            "SELECT * FROM students WHERE roll LIKE ?",
            ('%' + roll + '%',)
        )

        return self.cursor.fetchall()
    def get_student_by_roll(self, roll):

        self.cursor.execute(
            "SELECT * FROM students WHERE roll=?",
            (str(roll),)
        )
        return self.cursor.fetchone()
    def save_exam_result(
        self,
        roll,
        name,
        duration,
        violations,
        status,
        report_path
    ):

        from datetime import datetime

        self.cursor.execute("""

        INSERT INTO exam_results(

            roll,

            name,

            exam_date,

            duration,

            violations,

            status,

            report_path

        )

        VALUES(?,?,?,?,?,?,?)

        """,

        (

            roll,

            name,

            datetime.now().strftime("%d-%m-%Y %H:%M:%S"),

            duration,

            violations,

            status,

            report_path

        ))

        self.connection.commit()
    def get_exam_results(self):

        self.cursor.execute(

            "SELECT * FROM exam_results ORDER BY id DESC"

        )

        return self.cursor.fetchall()
    def get_total_exams(self):

        self.cursor.execute(

            "SELECT COUNT(*) FROM exam_results"

        )

        return self.cursor.fetchone()[0]
    def get_average_violations(self):

        self.cursor.execute(

            "SELECT AVG(violations) FROM exam_results"

        )

        value = self.cursor.fetchone()[0]

        if value is None:
            return 0

        return round(value,2)
    def get_highest_violations(self):

        self.cursor.execute(

            "SELECT MAX(violations) FROM exam_results"

        )

        value = self.cursor.fetchone()[0]

        if value is None:
            return 0

        return value
    def get_questions(self):
        self.cursor.execute("SELECT * FROM questions")
        return self.cursor.fetchall()


    def get_question_by_id(self, question_id):
        self.cursor.execute(
            "SELECT * FROM questions WHERE id=?",
            (question_id,)
        )
        return self.cursor.fetchone()
    def save_student_answer(
            self,
            roll,
            question_id,
            selected_answer,
            correct_answer,
            is_correct
        ):

        self.cursor.execute("""
        INSERT INTO student_answers(

            roll,
            question_id,
            selected_answer,
            correct_answer,
            is_correct

        )
        VALUES(?,?,?,?,?)
        """,

        (
            roll,
            question_id,
            selected_answer,
            correct_answer,
            is_correct
        ))

        self.connection.commit()
    def get_student_answers(self, roll):

        self.cursor.execute("""

        SELECT *

        FROM student_answers

        WHERE roll=?

        """,(roll,))

        return self.cursor.fetchall()