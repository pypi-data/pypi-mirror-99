from tensorflow.keras import activations, constraints, initializers, regularizers

LAYER_KWARGS = {"activation", "use_bias"}
KERAS_KWARGS = {
    "trainable",
    "name",
    "dtype",
    "dynamic",
    "input_dim",
    "input_shape",
    "batch_input_shape",
    "batch_size",
    "weights",
    "activity_regularizer",
    "autocast",
    "implementation",
}


def is_layer_kwarg(key):
    return key not in KERAS_KWARGS and (
        key.endswith("_initializer")
        or key.endswith("_regularizer")
        or key.endswith("_constraint")
        or key in LAYER_KWARGS
    )


def is_keras_kwarg(key):
    return key in KERAS_KWARGS


def deserialize_kwarg(key, attr):
    if key.endswith("_initializer"):
        return initializers.get(attr)
    if key.endswith("_regularizer"):
        return regularizers.get(attr)
    if key.endswith("_constraint"):
        return constraints.get(attr)
    if key == "activation":
        return activations.get(attr)
    return attr


def serialize_kwarg(key, attr):
    if key.endswith("_initializer"):
        return initializers.serialize(attr)
    if key.endswith("_regularizer"):
        return regularizers.serialize(attr)
    if key.endswith("_constraint"):
        return constraints.serialize(attr)
    if key == "activation":
        return activations.serialize(attr)
    if key == "use_bias":
        return attr
