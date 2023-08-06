# get_username.py
from corelibs import config, lazy as lz

username = lz.get_username()
print("Le nom de l'utilisateur actuel est \"{username}\"".format(username=username))
