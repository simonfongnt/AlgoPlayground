import os
import pickle

# Search for files
path = os.path.join(
            'dist',
            'KERAS_NN_SAMPLE',
            )
_, _, filenames = next(os.walk(path))

KERAS_NN_SAMPLE_FILE = ''
for filename in filenames:
    if (
            'KERAS_NN_SAMPLE' in filename
        and (
                not KERAS_NN_SAMPLE_FILE
            or  int(filename.split('-')[2]) > int(KERAS_NN_SAMPLE_FILE.split('-')[2])
                )
            ):
        KERAS_NN_SAMPLE_FILE = filename
        
# load AlgoModel
path = os.path.join(
            'dist',
            'KERAS_NN_SAMPLE',
            KERAS_NN_SAMPLE_FILE,
            )
with open(path, 'rb') as mFile:
    model = pickle.load(
        mFile
    )

print(
    model.Info(),
    model.Predict([20000, 30000, 10000, 25000]),
)


# Search for files
path = os.path.join(
            'dist',
            'SKLEARN_SVC_SAMPLE',
            )
_, _, filenames = next(os.walk(path))

SKLEARN_SVC_SAMPLE_FILE = ''
for filename in filenames:
    if (
            'SKLEARN_SVC_SAMPLE' in filename
        and (
                not SKLEARN_SVC_SAMPLE_FILE
            or  int(filename.split('-')[2]) > int(SKLEARN_SVC_SAMPLE_FILE.split('-')[2])
                )
            ):
        SKLEARN_SVC_SAMPLE_FILE = filename
        
# load AlgoModel
path = os.path.join(
            'dist',
            'SKLEARN_SVC_SAMPLE',
            SKLEARN_SVC_SAMPLE_FILE,
            )
with open(path, 'rb') as mFile:
    model = pickle.load(
        mFile
    )

print(
    model.Info(),
    model.Predict([20000, 30000, 10000, 25000]),
)

