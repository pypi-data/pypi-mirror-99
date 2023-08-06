# is_platform.py
from corelibs import config, lazy as lz

print(lz.is_platform("Windows"))  # vérfie si l'OS est Windows ou non...
print(lz.is_platform("Linux"))
print(lz.is_platform("OSX"))

print(lz.is_platform("INCONNUE"))