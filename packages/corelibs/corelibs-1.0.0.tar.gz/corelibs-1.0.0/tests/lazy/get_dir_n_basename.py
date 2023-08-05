# get_dir_n_basename.py
# %%
from corelibs import lazy as lz


# %%
# chemin + fichier (si chemin seul, sera retourné alors le nom du dossier + le chemin amenant au dossier)
dir_n_basename = lz.get_dir_n_basename(r"C:\Users\M47624\corelibs\tests\lazy\get_dir_n_basename.py")
# récupération par index
print("Le chemin est \"{dir}\"".format(dir=dir_n_basename[0]))
print("Le fichier est \"{base}\"".format(base=dir_n_basename[1]))

# %%
# récupération par attributs
print("Le chemin est \"{dir}\"".format(dir=dir_n_basename.dir_path))
print("Le fichier est \"{base}\"".format(base=dir_n_basename.base_name))

# %%
# sortie "séparée" ou "déballée" (unpacked)
dir, base = lz.get_dir_n_basename(r"C:\Users\M47624\corelibs\tests\lazy\get_dir_n_basename.py")
print("Le chemin est \"{dir}\"".format(dir=dir))
print("Le fichier est \"{base}\"".format(base=base))
