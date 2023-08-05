# is_siret.py
# %%
from corelibs import cleanse as cls

# vérification sur 1 siret correctement formaté
res = cls.is_siret(("33243395200022"))
print(res)  # affichera un booléen, ici True

# vérication sur le même siret avec un retour en chaîne de cractères
res = cls.is_siret("33243395200022", check_only=False)
print(res)  # affichera 33243395200022

# extraction du même siret validé
res = cls.is_siret("33243395200022", check_only=False, extraction=True)
print(res)  # affichera Siret(siren='332433952', nic='00022', siret='33243395200022')
print(f"Le siret {res.siret} est composé du siren {res.siren} et du nic {res.nic}")  # affichera Le siret 33243395200022 est composé du siren 332433952 et du nic 00022

# vérification sur une liste de sirets
sirets = (
    "33243395200022",  # siret sur 14 OK
    "33243395200021",  # siret sur 14 KO
    "00032517500057",  # siret sur 14 OK
    "32517500024",  # siret sur 11 OK
    "32517501024",  # siret sur 11 KO
    "35600000049837",  # cas particulier La Poste
    "35600000052135",  # cas particulier La Poste
)

print(cls.is_siret(sirets))  # affichera [True, False, True, True, False, True, True]
print(cls.is_siret(sirets, check_only=False))  # affichera la version corrigée ['33243395200022', '', '00032517500057', '00032517500024', '', '35600000049837', '35600000052135']
print(cls.is_siret(sirets, check_only=False, new_siret="99999999999999"))  # affichera ['33243395200022', '99999999999999', '00032517500057', '00032517500024', '99999999999999', '35600000049837', '35600000052135']


# extractions sur la même liste avec une annotation quand le siren est celui de La Poste
is_laposte = lambda _: "(Établissement La Poste)" if _ == "356000000" else ""
for s in cls.is_siret(sirets, check_only=False, new_siret="---------------", extraction=True):
    print(f"Le siret {s.siret} est composé du siren {s.siren} et du nic {s.nic} {is_laposte(s.siren)}")
# affichera
# Le siret 33243395200022 est composé du siren 332433952 et du nic 00022
# Le siret --------------- est composé du siren --------- et du nic -----
# Le siret 00032517500057 est composé du siren 000325175 et du nic 00057
# Le siret 00032517500024 est composé du siren 000325175 et du nic 00024
# Le siret --------------- est composé du siren --------- et du nic -----
# Le siret 35600000049837 est composé du siren 356000000 et du nic 49837 (Établissement La Poste)
# Le siret 35600000052135 est composé du siren 356000000 et du nic 52135 (Établissement La Poste)
