import pandas as pd
import functions as fx
import json

with open('id_to_number.json') as f:
    id_to_number = json.load(f)

################################################################################################################
# THIS CODE IS FOR INITIALIZING THE DATAFRAME TO CONCATENATE TO

i=0
student = fx.csv_to_df('student_{}.csv'.format(i))
student_id = student['student_id'].iloc[0]
# drop unnecessary variables
student.drop(['Unnamed: 0','activity_value','activity_id','chapter_name', 'level_name', 'level_id', 'block_id', 'date','activityable_id', 'student_id'], axis=1, inplace=True)
#     print(i,student.shape,student['activity_no'].unique())

#get dummy variables for categorical variables
dummies = pd.get_dummies(student)

#normalize the interval and block try counter
dummies['interval'] = (dummies['interval']-dummies['interval'].min())/(dummies['interval'].max()-dummies['interval'].min())
dummies['block_try_counter'] = (dummies['block_try_counter']-dummies['block_try_counter'].min())/(dummies['block_try_counter'].max()-dummies['block_try_counter'].min())

# group the activities by sessions number (activity_no)
groups = dummies.groupby('activity_no', dropna=False)
groups.size()

#calculate the mean values for each variable
sessions = groups.mean()
sessions['student_id'] = student_id
sessions['student_no'] = i
sessions['student_level'] = id_to_number[student_id]


#drop the session if it consists of less than 10 activity values
sessions['size']=groups.size()

sessions = sessions[sessions['size']>=10]
sessions.drop('size', axis=1)
running_sessions = pd.DataFrame(sessions).fillna(0)

################################################################################################################


################################################################################################################
# THIS CODE IS FOR FILLING THE DATAFRAME:
for i in range(1,1800):
    student = fx.csv_to_df('student_{}.csv'.format(i))
    print(i)
    if student.shape[0]>0:
        student_id = student['student_id'].iloc[0]
        # drop unnecessary variables
        student.drop(['Unnamed: 0','activity_value','activity_id','chapter_name', 'level_name', 'level_id', 'block_id', 'date','activityable_id', 'student_id'], axis=1, inplace=True)
    #     print(i,student.shape,student['activity_no'].unique())
        #get dummy variables for categorical variables
        dummies = pd.get_dummies(student)

        #normalize the interval and block try counter
        # dummies['interval'] = (dummies['interval']-dummies['interval'].min())/(dummies['interval'].max()-dummies['interval'].min())
        # dummies['block_try_counter'] = (dummies['block_try_counter']-dummies['block_try_counter'].min())/(dummies['block_try_counter'].max()-dummies['block_try_counter'].min())

        # group the activities by sessions number (activity_no)
        groups = dummies.groupby('activity_no', dropna=False)
        groups.size()

        #calculate the mean values for each variable
        sessions = groups.mean()
        sessions['student_id'] = student_id
        sessions['student_no'] = i
        sessions['student_level'] = id_to_number[student_id]

        #drop the session if it consists of less than 10 activity values
        sessions['size']=groups.size()

        sessions = sessions[sessions['size']>=10]
        sessions.drop('size', axis=1)
        sessions = pd.DataFrame(sessions).fillna(0)

        running_sessions = pd.concat([running_sessions, sessions])

print(running_sessions.shape)

running_sessions.to_csv('sessions.csv', sep=';')

print('done, and saved!')