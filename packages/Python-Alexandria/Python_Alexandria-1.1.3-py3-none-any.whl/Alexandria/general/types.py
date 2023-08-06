import numpy as np


def to_ndarrays(*args):
    import inspect
    args, _, _, values = inspect.getargvalues(inspect.currentframe())
    inputs = np.array(values["args"], dtype=object).squeeze()
    for i in range(len(inputs)):
        if isinstance(inputs[i], np.ndarray):
            pass
        else:
            inputs[i] = np.array(inputs[i])
    return inputs
