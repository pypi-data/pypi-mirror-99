# get_hostname.py
from corelibs import config, lazy as lz

hostname = lz.get_hostname()
print("Le nom de l'ordinateur actuel est \"{hostname}\"".format(hostname=hostname))
