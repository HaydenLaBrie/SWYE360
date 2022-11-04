from urllib.parse import urlparse
import mysql.connector
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from datetime import datetime
import numpy
import matplotlib.dates as mdates



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


# creates the top 5 user software for district
def create_district_chart(view):
    t = ['null', 'null']
    mycursor = mydb.cursor()
    mycursor.execute(
        "SELECT urlAppId, appdetails, SUM(totalSpentTime) AS TotalTime FROM students_analytics WHERE districtid='14085' GROUP BY urlAppId ORDER BY TotalTime DESC",
        ())
    top_used_software = mycursor.fetchall()
    parse_and_print(top_used_software, view, t)
    return top_used_software


# creates the top 5 used software for school
def create_school_chart(school, view):
    t = [school, 'null']
    mycursor = mydb.cursor()
    mycursor.execute(
        "SELECT urlAppId, appdetails, SUM(totalSpentTime) AS TotalTime FROM students_analytics WHERE schoolid= %s GROUP BY urlAppId ORDER BY TotalTime DESC",
        (school,))
    top_used_software = mycursor.fetchall()
    parse_and_print(top_used_software, view, t)
    return top_used_software

# gets the student identifier from given first and last name
def get_student_email(firstName, lastName, view):
    t = [firstName, lastName]
    mycursor = mydb.cursor()
    mycursor.execute("SELECT first_name, last_name, email FROM student WHERE first_name = %s AND last_name = %s",
                     (firstName, lastName))
    x = mycursor.fetchall()
    currentUserID = x[0][2]
    return currentUserID


# gets the url's of top software and puts them to respective pie graph slice
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
    user='Jovanni',
    password='AdamantineKing@44',
    port='3306',
    database='swye360'
)

# asks the user what they want to do;
# 1 = top 5 district software;
# 2 = top 5 student software;
# 3 = top 5 school software;
# 4 = compare students
view = input("Please type integer to select from menu and hit enter \n1.District\n2.Student\n3.School\n4.Compare\n")
view = int(view)
if view == 2:
    firstName = input("Please enter First name: ")
    lastName = input("Please enter Last name: ")
    most_used = create_student_chart(firstName, lastName, view)
    print_top_5_to_console(most_used)
elif view == 3:
    schoolid = input("Please enter schoolid: ")
    school = int(schoolid)
    most_used = create_school_chart(schoolid, view)
elif view == 4:
    num = 0
    while True:
        try:
            num = int(input("Enter number of students to compare: "))
        except ValueError:
            print("Please enter a valid number 2-6")
            continue
        # user can only compare between 2 and 6 users
        plt.xticks(rotation=45, ha='right')
        if num >= 2 and num <= 6:
            for x in range(num):
                firstName = input("Please enter Student 1 First name: ")
                lastName = input("Please enter Student 1 Last name: ")
                userEmail = get_student_email(firstName, lastName, view)
                mycursor = mydb.cursor()
                mycursor.execute("SELECT grade FROM student WHERE email = %s", (userEmail,))
                gradeLevel = mycursor.fetchall()
                print(firstName + " " + lastName + " Current Grade Level: " + gradeLevel[0][0])

                grade2 = []
                grade3M = []
                grade3R = []
                grade4M = []
                grade4R = []
                grade5M = []
                grade5R = []
                grade6M = []
                grade6R = []
                if int(gradeLevel[0][0]) >= 2:
                    mycursor.execute(
                        "SELECT email, DRTM_Percent_Score, DRTM_Date_Taken, FLCBA_Percent_Score, FLCBA_Date_Taken, CBA2D3D_Percent_Score, CBA2D3D_Date_Taken, MDCBA_Percent_Score, MDCBA_Date_Taken, PVCBA_Percent_Score, PVCBA_Date_Taken FROM student AS person LEFT JOIN assessments_grade2 AS a1 ON person.email=a1.Local_ID WHERE email = %s",
                        (userEmail,))
                    DUMBQUERY = mycursor.fetchall()
                    print("Grade 2: ", end=" ")
                    i = 0
                    while i < len(DUMBQUERY[0]):
                        if DUMBQUERY[0][i] == '-' or DUMBQUERY[0][i] == 'None':
                            i = i + 1
                        else:
                            grade2.append(DUMBQUERY[0][i])
                            i = i + 1
                    print(grade2)

                if int(gradeLevel[0][0]) >= 3:
                    mycursor.execute(
                        "SELECT email, a2.Math_CBA1_Percent_Score, a2.Math_CBA1_Date_Taken, a2.CBA_2_Math_Percent_Score, a2.CBA_2_Math_Date_Taken, a2.CBA_3_Math_Percent_Score, a2.CBA_3_Math_Date_Taken, a2.CBA_4_Math_Percent_Score, a2.CBA_4_Math_Date_Taken, a2.CBA_5_Math_Percent_Score, a2.CBA_5_Math_Date_Taken, Assessment_Financial_Literacy_Percent_Score, Assessment_Financial_Literacy_Date_Taken, a2.STAAR_Mathematics_Percent_Score, a2.STAAR_Mathematics_Date_Taken FROM student AS person LEFT JOIN assessments_grade3_math AS a2 ON person.email=a2.Local_ID WHERE email = %s",
                        (userEmail,))
                    DUMBQUERY = mycursor.fetchall()
                    print("Grade 3 Math: ", end=" ")
                    i = 0
                    while i < len(DUMBQUERY[0]):
                        if DUMBQUERY[0][i] == '-' or DUMBQUERY[0][i] is None:
                            i = i + 1
                        else:
                            grade3M.append(DUMBQUERY[0][i])
                            i = i + 1
                    print(grade3M)
                    mycursor.execute(
                        "SELECT email, Reading_Non_Fiction_Percent_Score, Reading_Non_Fiction_Date_Taken, Reading_2021_Percent_Score, Reading_2021_Date_Taken, McCrary_CBA3_Reading_Percent_Score, McCrary_CBA3_Reading_Date_Taken, Reading_Test_Percent_Score, Reading_Test_Date_Taken, McCrary_CBA4_Reading_Percent_Score, McCrary_CBA4_Reading_Date_Taken, Benchmark_2019_Percent_Score, Benchmark_2019_Date_Taken, Reading_fiction_Percent_Score, Reading_fiction_Date_Taken, a3.Reading_CBA5_Percent_Score, a3.Reading_CBA5_Date_Taken, Staar_Benchmark_Percent_Score, Staar_Benchmark_Date_Taken, a3.STAAR_Reading_Percent_Score, a3.STAAR_Reading_Date_Taken FROM student AS person LEFT JOIN assessments_grade3_reading AS a3 ON person.email=a3.Local_ID WHERE email = %s",
                        (userEmail,))
                    DUMBQUERY = mycursor.fetchall()
                    print("Grade 3 Reading: ", end=" ")
                    i = 0
                    while i < len(DUMBQUERY[0]):
                        if DUMBQUERY[0][i] == '-' or DUMBQUERY[0][i] is None:
                            i = i + 1
                        else:
                            grade3R.append(DUMBQUERY[0][i])
                            i = i + 1
                    print(grade3R)

                if int(gradeLevel[0][0]) >= 4:
                    mycursor.execute(
                        "SELECT email, a4.Math_CBA1_Percent_Score, a4.Math_CBA1_Date_Taken, a4.Math_CBA2_Percent_Score, a4.Math_CBA2_Date_Taken, a4.Math_CBA3_Percent_Score, a4.Math_CBA3_Date_Taken, a4.Math_CBA4_Percent_Score, a4.Math_CBA4_Date_Taken, a4.Math_CBA5_Percent_Score, a4.Math_CBA5_Date_Taken, Math_CBA6_Raw_Score, Math_CBA6_Date_Taken, Math_CBA7_Percent_Score, Math_CBA7_Date_Taken, Math_CBA8_Percent_Score, Math_CBA8_Date_Taken, a4.STAAR_Mathematics_Percent_Score, a4.STAAR_Mathematics_Date_Taken FROM student AS person LEFT JOIN assessments_grade4_math AS a4 ON person.email=a4.Local_ID WHERE email = %s",
                        (userEmail,))
                    DUMBQUERY = mycursor.fetchall()
                    print("Grade 4 Math: ", end=" ")
                    i = 0
                    while i < len(DUMBQUERY[0]):
                        if DUMBQUERY[0][i] == '-' or DUMBQUERY[0][i] is None:
                            i = i + 1
                        else:
                            grade4M.append(DUMBQUERY[0][i])
                            i = i + 1
                    print(grade4M)
                    mycursor.execute(
                        "SELECT email, Reading_CBA1_Percent_Score, Reading_CBA1_Date_Taken, Reading_CBA2_Percent_Score, Reading_CBA2_Date_Taken, Reading_CBA3_Percent_Score, Reading_CBA3_Date_Taken, Reading_CBA4_Percent_Score, Reading_CBA4_Date_Taken, a5.Reading_CBA5_Percent_Score, a5.Reading_CBA5_Date_Taken, Reading_CBA6_Percent_Score, Reading_CBA6_Date_Taken, Reading_CBA6_BIOGRAPHY_Percent_Score, Reading_CBA6_BIOGRAPHY_Date_Taken, Reading_CBA7_FICTION_Percent_Score, Reading_CBA7_FICTION_Date_Taken, Reading_CBA8_POETRY_Percent_Score, Reading_CBA8_POETRY_Date_Taken, STAAR_Reading_Benchmark_Percent_Score, STAAR_Reading_Benchmark_Date_Taken, STAAR_Reading_Benchmark2_Percent_Score, STAAR_Reading_Benchmark2_Date_Taken, May_STAAR_Reading_Percent_Score, May_STAAR_Reading_Date_Taken FROM student AS person LEFT JOIN assessments_grade4_reading AS a5 ON person.email=a5.Local_ID WHERE email = %s",
                        (userEmail,))
                    DUMBQUERY = mycursor.fetchall()
                    print("Grade 4 Reading: ", end=" ")
                    i = 0
                    while i < len(DUMBQUERY[0]):
                        if DUMBQUERY[0][i] == '-' or DUMBQUERY[0][i] is None:
                            i = i + 1
                        else:
                            grade4R.append(DUMBQUERY[0][i])
                            i = i + 1
                    print(grade4R)

                if int(gradeLevel[0][0]) >= 5:
                    mycursor.execute(
                        "SELECT email, Module_2_CBA_Multiply_and_Divide_Percent_Score, Module_2_CBA_Multiply_and_Divide_Date_Taken, Multiply_and_Divide_Fractions_Percent_Score, Multiply_and_Divide_Fractions_Date_Taken, Multiplying_Decimals_Percent_Score, Multiplying_Decimals_Date_Taken, Multiplying_Decimals_MOD_Percent_Score, Multiplying_Decimals_MOD_Date_Taken, Add_and_Subtract_Fractions_Percent_Score, Add_and_Subtract_Fractions_Date_Taken, a6.STAAR_Mathematics_Percent_Score, a6.STAAR_Mathematics_Date_Taken FROM student AS person LEFT JOIN assessments_grade5_math AS a6 ON person.email=a6.Local_ID WHERE email = %s",
                        (userEmail,))
                    DUMBQUERY = mycursor.fetchall()
                    print("Grade 5 Math: ", end=" ")
                    i = 0
                    while i < len(DUMBQUERY[0]):
                        if DUMBQUERY[0][i] == '-' or DUMBQUERY[0][i] is None:
                            i = i + 1
                        else:
                            grade5M.append(DUMBQUERY[0][i])
                            i = i + 1
                    print(grade5M)
                    mycursor.execute(
                        "SELECT email, CBA1_Narrative_Nonfiction_Percent_Score, CBA1_Narrative_Nonfiction_Date_Taken, CBA2_Expository_Folktale_Poetry_Percent_Score, CBA2_Expository_Folktale_Poetry_Date_Taken, CBA3_Realistic_Fiction_Percent_Score, CBA3_Realistic_Fiction_Date_Taken, CBA4_Biography_Drama_Poetry_Percent_Score, CBA4_Biography_Drama_Poetry_Date_Taken, CBA5_Expository_Historical_Fiction_Percent_Score, CBA5_Expository_Historical_Fiction_Date_Taken, CBA6_Argumentative_Text_Percent_Score, CBA6_Argumentative_Text_Date_Taken, a7.STAAR_Reading_Percent_Score, a7.STAAR_Reading_Date_Taken FROM student AS person LEFT JOIN assessments_grade5_reading AS a7 ON person.email=a7.Local_ID WHERE email = %s",
                        (userEmail,))
                    DUMBQUERY = mycursor.fetchall()
                    print("Grade 5 Reading: ", end=" ")
                    i = 0
                    while i < len(DUMBQUERY[0]):
                        if DUMBQUERY[0][i] == '-' or DUMBQUERY[0][i] is None:
                            i = i + 1
                        else:
                            grade5R.append(DUMBQUERY[0][i])
                            i = i + 1
                    print(grade5R)

                if int(gradeLevel[0][0]) >= 6:
                    mycursor.execute(
                        "SELECT email, Geometry_Test_Percent_Score, Geometry_Test_Date_Taken, Geometry_Test_mod_Percent_Score, Geometry_Test_mod_Date_Taken, histograms_box_plots_Percent_Score, histograms_box_plots_Date_Taken, histograms_box_plots_MOD_Percent_Score, histograms_box_plots_MOD_Date_Taken, metric_mean_median_Percent_Score, metric_mean_median_Date_Taken, metric_mean_median_MOD_Percent_Score, metric_mean_median_MOD_Date_Taken, Algebraic_Representations_Test_Percent_Score, Algebraic_Representations_Test_Date_Taken, Algebraic_Representations_Test_mod_Percent_Score, Algebraic_Representations_Test_mod_Date_Taken, Expressions_Test_Percent_Score, Expressions_Test_Date_Taken, Expressions_Test_mod_Percent_Score, Expressions_Test_mod_Date_Taken, Financial_Literacy_Percent_Score, Financial_Literacy_Date_Taken, Financial_Literacy_MOD_Percent_Score, Financial_Literacy_MOD_Date_Taken, Integers_Test_Percent_Score, Integers_Test_Date_Taken, Integers_Test_mod_2_Percent_Score, Integers_Test_mod_2_Date_Taken, Numerical_Representations_Percent_Score, Numerical_Representations_Date_Taken, Percent_Test_Percent_Score, Percent_Test_Date_Taken, Integers_Test_mod_Percent_Score, Integers_Test_mod_Date_Taken, Numerical_Representations_Mod_Percent_Score, Numerical_Representations_Mod_Date_Taken, Ratios_and_Rates_Test_mod_Percent_Score, Ratios_and_Rates_Test_mod_Date_Taken, Positive_Rational_Numbers_Percent_Score, Positive_Rational_Numbers_Date_Taken, Positive_Rational_Numbers_mod_Percent_Score, Positive_Rational_Numbers_mod_Date_Taken, Ratios_and_Rates_Test_Percent_Score, Ratios_and_Rates_Test_Date_Taken, Percents_Test_mod_Percent_Score, Percents_Test_mod_Date_Taken FROM student AS person LEFT JOIN assessments_grade6_math AS a8 ON person.email=a8.Local_ID WHERE email = %s",
                        (userEmail,))
                    DUMBQUERY = mycursor.fetchall()
                    print("Grade 6 Math: ", end=" ")
                    i = 0
                    while i < len(DUMBQUERY[0]):
                        if DUMBQUERY[0][i] == '-' or DUMBQUERY[0][i] is None:
                            i = i + 1
                        else:
                            grade6M.append(DUMBQUERY[0][i])
                            i = i + 1
                    print(grade6M)
                    mycursor.execute(
                        "SELECT email, ELA_CBA_1_Percent_Score, ELA_CBA_1_Date_Taken, ELA_CBA_2_Percent_Score, ELA_CBA_2_Date_Taken, ELA_CBA_3_Percent_Score, ELA_CBA_3_Date_Taken, ELA_CBA_4_Percent_Score, ELA_CBA_4_Date_Taken, ELA_Parts_of_Speech_Percent_Score, ELA_Parts_of_Speech_Date_Taken, Figurative_Language_Test_Percent_Score, Figurative_Language_Test_Date_Taken, ELA_CBA_5_Percent_Score, ELA_CBA_5_Date_Taken, CBA_2_Percent_Score, CBA_2_Date_Taken, CBA_3_Percent_Score, CBA_3_Date_Taken, Reading_CBA_4_Percent_Score, Reading_CBA_4_Date_Taken, CBA_5_Percent_Score, CBA_5_Date_Taken, CBA_7_Percent_Score, CBA_7_Date_Taken, CBA_10_Percent_Score, CBA_10_Date_Taken, Reading_CBA_9_Percent_Score, Reading_CBA_9_Date_Taken, CBA_8_Percent_Score, CBA_8_Date_Taken, Benchmark_Percent_Score, Benchmark_Date_Taken FROM student AS person LEFT JOIN assessments_grade6_reading AS a9 ON person.email=a9.Local_ID WHERE email = %s",
                        (userEmail,))
                    DUMBQUERY = mycursor.fetchall()
                    print("Grade 6 Reading: ", end=" ")
                    i = 0
                    while i < len(DUMBQUERY[0]):
                        if DUMBQUERY[0][i] == '-' or DUMBQUERY[0][i] is None:
                            i = i + 1
                        else:
                            grade6R.append(DUMBQUERY[0][i])
                            i = i + 1
                    print(grade6R)
                # if int(gradeLevel[0][0]) > 7:
                #     mycursor.execute("SELECT email, ELA_CBA_1_Percent_Score, ELA_CBA_1_Date_Taken, ELA_CBA_2_Percent_Score, ELA_CBA_2_Date_Taken, ELA_CBA_3_Percent_Score, ELA_CBA_3_Date_Taken, ELA_CBA_4_Percent_Score, ELA_CBA_4_Date_Taken, ELA_Parts_of_Speech_Percent_Score, ELA_Parts_of_Speech_Date_Taken, Figurative_Language_Test_Percent_Score, Figurative_Language_Test_Date_Taken, ELA_CBA_5_Percent_Score, ELA_CBA_5_Date_Taken, CBA_2_Percent_Score, CBA_2_Date_Taken, CBA_3_Percent_Score, CBA_3_Date_Taken, Reading_CBA_4_Percent_Score, Reading_CBA_4_Date_Taken, CBA_5_Percent_Score, CBA_5_Date_Taken, CBA_7_Percent_Score, CBA_7_Date_Taken, CBA_10_Percent_Score, CBA_10_Date_Taken, Reading_CBA_9_Percent_Score, Reading_CBA_9_Date_Taken, CBA_8_Percent_Score, CBA_8_Date_Taken, Benchmark_Percent_Score, Benchmark_Date_Taken FROM student AS person LEFT JOIN assessments_grade6_reading AS a9 ON person.email=a9.Local_ID WHERE email = %s", (userEmail,))
                #     DUMBQUERY = mycursor.fetchall()
                #     print(DUMBQUERY)

                # store the length of each database 9 in total
                lengthOfData = [len(grade2), len(grade3M), len(grade3R), len(grade4M), len(grade4R), len(grade5M),
                                len(grade5R), len(grade6M), len(grade6R)]

                examScoreM = [] #math score for given student
                dateofExamM = [] #day of taken exam for given student
                examScoreR = []
                dateofExamR = []
                for x in range(9):
                    if lengthOfData[x] > 1:
                        # if x == 0:
                        #     examScoreM.append(grade2[1::2])
                        #     type(grade2[2::2])
                        #     dateofExamM.append(grade2[2::2])
                        if x == 1:
                            examScoreM.append(grade3M[1::2])
                            dateofExamM.append(grade3M[2::2])
                        if x == 2:
                            examScoreR.append(grade3R[1::2])
                            dateofExamR.append(grade3R[2::2])
                        if x == 3:
                            examScoreM.append(grade4M[1::2])
                            dateofExamM.append(grade4M[2::2])
                        if x == 4:
                            examScoreR.append(grade4R[1::2])
                            dateofExamR.append(grade4R[2::2])
                        if x == 5:
                            examScoreM.append(grade5M[1::2])
                            dateofExamM.append(grade5M[2::2])
                        if x == 6:
                            examScoreR.append(grade5R[1::2])
                            dateofExamR.append(grade5R[2::2])
                        if x == 7:
                            examScoreM.append(grade6M[1::2])
                            dateofExamM.append(grade6M[2::2])
                        if x == 8:
                            examScoreR.append(grade6R[1::2])
                            dateofExamR.append(grade6R[2::2])

                flattenlist = []
                flattenlist = list(numpy.concatenate(dateofExamM).flat)
                dateofExamM.clear()
                dateofExamM = flattenlist
                print(dateofExamM)

                flattenlist1 = []
                flattenlist1 = list(numpy.concatenate(dateofExamR).flat)
                dateofExamR.clear()
                dateofExamR = flattenlist1
                print(dateofExamR)

                flattenlist2 = []
                flattenlist2 = list(numpy.concatenate(examScoreM).flat)
                examScoreM.clear()
                examScoreM = flattenlist2
                print(examScoreM)

                flattenlist3 = []
                flattenlist3 = list(numpy.concatenate(examScoreR).flat)
                examScoreR.clear()
                examScoreR = flattenlist3
                print(examScoreR)
                while True:
                    try:
                        whatToLookFor = str(input("Type M for Math, Type R for Reading: "))
                    except ValueError:
                        print("Please enter a valid number 2-6")
                        continue
                    if whatToLookFor == "R" or whatToLookFor == "r":
                        temporary = []
                        z = str(examScoreR[0])
                        n = 0
                        while n < len(examScoreR):
                            temporary.append(str(examScoreR[n]))
                            n = n + 1
                        newstr = []
                        n = 0
                        while n < len(temporary):
                            newstr.append(int(temporary[n].replace("%", "")))
                            n = n + 1

                        # replaces the slashes, and sorts the date, and brings the exam scores along with it.
                        dateofExamR = [x.replace("/", "-") for x in dateofExamR]
                        dateofExamR, newstr = zip(
                            *sorted(zip(dateofExamR, newstr), key=lambda date: datetime.strptime(date[0], '%m-%d-%y')))
                        data = list(zip(dateofExamR, newstr))
                        print(dateofExamR)
                        print(newstr)

                        # plot lines
                        x = [datetime.strptime(d, '%m-%d-%y').date() for d in dateofExamR]
                        plt.xticks(rotation=45, ha='right')
                        plt.plot(x, newstr, label=str(firstName) + " " + str(lastName) + " R")

                        break
                    elif whatToLookFor == "M" or whatToLookFor == "m":
                        temporary = []
                        z = str(examScoreM[0])
                        n = 0
                        while n < len(examScoreM):
                            temporary.append(str(examScoreM[n]))
                            n = n + 1
                        newstr = []
                        n = 0
                        while n < len(temporary):
                            newstr.append(int(temporary[n].replace("%", "")))
                            n = n + 1

                        # replaces the slashes, and sorts the date, and brings the exam scores along with it.
                        dateofExamM = [x.replace("/", "-") for x in dateofExamM]
                        dateofExamM, newstr = zip(
                            *sorted(zip(dateofExamM, newstr), key=lambda date: datetime.strptime(date[0], '%m-%d-%y')))
                        data = list(zip(dateofExamM, newstr))
                        print(dateofExamM)
                        print(newstr)

                        # plot lines
                        x = [datetime.strptime(d, '%m-%d-%y').date() for d in dateofExamM]
                        plt.xticks(rotation=45, ha='right')
                        plt.plot(x, newstr, label=str(firstName) + " " + str(lastName) + " M")

                        break
                    else:
                        print('Please Enter M or R')
            plt.title('Compare View')
            plt.ylabel('Grades')
            plt.xlabel('Time')
            plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m-%d-%y'))
            plt.gca().xaxis.set_major_locator(mdates.DayLocator())
            n = 50
            [l.set_visible(False) for (i,l) in enumerate(plt.gca().xaxis.get_ticklabels()) if i % n != 0]
            plt.legend()
            plt.tight_layout()
            plt.show()
            plt.gcf().autofmt_xdate()

            break
        else:
            print('number of students must be between 2-6')
else:
    most_used = create_district_chart(view)
    print_top_5_to_console(most_used)
