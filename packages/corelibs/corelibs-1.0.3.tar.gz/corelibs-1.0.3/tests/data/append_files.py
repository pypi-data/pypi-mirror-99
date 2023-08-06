# append_files.py
# %%
from corelibs import data, log, tools


# %%
# stress test sur un fichier des établissements d'open data gouv.fr
# taille fichier : 29 928 195 lignes, pour un poids total de 4.88 Go
# concaténation 3 fois le fichier originale
@log.timing()
@log.status_bar()
def stress_test():
    data.append_files(
        source_dir_path=r"D:\OneDrive\Desktop\StockEtablissement_utf8",  # factorisation chemin fichiers sources
        files_2_append=(
            "StockEtablissement_utf8.csv",
            "StockEtablissement_utf8.tsv",
            "fichier_inexistant.toto",  # => lève une erreur, sans action et continue...
            r"D:\OneDrive\Documents\_TEST_\StockEtablissement_utf8.csv"  # fichier se trouvant à un autre emplacement
        ),
        out_file_path=r"D:\OneDrive\Documents\_TEST_\StockEtablissement_utf8_A3T.csv"
    )


stress_test()  # Durée exécution : 00:04:10.60


# %%
# Vérification poids fichier
print(tools.get_file_properties(r"D:\OneDrive\Documents\_TEST_\StockEtablissement_utf8_A3T.csv"))
# FileProperties(st_mode=33206, st_ino=3659174697355776, st_dev=3199390331, st_nlink=1, st_uid='miche', st_gid=0, st_size='14.65 Go', st_atime='20/01/2021 23:44:12', st_mtime='20/01/2021 23:44:12', st_ctime='20/01/2021 23:18:42')


# %%
# Vérification nb de lignes
@log.timing()
@log.status_bar()
def stress_test():
    print(
        tools.get_total_lines_in_file(
            r"D:\OneDrive\Documents\_TEST_\StockEtablissement_utf8_A3T.csv"
        )
    )


stress_test()  # Durée exécution : 00:02:40.59 pour lire et compter 89 784 581 de lignes


# %%
# %%time
print(tools.get_fingerprint(r"D:\OneDrive\Documents\_TEST_\StockEtablissement_utf8_A3T.csv"))
# 9ebe16404b9654fa790ed16ebcf5d4d6afd44ff62bb9a98a22533783dc0200f6 (2min 29s)


# %%
# nettoyage fichier, puisque la concaténation est faite sur des fichiers csv et tsv...
@log.timing()
@log.status_bar()
def stress_test():
    data.replace_in_file(
        path=r"D:\OneDrive\Documents\_TEST_\StockEtablissement_utf8_A3T.csv",
        pattern=b"\x09",  # <=> tab
        replace=b"\x2C",  # <=> ,
        ignore_errors=True
    )


stress_test()  # Durée exécution : 00:05:47.55 pour nettoyer 90 millions de lignes
