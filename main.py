import mysql.connector

mydb = mysql.connector.connect(
    host='localhost',
    user='root',
    password='Alliance98',
    port='3306',
    database='swye360'
)
# Get user input (Student Name);
# Select ID of Student Name
# Top Software used of userID
# Store it in an array
# Export it to graphing software (library)

#testsdfggdf

firstName = input("Please enter First name: ")
lastName = input("Please enter Last name: ")


mycursor = mydb.cursor()
mycursor.execute("SELECT first_name, last_name, studentlogin FROM student WHERE first_name = %s", (firstName,))

x = mycursor.fetchall()
print(x[0][0])


# mycursor = mydb.cursor()
#
# mycursor.execute('SELECT id, first_name FROM student')
#
# x = mycursor.fetchall()
# print(type(x))
#
# for y in x:
#     print(y)