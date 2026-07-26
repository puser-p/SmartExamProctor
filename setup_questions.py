from database.db_manager import DatabaseManager

db = DatabaseManager()

questions = [

(
"What is Python?",
"A Programming Language",
"Database",
"Browser",
"Operating System",
"A Programming Language"
),

(
"Which keyword is used for loop?",
"if",
"for",
"class",
"whilee",
"for"
),

(
"Which library is used for Computer Vision?",
"Numpy",
"OpenCV",
"Pandas",
"Tensorflow",
"OpenCV"
),

(
"Which database are we using?",
"MySQL",
"Oracle",
"SQLite",
"MongoDB",
"SQLite"
),

(
"What does AI stand for?",
"Artificial Intelligence",
"Advanced Internet",
"Auto Input",
"Artificial Internet",
"Artificial Intelligence"
)

]

conn = db.connection
cursor = conn.cursor()

cursor.executemany("""
INSERT INTO questions(
question,
option1,
option2,
option3,
option4,
answer
)
VALUES(?,?,?,?,?,?)
""",questions)

conn.commit()

print("Questions Inserted")