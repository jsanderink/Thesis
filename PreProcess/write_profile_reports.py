from pandas_profiling import ProfileReport
import functions as fx
import os
import pandas as pd

files = os.listdir()
csvs = [file for file in files if str(file[-1])=="v"]

# print(csvs)

for csv in csvs:
    try:
        df = pd.read_csv(csv, delimiter=';')
        ProfileReport(df).to_file('profile_report_'+str(csv[7:-4]+'.html'))
    except:
        ZeroDivisionError()
