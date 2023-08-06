# delete_files.py
# %%
from corelibs import lazy as lz


# %%
# Suppression d'un fichier ciblé et nommé "Nouveau document texte.txt"
file_2_del = r"D:\OneDrive\Documents\_TEST_\DosASupp\Nouveau document texte.txt"
lz.delete_files(file_2_del, verbose=True)

# %%
# Suppression de tous les fichiers avec une extension .RTF
files_2_del = r"D:\OneDrive\Documents\_TEST_\DosASupp"
lz.delete_files(files_2_del, extension="*.rtf", verbose=True)

# %%
# Suppression de tous les fichiers avec une extension .DOC* et .XLS*
files_2_del = r"D:\OneDrive\Documents\_TEST_\DosASupp"
lz.delete_files(files_2_del, extension="*.doc*,*.xls*", verbose=True)

# %%
# L'extension peut prendre un modèle regex, par exemple :
# Suppression de tous les fichiers ayant le mot _LOG_ dans le nom
files_2_del = r"D:\OneDrive\Documents\_TEST_\DosASupp"
lz.delete_files(files_2_del, extension="*_LOG_*", verbose=True)

# %%
# Suppression complète
#   • tous les fichiers à l'intérieur du dossier DosASupp
#   • une fois vide, le dossier DosASupp est supprimé
folder_2_del = r"D:\OneDrive\Documents\_TEST_\DosASupp"
lz.delete_files(folder_2_del, extension="*", verbose=True)
