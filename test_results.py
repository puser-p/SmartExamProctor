from database.db_manager import DatabaseManager

db = DatabaseManager()

results = db.get_exam_results()

for row in results:

    print(row)

db.close()