# copy.py
# %%
from corelibs import lazy as lz


# %%
# Création dossier destination
repertoire_destination = r"D:\OneDrive\Documents\_TEST_\_COPY_DESTINATION_"
lz.mkdir(repertoire_destination, make_scaffolding=False)

# %%
# Copie simple de fichier standard, sans renommage
lz.copy(r"\\wsl$\Ubuntu-20.04\root\.zsh_history", repertoire_destination)  # chemin réseau...

# %%
# Copie simple de fichier standard, avec renommage
lz.copy(r"D:\OneDrive\Documents\_TEST_\_éèçàoöôîïêëùûü;.txt", repertoire_destination + "\\nouveau_nom.txt")

# %%
# Copie simple de répertoire standard, sans renommage
lz.copy(r"D:\OneDrive\Documents\_TEST_\__R2D2-LOGS__", repertoire_destination + "\\__R2D2-LOGS__")  # IMPORTANT!!! remettre le même nom de dossier destination, autrement, la copie se fera au niveau du répertoire parent

# %%
# Copie simple de répertoire standard, avec renommage
lz.copy(r"D:\OneDrive\Documents\_TEST_\__R2D2-LOGS__", repertoire_destination + "\\__R2D2__")

# %%
# Copie via mode modèle
lz.copy(r"D:\OneDrive\Documents\_TEST_\*.sas*", repertoire_destination)  # modèle avec extension
# ou
lz.copy(r"D:\OneDrive\Documents\_TEST_\*2020-11-11*", repertoire_destination)  # modèle sans extension, comprenant la chaîne "2020-11-11" dans le nom

# %%
# Copie groupée dans un dossier
lz.copy((
    r"D:\OneDrive\Documents\_TEST_\*.sas*",  # avec schéma
    r"D:\OneDrive\Documents\_TEST_\2020-11-11.jpg",
    r"D:\OneDrive\Documents\_TEST_\__R2D2-LOGS__"  # dossier...
), repertoire_destination)

# %%
# Copie groupée d'une liste de fichiers dans une autre liste de fichiers (fonctionnement 1-1, i.e. même nombre de fichiers en entrée et en sortie, traitée de manière itérative)
lz.copy((
    r"D:\OneDrive\Documents\_TEST_\*.sas*",  # avec schéma
    r"D:\OneDrive\Documents\_TEST_\2020-11-11.jpg",
    r"D:\OneDrive\Documents\_TEST_\__R2D2-LOGS__",  # dossier...
), (
    repertoire_destination,  # sans renommage
    repertoire_destination + "\\2020-11-11_NOUVEAU_NOM.jpg",  # avec renommage
    repertoire_destination + "\\__R2D2-NEW__",  # avec renommage
))
