# cipher.py
# %%
from corelibs import tools

cle_secrete = "Clé secrète de la morkitu! • 28Nov2013KT"

# %%
# chiffrement chaine de caractères
message = """
import corelibs

dict = {"msg": "Hello Kim", "from": "papa"}
print("message encapsulé chiffré", "•"*31, dict, dict["msg"], corelibs)

corelibs.lazy.merge_dictionaries(dict, {"from": "papa ❤ =}"})
"""

message_chiffre = tools.cipher(message, cle_secrete)
print(message_chiffre)
# affiche le binaire suivant
# b'x\xda\x1d\xc1k\xb3B@\x00\x00\xd0_\xd4\x8c\xc7\xb6\xf4Q\x96\xc8s\xc3j}1j\xf3\x0c[\xa4\xf8\xf5w\xe6\x9e\xd3\x11H\xe9
# \x1a\xf2B^[\xd2\xab`/:v[i\xc7\xfa\xa5k\xffN\x9a\xe7\xf5\x1c\x8eF\x8ca\rygH\xcf\xeb\xb2\x9b\x0e\xef\xf1\xeb"\xeew;U
# \x16\xc06\x98\xc2\xfeJ\xb2\xdfY\xaemu\x8aZL\x16U\xb6H\xcb\x16\x81IL\xc9\xe9\xef\xc3\x15\xf7\xed\xc4~"R\xd39$\xd5\x92
# \xa5j|/\xa5\xa1>\x0b\x10m\xac\x8d\x18*(\x1f\xb0\xe3Z\x82(\x9a\xa5\x05f\x1b\xb0\x8b\x0e2\x06\xcbtRB\xd0\x9c"\xdex\xda.
# \xd9?\xbe\xa8#\xe64\xadh\x9e\x0f\x83\x96OpX\xd7\xb2\x07\x85\\>nR\x83\xa5\xd3\xc9\xafW\x9a\xe6\xa6b]\x9a1\xd1W-\x86\xe6
# \x83\xf7\x98\xf6r\xf6Z\x19\xf3j/\xe7\xe0H\xa2\x98\\}\x0c`E\x140\xe2\xa6\x15P1\xc8\xe0\xc6\xaa0\xe0\xf3R$\xa3\xad\xc7
# m&\xd9x\x94\x04\x1a\xddC\x8b\xebN\xea"\xa5\x1a\xc3\\4\xdfKl\x14\xb7\xef>\x82\x8b\xfa\xc6;oN\xf0V\x9dq\xaf\x0f\x98l
# \xf1\xf0L\xca\x80er0YA\x80\x8c\xe4\xf79:\x8b\x81^n\x8e\x94\xc8\xf0\xda?\xb9,}\xc7'



# %%
# chiffrement fichier hello.py ayant comme contenu :
# import sys
#
# sys.path.append(r"D:\OneDrive\Documents\[PYTHON_PROJECTS]\corelibs")
#
# import corelibs
#
# dict = {"msg": "Hello Kim", "from": "papa"}
# print("message encapsulé chiffré", "•"*31, dict, dict["msg"], corelibs)
#
# corelibs.lazy.merge_dictionaries(dict, {"from": "papa ❤ =}"})

tools.cipher(r"D:\OneDrive\Documents\_TEST_\Chiffrements\hello.py", cle_secrete)
# résultat fichier binaire hello.py.clk
# 78da 1dc1 d7b2 4340 0000 d02f 32a3 2578
# d4a2 5bbb ba17 838d 1021 ca92 c8d7 df99
# 7b8e 248d 549c 5626 57fe 185a 7cda 4495
# 9e40 9695 6e51 e57f 86ec a79d 6467 218c
# edbc a60f 1435 8cb3 3fb9 a00a f5fc 9bc7
# db39 8aa2 d57c b6f3 048f c37b 247b 4aa6
# caaf 2395 f5ea 6860 f05a 7cb2 340d e201
# 91bd 2ec3 0dc4 fac8 8869 feba 6514 adcd
# eb1b 6a32 d117 804f 4e85 7a85 55f2 3528
# 67be 7b2d 6865 0e99 a477 3f38 4d0a dd36
# 33c2 ac0d 9f2f a4f7 5bb3 9892 aeba 46ef
# 8463 d374 f629 988e f8f0 8b67 3c13 e4be
# 32a3 5751 0d0b adf6 224f 99dd eb56 7a74
# b8fa b627 16e7 ea76 dc46 e8a3 93c6 1b5f
# 840f c752 5f7e b107 0ebf beee da06 58c4
# 29f0 80f5 e03c 0ac1 d2af b842 c58e 2e7d
# 27a7 1cbf 2b9e 2318 7cce 2a31 389c 5037
# 0719 013e b392 66d1 0f84 27d6 9312 4ac1
# c3f4 a0ac 6953 41e3 f6e5 c5ce 220c e331
# 58f9 1249 46df abbf 1b63 3db9 9a2f e470
# d835 e31b 4c65 d802 fffd 4bbe 356d e5ec
# e74e 0667 ab58 dfcc fc7e 9d93 df8f 7c38
# 4bde bb49 a305 0c47 1c04 b895 3621 72cc
# ea92 2c3a 7f0f 07dd 0b02 b7ed 6f2f 5abc
# 4001 d516 0876 a296 62d8 81e5 d298 8a30
# 0f50 974f a7dc 9db2 bd45 cd1f c744 a9e7

