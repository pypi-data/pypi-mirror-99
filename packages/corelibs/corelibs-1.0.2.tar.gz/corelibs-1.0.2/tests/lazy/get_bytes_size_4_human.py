# get_bytes_size_4_human.py
# %%
from corelibs import lazy as lz


# %%
byte_size = lz.get_bytes_size_formats(0)
print(lz.get_bytes_size_4_human(byte_size))
# affiche par défaut la valeur 0 octet

# %%
byte_size = lz.get_bytes_size_formats(153800565)
print(lz.get_bytes_size_4_human(byte_size))
# affiche par défaut la valeur 146.68 Mo

# %%
byte_size = lz.get_bytes_size_formats(1739886085)
print(lz.get_bytes_size_4_human(byte_size))
# affiche par défaut la valeur 1.62 Go

# %%
# affichage forcé dans une unité de mesure souhaitée
print(lz.get_bytes_size_4_human(byte_size, default_format="Mo"))  # affiche 1 659.28 Mo

# %%
# affichage forcé en Mo, mais sans l'unité de mesure
print(lz.get_bytes_size_4_human(byte_size, size_unit=False, default_format="Mo"))  # affiche 1659.28
