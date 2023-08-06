# archive.py
from corelibs import lazy as lz, tools as to


archive = to.Archive()
# Compression via un fichier de configuration YAML
exit_code = archive.zip(yaml_file=r"D:/OneDrive//\\//Documents\_TEST_\TEST.yaml")  # pas beau, mais on peut rentrer ce que l'on veut...

# Compression manuelle
exit_code = archive.zip(
    archive_name=r"D:/OneDrive/Documents\_TEST_\MON_ARCHIVE_" + lz.get_timestamp(),
    files_2_zip=(
        #  fichiers présents à la racine de l'archive (i.e. "D:/OneDrive/Documents\_TEST_")
        "1-01 Act One Questo Mar Rosso.m4a",
        "_éèçàoöôîïêëùûü;.txt",
        # fichier à un emplacement spécifique, ici "D:\OneDrive\Documents\_TEST_\A zip"
        r"D:\OneDrive\Documents\_TEST_\A zip\A zip - Copie"
    )
)

# stress test sur un fichier des établissements d'open data gouv.fr
# taille fichier : 29 928 195 lignes, pour un poids total de 4.88 Go
archive.zip(
    archive_name=r"D:\OneDrive\Desktop\StockEtablissement_utf8\StockEtablissement_utf8" + lz.get_timestamp(),
    files_2_zip=r"D:\OneDrive\Desktop\StockEtablissement_utf8\StockEtablissement_utf8.csv"
)
