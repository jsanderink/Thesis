import json
from datetime import datetime

START = datetime.now()

import functions as fx
import score_values2 as sv
import numpy as np
import argparse

parser = argparse.ArgumentParser(description="enter the different json files (activities; answer_activities ; level_complete_activities")

parser.add_argument('folder', metavar='folder',type=str, help='the folder in which all the json files can be found')

args = parser.parse_args()

# Define folder of this import
jsonFolder = args.folder

# Define files names
activities = 'activities.json'
answer_activities = 'answerActivities.json'
level_complete_activities = 'levelCompleteActivities.json'

# folder name
folder = '../storage/app/learning-analytics/{}/{}'

# example json files
# folder = '../storage/app/learning-analytics/2021-09-24/{}'

# TAKE THE FILES FROM WHICH I NEED INFORMATION
print("# TAKE THE FILES FROM WHICH I NEED INFORMATION")
# You can put another path variable in here
with open(folder.format(jsonFolder, activities)) as f:
    activities = json.load(f)

with open('static-data/id_to_number.json') as f:
    id_to_number = json.load(f)

with open(folder.format(jsonFolder, answer_activities)) as f:
    answer_activities = json.load(f)

with open(folder.format(jsonFolder, level_complete_activities)) as f:
    level_complete_activities = json.load(f)

redundant = fx.csv_to_df("static-data/overview_blocks_redundant.csv")

# DIT MOET NOG EEN JSON WORDEN DENK IK!
# answer_activities = fx.csv_to_df(folder.format('export_answer_activities.csv'))
# level_complete_activities = fx.csv_to_df(folder.format('export_level_complete_activities.csv'))
blocks = fx.csv_to_df("static-data/export_blocks.csv")


# FILTER ON USABLE ACTIVITIES AND TAKE THE STUDENT IDS
print("# FILTER ON USABLE ACTIVITIES AND TAKE THE STUDENT IDS")
# taking only the activities of interest
usable = [activity for activity in activities if activity['type'] in ['answer', 'clippy', 'level-complete']]

# Unique Students in this JSON:
student_ids = list(set([activity['user_id'] for activity in usable]))

# ADD VARIABLES TO ACTIVITIES:
print('# ADD VARIABLES TO ACTIVITIES')
# Datetime, Current_Level, Info on the blocks, stars, scores

total_usable = len(usable)
counter = 0

# first i am giving the acitivities their properties (without interval)
for activity in usable:
    counter = counter + 1
    activity['datetime'] = datetime.strptime(activity['activity_at'], '%Y-%m-%d %H:%M:%S')

    usable

    try:
        activity['current_level'] = id_to_number[activity['user_id']]
    except:
        activity['current_level'] = 2
    #         print("HACKED THE STUDENT LEVEL")

    # Reset/Initiate some the variables:
    activity['block_id'] = np.nan
    activity['block_type'] = np.nan
    activity['level_name'] = np.nan
    activity['chapter_name'] = np.nan
    activity['mission_name'] = np.nan
    activity['level_type'] = np.nan
    activity['level_id'] = np.nan
    activity['stars'] = np.nan
    activity['score'] = np.nan
    activity['clippy_hint'] = 0

    activity_type = activity['type']

    # ANSWER ACTIVITIES
    if activity_type == "answer":

        # Find the ID of the block based on the activityable_id if the activity
        activity['block_id'] = fx.find_block_id_by_activityable_answer_id(answer_activities,activity['activityable_id'])

        try:
            activity['block_type'] = \
            redundant[redundant['block_id'] == activity['block_id']]['block_type'].values.tolist()[0]
            activity['level_name'] = \
            redundant[redundant['block_id'] == activity['block_id']]['level_name'].values.tolist()[0]
            activity['chapter_name'] = \
            redundant[redundant['block_id'] == activity['block_id']]['chapter_name'].values.tolist()[0]
            activity['mission_name'] = \
            redundant[redundant['block_id'] == activity['block_id']]['mission_name'].values.tolist()[0]
            activity['level_type'] = \
            redundant[redundant['block_id'] == activity['block_id']]['level_type'].values.tolist()[0]
            activity['level_id'] = redundant[redundant['block_id'] == activity['block_id']]['level_id'].values.tolist()[
                0]
        except:
            pass

    # LEVEL COMPLETE ACTIVITIES
    if activity_type == "level-complete":

        activity['level_id'], activity['stars'] = fx.find_level_id_and_stars_by_activityable_level_complete_id(level_complete_activities, activity['activityable_id'])
        try:
            activity['level_type'] = \
            redundant[redundant['level_id'] == activity['level_id']]['level_type'].values.tolist()[0]
            activity['level_name'] = \
            redundant[redundant['level_id'] == activity['level_id']]['level_name'].values.tolist()[0]
            activity['chapter_name'] = \
            redundant[redundant['level_id'] == activity['level_id']]['chapter_name'].values.tolist()[0]
            activity['mission_name'] = \
            redundant[redundant['level_id'] == activity['level_id']]['mission_name'].values.tolist()[0]
        except:
            pass

        # CLIPPY
    if activity_type == 'clippy':
        activity_value = activity['value']

        if 'levelId' in activity_value:
            activity['level_id'] = activity_value['levelId']

            try:
                activity['level_type'] = \
                redundant[redundant['level_id'] == activity['block_id']]['level_type'].values.tolist()[0]
                activity['level_name'] = \
                redundant[redundant['level_id'] == activity['block_id']]['level_name'].values.tolist()[0]
                activity['chapter_name'] = \
                redundant[redundant['level_id'] == activity['block_id']]['chapter_name'].values.tolist()[0]
                activity['mission_name'] = \
                redundant[redundant['level_id'] == activity['block_id']]['mission_name'].values.tolist()[0]
            except:
                pass

    value = activity['value']
    blocktype = activity['block_type']
    activitytype = activity['type']
    block_id = activity['block_id']
    activity_id = activity['id']
    mission_name = activity['mission_name']

    # Score the answer activities
    print("     # Score the answer activities {}/{}".format(counter,total_usable))
    if activity_type == 'level-complete':
        pass
    elif activity_type == 'clippy':
        activity['clippy_hint'] = 1
    elif blocktype == 'question_check_list':
        activity['score'] = sv.score_question_checklist(value, block_id)
        # print('type = {} | and score = {}'.format(blocktype, score))
    elif blocktype == 'question_multiple_choice':
        activity['score'] = sv.score_multiple_choice(value)
        # print('type = {} | and score = {}'.format(blocktype, score))
    elif blocktype == 'question_fill_in_the_blank':
        activity['score'] = sv.score_fill_in_the_blank(value, block_id)
    elif blocktype == 'question_place_in_order':
        activity['score'] = sv.score_place_in_order(value, block_id)
        # print('type = {} | and score = {}'.format(blocktype, score))
    elif blocktype == 'question_study_group_list':
        activity['score'] = sv.score_study_group_list(value)
        # print('type = {} | and score = {}'.format(blocktype, score))
    elif blocktype == 'question_text_long' or blocktype == 'question_text_short':
        activity['score'] = sv.score_text_short_long(value)
        # print('type = {} | and score = {}'.format(blocktype, score))
    elif blocktype == 'question_number':
        activity['score'] = sv.score_question_number(value, block_id)
        # print('type = {} | and score = {}'.format(blocktype, score))
    elif blocktype == 'question_text_list':
        activity['score'] = sv.score_question_text_list(value, block_id)
    elif blocktype == 'question_upload':
        activity['score'] = sv.score_question_upload(value)
    elif blocktype == 'question_link':
        activity['score'] = sv.score_link_upload(value)
    elif value == 'xxx':
        activity['score'] = 0.0
        # print(score)
    else:
        print(activitytype, block_id, blocktype, value)
        print('ERROR\n\n\n\n\n')

# DETERMINE THE ACTIVITIES PER STUDENT
print("# DETERMINE THE ACTIVITIES PER STUDENT")

student_sessions = {student_id:{} for student_id in student_ids}

for student_id in student_ids:
    student_x = [activity for activity in usable if activity['user_id'] ==student_id]
    print("student", student_id, 'has', len(student_x), "activities")

    if(len(student_x) <= 4):
        print("skipping this student cause less then 10 activities in the session")
        continue

    # ADDING INTERVALS, SESSION NUMBERS, AND BLOCK_TRY_COUNTERS
    print("# ADDING INTERVALS, SESSION NUMBERS, AND BLOCK_TRY_COUNTERS")

    # Adding interval and session counter
    session_counter = 1

    for activity_no in reversed(range(len(student_x) - 1)):

        time_stamp = student_x[activity_no]['activity_at']

        # adding intervals
        student_x[activity_no]['interval'] = (
                    student_x[activity_no - 1]['datetime'] - student_x[activity_no]['datetime']).total_seconds()
        if student_x[activity_no]['interval'] < 0:
            student_x[activity_no]['interval'] = 0

        # adding session numbers
        # iteratively adding session numbers based on whether there was a 5 mins interval
        student_x[activity_no]['session_counter'] = session_counter
        if student_x[activity_no]['interval'] >= 500:
            session_counter += 1
            student_x[activity_no]['session_counter'] = session_counter
            student_x[activity_no]['interval'] = 0.0

        # adding block_try_counters
        number_of_tries = 1
        student_x[activity_no]['block_try_counter'] = number_of_tries
        try:
            while student_x[activity_no]['block_id'] == student_x[activity_no + number_of_tries]['block_id']:
                #             print(number_of_tries)
                number_of_tries += 1
                student_x[activity_no]['block_try_counter'] = number_of_tries
            if student_x[activity_no]['block_try_counter'] > 20:
                student_x[activity_no]['block_try_counter'] = 20
        except:
            pass

        # first activity (in time) should belong to session 1 and have interval 0 and block_try_counter 1
        student_x[-1]['session_counter'] = 1
        student_x[-1]['interval'] = 0
        student_x[-1]['block_try_counter'] = 1

    # MAKING THE SESSIONS (PER STUDENT)
    # Make Sessions
    for session_no in list(set([activity['session_counter'] for activity in student_x])):
        # Take the subset of the student:
        session = [activity for activity in student_x if activity['session_counter'] == session_no]

        try:
            session_interval = np.nanmean([activity['interval'] for activity in student_x if
                                           activity['session_counter'] == session_no and isinstance(activity['interval'],
                                                                                                    (int, float))])
        except:
            session_interval = np.nan()

        try:
            session_stars = np.nanmean([activity['stars'] for activity in student_x if
                                        activity['session_counter'] == session_no and isinstance(activity['stars'],
                                                                                                 (int, float))])
        except:
            session_stars = np.nan
        try:
            session_score = np.nanmean([activity['score'] for activity in student_x if
                                        activity['session_counter'] == session_no and isinstance(activity['score'],
                                                                                                 (int, float))])
        except:
            session_score = np.nan

        try:
            session_clippy = np.nanmean([activity['clippy_hint'] for activity in student_x if
                                         activity['session_counter'] == session_no and isinstance(activity['clippy_hint'],
                                                                                                  (int, float))])
        except:
            session_clippy = np.nan

        try:
            session_block_try = np.nanmean([activity['block_try_counter'] for activity in student_x if
                                            activity['session_counter'] == session_no and isinstance(
                                                activity['block_try_counter'], (int, float))])
        except:
            session_block_try = np.nan

        session = {'interval': session_interval,
                   'stars': session_stars,
                   'score': session_score,
                   'clippy': session_clippy,
                   'block_try_counter': session_block_try,
                   'timestamp': time_stamp}
        print(session)

        student_sessions[student_id][session_no] = session

# print(student_sessions)
with open(folder.format(jsonFolder, 'student_sessions.json'), 'w') as fp:
    json.dump(student_sessions, fp)

print("Done, student_sessions.json is written")
print("This took", datetime.now()-START)
