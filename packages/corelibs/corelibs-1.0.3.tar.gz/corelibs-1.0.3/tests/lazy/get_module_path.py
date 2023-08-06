# get_module_path.py
from corelibs import lazy as lz

path = lz.get_module_path()
print("Le chemin du programme python est \"{path}\"".format(path=path))
