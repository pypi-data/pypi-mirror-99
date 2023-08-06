# split_file.py
# %%
import pandas as pd
from corelibs import data, log, tools


# %%
# stress test sur un fichier des établissements d'open data gouv.fr
# taille fichier : 29 928 195 lignes, pour un poids total de 4.88 Go
# découpage par tranche de 10 millions de lignes avec les entêtes (par défaut)
@log.timing()
@log.status_bar()
def stress_test():
    data.split_file(r"D:\OneDrive\Desktop\StockEtablissement_utf8\StockEtablissement_utf8.tsv", chunk=10000000)


stress_test()  # Durée exécution : 00:02:02.60


# %%
# %%time
# vérifications par scan modèles
wcl = tools.get_total_lines_in_folder(
    dir_2_scan=r"D:\OneDrive\Desktop\StockEtablissement_utf8",
    files_pattern="*_part_*.tsv"
)
print(wcl)  # Wcl(total_files=3, total_lines=29928199) - Durée exécution : 12.2s
# il y a un delta de 6 lignes avec la comparaison via pandas ci-dessous (ce delta est normal)


# %%
# vérifications entêtes
for i in range(3):
    data.head(
        r"D:\OneDrive\Desktop\StockEtablissement_utf8\StockEtablissement_utf8_part_{i}.tsv".format(i=i),
        chunk=10,
        start_file=True
    )


# %%
# vérification pandas
@log.timing()
@log.status_bar()
def verif_pandas():
    for i in range(3):
        df = pd.read_csv(
            r"D:\OneDrive\Desktop\StockEtablissement_utf8\StockEtablissement_utf8_part_{i}.tsv".format(i=i),
            sep="\t",
            dtype=str,
            usecols=["siren"],
            engine="python"
        )
        print(f"total lignes {i}", len(df))
        del df


verif_pandas()  # Durée exécution : 00:28:23.79
# total lignes 0 10000000
# total lignes 1 10000000
# total lignes 2 9928193


# %%
# découpage par tranche de 10 millions de lignes sans les entêtes
@log.timing()
@log.status_bar()
def stress_test():
    data.split_file(
        r"D:\OneDrive\Desktop\StockEtablissement_utf8\StockEtablissement_utf8.tsv",
        chunk=10000000,
        skip_header=True
    )


stress_test()  # Durée exécution : 00:02:25.85


# %%
# %%time
# découpage arbitraire, à partir d'une position pour un nombre de lignes données
data.split_file(
    r"D:\OneDrive\Desktop\StockEtablissement_utf8\StockEtablissement_utf8.tsv",
    start=10000000,
    chunk=100,
    suffix="_xtr_"
)  # Durée exécution 1min
