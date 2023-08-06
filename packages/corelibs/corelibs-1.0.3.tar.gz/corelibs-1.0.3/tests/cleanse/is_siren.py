# is_siren.py
# %%
from corelibs import cleanse as cls

# vérification sur 1 siren correctement formaté
res = cls.is_siren("325175")
print(res)  # affichera un booléen, ici True

# vérication sur le même siren avec un retour en chaîne de cractères
res = cls.is_siren("325175", check_only=False)
print(res)  # affichera "000325175" qui est la version consolidée, avec le bon formatage pour respecter le format du siren sur 9 caractères

# vérification sur une liste de sirens
sirens = (
    "732829320",  # siren sur 9 OK
    "303663981",  # siren sur 9 KO
    "60801487",  # siren sur 8 OK
    "5450093",  # siren sur 7 OK
    "325175",  # siren sur 6 OK
)

print(cls.is_siren(sirens))  # affichera [True, False, True, True, True]
print(cls.is_siren(sirens, check_only=False))  # affichera la version corrigée ['732829320', '', '060801487', '005450093', '000325175'] <= le 2ème siren qui est faux est par défaut remplacé par une chaîne vide
print(cls.is_siren(sirens, check_only=False, new_siren="999999999"))  # affichera ['732829320', '999999999', '060801487', '005450093', '000325175'], au lieu de ['732829320', '', '060801487', '005450093', '000325175'] qui est le comportement par défaut
