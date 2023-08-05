# get_caller_line_number.py
# %%
from corelibs import config, lazy as lz


# appel croisé correct...
def info(profondeur_appel=1):
    return lz.get_caller_line_number(profondeur_appel)


print(f"Le numéro de la ligne du module appelant est {info(profondeur_appel=1)}")

print(f"Le numéro de la ligne du module appelant est {info(profondeur_appel=2)}")

# appel direct incorrect...
lz.get_caller_line_number()
