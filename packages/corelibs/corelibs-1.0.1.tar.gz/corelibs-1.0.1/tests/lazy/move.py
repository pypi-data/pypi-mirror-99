# move.py
# %%
from corelibs import lazy as lz


# %%
# Création dossier destination
repertoire_destination = r"D:\OneDrive\Documents\_TEST_\_NEW_DESTINATION_"
lz.mkdir(repertoire_destination, make_scaffolding=False)

# %%
# Déplacement simple de fichier standard, sans renommage
lz.move(r"\\wsl$\Ubuntu-20.04\root\.zsh_history", repertoire_destination)  # chemin réseau...

# %%
# Déplacement simple de fichier standard, avec renommage
lz.move(r"D:\OneDrive\Documents\_TEST_\_éèçàoöôîïêëùûü;.txt", repertoire_destination + "\\nouveau_nom.txt")

# %%
# Déplacement simple de répertoire standard, sans renommage
lz.move(r"D:\OneDrive\Documents\_TEST_\__R2D2-LOGS__", repertoire_destination)

# %%
# Déplacement simple de répertoire standard, avec renommage
lz.move(r"D:\OneDrive\Documents\_TEST_\__R2D2-LOGS__", repertoire_destination + "\\__R2D2__")

# %%
# Déplacement via mode modèle
lz.move(r"D:\OneDrive\Documents\_TEST_\*.sas*", repertoire_destination)  # modèle avec extension
# ou
lz.move(r"D:\OneDrive\Documents\_TEST_\*2020-11-11*", repertoire_destination)  # modèle sans extension, comprenant la chaîne "2020-11-11" dans le nom

# %%
# Déplacement groupé dans un dossier
lz.move((
    r"D:\OneDrive\Documents\_TEST_\*.sas*",  # avec schéma
    r"D:\OneDrive\Documents\_TEST_\2020-11-11.jpg",
    r"D:\OneDrive\Documents\_TEST_\__R2D2-LOGS__"  # dossier...
), repertoire_destination)

# %%
# Déplacement groupé d'une liste de fichiers dans une autre liste de fichiers (fonctionnement 1-1, i.e. même nombre de fichiers en entrée et en sortie, traitée de manière itérative)
lz.move((
    r"D:\OneDrive\Documents\_TEST_\*.sas*",  # avec schéma
    r"D:\OneDrive\Documents\_TEST_\2020-11-11.jpg",
    r"D:\OneDrive\Documents\_TEST_\__R2D2-LOGS__",  # dossier...
), (
    repertoire_destination,  # sans renommage
    repertoire_destination + "\\2020-11-11_NOUVEAU_NOM.jpg",  # avec renommage
    repertoire_destination + "\\__R2D2-NEW__",  # avec renommage
))


# %%
########################################################################################################################
# NOTES ################################################################################################################
# Comme sous Unix, move peut être utilisé pour renomer un fichier (chemin source = chemin cible)
########################################################################################################################
lz.move(r"D:\OneDrive\Documents\_TEST_\_éèçàoöôîïêëùûü;.txt", r"D:\OneDrive\Documents\_TEST_\NOUVEAU_NOM.txt")
