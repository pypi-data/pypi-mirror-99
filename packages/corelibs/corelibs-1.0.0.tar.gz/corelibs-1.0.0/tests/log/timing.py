# timing.py
from corelibs import log
from numba import njit


cl = log.ColorLog()  # 1. créer une instance de ColorLog()


# Ajout décorateur timing() pour calculer le temps d'exécution de la fonction `ma_premiere_fonction_optimisee()`
@log.timing()
@njit()
def ma_premiere_fonction_optimisee(nb):
    total = 0
    for _ in range(nb):
        total = total + 1

    return total


cl.info(
    "le total est "
    + "{0:,}".format(
        ma_premiere_fonction_optimisee(30000000000)
    ).replace(",", " ")
)


# Faire sortir le résultat du décorateur timing() dans un fichier log spécifique, ici, l'objet `cl`
@log.timing(cl)
def ma_deuxieme_fonction_non_optimisee(nb):  # définition d'une 2ème fonction...
    total = 0
    for _ in range(nb):
        total = total + 1

    return total


cl.info(
    "le total est "
    + "{0:,}".format(
        ma_deuxieme_fonction_non_optimisee(30000000000)
    ).replace(",", " ")
)
