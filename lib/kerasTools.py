

import tensorflow as tf
class KerasTools():
    def __init__(
        self,
        ):
        pass
    def encode_numerical_feature(
            self,
            feature, 
            name, 
            dataset,
            ):
        # Create a Normalization layer for our feature
        normalizer = tf.keras.layers.experimental.preprocessing.Normalization()

        # Prepare a Dataset that only yields our feature
        feature_ds = dataset.map(lambda x, y: x[name])
        feature_ds = feature_ds.map(lambda x: tf.expand_dims(x, -1))

        # Learn the statistics of the data
        normalizer.adapt(feature_ds)

        # Normalize the input feature
        encoded_feature = normalizer(feature)
        return encoded_feature

        # return feature_ds