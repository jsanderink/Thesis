# Imports
import markov_clustering as mc
import networkx as nx
from sklearn.decomposition import PCA
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
import functions as fx
import pandas as pd
from datetime import datetime
from sklearn.metrics import silhouette_score

START = datetime.now()
print('start at', START)

print("I am going to write the file 'results_markov_gridsearch.txt' ")

# Preprocessing Part of the pipeline:

students = fx.csv_to_df('students_averaged.csv')
students.set_index('student_id', inplace=True)

preprocessor = Pipeline(
    [
        ("scaler", StandardScaler()),
        ("pca", PCA(n_components=2, random_state=42)),
    ]
)


# Assembling the pipeline:
markov_pipe = Pipeline(
    [
        ("preprocessor", preprocessor),
    ]
)

# fitting the Pipeline to the data:
markov_pipe.fit(students)

# Initialize PCA dataframe
pcadf = pd.DataFrame(
    markov_pipe["preprocessor"].transform(students),
    columns=["component_1", "component_2"],
)

#################################################################################################################
# Here I am going to look what the best modularity would be

# highest modularity is considered best

# generate positions as a dictionary where the key is the node id and the value
# is a tuple containing 2D coordinates
positions = {i: (pcadf.iloc[i][0], pcadf.iloc[i][1]) for i in range(pcadf.shape[0])}

# use networkx to generate the graph
network = nx.random_geometric_graph(pcadf.shape[0], 0.3, pos=positions)

# then get the adjacency matrix (in sparse form)
matrix = nx.to_scipy_sparse_matrix(network)


# inflation 1.5 to 2.5 with stepsize 0.1
# expansion 2 to 20 with stepsize 1

print('starting with the actual gridsearch2', datetime.now())

with open('results_markov_gridsearch.txt', 'w') as f:
    for inflation in [i / 10 for i in range(26, 15, -1)]:
        for expansion in [i for i in range(2, 6)]:
            smallstart = datetime.now()
            result = mc.run_mcl(matrix, inflation=inflation, expansion=expansion)
            clusters = mc.get_clusters(result)
            Q = mc.modularity(matrix=result, clusters=clusters)

            print("inflation:", inflation,
                  "expansion:", expansion,
                  "modularity:", Q,
                  "this took", datetime.now()-smallstart)
            f.write(str(' '.join(["inflation:", str(inflation), "expansion:", str(expansion), "modularity:", str(Q), '\n'])))

print('this took', datetime.now()-START)
