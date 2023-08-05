# get_locale_tab.py
# %%
from corelibs import lazy as lz


# %%
# Affichage sous une forme lisible pour un humain
# Afficher la liste des codes langues disponibles par défaut (détection de l'OS)
lz.get_locale_tab()

# Forcer l'affichage pour toutes les plateformes disponibles
lz.get_locale_tab(platform_os="all")

# Afficher la liste pour Windows
lz.get_locale_tab(platform_os="Windows")

# Afficher la liste pour Unix
lz.get_locale_tab(platform_os="Unix")


# %%
# Récupération de la liste dans une variable
locale_tab_list = lz.get_locale_tab(platform_os="all", yaml_dumping=False)
print(locale_tab_list["Windows"]["fr"])  # affichera français (France)
