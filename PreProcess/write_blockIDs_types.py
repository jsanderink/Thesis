import functions as fx
import csv
from datetime import datetime


with open ('answer_with_blocks.csv', 'w', newline='') as f:
    writer = csv.writer(f, delimiter=';')
    writer.writerow(('Unnamed: 0', 'id', 'user_id', 'type', 'value', 'activityable_id',
       'activityable_type', 'activity_at', 'created_at', 'updated_at', 'date',
       'user_type', 'block_id','block_type'))



    i = 0
    j=0
    percentage = 0
    starttime = datetime.now()
    print(starttime)

    act_w_us = fx.csv_to_df("activities_with_usertypes.csv")
    answer_values = act_w_us[(act_w_us["user_type"] == 'student') & (act_w_us["type"] == 'answer')]
    answer_values['block_id'] = None
    answer_activities = fx.csv_to_df("export_answer_activities.csv")

    for ind in answer_values.index:
        row = list(answer_values.iloc[j])
        row[-1] = answer_activities[answer_activities['id'] == answer_values['activityable_id'][ind]]['block_id'].iloc[
            0]
        row.extend(fx.see_block(row[-1]))

        j = j + 1
        i = i + 1
        writer.writerow(row)
        if i > 182:
            now = datetime.now()
            time_elapsed = now - starttime
            percentage = percentage + 0.1
            print(round(percentage,1), "% time elapsed is", time_elapsed)
            i = 0

print('END OF SCRIPT REACHED')