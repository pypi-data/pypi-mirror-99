# merge_dictionaries.py
# %%
from corelibs import lazy as lz

# %%
x = None
y = {"prenom": "Kim", "age": 6}
z = lz.merge_dictionaries(x, y)
print(z)  # {'prenom': 'Kim', 'age': 6}

# %%
# inversion
z = lz.merge_dictionaries(y, x)
print(z)  # None

# %%
x = {"a": 1, "b": 2}
y = {"b": 10, "c": 11}
z = lz.merge_dictionaries(x, y)
print(z)  # {"a": 1, "b": 10, "c": 11}

# %%
x = {"b": 10, "c": 11}
y = {"a": 1, "b": {"b1": "hello", "b2": 3}}
z = lz.merge_dictionaries(x, y)
print(z)  # {"b": {"b1": "hello", "b2": 3}, "c": 11, "a": 1}

# %%
x = {"b": {"b1": "hello", "b2": 3}, "c": 11}
y = {"a": 1, "b": {"b1": "Kim", "b2": 6}}
z = lz.merge_dictionaries(x, y)
print(z)  # {"b": {"b1": "Kim", "b2": 6}, "c": 11, "a": 1}

# %%
DICT_USER = {
    "asctime": {"color": "BLACK"},
    "levelname": {"color": "WHITE"}
}

DICT_REF = {
    "asctime": {"color": 242, "bright": True},
    "hostname": {"color": "magenta"},
    "username": {"color": "yellow"},
    "levelname": {"color": 242, "bright": True},
    "name": {"color": "blue"},
    "programname": {"color": "cyan"}
}

MERGED_DICT = lz.merge_dictionaries(DICT_REF, DICT_USER)
print(MERGED_DICT)  # {
#   "asctime": {"color": "BLACK", "bright": True},
#   "hostname": {"color": "magenta"},
#   "username": {"color": "yellow"},
#   "levelname": {"color": "WHITE", "bright": True},
#   "name": {"color": "blue"},
#   "programname": {"color": "cyan"}
# }

