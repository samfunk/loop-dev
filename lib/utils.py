import numpy as np
import pandas as pd
import itertools as it


def make_grid(payload, id):
    values = list()
    for variable in payload.get("params"):
        _check_presense(["name", "type"], variable)
        if variable.get("type") == "int":
            _check_inclusion(["min", "max"], variable)
            values.append({"name": variable.get("name"),
                           "values": list(range(variable.get("min"), variable.get("max") + 1))})
        elif variable.get("type") == "float":
            _check_inclusion(["min", "max", "num_points"], variable)
            values.append({"name": variable.get("name"),
                           "values": list(np.linspace(variable.get("min"), variable.get("max"),
                                          variable.get("num_points"), endpoint=True))})
        elif variable.get("type") == "enum":
            _check_inclusion(["options"], variable)
            values.append({"name": variable.get("name"), "values": variable.get("options")})
        else:
            error_string = "Variable {} has incorrect type. Must be one of: int, float, enum"
            raise TypeError(error_string.format(variable.get("name")))

    return expand_grid({x.get("name"): x.get("values") for x in values})


def _raise_type_error(missing):
    raise TypeError("All variables must have a {}".format(missing))


def _check_presense(keys, dictionary):
    for key in keys:
        if key not in dictionary:
            _raise_type_error(key)


def _check_inclusion(keys, variable):
    for key in keys:
        if key not in variable:
            error_string = "Variable {} of type {} must have <{}> key associated with it"
            raise TypeError(error_string.format(variable.get("name"), variable.get("type"), key))


def expand_grid(value_hash):
    return pd.DataFrame(list(it.product(*[y for x, y in value_hash.items()])),
                        columns=[x for x in value_hash])
