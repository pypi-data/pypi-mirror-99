# Exemple instructions pour utiliser le fichier config utilisateur de manière globale et locale (portée au sein du programme actif)

import user_config as uc

print(uc.MA_CONSTANTE_UTILISATEUR)  # affichera "Hello! =}"

# écrasement des constantes utilisateurs, avec une portée locale
uc.MA_CONSTANTE_UTILISATEUR = "Hello Kim ❤ =}"
print(uc.MA_CONSTANTE_UTILISATEUR)  # affiche "Hello Kim ❤ =}"

# idem pour les constantes corelibs (attention à lire les documentations officielles tiers pour ne pas tout casser...)
DEFAULT_MIN_BYTE_SIZE_FORMAT = {  # définition locale
    "octet": {"min_size": 0},
    "Ko": {"min_size": 1},
    "Mo": {"min_size": 1},
    "Go": {"min_size": 1},
    "To": {"min_size": 1}
}
print(DEFAULT_MIN_BYTE_SIZE_FORMAT)  # affiche {'octet': {'min_size': 0}, 'Ko': {'min_size': 1}, 'Mo': {'min_size': 1}, 'Go': {'min_size': 1}, 'To': {'min_size': 1}}

print(uc.DEFAULT_MIN_BYTE_SIZE_FORMAT)  # {'octet': {'min_size': 0}, 'Ko': {'min_size': 1}, 'Mo': {'min_size': 1}, 'Go': {'min_size': 1}, 'To': {'min_size': 0.5}}

# Le fichier user_config.py se trouve dans le dossier caché nommé ".corelibs" se trouvant à :
#   • %HOMEPATH%/.corelibs sous Windows
#   • ~/.corelibs sous Linux
#
# accessible manuellement ou via l'interface graphique Corelibs avec la commande terminale
#    $ corelibs
#
# ce fichier de configuration est modifiable à discrétion avec en particulier, la possibilité de rajouter des variables utilisateurs propres globalement vu par n'importe quel programme qui en fait l'import
