# statusbars_decorator.py
from corelibs import log


# Ajout décorateur status_bar() pour afficher des informations dans le terminal
# /!\ ATTENTION /!\
#     Jupyter Notebook n'étant pas un terminal, il ne se passera rien... =}
@log.status_bar("Ma barre de statut figée")
def ma_fonction_avec_barre_statut(nb):
    for _ in range(nb):
        print("{_} : les informations défilent au dessus de la 1ère barre...".format(_="{:0>3}".format(_)))


ma_fonction_avec_barre_statut(3)
print(log.decorator_return["duration"]["status_bar"])  # durée de l'étape status_bar
print("\n")


@log.status_bar()  # Sans titre...
def ma_deuxieme_fonction_de_la_morkitu_avec_decorateur():
    for _ in range(3):
        print(f"{_: >3} : les informations défilent au dessus de la 2ème barre...")


ma_deuxieme_fonction_de_la_morkitu_avec_decorateur()
print(log.decorator_return["duration"]["status_bar"])  # durée de la seconde étape (car écrasement)


# Arrêt et fonctionnement normal à partir de maintenant...
print("\n")
for _ in range(3):
    print("hé "*((_+1)*2) + "... =}")
