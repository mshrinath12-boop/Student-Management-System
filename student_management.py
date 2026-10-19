import os
import mysql.connector
from dotenv import load_dotenv
load_dotenv()

connection= mysql.connector.connect (
    host= os.getenv("DB_HOST"),
    user= os.getenv("DB_USER"),
    password= os.getenv("DB_PASSWORD"),
    database= os.getenv("DB_NAME"),
    auth_plugin='caching_sha2_password' 
)
if connection.is_connected():
    print("MySQL connection is Successful")
print("Connected database:", connection.database) 
def view_students():
   cursor= connection.cursor()
   try:
      cursor.execute("SELECT * FROM students")
      students= cursor.fetchall()      
      for student in students:
         print(f"ID:{student[0]} | Name: {student[1]} | Age: {student[2]} | Email: {student[3]} | Course: {student[4]} | City: {student[5]}")
   finally:
      cursor.close()
query = """
INSERT INTO students (name, age, email, course, city)
VALUES (%s, %s, %s, %s, %s)
"""
update_query= """
UPDATE students 
SET course= %s
WHERE student_id= %s
"""
def add_student():
   
   name= input ("Enter Student name: ")
   email= input ("Enter Student email: ")
   course= input ("Enter Student course: ")
   city= input ("Enter Student city: ")
   try:
    
     age=  int(input("Enter Student age: "))
   except ValueError:
    print("Please enter a valid age!")
    return
   if age <= 0:
    print("Age must be greater than zero!")
    return
   cursor= connection.cursor()
   try:
      cursor.execute(query,(name,age,email,course,city))
      connection.commit()
      print ("Student added successfully")
   except mysql.connector.errors.IntegrityError:
      print("Email already registered")
   finally:
      cursor.close()   
def update_student():
   try:
      student_id= int(input("Enter Student Id: ")) 
   except ValueError:
       print("Please enter a valid numeric Student ID!")
       return
   
   new_course = input("Enter New course: ").strip()
   if not new_course:
        print("Course cannot be empty!")
        return
   cursor = connection.cursor()
   try:
      cursor.execute(update_query, (new_course, student_id))
      connection.commit()
      if cursor.rowcount > 0:
            print("Student course updated successfully!")
      else:
            print("No rows changed. Check the Student ID or course.")

   except mysql.connector.Error as err:
        connection.rollback()
        print(f"Database error: {err}")

   finally:
        cursor.close()
   cursor= connection.cursor() 
   try:
      cursor.execute(update_query,(new_course,student_id))
      connection.commit()
      if cursor.rowcount > 0:
         print("Student Course Updated successfully")
      else:
         print("No row changed Check the student id or course")
   except mysql.connector.Error as err:
      connection.rollback()
      print(f"Databse error: {err}")



  
try:     
   while True:
      print("Student management system")
      print("1. Add Student")
      print("2. View Student")
      print("3. Exit")
      choice= input("Enter Your choice: ")
      if choice== "1":
         add_student()
      elif choice== "2":
         view_students()   
      elif choice== "3":
         print("Exiting")
         break
finally:
   connection.close()
   print("Database connection closed")