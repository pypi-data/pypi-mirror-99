# convert_2_dict.py
# %%
from collections import namedtuple
from corelibs import lazy as lz


# création d'un objet PuPuce tuple nommé
PuPuce = namedtuple("PuPuce", ["name", "age"])
kim = PuPuce(
    name="Kim",
    age=6
)
print(kim)  # affiche PuPuce(name='Kim', age=6)
print(lz.is_namedtuple_instance(kim))  # affiche bien True

# %%
# conversion en dictionnaire
print(lz.convert_2_dict(kim))  # affiche {'name': 'Kim', 'age': 6}

# %%
# création d'un tuple nommé imbriqué
NestedPuPuce = namedtuple("NestedPuPuce", ["name", "age", "nested_tuple"])
kim2 = NestedPuPuce(
    name="Kim",
    age=6,
    nested_tuple=kim
)
print(kim2)  # affiche NestedPuPuce(name='Kim', age=6, nested_tuple=PuPuce(name='Kim', age=6))

# %%
# conversion en dictionnaire
print(lz.convert_2_dict(kim2))  # {'name': 'Kim', 'age': 6, 'nested_tuple': {'name': 'Kim', 'age': 6}}

# %%
# tableau non convertissable
print(lz.convert_2_dict(["TRUONG", "Kim", 6]))  # ['TRUONG', 'Kim', 6]

# %%
# conversion d'un tuple nommé au sein du tableau...
print(lz.convert_2_dict(["TRUONG", "Kim", 6, kim2]))  # ['TRUONG', 'Kim', 6, {'name': 'Kim', 'age': 6, 'nested_tuple': {'name': 'Kim', 'age': 6}}]
