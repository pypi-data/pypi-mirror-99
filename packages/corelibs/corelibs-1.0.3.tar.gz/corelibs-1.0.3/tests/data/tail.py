# tail.py
# %%
from corelibs import data, log


# stress test sur un fichier des établissements d'open data gouv.fr
# taille fichier : 29 928 195 lignes, pour un poids total de 4.88 Go
@log.timing()
@log.status_bar()
def stress_test():
    return data.tail(
        r"D:\OneDrive\Desktop\StockEtablissement_utf8\StockEtablissement_utf8.tsv",
        chunk=1048576  # Excel > 2007
    )


preview_path = stress_test()  # Durée exécution : 00:00:03.23 pour extraire 1048576 de lignes sur les 30 millions de lignes du fichier sources
