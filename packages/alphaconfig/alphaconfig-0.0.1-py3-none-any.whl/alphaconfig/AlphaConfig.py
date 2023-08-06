r"""
Author:
    Yiqun Chen
Docs:
    An easy module for configuration.
"""

import os, copy, yaml, json

class AlphaConfig(object):
    r"""
    Info:
        An module for configuration, which is easy to read and easy to use.
    """
    def __init__(self, src_dict: dict=None, path2yaml: os.PathLike=None, path2json: os.PathLike=None, read_only: bool=False, **kwargs):
        super(AlphaConfig, self).__init__()
        self.__dict__["_level_"] = 0
        self.__dict__["_prefix_"] = "_AlphaConfig_"
        self.__dict__["_read_only_"] = read_only
        if src_dict is not None:
            self._build_from_dict_(src_dict)
        if kwargs:
            self._build_from_dict_(kwargs)
        if path2yaml is not None:
            if os.path.exists(path2yaml):
                try:
                    with open(path2yaml, 'r') as fp:
                        src_dict = yaml.safe_load(fp)
                        self._build_from_dict_(src_dict)
                except:
                    raise IOError("Failed to load configs from such file: {}".format(path2yaml))
            else:
                raise FileNotFoundError("Failed to find such yaml file: {}".format(path2yaml))
        if path2json is not None:
            if os.path.exists(path2json):
                try:
                    with open(path2json, 'r') as fp:
                        src_dict = json.load(fp)
                        self._build_from_dict_(src_dict)
                except:
                    raise IOError("Failed to load configs from such file: {}".format(path2json))
            else:
                raise FileNotFoundError("Failed to find such yaml file: {}".format(path2json))


    def is_read_only(self):
        return self._read_only_


    def cvt2dict(self):
        r"""
        Info:
            Convert to a python builtin dict.
        """
        trg_dict = {}
        _prefix_ = self.__dict__["_prefix_"]
        for key, value in self.__dict__.items():
            value = value.cvt2dict() if isinstance(value, self.__class__) else value
            if _prefix_ in key:
                new_key = key.replace(_prefix_, "")
                trg_dict[new_key] = value
        return trg_dict


    def cvt_state(self, read_only: bool=None):
        r"""
        Info:
            Convert the state as read only or not.
        """
        if read_only is None:
            self.__dict__["_read_only_"] = not self.__dict__["_read_only_"]
        elif read_only in [True, False]:
            self.__dict__["_read_only_"] = read_only
        else:
            raise ValueError("Expect attribute read_only takes value from [True, False, None], but got {}".format(read_only))
        return self.__dict__["_read_only_"]


    def keys(self):
        return self.cvt2dict().keys()


    def values(self):
        return self.cvt2dict().values()


    def items(self):
        return self.cvt2dict().items()


    def _update_(self):
        _prefix_ = self.__dict__["_prefix_"]
        _level_ = self.__dict__["_level_"]
        for key, value in self.__dict__.items():
            if not _prefix_ in key:
                continue
            if isinstance(value, self.__class__):
                value.__dict__["_level_"] = _level_ + 1
                value._update_()


    def _build_from_dict_(self, src_dict: dict):
        for key, value in src_dict.items():
            self.__setattr__(key, value)
        

    def _cvt_attr_(self, name: str):
        return "{}{}".format(self._prefix_, str(name))


    def __setitem__(self, key, value):
        self.__setattr__(key, value)


    def __setattr__(self, key, value):
        if self._read_only_:
            raise AttributeError("A read only AlphaConfig instance is not allowed to modify its attribute.")
        value = self.__class__(value) if isinstance(value, dict) else value
        self.__dict__[self._cvt_attr_(key)] = value
        self._update_()


    def __getitem__(self, key):
        return self.__getattr__(key)


    def __getattr__(self, key):
        if not self._cvt_attr_(key) in self.__dict__.keys():
            if self._read_only_:
                raise AttributeError("No such attribute: {}".format(key))
            self.__dict__[self._cvt_attr_(key)] = self.__class__()
            self._update_()
        return self.__dict__[self._cvt_attr_(key)]


    def __getstate__(self):
        return self.__dict__


    def __setstate__(self, state):
        self.__dict__.update(state)


    def __eq__(self, other):
        return self.__dict__ == other.__dict__


    def __iter__(self):
        return iter(self.cvt2dict().items())


    def __copy__(self):
        trg_dict = self.__class__()
        _prefix_ = self.__dict__["_prefix_"]
        for key, value in self.__dict__.items():
            if _prefix_ in key:
                key = key.replace(_prefix_, "")
                trg_dict[key] = value
        return trg_dict


    def __deepcopy__(self, memo):
        other = self.__class__()
        _prefix_ = self.__dict__["_prefix_"]
        for key, value in self.__dict__.items():
            if id(self) in memo:
                continue
            if _prefix_ in key:
                _key = key.replace(_prefix_, "")
                other[copy.deepcopy(_key)] = copy.deepcopy(value, memo)
        memo[id(self)] = self
        return other


    def __str__(self):
        start = "-"
        string = []
        if self._level_ == 0:
            string.append("* ATTRIBUTES *")
        for key, value in self.__dict__.items():
            if not self._prefix_ in key:
                continue
            substring = "{}{} {}: {}{}".format(
                "\t"*self.__dict__["_level_"], 
                start, 
                key.replace(self._prefix_, ""), 
                "\n" if isinstance(value, self.__class__) else "", 
                str(value), 
            )
            string.append(substring)
        string = "\n".join(string)
        return string

