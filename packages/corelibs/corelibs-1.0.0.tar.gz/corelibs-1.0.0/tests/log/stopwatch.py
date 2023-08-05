# stopwatch.py
from corelibs import log


# Instanciation log
cl = log.TermColorLog(output_2_log_file=False)

# Instanciation Chronomètre
sw = log.StopWatch(cl)


# Ajout décorateur timing() pour calculer le temps d'exécution de la fonction `ma_fonction()`
@log.timing()
# Cumuler décorateur status_bar() pour afficher la barre de statut
@log.status_bar()
def ma_fonction(nb):
    for _ in range(nb):
        pass


ma_fonction(200000000)
ma_fonction(200000000)

duration = sw.stop()  # ici nous avons les infos sur la durée totale d'exécution...
cl.info(duration)
