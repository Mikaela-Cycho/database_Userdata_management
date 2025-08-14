import psycopg2
from psycopg2 import sql
import psycopg2
from psycopg2 import IntegrityError

# Database connection parameters
conn_params = {
    'dbname': 'school',
    'user': 'postgres', # Replace 'dummy_user' with your actual database username
    'password': 'sy199912', # Replace 'dummy_password' with your actual database password
    'host': 'localhost'
}

# cursor = connection.cursor()

#Function to connect to the database
def connect_db():
    conn = psycopg2.connect(**conn_params)
    return conn

# CRUD operations
def getAllStudents():
    conn = connect_db() #connect to database
    cur = conn.cursor()
    cur.execute("SELECT * FROM students") 
    records = cur.fetchall()
    print("Student Records:")
    for rec in records:
        print(rec)
    cur.close()
    conn.close()

#add student function
def addStudent(first_name, last_name, email, enrollment_date):
    # insert a new student record into the database. use try and except to avoid app crushing 
    try: 
        conn = connect_db()
        cur = conn.cursor()
        cur.execute("INSERT INTO students (first_name, last_name, email, enrollment_date) VALUES (%s, %s, %s, %s)",
                    (first_name, last_name, email, enrollment_date))
        conn.commit()
        print("Student added successfully.")
    except IntegrityError:
        print("Error: A student with the same email already exists.")
    finally:
        cur.close()
        conn.close()


#update the email address for the specified student
def updateStudentEmail(student_id, new_email):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("UPDATE students SET email = %s WHERE student_id = %s",
                (new_email, student_id))
    if cur.rowcount == 0: #checker
        print("No student found with the specified ID.")
    else:
        conn.commit()
        print("Student email updated successfully.")
    
    cur.close()
    conn.close()



# to delete student from the database
def deleteStudent(student_id):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM students WHERE student_id = %s", (student_id,))
    if cur.rowcount == 0: # checker
        print("No student found with the specified ID.")
    else:
        conn.commit()
        print("Student deleted successfully.")
    cur.close()
    conn.close()


# main function for testing, give the user 5 choices
def main():
    while True: #loop until user chooses 5
        print("\nAvailable actions: \n1. Show all students \n2. Add a student \n3. Update a student's email \n4. Delete a student \n5. Exit")
        choice = input("Enter your choice (1-5): ")

        if choice == '1':
            getAllStudents()
        elif choice == '2':
            first_name = input("Enter first name: ")
            last_name = input("Enter last name: ")
            email = input("Enter email: ")
            enrollment_date = input("Enter enrollment date (YYYY-MM-DD): ")
            addStudent(first_name, last_name, email, enrollment_date)
        elif choice == '3':
            student_id = input("Enter student ID to update email: ")
            new_email = input("Enter new email: ")
            updateStudentEmail(int(student_id), new_email)
        elif choice == '4':
            student_id = input("Enter student ID to delete: ")
            deleteStudent(int(student_id))
        elif choice == '5':
            print("Exiting program.")
            break
        else:
            print("Invalid choice, please try again.")


if __name__ == "__main__":
    main()