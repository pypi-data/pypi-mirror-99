# open_explorer.py
from corelibs import lazy as lz

lz.open_explorer(lz.get_home())
lz.open_explorer(r"D:\OneDrive\Documents\_TEST_")

lz.open_explorer(lz.get_home() + r"\.corelibs")  # ouvre le dossier contenant les données utilisateurs comme user_config.py

