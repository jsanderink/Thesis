import csv
import pandas as pd
import functions as fx
from datetime import datetime, timedelta
import numpy as np
import write_scores_ea as wse

GLOBAL_START = datetime.now()
print(GLOBAL_START)

answer_activities = fx.csv_to_df('export_answer_activities.csv')
redundant = fx.csv_to_df("overview_blocks (redundant).csv")
large_df = fx.csv_to_df('intervals.csv')
level_complete_activities = fx.csv_to_df('export_level_complete_activities.csv')

# I am going to iterate over all students
student_ids = large_df['user_id'].unique()

for j in range(210,len(student_ids)):

    start = datetime.now()
    student_id = np.nan
    student_id = student_ids[j]

    print("\n\nStudent", j, student_id)

    with open("student_{}.csv".format(j), 'w', newline='') as f:

        # Intialize a write and write the headers row
        writer = csv.writer(f, delimiter=';')
        writer.writerow(('activity_id',
                         'student_id',
                         'activity_type',
                         'activity_value',
                         'date',
                         'interval',
                         'activity_no',
                         'activityable_id',
                         'mission_name',
                         'chapter_name',
                         'level_name',
                         'level_type',
                         'level_id',
                         'block_id',
                         'block_type',
                         'stars'))

        # those are the types of activities that I want to include in my dataset
        to_select = ['answer', 'level-complete','primm-hint', 'clippy']

        # Set the activities of student x in the right dataframe and drop unneccesary columns
        activities_student_x = large_df[(large_df['type'].isin(to_select)) & (large_df['user_id'] == student_id)]

        # Iterate over the selected activities of student J
        # Code below takes all relevant variables which i will put in a list and write to a csv

        i = 0

        for ind in activities_student_x.index:

            # Reset the variables:
            activity_id = np.nan
            activity_type = np.nan
            activity_value = np.nan
            date = np.nan
            interval = np.nan
            activity_no = np.nan
            activityable_id = np.nan

            block_id = np.nan
            block_type = np.nan
            level_name = np.nan
            chapter_name = np.nan
            mission_name = np.nan
            level_type = np.nan
            level_id = np.nan
            stars = np.nan

            # First the variables that I want independent of the type of the activity
            activity_id = activities_student_x['id'][ind]
            activity_type = activities_student_x['type'][ind]
            activity_value = activities_student_x['value'][ind]
            date = activities_student_x['date'][ind]
            interval = activities_student_x['Interval'][ind]
            activity_no = activities_student_x['Activity#'][ind]
            activityable_id = activities_student_x['activityable_id'][ind]

            # ANSWER ACTIVITIES
            if activities_student_x['type'][ind] == 'answer':
                block_id = answer_activities[answer_activities['id'] == activityable_id]['block_id'].values.tolist()[0]

                block = redundant[redundant['block_id'] == block_id].values
                # specifically needed from activities with the type "answer"
                if block.any():
                    block_type = redundant[redundant['block_id'] == block_id]['block_type'].values.tolist()[0]
                    level_name = redundant[redundant['block_id'] == block_id]['level_name'].values.tolist()[0]
                    chapter_name = redundant[redundant['block_id'] == block_id]['chapter_name'].values.tolist()[0]
                    mission_name = redundant[redundant['block_id'] == block_id]['mission_name'].values.tolist()[0]
                    level_type = redundant[redundant['block_id'] == block_id]['level_type'].values.tolist()[0]
                    level_id = redundant[redundant['block_id'] == block_id]['level_id'].values.tolist()[0]

            # LEVEL COMPLETE ACTIVITIES
            if activities_student_x['type'][ind] == 'level-complete':

                level_complete = level_complete_activities[level_complete_activities['id'] == activityable_id].values
                if level_complete.any():
                    stars = level_complete_activities[level_complete_activities['id'] == activityable_id][
                        'stars'].values.tolist()[0]
                    level_id = level_complete_activities[level_complete_activities['id'] == activityable_id][
                        'level_id'].values.tolist()[0]

                    level = redundant[redundant['level_id'] == level_id].values

                    if level.any():
                        level_type = redundant[redundant['level_id'] == level_id]['level_type'].values.tolist()[0]
                        level_name = redundant[redundant['level_id'] == level_id]['level_name'].values.tolist()[0]
                        chapter_name = redundant[redundant['level_id'] == level_id]['chapter_name'].values.tolist()[0]
                        mission_name = redundant[redundant['level_id'] == level_id]['mission_name'].values.tolist()[0]

            # PRIMM HINTS
            if activities_student_x['type'][ind] == 'primm-hint':

                activity_value = activities_student_x['value'][ind]
                level_id = fx.value_to_dict2(activity_value)['levelId']

                level = redundant[redundant['level_id'] == level_id].values
                if level.any():
                    level_type = redundant[redundant['level_id'] == level_id]['level_type'].values.tolist()[0]
                    level_name = redundant[redundant['level_id'] == level_id]['level_name'].values.tolist()[0]
                    chapter_name = redundant[redundant['level_id'] == level_id]['chapter_name'].values.tolist()[0]
                    mission_name = redundant[redundant['level_id'] == level_id]['mission_name'].values.tolist()[0]

            # CLIPPY
            if activities_student_x['type'][ind] == 'clippy':
                activity_value = activities_student_x['value'][ind]
                if 'levelId' in fx.value_to_dict2(activity_value):
                    level_id = fx.value_to_dict2(activity_value)['levelId']
                    level = redundant[redundant['level_id'] == level_id].values
                    if level.any():
                        level_type = redundant[redundant['level_id'] == level_id]['level_type'].values.tolist()[0]
                        level_name = redundant[redundant['level_id'] == level_id]['level_name'].values.tolist()[0]
                        chapter_name = redundant[redundant['level_id'] == level_id]['chapter_name'].values.tolist()[0]
                        mission_name = redundant[redundant['level_id'] == level_id]['mission_name'].values.tolist()[0]

            row = [activity_id,
                   student_id,
                   activity_type,
                   activity_value,
                   date,
                   interval,
                   activity_no,
                   activityable_id,
                   mission_name,
                   chapter_name,
                   level_name,
                   level_type,
                   level_id,
                   block_id,
                   block_type,
                   stars]

            i = i + 1
            writer.writerow(row)

    wse.write_scores(j)
    print('student {} is done time spent is {}'.format(j, (datetime.now() - start)))
    print("student_{}.csv is saved correctly!".format(j))



GLOBAL_END = datetime.now()
print(GLOBAL_END)

print('this took {}'.format(GLOBAL_END-GLOBAL_START))
