
# AlphaConfig

## Introduction

AlphaConfig is easy to read and easy to use, which is designed for configuration.

## Installation

You can install AlphaConfig by pip.

```
pip install AlphaConfig
```

## APIs

### __init__(src_dict: dict=None, path2yaml: os.PathLike=None, path2json: os.PathLike=None, read_only: bool=False, **kwargs)

```
Info:
    Initialize a AlphaConfig instance.
Args:
    src_dict (dict): Create an AlphaConfig instance from python builtin's dict, default is None.
    path2yaml (os.PathLike): Create an AlphaConfig instance from a yaml file, default is None.
    path2json (os.PathLike): Create an AlphaConfig instance from a json file, default is None.
    read_only (bool): Set the state of AlphaConfig instance, modification is allowed only if its value is False.
    kwargs (key-value pairs): Create attribute-value pairs from key-value pairs.
```

#### Example

```python
from alphaconfig import AlphaConfig
test_dict = {
    "attr_1": 1, 
    "attr_2": {
        "attr_2_1": [2, 3], 
        "attr_2_2": "this is attr_2_2", 
    }
}
configs = AlphaConfig(test_dict, attr_3="value_3")
print(configs)
# * ATTRIBUTES *
# - attr_1: 1
# - attr_2: 
#         - attr_2_1: [2, 3]
#         - attr_2_2: this is attr_2_2
# - attr_3: value_3
```

### is_read_only()

```
Info:
    Allow user to check whether an instance is read only or not.
Returns:
    (bool): True if it is read only else False.
```

### cvt2dict()

```
Info:
    Convert an AlphaConfig instance to a python builtin's dict.
Returns:
    (dict)
```

#### Examples

```python
test_dict = {
    "attr_1": 1, 
    "attr_2": {
        "attr_2_1": [2, 3], 
        "attr_2_2": "this is attr_2_2", 
    }
}
configs = AlphaConfig(test_dict, attr_3="value_3")
print(configs.cvt2dict())
# {'attr_1': 1, 'attr_2': {'attr_2_1': [2, 3], 'attr_2_2': 'this is attr_2_2'}, 'attr_3': 'value_3'}
```

### cvt_state(read_only: bool=None)

```
Info:
    Convert the readable state according to the given arg.
Args:
    read_only (bool): Set the readable state, if no value is given, revert the state.
Returns:
    (bool): The final readable state.
```

### keys()

```
Info:
    Get all user-defined attributes. This method act like a python builtin's dict.
Returns:
    (dict_keys)
```

### values()

```
Info:
    Get all user-defined values of corresponding keys. This method act like a python builtin's dict.
Returns:
    (dict_values)
```

### items()

```
Info:
    Get all user-defined values of corresponding keys. This method act like a python builtin's dict.
Returns:
    (dict_items)
```

### iter()

AlphaConfig supports `iter`.

#### Example

```python
test_dict = {
    "attr_1": 1, 
    "attr_2": {
        "attr_2_1": [2, 3], 
        "attr_2_2": "this is attr_2_2", 
    }
}
config = AlphaConfig(test_dict)
    for it in config:
        print(it)
# ('attr_1', 1)
# ('attr_2', {'attr_2_1': [2, 3], 'attr_2_2': 'this is attr_2_2'})
```

### copy and deepcopy

AlphaConfig supports copy and deepcopy, just call `copy` module.
