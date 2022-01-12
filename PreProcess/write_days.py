import csv
import pandas as pd
import functions as fx


with open ('days per student.csv', 'w', newline='') as f:
    writer = csv.writer(f, delimiter=';')
    writer.writerow(('days', 'user_ID'))
    for i in range(len(fx.students())):
        writer.writerow((len(fx.days_student(i)), fx.students()[i]))
        print(i, fx.students()[i])