# is_namedtuple_instance.py
from collections import namedtuple
from corelibs import lazy as lz


# création d'un objet PuPuce tuple nommé
PuPuce = namedtuple("PuPuce", ["name", "age"])
kim = PuPuce(
    name="Kim",
    age=6
)
print(kim)  # affiche bien PuPuce(name='Kim', age=6)

print(lz.is_namedtuple_instance(kim))  # affiche bien True

print(lz.is_namedtuple_instance("Coucou Kim"))  # affiche False
