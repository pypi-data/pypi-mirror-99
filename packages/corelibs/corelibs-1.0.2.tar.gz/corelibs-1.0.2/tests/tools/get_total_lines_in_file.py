# get_total_lines_in_file.py
from corelibs import tools as to, log

print(
    "Total lignes lues :",
    to.get_total_lines_in_file(r"\\wsl$\Ubuntu-20.04\root\.zsh_history")
)  # affiche Total lignes lues : 46

print(
    "Total lignes lues :",
    to.get_total_lines_in_file(r"D:\OneDrive\Documents\_TEST_\SAS\Librairie_SAS\00_LIB_Macros_Communes.sas")
)  # affiche Total lignes lues : 4060


# stress test sur un fichier des établissements d'open data gouv.fr
# taille fichier : 29 928 195 lignes, pour un poids total de 4.88 Go
@log.timing()
@log.status_bar()
def stress_test():
    print(
        "Total lignes lues :",
        to.get_total_lines_in_file(r"D:\OneDrive\Desktop\StockEtablissement_utf8\StockEtablissement_utf8.tsv")
    )


stress_test()  # Durée exécution : 00:00:12.07
# Total lignes lues : 29928195
