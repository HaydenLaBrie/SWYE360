from urllib.parse import urlparse
import mysql.connector
import matplotlib.pyplot as plt
import pandas as pd
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

# firstName = input("Please enter First name: ")
# lastName = input("Please enter Last name: ")
firstName = "Hayden"
lastName = "Jones"

mycursor = mydb.cursor()
mycursor.execute("SELECT first_name, last_name, studentlogin FROM student WHERE first_name = %s AND last_name = %s",
                 (firstName, lastName))

x = mycursor.fetchall()

# Prints user id
currentUserID = x[0][2]
# print(currentUserID)

# gets the appid, appdetails, start, end, totalSpentTime, urlAppId, and sort by time spent
mycursor.execute(
    "SELECT appid, appdetails, start, end, totalSpentTime, urlAppId FROM swye360.students_analytics WHERE loginid= %s ORDER BY totalSpentTime DESC",
    (currentUserID,))
x = mycursor.fetchall()
# print(x[0][5])

# Gets rid of duplicate urlAppId's SQL command that groups by appid and sums up the total time spent for duplicate
# appid values. Returns appid, the app information, start and end time, sum total, and URLappID.
mycursor.execute(
    "SELECT appid, MAX(appdetails), MAX(start), MAX(end), SUM(totalSpentTime), MAX(urlAppId) FROM swye360.students_analytics group by appid ORDER BY SUM(totalSpentTime) DESC")
top_used_software = mycursor.fetchall()
print("#1: " + top_used_software[0][1] + " ---- " + "Total time: " + str(top_used_software[0][4]))
print("#2: " + top_used_software[1][1] + " ---- " + "Total time: " + str(top_used_software[1][4]))
print("#3: " + top_used_software[2][1] + " ---- " + "Total time: " + str(top_used_software[2][4]))
print("#4: " + top_used_software[3][1] + " ---- " + "Total time: " + str(top_used_software[3][4]))
print("#5: " + top_used_software[4][1] + " ---- " + "Total time: " + str(top_used_software[4][4]))

# parses each website via objects
W1 = urlparse(top_used_software[0][1])
W2 = urlparse(top_used_software[1][1])
W3 = urlparse(top_used_software[2][1])
W4 = urlparse(top_used_software[3][1])
W5 = urlparse(top_used_software[4][1])

sizes = [int(top_used_software[0][4]),
        int(top_used_software[1][4]),
        int(top_used_software[2][4]),
        int(top_used_software[3][4]),
        int(top_used_software[4][4])]
Website1 = W1.netloc
Website2 = W2.netloc
Website3 = W3.netloc
Website4 = W4.netloc
Website5 = W5.netloc

if Website1 == '':
    Website1 = W1.path
if Website2 == '':
    Website2 = W2.path
if Website3 == '':
    Website3 = W3.path
if Website4 == '':
    Website4 = W4.path
if Website5 == '':
    Website5 = W5.path

labels = [str(Website1), str(Website2), str(Website3), str(Website4), str(Website5)]
# Pie chart, where the slices will be ordered and plotted counter-clockwise:

fig, ax = plt.subplots()
ax.pie(sizes, labels=labels, autopct='%1.1f%%')
ax.axis('equal')  # Equal aspect ratio ensures the pie chart is circular.
ax.set_title('Top Used Software')


plt.show()
