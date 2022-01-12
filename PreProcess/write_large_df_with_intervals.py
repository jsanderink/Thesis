import csv
import pandas as pd
import functions as fx
from datetime import datetime, timedelta

START = datetime.now()
data = fx.csv_to_df("activities_with_usertypes.csv")
students = data[data['user_type'] == 'student']
user_ids = students['user_id'].unique()
columns = ['Unnamed: 0', 'id', 'user_id', 'type', 'value', 'activityable_id', 'activityable_type', 'activity_at',
           'created_at', 'updated_at', 'date', 'user_type', 'Interval', 'Activity#', "day"]

INTERVAL = 900

with open('intervals_in_large_df.csv', 'w', newline='') as f:
    writer = csv.writer(f, delimiter=';')
    writer.writerow(columns)

    for student in user_ids        :
        # current_time = datetime.now()
        current_student = students[students['user_id'] == student]

        activity = 1

        # append Interval
        for ind in current_student.index:
            row = (list(current_student.loc[ind]))

            if ind == 0:
                interval = 0
            else:
                time_current_activity = datetime.strptime(current_student['date'][ind], '%Y-%m-%d %H:%M:%S')
                time_prev_activity = datetime.strptime(current_student['date'][ind-1], '%Y-%m-%d %H:%M:%S')
                interval = time_current_activity-time_prev_activity
            print(interval)

            # if interval.total_seconds() < 0: interval = timedelta(seconds=-1)
            # row.append(interval)
            # if interval.total_seconds() > INTERVAL:
            #     activity = activity + 1
            #     print('new activity!', activity, student)
            #     # print(datetime.now())
            #
            # # append Activity number
            # row.append(activity)
            # row.append(date2)
            #
            # # write the row to the csv
            # writer.writerow(row)
            #
            # current_time = datetime.strptime(current_student['date'][ind], '%Y-%m-%d %H:%M:%S')

END = datetime.now()

print('this took', END-START)

