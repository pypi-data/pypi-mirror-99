# strip_non_printable_file.py
# %%
from corelibs import cleanse as cls, log


# %%
# nettoyage fichier des caractères non imprimables
@log.timing()
@log.status_bar()
def stress_test():
    cls.strip_non_printable_file(
        r"D:\OneDrive\Documents\_TEST_\StockEtablissement_utf8_A3T.csv",
        time_stamp=None,
        strip_non_breaking_space=True
    )


# stress_test()
# non printable seul :
# Durée exécution : 00:01:36.11 pour 30 millions de lignes
# Durée exécution : 00:04:48.07 pour 90 millions de lignes
# non printable + non breaking space
# Durée exécution : 00:02:25.80 pour 30 millions de lignes
# Durée exécution : 00:07:11.64 pour 90 millions de lignes

