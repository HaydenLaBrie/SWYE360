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
print(x)
i = 0
while x[i][1] != lastName:
    i = i + 1

##Prints user id
currentUserID = x[i][2]
print(currentUserID)

#gets the appid, appdetails, start, end, totalSpentTime, urlAppId, and sort by time spent
mycursor.execute("SELECT appid, appdetails, start, end, totalSpentTime, urlAppId FROM swye360.students_analytics WHERE loginid= %s ORDER BY totalSpentTime DESC", (currentUserID,))
x = mycursor.fetchall()
print(x)


#next step is getting rid of duplicate urlAppId's since you can't do it in SQL. Get top 5 unique...

# mycursor = mydb.cursor()
#
# mycursor.execute('SELECT id, first_name FROM student')
#
# x = mycursor.fetchall()
# print(type(x))
#
# for y in x:
#     print(y)