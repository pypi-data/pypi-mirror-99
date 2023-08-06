# get_file_extension.py
# %%
from corelibs import lazy as lz

# %%
stem, suffix = lz.get_file_extension(r"\\file\path\file name.tar.gz")
print(f"Le nom du fichier sans extension est \"{stem}\"")
# Le nom du fichier sans extension est "file name"

# %%
print(f"Le nom de l'extension par défaut est \"{suffix}\"")
# Le nom de l'extension par défaut est ".tar.gz"

# %%
stem, suffix = lz.get_file_extension(r"\\file\path\file name.tar.gz", split_extensions=True)
print("Le nom du fichier sans extension est \"{stem}\"".format(stem=stem))
# Le nom du fichier sans extension est "file name"

# %%
print("Le tableau des extensions est \"{suffix}\"".format(suffix=suffix))
# Le tableau des extensions est "['.tar', '.gz']"

# %%
file_properties = lz.get_file_extension(r"\\file\path\file name.tar.gz", split_extensions=True)
print("Le nom du fichier sans extension est \"{stem}\"".format(stem=file_properties.file_name))
# Le nom du fichier sans extension est "file name"

# %%
print("Le tableau des extensions est \"{suffix}\"".format(suffix=file_properties.file_extension))
# Le tableau des extensions est "['.tar', '.gz']"
