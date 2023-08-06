# Pour écraser et utiliser un config localement

from corelibs import config
import user_config as uc

print(uc.MA_CONSTANTE_UTILISATEUR)  # affichera "Hello! =}"

# écrasement local avec les constantes utilisateurs
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

print(config.DEFAULT_MIN_BYTE_SIZE_FORMAT)  # {'octet': {'min_size': 0}, 'Ko': {'min_size': 1}, 'Mo': {'min_size': 1}, 'Go': {'min_size': 1}, 'To': {'min_size': 0.5}}