# statusbars.py
# %%
import random

from corelibs import log

# /!\ ATTENTION /!\
#     Jupyter Notebook n'étant pas un terminal, il ne se passera rien... =}
# Instanciations
sb = log.StatusBars()
cl = log.ColorLog(output_2_log_file=False, log_level=10)

log_methods = {  # dictionnaire avec les adresses des différentes méthode présentes dans TermColorLog
    0: {
        "status": "success",
        "callback": cl.debug
    },
    1: {
        "status": "success",
        "callback": cl.info
    },
    2: {
        "status": "warning",
        "callback": cl.warning
    },
    3: {
        "status": "error",
        "callback": cl.error
    },
    4: {
        "status": "error",
        "callback": cl.critical
    }
}

message = "Hello, simple log dynamique avec un niveau aléatoire"


# 1ère étape
total_iteration = 53
desc_1 = sb.init_sub_process(color="cyan")  # initialisation d'un sous process pour afficher les infos de la boucle
pb_1 = sb.init_progress_bar(total=total_iteration, desc="1ère Étape :")  # initialisation barre de progression

for i in range(total_iteration):
    _ = random.choice(range(5))
    log_methods[_]["callback"](f"{i} - {message}")  # ici les logs ne sont pas rattachées donc l'affichage se fait en défilement normal dans le terminal...
    duree_etape = sb.update_progress_bar(
        pb_1,
        status_text=f"{(i + 1): >{2}}/{total_iteration} - Reste {(total_iteration - i - 1): >{2}}".rjust(26, " "),
        status=log_methods[_]["status"]
    )
    sb.update_sub_process(desc_1, f"{i} - {message}")

cl.info(duree_etape)  # affichage durée 1ère étape


# 2ème étape
desc_2 = sb.init_sub_process(color="green", justify="left")  # initialisation sous process 2ème étape
sb.update_sub_process(desc_2, f"Coucou ceci est ma 2ème Étape et elle est affichée dans un sous process fils... "
                              "Après la fin du (ou des) process qui me précède(nt) =}")


# 3ème étape en erreur
factor = 2
pb_2 = sb.init_progress_bar(total=total_iteration * factor, color="magenta", desc="3ème Étape :")

for i in range(total_iteration * factor):
    duree_3_etape = sb.update_progress_bar(pb_2,
                                           f"{(i + 1): >{3}}/{total_iteration * factor}".rjust(23, " "),
                                           "error")

cl.info(duree_3_etape)  # affichage durée 3ème étape


# 4ème étape en warning
factor = 3
pb_3 = sb.init_progress_bar(total=total_iteration * factor, color="magenta", desc="4ème Étape :")

for i in range(total_iteration * factor):
    duree_4_etape = sb.update_progress_bar(pb_3,
                                           f"{(i + 1): >{3}}/{total_iteration * factor}".rjust(23, " "),
                                           "warning")

cl.info(duree_4_etape)  # affichage durée 4ème étape


# 5ème étape normale avec changement de couleur par défaut
factor = 4
pb_4 = sb.init_progress_bar(total=total_iteration * factor, color="magenta", desc="5ème Étape :")

for i in range(total_iteration * factor):
    duree_5_etape = sb.update_progress_bar(pb_4,
                                           f"{(i + 1): >{3}}/{total_iteration * factor}".rjust(23, " ")
                                           )

cl.info(duree_5_etape)  # affichage durée 4ème étape


duree_totale = sb.terminate()
cl.info(duree_totale)  # durée totale de statusbars.py
