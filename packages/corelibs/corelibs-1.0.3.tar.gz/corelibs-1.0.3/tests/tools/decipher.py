# decipher.py
# %%
from corelibs import tools, lazy as lz

cle_secrete = "Clé secrète de la morkitu! • 28Nov2013KT"

# %%
# déchiffrement chaine de caractères
message = """
import corelibs

dict = {"msg": "Hello Kim", "from": "papa"}
print("message encapsulé chiffré", "•"*31, dict, dict["msg"], corelibs)

corelibs.lazy.merge_dictionaries(dict, {"from": "papa ❤ =}"})
"""

message_chiffre = tools.cipher(message, cle_secrete)

message_dechiffre = tools.decipher(message_chiffre, cle_secrete)
print(message_dechiffre)
# affiche
# import corelibs
#
# dict = {"msg": "Hello Kim", "from": "papa"}
# print("message encapsulé chiffré", "•"*31, dict, dict["msg"], corelibs)
#
# corelibs.lazy.merge_dictionaries(dict, {"from": "papa ❤ =}"})

# %%
# exécution dynamique de la chaîne déchiffrée
exec(message_dechiffre)  # affichera le print chiffré => message encapsulé chiffré ••••••••••••••••••••••••••••••• {'msg': 'Hello Kim', 'from': 'papa'} Hello Kim <module 'corelibs' from 'D:\\OneDrive\\Documents\\[PYTHON_PROJECTS]\\corelibs\\corelibs\\__init__.py'>

print("dictionnaire défini dans la chaine déchiffrée : ", dict)  # dictionnaire défini dans la chaine déchiffrée :  {'msg': 'Hello Kim', 'from': 'papa ❤ =}'}
# note :
# le dictionnaire initiale est {"msg": "Hello Kim", "from": "papa"}
# mais la valeur a été écrasée par l'instruction corelibs.lazy.merge_dictionaries(dict, {"from": "papa ❤ =}"})
# ce qui donne bien
# dictionnaire défini dans la chaine déchiffrée :  {'msg': 'Hello Kim', 'from': 'papa ❤ =}'}


# %%
# déchiffrement fichier .clk
tools.decipher(r"D:\OneDrive\Documents\_TEST_\Chiffrements\hello.py.clk", cle_secrete)

# %%
# exécution du fichier déchiffré 1ère version
lz.add_dir_path_2_project(r"D:\OneDrive\Documents\_TEST_\Chiffrements")
import hello  # charge le module hello.py déchiffré
print("*"*31, hello.dict)  # affichera ******************************* {'msg': 'Hello Kim', 'from': 'papa ❤ =}'}

# %%
# ou si les chemins sont bien définis, 2ème version
exec(open(r"D:\OneDrive\Documents\_TEST_\Chiffrements\hello.py", encoding="utf-8").read())
import hello as lo  # charge le module hello.py déchiffré
print("•"*31, lo.dict)  # affichera ••••••••••••••••••••••••••••••• {'msg': 'Hello Kim', 'from': 'papa ❤ =}'}
# attention, la 2ème version fonctionne car dans le programme hello.py, il y a une instruction sys.path.append(...)
