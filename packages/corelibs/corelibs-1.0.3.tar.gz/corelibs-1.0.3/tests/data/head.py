# head.py
# %%
from corelibs import data, log


# stress test sur un fichier des établissements d'open data gouv.fr
# taille fichier : 29 928 195 lignes, pour un poids total de 4.88 Go
@log.timing()
@log.status_bar()
def stress_test():
    return data.head(r"D:\OneDrive\Desktop\StockEtablissement_utf8\StockEtablissement_utf8.csv", start_file=True)


preview_path = stress_test()  # Durée exécution : 00:00:00.58 pour récupérer 65K/30 millions de lignes


# %%
# prévisualisation en mode web...
data.preview(preview_path, separator=",")
