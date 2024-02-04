import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning) 

import os
import pandas as pd
import json

path_to_jsons = os.path.join('data', 'data', 'jsons')
dfs = []
files = []

for file in os.listdir(path_to_jsons):
	with open(os.path.join(path_to_jsons, file)) as f:
		dfs.append(pd.json_normalize(json.load(f)))

df = pd.concat(dfs, ignore_index=True)
with open('doc2vec_testing/output.csv', 'w') as csvout:
    df.T.to_csv(csvout)