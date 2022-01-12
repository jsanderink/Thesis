import csv
import pandas as pd
import functions as fx
from datetime import datetime, timedelta
import numpy as np


blocks = fx.csv_to_df("export_blocks.csv")

def score_question_checklist(value, block_id):
    # Getting the number of (correct) answers
    block_info = blocks[blocks['id'] == block_id]['block_info'].values.tolist()[0]
    block_dict = fx.value_to_dict2(block_info)

    number_of_items = 0
    number_of_correct_items = 0

    for item in block_dict['answers']:
        if 'correct' not in (list(item.keys())):
            return 0.0
        number_of_items += 1
        if item['correct']:
            number_of_correct_items += 1



    if type(value) == str:
        # print('this value is not a dictionary but a string')
        return 0.0

    given_correct = 0
    given_false = 0

    for item in value:
        if 'correct' not in (list(item.keys())):
            return 0.0
        else:
            if item['correct']: given_correct += 1
            if not item['correct']: given_false += 1

    # Calculating the score
    precision = given_correct / (given_correct + given_false)
    recall = given_correct / number_of_correct_items

    f_1 = 0

    try:
        f_1 = 2 * (precision * recall) / (precision + recall)
    except:
        ZeroDivisionError

    return f_1


def score_multiple_choice(value):
    score = 0

    if type(value) == str:
        # print('this value is not a dictionary but a string')
        return 0.0

    if 'correct' not in (list(value.keys())):
        # print('no correct answer in this question')
        return 0.0

    if value['correct']:
        score = score + 1
    return score

def score_fill_in_the_blank(value, block_id):
    # looking for the correct answers
    block_info = blocks[blocks['id'] == block_id]['block_info'].values.tolist()[0]
    block_dict = fx.value_to_dict2(block_info)

    # initially score = 0
    score = 0

    # If the given answer is a correct listed answer, then the score for that question is 1
    for answer in block_dict['possibleAnswers']:
        if answer['given'] == value and answer['correct'] == True:
            score = 1

    return score


def streak(l):
    """Identify a streak and return the length"""
    b_start, b_end = 0, 0

    start = 0

    # Iterate over the numbers 1 to length of list

    for i in range(1, len(l)):
        # See if i is one larger than i-1
        if l[i] != l[i - 1] + 1:
            start = i

        # current index minus the start of the streak is the streak length
        # if this length is longer than previous best, update the streak length
        if (i - start) > (b_end - b_start):
            b_start, b_end = start, i

    return b_end - b_start + 1


def score_place_in_order(value, block_id):
    block_info = blocks[blocks['id'] == block_id]['block_info'].values.tolist()[0]
    block_dict = fx.value_to_dict2(block_info)

    order = []

    for item in value:
        order.append(item['correctOrder'])

    correct_indices = [i == j for i, j in zip(sorted(order), order)]

    correct_index_score = sum(correct_indices) / len(correct_indices)
    #     print('correct_index_score:', correct_index_score)
    streak_score = streak(order) / len(order)
    #     print('streak score:', streak_score)
    #     print('total score:', (correct_index_score+streak_score)/2, '\n')
    return (correct_index_score + streak_score) / 2


def score_study_group_list(value):
    # print('ERROR')
    return 0.0


def score_text_short_long(value):
    if len(value) > 0:
        return 1
    else:
        return 0

def score_question_upload(value):
    return value

def score_link_upload(value):
    return value

def score_question_text_list(value, block_id):
    # taking the number of answers out of the value variable
    int_value = len(value)

    # looking for the correct answers
    block_info = blocks[blocks['id'] == block_id]['block_info'].values.tolist()[0]
    block_dict = fx.value_to_dict2(block_info)

    # initially score = 0
    score = 0
    diff = block_dict['maxItems'] - block_dict['minItems']

    # look if score is between min and max
    if int_value >= block_dict['minItems'] and int_value <= block_dict['maxItems']:
        score = 0.5
        if diff == 0:
            score = 1
        elif diff > 0:
            more_than_min = int_value - block_dict['minItems']
            score = 0.5 + ((0.5 / diff) * more_than_min)

    return score

def score_question_number(value, block_id):
    # print(block_id, value)
    value = int(float(fx.value_to_dict2(value)))

    block_info = blocks[blocks['id'] == block_id]['block_info'].values.tolist()[0]
    block_dict = fx.value_to_dict2(block_info)

    # block_dict['correctType'] could be 'equals', 'between', 'max', 'min'

    # print(block_dict)

    if block_dict['correctType'] == 'equals':
        if block_dict['equals'] == value:
            return 1.0
        if block_dict['equals'] != value:
            return 0

    if block_dict['correctType'] == 'between':
        if value < block_dict['min'] or value > block_dict['max']:
            return 0
        if value >= block_dict['min'] and value <= block_dict['max']:
            return 1

    if block_dict['correctType'] == 'max':
        if value <= block_dict['max']:
            return 1
        if value > block_dict['max']:
            return 0

    if block_dict['correctType'] == 'min':
        if value >= block_dict['min']:
            return 1
        if value < block_dict['min']:
            return 0




def clippy_hint_counter(value):
    return 1


def try_counter(student):
    """Input a student dataframe and get a list of tries in the form of a list"""
    block_ids = student['block_id']
    shifted = block_ids.shift()

    block_ids.ne(shifted)

    student['start_new_block'] = block_ids.ne(block_ids.shift())
    student['start_new_block'] = student['start_new_block'].cumsum()

    count = student.groupby('start_new_block').cumcount() + 1
    count = count.where(count <=25,25)

    student['block_try_counter'] = count
    return student['block_try_counter'].values.tolist()
