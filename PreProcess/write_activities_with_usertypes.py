# activities_with_usertypes.csv moet worden geschreven
# Dit betekent dat voor elke rij in export_activities.csv er een kolom met de usertype bij moet komen

import csv
import functions as fx
import numpy as np
from datetime import datetime

activities = fx.csv_to_df('export_activities.csv')

print(activities.shape)
print(activities.columns)

activities['user_type'] = np.nan
activities['date'] = np.nan

users = fx.csv_to_df('export_users.csv')

begin = datetime.now()

print('BEGIN', begin)

with open('activities_with_usertypes.csv', 'w', newline='') as f:
    writer = csv.writer(f, delimiter=';')
    writer.writerow((list(activities.columns)))

    for ind in activities.index:
        user_id = activities['user_id'][ind]

        try:
            date = datetime.strptime(activities['activity_at'][ind], '%Y-%m-%d %H:%M:%S')
            user_type = users[users['id'] == user_id]['userable_type'].iloc[0]

            print(ind, 'time to go = ',  (activities.shape[0]-ind)*((datetime.now()-begin)/(ind+1)))

            activities['user_type'][ind] = user_type
            activities['date'][ind] = date

            writer.writerow((list(activities.iloc[ind])))
        except IndexError as error:
            print("ERROR", error)

