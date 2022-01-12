import pandas as pd
# from pandas_profiling import ProfileReport
from os import listdir

import matplotlib
# matplotlib.use('TkAgg')
import json

print(matplotlib.rcParams['backend'])
from datetime import datetime
import csv
from ast import literal_eval
import random
import os

# Deze functie duurt lang, alleen runnen als nieuwe data beschikbaar
# def make_profile_reports():
#     """Make profile reports when new CSVs are available"""
#     files = os.listdir()
#     csvs = [file for file in files if str(file[-1])=="v"]
#     for csv in csvs:
#         try:
#             df = pd.read_csv(csv, delimiter=';')
#             ProfileReport(df).to_file('profile_report_'+str(csv[7:-4]+'.html'))
#         except:
#             ZeroDivisionError()

def average(lst):
    try:
        return sum(lst) / len(lst)
    except:
        return 0.5

def sort_dict_on_keys(dictio):
    return sorted(dictio.items(), key=lambda x: x[1], reverse=True)

def csv_to_df(csv):
    "input csv name and returns a pandas dataframe"
    return pd.read_csv(csv, delimiter=';')


def show_csvs():
    """shows which csvs are in the current directory (just the names)"""
    files = listdir()
    csvs = [file for file in files if str(file[-1])=="v"]
    for csv in csvs:
        print(csv[7:-4])

def files():
    """shows which csvs are in the current directory (complete file names)"""
    files = os.listdir()
    csvs = [file for file in files if str(file[-1])=="v"]
    return csvs

def columns_unique(df):
    """print whether the values in the columns in the inputted dataframe are unique identifiers"""
    for column in df.columns:
        print(column, 'is all unique:', df[column].count() == df[column].nunique())

def students():
    """Returns a list of all unique IDs of students in the current activity dataset"""
    df = pd.read_csv('activities_with_usertypes.csv', delimiter=';')
    df = df[df['user_type']=='student']
    return list(set(df['user_id']))

def activities_student(number):
    """INPUT = number X,  returns a dataframe for student X with all activities of that student"""
    student = students()[number]
    df = csv_to_df('activities_with_usertypes.csv')
    return df.loc[df['user_id'] == student]

def days_student(number):
    """Returns the number of different days that a student has worked with the system"""
    return set([item[0:10] for item in list(activities_student(number)['date'])])


def value_to_dict(NUMBER, df):
    """Input an index and a dataframe and get the dictionary back"""
    true = True
    false = False

    value = df['value'][NUMBER]

    if value == 'xxx':
        #         print('value is:', value)
        test1= {'value':'xxx'}
        value = json.dumps(test1)
        return value

    value = literal_eval(df['value'][NUMBER]).decode('utf-8')

    if value[0]=='[':
        #         print('value (i think list) is ', value)
        value = json.loads(value)
        value_dict = {i:value[i] for i in range(len(value))}
        value = json.dumps(value_dict)
    if value=='{}':
        value_dict = {'empty':'empty'}
        value = json.dumps(value_dict)
    value = json.loads(decrease_json(value))

    return value

def value_to_dict2(given_value):
    """Input a value and get the dictionary back"""
    true = True
    false = False

    if isinstance(literal_eval(given_value), int):
        return literal_eval(given_value)

    if given_value == 'xxx':
        #         print('value is:', value)
        test1= {'value': 1}
        value = json.dumps(test1)
        return value
    try:
        value = literal_eval(given_value).decode('utf-8')

        if (value[0]=='['):
            #         print('value (i think list) is ', value)
            value = json.loads(value)
            value_dict = {i:value[i] for i in range(len(value))}
            value = json.dumps(value_dict)
        if value=='{}':
            value_dict = {'empty':'empty'}
            value = json.dumps(value_dict)
        value = json.loads(decrease_json(value))

        return value
    except:
        return None

def decrease_json(string):
    """input a value from the dataset and get a smaller string back"""
    if '{' and '}' in string:
        while string[0] != '{':
            string = string[1:]
        while string[-1] != '}':
            string = string[:-1]
    return string

def student_ids():
    "get a student ID dataframe"
    own_DF = pd.DataFrame()
    own_DF['student_ID'] = students()
    return own_DF

def write_student_IDs():
    """writes all the different student IDs in a separate file"""
    with open('student_IDs.txt', 'w') as f:
        for idnr in students():
            f.write(idnr+'\n')

def level_to_numeric():
    """returns a dictionary (INPUT = level; OUTPUT = number)"""
    return{
        "LWOO":1,  #Leerwegondersteunend onderwijs
        "PO":2,  #Primair onderwijs
        "VMBO-B":2,  #Basisberoepsgerichte leerweg
        "VMBO-K":2,  #Kaderberoepsgerichte leerweg
        "VMBO-G":2,  #Gemengde leerweg
        "VMBO":2,  #Koepel term
        "MAVO":2,
        "VMBO-GT":2,
        "VMBO-T":3,  #Theoretische leerweg
        "VMBO / HAVO":3,
        "HAVO":4,
        "HAVO / VWO":5,
        "VWO":6,
        "ATHENEUM":6,
        "GYMNASIUM":6,
    }


def level_id_to_name(level_id):
    "put in level_id and get back all rows from the redundant overview of that level as a dataframe"
    overview = csv_to_df("overview_blocks (redundant).csv")
    return overview[overview['level_id']==level_id]

def numeric_to_level():
    """returns a dictionary (INPUT = number; OUTPUT = level)"""
    inv_map = {}
    for k, v in level_to_numeric().items():
        inv_map[v] = inv_map.get(v, []) + [k]
    return inv_map

def write_intervals():
    """Writes the interval file upon calling, my local machine takes 90-120 minutes to run this function"""
    amount_of_students = len(students())

    with open('intervals.csv', 'w') as f:
        writer = csv.writer(f)

        for j in range(amount_of_students):
            begin = datetime.now()

            #Initialization of a dataframe of an individual student
            student = activities_student(j)

            # Making the 'activity_at' variable a datetime variable as student['date']
            student['date'] = pd.to_datetime(student['activity_at'], dayfirst=True)

            # sort the dataframe on the newly created date variable
            student.sort_values('date', inplace=True)

            # Add the intervals
            student['interval'] = list(student['date'].diff())
            student['SessionID'] = (student.date-student.date.shift(1) > pd.Timedelta(90, 's')).cumsum()+1
            for i in range(len(student)):
                writer.writerow((student['user_id'].iloc[i],student['type'].iloc[i],student['SessionID'].iloc[i], student['date'].iloc[i], student['interval'].iloc[i].total_seconds()))
            end = datetime.now()
            time_passed = end-begin
        print("Student", j, "          took {0} seconds, {1} students left, will take approx {2}".format(time_passed, (amount_of_students-j),time_passed*(len(amount_of_students)-j)))

def intersection(lst1, lst2):
    """Find intersection between two lists"""
    return list(set(lst1) & set(lst2))

def see_question(activityable_id):
    """Find a question based on the activityable_id"""
    redundant = csv_to_df('overview_blocks (redundant).csv')
    answer_activities = csv_to_df('export_answer_activities.csv')
    block_id = answer_activities.iloc[activityable_id]['block_id']
    return redundant[redundant['block_id']==block_id]

def write_days():
    """writes the amount of days per student in a separate file"""

    with open ('days per student.csv', 'w') as f:
        writer = csv.writer(f, delimiter=';')
        writer.writerow(('days', 'user_ID'))
        for i in range(len(students())):
            writer.writerow((len(days_student(i)), students()[i]))
            print(i, students()[i])

    print('im done!')

def see_value(NUMBER, df):
    """Input a number and a dataframe, get back the row of the dataframe with the corresponding index"""
    row = df.iloc[NUMBER]

    return row['value']

def see_random_activity():
    """speaks for itself"""
    df=csv_to_df('activities_with_usertypes.csv')
    randint = random.randint(0,df.shape[0])
    print(randint,
          '\n',
          check_value(randint)[0],
          '\n',
          json.dumps(value_to_dict(randint,df), indent=4))

def check_value(NUMBER):
    """input an index of an activity and get the type of the activity back, if it is an answer activity you will see which
    block is answered"""
    answers = csv_to_df('export_answer_activities.csv')
    df = csv_to_df('activities_with_usertypes.csv')
    if df['type'].iloc[NUMBER] == 'answer':
        value = df['value'].iloc[NUMBER]
        activity_id = df['activityable_id'].iloc[NUMBER]
        block_id = answers[answers['id']==activity_id].iloc[0]['block_id']
    #         print(redundant[redundant['block_id']==block_id].head())
    return(df['type'].iloc[NUMBER], df.iloc[NUMBER])

def see_block(ID):
    """ Input a block ID and get a dataframe with 1 row back with information about that block"""
    redundant = csv_to_df("overview_blocks (redundant).csv")
    return redundant[redundant['block_id']==ID]

def dict_to_json(dictio, name):
    with open("{}.json".format(name), "w") as outfile:
        json.dump(dictio, outfile)

def find_block_id_by_activityable_answer_id(answer_activities, activityable_id):
    return [activity['block_id'] for activity in answer_activities if activity['id']==activityable_id][0]

def find_level_id_and_stars_by_activityable_level_complete_id(level_complete_activities, activityable_id):
    """returns level_id and amount of stars captured based on the activityable id of an level_complete activity"""
    wanted =  [activity for activity in level_complete_activities if activity['id']==activityable_id][0]
    return wanted['level_id'], wanted['stars']

def most_frequent(List):
    return max(set(List), key = List.count)
