# unarchive.py
from corelibs import tools as to


archive = to.Archive()
# Décompression via un fichier de configuration YAML
exit_code = archive.unzip(yaml_file=r"D:\OneDrive\Documents\_TEST_\TEST.yaml")

# Décompression manuelle
exit_code = archive.unzip(
    archive_name=r"D:\OneDrive\Documents\_TEST_\\/TEST.28112013.7z",  # pas beau, mais on peut rentrer ce que l'on veut
    files_2_unzip=(
        #  fichiers décompressés à la racine de l'archive (i.e. "D:\OneDrive\Documents\_TEST_\\/")
        r"D:\OneDrive\Desktop\1-01 Act One Questo Mar Rosso.m4a",
        "_éèçàoöôîïêëùûü;.txt",
        # fichier décompressé à un emplacement spécifique, ici "D:\OneDrive\Documents\_TEST_\A zip"
        r"D:\OneDrive\Documents\_TEST_\dossier compressé"
    )
)
