# get_abspath.py
from corelibs import lazy as lz

abs_path = lz.get_abspath(r"C:\documents/dir", "toto")
print(f"Le chemin absolu normalisé est \"{abs_path}\"")
