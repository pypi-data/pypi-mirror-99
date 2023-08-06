# get_fingerprint.py
# %%
from corelibs import tools as to, log


# %%
# Même empreinte = Même fichier (quelque soit son nom, sa date de modif, propriétaire etc...)
# fichier 1
filename = r"D:\OneDrive\Documents\_TEST_\2020-11-11.jpg"
print(to.get_file_properties(filename))  # FileProperties(st_mode=33206, st_ino=11540474045256220, st_dev=3199390331, st_nlink=1, st_uid='Invités', st_gid=0, st_size='96.26 Ko', st_atime='14/11/2020 22:12:45', st_mtime='11/11/2020 22:10:46', st_ctime='11/11/2020 22:10:39')
print(to.get_fingerprint(filename))  # b6bbd28aebe109adda9bc16a8f838a5043d7980968a37a5d48f890f7fb4d89dc

# %%
# fichier 1 copié et les propriétés affichent bien une différence
copy_filename = r"D:\OneDrive\Documents\_TEST_\2020-11-11 - Copie.jpg"
print(to.get_file_properties(copy_filename))  # FileProperties(st_mode=33206, st_ino=19984723346576074, st_dev=3199390331, st_nlink=1, st_uid='miche', st_gid=0, st_size='96.26 Ko', st_atime='14/11/2020 22:06:59', st_mtime='11/11/2020 22:10:46', st_ctime='14/11/2020 21:56:29')
print(to.get_fingerprint(copy_filename))  # b6bbd28aebe109adda9bc16a8f838a5043d7980968a37a5d48f890f7fb4d89dc

# %%
# algorithme disponible pour le hashage
print(to.get_fingerprint(filename, algorithm="blake2b"))  # 0a0ba79c2e6535b256c110bf823ea21b32fa7d1fdbeb16374ec3437269ad1f01e4dfb6a72b0dab929807737a331ac6a8988ebb6943d4ef10e5650128f4ac0ef0
print(to.get_fingerprint(filename, algorithm="blake2s"))  # 0c6b739b821f0fb560e5545445e3a4c600ffc171e506ff307be0528f9d274b56
print(to.get_fingerprint(filename, algorithm="md5"))  # 62383435cc0519bad598cc51783c5d47
print(to.get_fingerprint(filename, algorithm="sha1"))  # f50a38a0c0952f96ae98aa54da7929bfb463f8dd
print(to.get_fingerprint(filename, algorithm="sha224"))  # c176d2d98a4f8563762ce3863efb942dbb9c496b4bee89a0374e42fa
print(to.get_fingerprint(filename, algorithm="sha256"))  # b6bbd28aebe109adda9bc16a8f838a5043d7980968a37a5d48f890f7fb4d89dc
print(to.get_fingerprint(filename, algorithm="sha384"))  # c839a0c58ef1ba3a7577de093f3d0e3746600b7b28fa08881f62aa7d4871220b9373ebdc620704e84c965d972cf887fb
print(to.get_fingerprint(filename, algorithm="sha512"))  # 39e72a89e167aa86f998e61763b0b43619cb6347118dd5f6713f830688b7e16cc8b006e8027a3bf1b0c260d24a76a13e7e233c3ab179f4e76865215a1d4007a4
print(to.get_fingerprint(filename, algorithm="sha3_256"))  # e0009df152ee03665a3f26bc434d143873f2abc900e85e4e45d85608d6fd1787
print(to.get_fingerprint(filename, algorithm="sha3_224"))  # 0f6ab25b4406ed8f98decae73375451286166d2e3d01095c15530069
print(to.get_fingerprint(filename, algorithm="sha3_384"))  # 3d3d00f27d1663273d80cd9d4f1f55cf2f185d12f7c4387a77e91daae5ff179ecf8692c975b2f86b92010de5202ce32a
print(to.get_fingerprint(filename, algorithm="sha3_512"))  # ec208132962c717b6f92105ff04a2af93e2195fca22babc17b2b5ddb784b05c913b86cf09dd37e4ec699e342056051f61f400f290e7b8d5f4e8756d08d6e87ff

# %%
# Empreinte d'une chaine de caractère
str_2_hash = "Hello Kim!"
print(
    "L'empreinte SH256 de \"{str_2_hash}\" est \"{str_hashed}\""
    .format(
        str_2_hash=str_2_hash,
        str_hashed=to.get_fingerprint(str_2_hash)
    )
)  # L'empreinte SH256 de "Hello Kim!" est "8c9affc6a8329ea9c8a87cfe989565c21b24136dc57ccf9407aeefbcac87f97a"

# %%
str_2_hash = "/!\\ ATTENTION /!\\"  # doit être forcé comme chaine de caractères pour l'évaluation car contient des caractères \ et /
print(
    "L'empreinte SH256 de \"{str_2_hash}\" est \"{str_hashed}\""
    .format(
        str_2_hash=str_2_hash,
        str_hashed=to.get_fingerprint(str_2_hash, eval_as_string=True)
    )
)  # L'empreinte SH256 de "/!\ ATTENTION /!\" est "20f2328fcc5d513e330f5badadac2c0bd2685d8a21ce49daf7690cc6e783ff65"


# %%
# stress test sur un fichier des établissements d'open data gouv.fr
# taille fichier : 29 928 195 lignes, pour un poids total de 4.88 Go
@log.timing()
@log.status_bar()
def stress_test():
    str_2_hash = r"D:\OneDrive\Desktop\StockEtablissement_utf8\StockEtablissement_utf8.csv"
    print(
        "L'empreinte SH256 de \"{str_2_hash}\" est \"{str_hashed}\""
        .format(
            str_2_hash=str_2_hash,
            str_hashed=to.get_fingerprint(str_2_hash)
        )
    )


stress_test()  # Durée exécution : 00:00:12.07
# L'empreinte SH256 de "D:\OneDrive\Desktop\StockEtablissement_utf8\StockEtablissement_utf8.csv" est "072c0f2dc85bd326197318546da4331e6c900c39302145fc7013532aaedf4af8"
