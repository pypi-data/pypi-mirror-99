# add_dir_path_2_project.py
from corelibs import lazy as lz

# inclusion du dossier parent contenant les programmes à inclure, ici D:\OneDrive\Documents\_TEST_\PY_2_IMPORT
lz.add_dir_path_2_project(r"D:\OneDrive\Documents\_TEST_\PY_2_IMPORT")

try:
    import programme_importe as pi
except ImportError:
    raise Exception("\n\nProblème import programme tiers d'un emplacement loufoque, hors projet")

pi.say_hello("Kim!")  # affichera Hello Kim! si tout est OK
