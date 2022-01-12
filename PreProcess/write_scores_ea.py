import csv
import pandas as pd
import functions as fx
from datetime import datetime, timedelta
import numpy as np
import score_values as sv

# deze cell is met SV

def write_scores(j):
    blocks = fx.csv_to_df("export_blocks.csv")

    score_column = []
    primm_hints = []
    clippy_hints = []

    activities_student_x = fx.csv_to_df('student_{}.csv'.format(j))
    print("STUDENT", j, "Number of activities:",len(activities_student_x))

    for i in range(len(activities_student_x)):
        score = np.nan
        primm_hint = np.nan
        clippy_hint = np.nan

        value = activities_student_x['activity_value'][i]
        blocktype = activities_student_x['block_type'][i]
        activitytype = activities_student_x['activity_type'][i]
        block_id = activities_student_x['block_id'][i]
        activity_id = activities_student_x['activity_id'][i]
        mission_name = activities_student_x['mission_name']

        # print('\nSTUDENT', j, i, activity_id, '\n', block_id, activitytype, '\n', blocktype, '\n', value)

        if activitytype == 'level-complete':
            # print('level-complete')
            pass
        elif activitytype == 'clippy':
            clippy_hint = 1
        elif activitytype == 'primm-hint':
            primm_hint = sv.primm_hint_counter(value, block_id)
            # print('primm hint is', primm_hint)
        elif blocktype == 'question_check_list':
            score = sv.score_question_checklist(value, block_id)
            # print('type = {} | and score = {}'.format(blocktype, score))
        elif blocktype == 'question_multiple_choice':
            score = sv.score_multiple_choice(value)
            # print('type = {} | and score = {}'.format(blocktype, score))
        elif blocktype == 'question_fill_in_the_blank':
            sv.score_fill_in_the_blank(value, block_id)
        elif blocktype == 'question_place_in_order':
            score = sv.score_place_in_order(value, block_id)
            # print('type = {} | and score = {}'.format(blocktype, score))
        elif blocktype == 'question_study_group_list':
            score = sv.score_study_group_list(value)
            # print('type = {} | and score = {}'.format(blocktype, score))
        elif blocktype == 'question_text_long' or blocktype == 'question_text_short':
            score = sv.score_text_short_long(value)
            # print('type = {} | and score = {}'.format(blocktype, score))
        elif blocktype == 'question_number':
            score = sv.score_question_number(value, block_id)
            # print('type = {} | and score = {}'.format(blocktype, score))
        elif blocktype == 'question_text_list':
            score = sv.score_question_text_list(value, block_id)
        elif blocktype == 'question_upload':
            score = sv.score_question_upload(value)
        elif blocktype == 'question_link':
            score = sv.score_link_upload(value)
        elif value == 'xxx':
            score = 0.0
            # print(score)
        else:
            print(activitytype, block_id, blocktype, value)
            print('ERROR\n\n\n\n\n')

        score_column.append(score)
        primm_hints.append(primm_hint)
        clippy_hints.append(clippy_hint)

    activities_student_x['scores'] = score_column
    activities_student_x['primm_hint'] = primm_hints
    activities_student_x['clippy_hint'] = clippy_hints

    activities_student_x['try_counter'] = sv.try_counter(activities_student_x)

    # if len(activities_student_x) != 0:
    #     print('average points per question is:', sum(score_column) / len(score_column))
    #     print('number of primm_hints is:', sum(primm_hints))
    #     print('number of clippy_hints is:', sum(clippy_hints))
    #     print('score column', sum(score_column), '\n', len(score_column), score_column)
    #     print('try counter is:', len(sv.try_counter(activities_student_x)) == len(score_column),
    #           sv.try_counter(activities_student_x))
    # if len(activities_student_x) == 0:
    #     print('STUDENT {} has no logged activities in this dataset'.format(j))

    activities_student_x.drop('start_new_block', axis=1, inplace=True)
    activities_student_x.drop('try_counter', axis=1, inplace=True)
    activities_student_x.to_csv('student_{}.csv'.format(j), sep=';')


