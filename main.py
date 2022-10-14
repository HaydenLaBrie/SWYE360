from urllib.parse import urlparse
import mysql.connector
import matplotlib.pyplot as plt


# prints the top 5 most used software for a given student to the console
def print_top_5_to_console(top):
    print("#1: " + top[0][1] + " ---- " + "Total time: " + str(top[0][2]))
    print("#2: " + top[1][1] + " ---- " + "Total time: " + str(top[1][2]))
    print("#3: " + top[2][1] + " ---- " + "Total time: " + str(top[2][2]))
    print("#4: " + top[3][1] + " ---- " + "Total time: " + str(top[3][2]))
    print("#5: " + top[4][1] + " ---- " + "Total time: " + str(top[4][2]))


# creates a pie chart for a given student and also returns a list of tuples.
# The list is 0 - 4 representing the top 5 websites
# The tuple is the website url and the total time spent in seconds
def create_student_chart(firstName, lastName, view):
    t = [firstName, lastName]
    mycursor = mydb.cursor()
    mycursor.execute("SELECT first_name, last_name, studentlogin FROM student WHERE first_name = %s AND last_name = %s",
                     (firstName, lastName))
    x = mycursor.fetchall()
    currentUserID = x[0][2]
    mycursor.execute(
        "SELECT urlAppId, appdetails, SUM(totalSpentTime) AS TotalTime FROM students_analytics WHERE loginid=%s GROUP BY urlAppId ORDER BY TotalTime DESC",
        (currentUserID,))
    top_used_software = mycursor.fetchall()
    # parses each website via objects
    parse_and_print(top_used_software, view, t)
    return top_used_software


def create_district_chart(view):
    t = ['null', 'null']
    mycursor = mydb.cursor()
    mycursor.execute(
        "SELECT urlAppId, appdetails, SUM(totalSpentTime) AS TotalTime FROM students_analytics WHERE districtid='14085' GROUP BY urlAppId ORDER BY TotalTime DESC",
        ())
    top_used_software = mycursor.fetchall()
    parse_and_print(top_used_software, view, t)
    return top_used_software


def create_school_chart(school, view):
    t = [school, 'null']
    mycursor = mydb.cursor()
    mycursor.execute(
        "SELECT urlAppId, appdetails, SUM(totalSpentTime) AS TotalTime FROM students_analytics WHERE schoolid= %s GROUP BY urlAppId ORDER BY TotalTime DESC",
        (school,))
    top_used_software = mycursor.fetchall()
    parse_and_print(top_used_software, view, t)
    return top_used_software


def parse_and_print(top_used_software, view, t):
    W1 = urlparse(top_used_software[0][1])
    W2 = urlparse(top_used_software[1][1])
    W3 = urlparse(top_used_software[2][1])
    W4 = urlparse(top_used_software[3][1])
    W5 = urlparse(top_used_software[4][1])
    sizes = [int(top_used_software[0][2]),
             int(top_used_software[1][2]),
             int(top_used_software[2][2]),
             int(top_used_software[3][2]),
             int(top_used_software[4][2])]
    Website1 = W1.netloc
    Website2 = W2.netloc
    Website3 = W3.netloc
    Website4 = W4.netloc
    Website5 = W5.netloc

    if W1.netloc == '':
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
    if view == 1:
        ax.set_title('TOP 5 USED SOFTWARE FOR DISTRICT\n')
    if view == 2:
        ax.set_title('TOP 5 USED SOFTWARE FOR' + t[0] + t[1])
    else:
        ax.set_title('TOP 5 USED SOFTWARE FOR' + t[0])
    plt.show()


mydb = mysql.connector.connect(
    host='localhost',
    user='root',
    password='Alliance98',
    port='3306',
    database='swye360'
)
view = input("Please type integer to select from menu and hit enter \n1.District\n2.Student\n3.School\n")
view = int(view)
if view == 2:
    firstName = input("Please enter First name: ")
    lastName = input("Please enter Last name: ")
    most_used = create_student_chart(firstName, lastName, view)
    print_top_5_to_console(most_used)
if view == 3:
    schoolid = input("Please enter schoolid: ")
    school = int(schoolid)
    most_used = create_school_chart(schoolid, view)
else:
    most_used = create_district_chart(view)
    print_top_5_to_console(most_used)
