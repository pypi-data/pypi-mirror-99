# progress_bar_decorator_version.py
import time

from corelibs import log

cl = log.ColorLog(output_2_log_file=False)


# Ajout décorateur status_bar() pour afficher des informations dans le terminal
# /!\ ATTENTION /!\
#     Jupyter Notebook n'étant pas un terminal, il ne se passera rien... =}
@log.progress_bar(title="Ma barre d'état décorée", desc="Ma première étape", color="magenta", desc_padding=64)
def ma_fonction_avec_barre_statut(nb):
    time.sleep(3)


ma_fonction_avec_barre_statut(3)
cl.info("Durée 1ère étape " + str(log.decorator_return["duration"]["progress_bar"]))
print("\n")


@log.progress_bar(color="cyan", desc_padding=64)  # Sans titre...
def ma_deuxieme_fonction_de_la_morkitu_avec_decorateur():
    for _ in range(3):
        cl.info(f"{_: >3} : les informations défilent au dessus de la 2ème barre...")
    time.sleep(5)


ma_deuxieme_fonction_de_la_morkitu_avec_decorateur()
print("\n")
cl.info("Durée 2ème étape " + str(log.decorator_return["duration"]["progress_bar"]))


@log.progress_bar(terminate=True, color="white", desc_padding=64)  # Ne pas oublier le terminate pour relâcher la barre d'état!!!
def ma_derniere_fonction_avec_terminate():
    time.sleep(7)


ma_derniere_fonction_avec_terminate()
cl.info("Durée dernière étape " + str(log.decorator_return["duration"]["progress_bar"]))
cl.info("Durée Totale : " + log.decorator_return["duration"]["total"].duration)


# Arrêt et fonctionnement normal à partir de maintenant...
print("\n")
for _ in range(3):
    print("hé "*((_+1)*2) + "... =}")
