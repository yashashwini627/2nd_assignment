import csv
import mysql.connector

csv_filename = "students.csv"
data = [
    [1, "yashashwini", 85],
    [2, "keerti" 90],
    [3, "shivaram", 78]
]

with open(csv_filename, mode="w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["id", "name", "marks"])
    writer.writerows(data)

new_record = [4, "David", 88]
with open(csv_filename, mode="a", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(new_record)

conn = mysql.connector.connect(host="localhost", user="root", password="Yvss@123")
cursor = conn.cursor()
cursor.execute("CREATE DATABASE IF NOT EXISTS student_db")
cursor.execute("USE student_db")
cursor.execute("""
    CREATE TABLE IF NOT EXISTS students (
        id INT PRIMARY KEY,
        name VARCHAR(50),
        marks INT
    )
""")

with open(csv_filename, mode="r") as file:
    reader = csv.reader(file)
    next(reader)  # Skip header
    for row in reader:
        cursor.execute("INSERT INTO students (id, name, marks) VALUES (%s, %s, %s) ON DUPLICATE KEY UPDATE name=%s, marks=%s", (row[0], row[1], row[2], row[1], row[2]))
conn.commit()

additional_records = [
    (5, "sunanda", 92),
    (6, "veer", 80)
]
cursor.executemany("INSERT INTO students (id, name, marks) VALUES (%s, %s, %s)", additional_records)
conn.commit()

output_filename = "students_from_db.csv"
cursor.execute("SELECT * FROM students")
data_from_db = cursor.fetchall()

with open(output_filename, mode="w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["id", "name", "marks"])
    writer.writerows(data_from_db)

print("Data from database:")
cursor.execute("SELECT * FROM students")
for row in cursor.fetchall():
    print(row)

cursor.close()
conn.close()
