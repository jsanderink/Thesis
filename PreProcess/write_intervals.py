import csv
import pandas as pd
import functions as fx
from datetime import datetime


global_start = datetime.now()
amount_of_students = len(fx.students())
print('started at {} \n there are {} students'.format(global_start, amount_of_students))

with open('intervals.csv', 'w', newline='') as f:
    writer = csv.writer(f, delimiter=';', )

    writer.writerow(('id', 'user_id', 'type', 'value', 'Activity#', 'date', 'Interval', 'activityable_id'))

    for j in range(amount_of_students):
        begin = datetime.now()

        # Initialization of a dataframe of an individual student
        student = fx.activities_student(j)

        # Making the 'activity_at' variable a datetime variable as student['date']
        student['date'] = pd.to_datetime(student['activity_at'], dayfirst=True)

        # sort the dataframe on the newly created date variable
        student.sort_values('date', inplace=True)

        # Add the intervals
        student['interval'] = list(student['date'].diff())
        student["interval"].fillna(pd.Timedelta(seconds=86400))
        # 300 sec (5 min) interval defines new session in this case
        student['SessionID'] = (student.date - student.date.shift(1) > pd.Timedelta(300, 's')).cumsum() + 1

        for i in range(len(student)):
            writer.writerow((student['id'].iloc[i],
                             student['user_id'].iloc[i],
                             student['type'].iloc[i],
                             student['value'].iloc[i],
                             student['SessionID'].iloc[i],
                             student['date'].iloc[i],
                             student['interval'].iloc[i].total_seconds(),
                             student['activityable_id'].iloc[i]))
        end = datetime.now()
        time_passed = end - begin
        print("Student", j, "          took {0} seconds, {1} students left, will take approx {2}".format(time_passed, (
                amount_of_students - j), time_passed * (amount_of_students - j)))

print("THE END; THIS TOOK", datetime.now()-global_start)