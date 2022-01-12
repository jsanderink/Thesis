import json
import functions as fx

from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from tabulate import tabulate

from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.mixture import GaussianMixture

import argparse
from collections import Counter

START = datetime.now()

SHOW_PLOTS='yes' #enter 'yes' or 'no'

# parser = argparse.ArgumentParser(description="enter the json file (student_sessions)")
# parser.add_argument('student_sessions', metavar='student_sessions',type=str, help='enter the student_sessions.json string')
# parser.add_argument('id_to_number', metavar='id_to_number',type=str, help='enter the id_to_number.json string (NON BASE)')

# args = parser.parse_args()
# student_sessions_json = args.student_sessions
# id_to_number = args.id_to_number

student_sessions_json = 'sessions.json'
id_to_number = 'id_to_number.json'

# Path can be adjusted to the proper json file

with open(student_sessions_json) as f:
    student_sessions = json.load(f)

folder = "static-data/{}"

with open(folder.format(id_to_number)) as f:
    id_to_number = json.load(f)

with open(folder.format('id_to_number_base.json')) as f:
    id_to_number_base = json.load(f)

with open('text_to_number_levels.json', 'r') as fp:
    text_to_number = json.load(fp)

# making a dataframe (easier to fit the pipeline to that)
students = pd.DataFrame(columns=['student_id','session_number','interval', 'stars', 'scores', 'clippy_hint', 'block_try_counter'])

students['student_id'] = [student for student in student_sessions for session in student_sessions[student]]
students['session_number'] = [session for student in student_sessions for session in student_sessions[student]]

students['interval'] = [student_sessions[student][session]['interval'] for student in student_sessions for session in student_sessions[student]]
students['stars'] = [student_sessions[student][session]['stars'] for student in student_sessions for session in student_sessions[student]]
students['scores'] = [student_sessions[student][session]['score'] for student in student_sessions for session in student_sessions[student]]
students['clippy_hint'] = [student_sessions[student][session]['clippy'] for student in student_sessions for session in student_sessions[student]]
students['block_try_counter'] = [student_sessions[student][session]['block_try_counter'] for student in student_sessions for session in student_sessions[student]]

students.fillna(0, inplace=True)
students_av = students.groupby(by='student_id').mean()
students_av['index'] = students_av.index
students_av.drop('index',axis=1 ,inplace=True)


# MAKING THE PIPELINE
print("# MAKING THE PIPELINE")

# Preprocessing Part of the pipeline:
preprocessor = Pipeline(
    [
        ("scaler", StandardScaler()),
        ("pca", PCA(n_components=2, random_state=42)),
    ]
)

# Clustering Part of the pipeline:
EM = Pipeline(
   [
       (
           "EM",
           GaussianMixture(n_components = 2,
                          random_state=42)
           ),
   ]
)

# Assembling the pipeline:
EM_pipe = Pipeline(
    [
        ("preprocessor", preprocessor),
        ("clusterer", EM)
    ]
)

#fitting the Pipeline to the data:
print("#FITTING THE PIPELINE TO THE DATA")
EM_pipe.fit(students_av)

preprocessed_data = EM_pipe["preprocessor"].transform(students_av)
predicted_labels = list(EM_pipe["clusterer"]["EM"].predict(preprocessed_data))

print(EM_pipe['clusterer']['EM'].n_components,
      'clusters and',
      EM_pipe['preprocessor']['pca'].n_components,
      'pca components; give silhouette score of:',
      silhouette_score(preprocessed_data, predicted_labels))

components = [2, 3, 4, 5]
clusters = [i for i in range(2, 9)]

EM_silhouette_scores = {}

for n_components in components:
    for n_clusters in clusters:
        EM_pipe['preprocessor']['pca'].n_components = n_components
        EM_pipe['clusterer']['EM'].n_components = n_clusters

        EM_pipe.fit(students_av)

        preprocessed_data = EM_pipe["preprocessor"].transform(students_av)
        predicted_labels = list(EM_pipe["clusterer"]["EM"].predict(preprocessed_data))

        EM_silhouette_scores['{}components{}clusters'.format(EM_pipe['preprocessor']['pca'].n_components,
                                                             EM_pipe['clusterer'][
                                                                 'EM'].n_components)] = silhouette_score(
            preprocessed_data, predicted_labels)
EM_silhouette_scores = fx.sort_dict_on_keys(EM_silhouette_scores)
print('highest silhouette_score for EM:', EM_silhouette_scores[0])

no_components = int(EM_silhouette_scores[0][0][0])
no_clusters = int(EM_silhouette_scores[0][0][11:12])
print(no_components, no_clusters)


#PLOTTING THE POSSIBLE SILHOUETTE SCORES
# if SHOW_PLOTS == 'yes':
#     print("#PLOTTING THE POSSIBLE SILHOUETTE SCORES")
#     plt.figure(figsize=(6, 6))
#     plt.plot(
#         range(len(EM_silhouette_scores)),
#         [score[1] for score in EM_silhouette_scores],
#         c="#fc4f30",
#         label="EM",
#     )
#     plt.title("the possible silhouette scores (EM)")
#     plt.savefig("visual/EM_CLUSTER_NEW{}.png".format(datetime.now().strftime("%Y%m%d-%H%M%S")))
#     print("figure = saved")

# fit pipeline with best parameters (as found in silhouettescore)
print("# fit pipeline with best parameters (as found in silhouettescore)")
EM_pipe["preprocessor"]["pca"].n_components = no_components
EM_pipe["clusterer"]["EM"].n_components = no_clusters

EM_pipe.fit(students_av)

# Initialize PCA dataframe
pcadf = pd.DataFrame(
    EM_pipe["preprocessor"].transform(students_av),
    columns=["component_{}".format(i) for i in range(1,no_components+1)]
)


# scale the original values scaled between -1 and 1
print("# scale the original values --> between -1 and 1")
x = StandardScaler().fit_transform(students_av)
x = pd.DataFrame(x, columns=students_av.columns)
x

# define preprocessed data and labels
preprocessed_data = EM_pipe["preprocessor"].transform(students_av)
predicted_labels = list(EM_pipe["clusterer"]["EM"].predict(preprocessed_data))

# fill PCA dataframe with predictions
pcadf["predicted_cluster"] = list(EM_pipe["clusterer"]["EM"].predict(preprocessed_data))

pcamodel = EM_pipe["preprocessor"]['pca']
pcamodel.n_components = 4
pca = pcamodel.fit_transform(x)

x["predicted_cluster"] = list(EM_pipe["clusterer"]["EM"].predict(preprocessed_data))
EM_clustermeans = x.groupby(by=["predicted_cluster"]).mean().add_suffix("_mean").transpose()
EM_clustermeans

EM_clusterstd = x.groupby(by=["predicted_cluster"]).std().add_suffix("_std").transpose()
EM_clusterstd

EM_clusters = pd.concat([EM_clustermeans, EM_clusterstd]).sort_index().round(decimals=4)
# EM_clusters['size'] =

EM_clusters.loc["size"] = list(x.groupby(by=["predicted_cluster"]).size())

type(x.groupby(by=["predicted_cluster"]).size())


print(tabulate(EM_clusters, headers='keys', tablefmt='fancy_grid'))
# print(tabulate(EM_clusters, headers='keys', tablefmt='latex'))


EM_clusters.to_excel("clusters/EM_clusters_NEW{}.xlsx".format(datetime.now().strftime("%Y%m%d-%H%M%S")))

print("writing to excel file is done! you can find the clusters and their specifics in 'EM_clusters_NEW.xlsx'")

print("now showing the plot")
x = StandardScaler().fit_transform(students_av)
x = pd.DataFrame(x, columns=students_av.columns)
x

score = pca[:,0:2]
coeff = np.transpose(pcamodel.components_[0:2, :])
labels = list(x.columns)
n = coeff.shape[0]

if SHOW_PLOTS == 'yes':
    fig = plt.figure(figsize=(10, 10))

    scat = sns.scatterplot(
        "component_1",
        "component_2",
        s=50,
        data=pcadf,
        hue="predicted_cluster",
        palette="Set2",
    )

    for i in range(n):
        plt.arrow(0, 0, 5*coeff[i,0], 5*coeff[i,1],color = 'r',alpha = 1)
        if labels is None:
            plt.text(coeff[i,0]* 5, coeff[i,1] * 5, "Var"+str(i+1), color = 'green', ha = 'center', va = 'center')
        else:
            plt.text(coeff[i,0]* 5, coeff[i,1] * 5, labels[i], color = 'b', ha = 'center', va = 'center', fontsize = 'x-large')

    plt.xlabel("PC{}".format(1))
    plt.ylabel("PC{}".format(2))
    plt.grid()
    plt.xlim([-6,6])
    plt.ylim([-6,6])
    plt.hlines(y = 0,xmax=6, xmin=-6, color='black', linewidth=2)
    plt.vlines(x = 0,ymax=6, ymin=-6, color='black', linewidth=2)

    fig.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.0)
    plt.title("Clustering Results from PCA of Students' sessions (Expectation Maximization)")
    # fig.show()
    fig.savefig("visual/VISUAL_EM{}.png".format(datetime.now().strftime("%Y%m%d-%H%M%S")))
    print("you can find the clustering results as a PNG file")

#################################################################################################################
#Determine the clusters that are larger than 10 students
larger_EM_clusters = EM_clusters[[column for column in EM_clusters if EM_clusters[column]['size']>10]]

# Determine Which cluster is the cluster that needs extra attention
worst_values = larger_EM_clusters.iloc[[0,2,4]].idxmax(axis=1)
worst_values2 = larger_EM_clusters.iloc[[6,8]].idxmin(axis=1)

best_values = larger_EM_clusters.iloc[[0,2,4]].idxmin(axis=1)
best_values2 = larger_EM_clusters.iloc[[6,8]].idxmax(axis=1)

worst_numbers = list(worst_values.values)
worst_numbers.extend(list(worst_values2.values))
best_numbers = list(best_values.values)
best_numbers.extend(list(best_values2.values))

worst_cluster, best_cluster = fx.most_frequent(worst_numbers), fx.most_frequent(best_numbers)
print('best cluster = {}\nworst cluster = {}'.format(best_cluster, worst_cluster))

#Determining the people who need less/more challenge
scaled_students = EM_pipe['preprocessor']['scaler'].fit_transform(students_av)
scaled_students = pd.DataFrame(data=scaled_students,index=students_av.index, columns=students_av.columns)
scaled_students['predicted_cluster'] = predicted_labels
scaled_students

# Put the students of the best and worst clusters in separate DataFrames
best_cluster_df = scaled_students[scaled_students['predicted_cluster']==best_cluster]
worst_cluster_df = scaled_students[scaled_students['predicted_cluster']==worst_cluster]

# In the best Cluster --> people who could go a level higher:

# Stars (above average = higher ; below average = lower)
best_high_stars = best_cluster_df[best_cluster_df['stars']>best_cluster_df['stars'].mean()]
best_low_stars = best_cluster_df[best_cluster_df['stars']<=best_cluster_df['stars'].mean()]

best_high_stars.shape, best_low_stars.shape

# Clippy Hints (above average = higher ; below average = lower)
best_high_clippy_hint = best_cluster_df[best_cluster_df['clippy_hint']>best_cluster_df['clippy_hint'].mean()]
best_low_clippy_hint = best_cluster_df[best_cluster_df['clippy_hint']<=best_cluster_df['clippy_hint'].mean()]

best_high_clippy_hint.shape, best_low_clippy_hint.shape

number_of_sd = 0

# Interval (below average - 1 SD = higher ; above average + 1 SD = lower)
best_high_interval = best_cluster_df[best_cluster_df['interval']>(best_cluster_df['interval'].mean()+number_of_sd*(best_cluster_df['interval'].std()))]
best_low_interval = best_cluster_df[best_cluster_df['interval']<(best_cluster_df['interval'].mean()-number_of_sd*(best_cluster_df['interval'].std()))]
best_medium_interval = pd.concat([best_cluster_df, best_high_interval, best_low_interval]).drop_duplicates(keep=False, inplace=False)

best_high_interval.shape, best_low_interval.shape, best_medium_interval.shape

number_of_sd = 0

# Block Try counter (below average + 1.5 SD = higher ; above average - 1.5 SD = lower)
best_high_block_try_counter = best_cluster_df[best_cluster_df['block_try_counter']>(best_cluster_df['block_try_counter'].mean()+(number_of_sd*best_cluster_df['block_try_counter'].std()))]
best_low_block_try_counter = best_cluster_df[best_cluster_df['block_try_counter']<(best_cluster_df['block_try_counter'].mean()-(number_of_sd*best_cluster_df['block_try_counter'].std()))]
best_medium_block_try_counter = pd.concat([best_cluster_df, best_high_block_try_counter, best_low_block_try_counter]).drop_duplicates(keep=False, inplace=False)

best_high_block_try_counter.shape, best_low_block_try_counter.shape, best_medium_block_try_counter.shape

number_of_sd = 0

# Scores (below average + 1.5 SD = higher ; above average - 1.5 SD = lower)
best_high_scores = best_cluster_df[best_cluster_df['scores']>(best_cluster_df['scores'].mean()+(number_of_sd*best_cluster_df['scores'].std()))]
best_low_scores = best_cluster_df[best_cluster_df['scores']<(best_cluster_df['scores'].mean()-(number_of_sd*best_cluster_df['scores'].std()))]
best_medium_scores = pd.concat([best_cluster_df, best_high_scores, best_low_scores]).drop_duplicates(keep=False, inplace=False)

best_high_scores.shape, best_low_scores.shape, best_medium_scores.shape

# make a list with student IDs if you are in the worst category for an attribute your ID is in the list
possible_best = list(best_high_clippy_hint.index)
possible_best.extend(list(best_low_stars.index))
possible_best.extend(list(best_high_interval.index))
possible_best.extend(list(best_high_block_try_counter.index))
possible_best.extend(list(best_low_scores.index))

# Count the occurences of IDs in the list
best_dict = (dict(sorted(Counter(possible_best).items(), key=lambda item: item[1], reverse=True)))


# Get the half with most occurrences and get their IDs
best = [student[0] for student in list(best_dict.items())[:len(best_dict)//2]]

# In the Worst Cluster --> people who could go a level lower:

# Stars (above average = higher ; below average = lower)
worst_high_stars = worst_cluster_df[worst_cluster_df['stars']>worst_cluster_df['stars'].mean()]
worst_low_stars = worst_cluster_df[worst_cluster_df['stars']<=worst_cluster_df['stars'].mean()]

worst_high_stars.shape, worst_low_stars.shape

# Clippy Hints (above average = higher ; below average = lower)
worst_high_clippy_hint = worst_cluster_df[worst_cluster_df['clippy_hint']>worst_cluster_df['clippy_hint'].mean()]
worst_low_clippy_hint = worst_cluster_df[worst_cluster_df['clippy_hint']<=worst_cluster_df['clippy_hint'].mean()]

worst_high_clippy_hint.shape, worst_low_clippy_hint.shape

number_of_sd = 0

# Interval (below average - 1 SD = higher ; above average + 1 SD = lower)
worst_high_interval = worst_cluster_df[worst_cluster_df['interval']>(worst_cluster_df['interval'].mean()+number_of_sd*(worst_cluster_df['interval'].std()))]
worst_low_interval = worst_cluster_df[worst_cluster_df['interval']<(worst_cluster_df['interval'].mean()-number_of_sd*(worst_cluster_df['interval'].std()))]
worst_medium_interval = pd.concat([worst_cluster_df, worst_high_interval, worst_low_interval]).drop_duplicates(keep=False, inplace=False)

worst_high_interval.shape, worst_low_interval.shape, worst_medium_interval.shape

number_of_sd = 0

# Block Try counter (below average + 1.5 SD = higher ; above average - 1.5 SD = lower)
worst_high_block_try_counter = worst_cluster_df[worst_cluster_df['block_try_counter']>(worst_cluster_df['block_try_counter'].mean()+(number_of_sd*worst_cluster_df['block_try_counter'].std()))]
worst_low_block_try_counter = worst_cluster_df[worst_cluster_df['block_try_counter']<(worst_cluster_df['block_try_counter'].mean()-(number_of_sd*worst_cluster_df['block_try_counter'].std()))]
worst_medium_block_try_counter = pd.concat([worst_cluster_df, worst_high_block_try_counter, worst_low_block_try_counter]).drop_duplicates(keep=False, inplace=False)

worst_high_block_try_counter.shape, worst_low_block_try_counter.shape, worst_medium_block_try_counter.shape

number_of_sd = 0

# Scores (below average + 1.5 SD = higher ; above average - 1.5 SD = lower)
worst_high_scores = worst_cluster_df[worst_cluster_df['scores']>(worst_cluster_df['scores'].mean()+(number_of_sd*worst_cluster_df['scores'].std()))]
worst_low_scores = worst_cluster_df[worst_cluster_df['scores']<(worst_cluster_df['scores'].mean()-(number_of_sd*worst_cluster_df['scores'].std()))]
worst_medium_scores = pd.concat([worst_cluster_df, worst_high_scores, worst_low_scores]).drop_duplicates(keep=False, inplace=False)

worst_high_scores.shape, worst_low_scores.shape, worst_medium_scores.shape

# make a list with student IDs if you are in the worst category for an attribute your ID is in the list
possible_worst = list(worst_high_clippy_hint.index)
possible_worst.extend(list(worst_low_stars.index))
possible_worst.extend(list(worst_high_interval.index))
possible_worst.extend(list(worst_high_block_try_counter.index))
possible_worst.extend(list(worst_low_scores.index))

# Count the occurences of IDs in the list
worst_dict = (dict(sorted(Counter(possible_worst).items(), key=lambda item: item[1], reverse=True)))

# Get the half with most occurrences and get their IDs
worst = [student[0] for student in list(worst_dict.items())[:len(worst_dict)//2]]


for key, value in id_to_number.items():
    # People who need a lower level get a lower level
    if key in worst:
        id_to_number[key] = value - 1
    # People who need a higher level get a higher level
    if key in best:
        id_to_number[key] = value + 1
    # People who are under their low level get back to their minimum level
    if key in id_to_number_base and id_to_number[key] < id_to_number_base[key]:
        id_to_number[key] = id_to_number_base[key]
    # People who are above the max level go to the maximum level
    if id_to_number[key] > 6:
        id_to_number[key] = 6
    if id_to_number[key] < 2:
        id_to_number[key] = 2

    number_to_text = {v: k for (k, v) in text_to_number.items()}
    text_value = number_to_text[id_to_number[key]]

    id_to_number[key] = text_value


with open('desired_level.json', 'w') as fp:
    json.dump(id_to_number, fp)

print("\n desired_level.json is written! ")

for i in range(2, 7):
    print("\noriginally --> of level {} there are {} students".format((number_to_text[i],i),
                                                                      sum(value == i for value in id_to_number_base.values())))

    print("new        --> of level {} there are {} students".format((number_to_text[i],i),
                                                                    sum(value == number_to_text[i] for value in id_to_number.values())))


print("\nDone, this took {}".format(datetime.now()-START))
