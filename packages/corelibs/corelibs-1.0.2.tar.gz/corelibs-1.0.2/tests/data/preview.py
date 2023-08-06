# preview.py
# %%
import pandas as pd

from corelibs import data

# %%  # prévisualisation standard à partir d'un fichier plat
# %%time
data.preview(
    r"D:\OneDrive\Desktop\StockEtablissement_utf8\StockEtablissement_utf8_tail_preview.tsv",
    separator="\t",
)
# 32s pour lire et afficher 1 048 576 de lignes
# 6min 27s pour lire et afficher 10 000 000 de lignes


# %%  # prévisualisation à partir d'un dataframe pandas
# %%time
df = pd.read_csv(
    r"D:\OneDrive\Desktop\StockEtablissement_utf8\StockEtablissement_utf8_tail_preview.tsv",
    sep="\t",
    dtype=str,
    engine="python",
    index_col=False
).fillna("")
data.preview(df)  # 1min 26s pour lire 1 048 576 de lignes
