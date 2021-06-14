from collections import defaultdict
from collections import namedtuple
import json
import os, glob
from numpy.core.fromnumeric import _var_dispatcher
import pandas as pd
import seaborn as sns
sns.set(style="whitegrid")

# convert file directory to a variant
# use string [sequential] and [parallel]
# after that the last .bench file is used
# all the other stuff comes after it

# this is a very specific case on which we would be starting on
# eg. /sequential/<date>/<commit-id>/<variant>.bench

def create_tuple(file, s):
    Value = namedtuple('Value', 'timestamp commit_id variant')
    s = '/' + s + '/'
    value = file.split(s)[1]
    # date  = value.split('/')[0].split('_')[0]
    timestamp  = value.split('/')[0]
    commit_id  = value.split('/')[1]
    variant  = value.split('/')[2].split('_')[0]
    v = Value(timestamp, commit_id, variant)
    return v

def create_dataframe(file, s):
    with open(file) as f:
        data = [json.loads(l) for l in f]
        df   = pd.json_normalize(data)
        value = create_tuple(file, s)
        df["variant"] = value.variant + '_' + value.timestamp.split('_')[0] + '_' + value.commit_id[:7]
    return df

def create_table(files, s):
    dataframes = [create_dataframe(file, s) for file in files]
    df = pd.concat(dataframes, sort=False)
    df = df.sort_values(['name'])
    return df

# file_directory (string) -> type_of_benchmark (string) -> benchfile_directories ([string])
def get_benchfiles(artifacts_dir, s):
    benchfiles = []
    stem_map = {
        'sequential' : '_1.orun.summary.bench',
        'parallel'   : '_1.orunchrt.summary.bench'
    }
    for root, dirs, files in os.walk(artifacts_dir):
        for file in files:
            if file.endswith(stem_map[s]):
                benchfiles.append((os.path.join(root, file)))
    return benchfiles

def files_to_dict(files, s):
    benches = defaultdict(list)
    for x in files:
        value = create_tuple(x, s)
        # s = '/' + s + '/'
        # l = x.split(s)[1]
        # d = l.split('/')
        # timestamp    = d[0]
        # commit       = d[1]
        # variant_root = d[2].split('_')[0]
        # variant_stem = d[2].split('_')[1]
        value_str = value.variant.split('_')[0] + '+' + value.commit_id + '_' + value.variant.split('_')[1]
        benches[value.timestamp].append(value_str)
    benches = dict(benches)
    return benches

def selected_benchfiles(artifact_dir, type_of_benchmark):
    pass

x = get_benchfiles("/home/sk/sandmark-nightly/sequential/", "sequential")
x = create_table(x, "sequential")
print(x['variant'])