# is_phone_number.py
# %%
from corelibs import cleanse as cls, log, config

config.DEFAULT_LOG_LEVEL = 10


# %%
# qualification par défaut, en n° français
liste_nationale = (
    "06 89 97.21-31",  # OK
    "06    89.97.21-32",  # OK
    "01.89.97.21.32",  # OK
    "01.89.97.21.320",  # KO
)

res = []
for n in liste_nationale:
    res.append(cls.is_phone_number(n))
print(res)  # affichera [True, True, True, False]


# %%
# qualifacation avec des n° au format international
liste_internationale = (
    "+3306 89 97.21-31",  # français OK
    "+3306 89 97.21-31 0",  # français KO
    "+4412 89.97.21-3------------------2",  # anglais OK
    "+4412 89.97.21-3------------------2 0",  # anglais KO
    "+1510 - 748 - 8230",  # américain OK
    "+1510 - 748 - 8230 - 0",  # américain KO
)
res = []
for n in liste_internationale:
    res.append(cls.is_phone_number(n))
print(res)  # affichera [True, False, True, False, True, False]


# %%
# normalisation et correction des n° de téléphone
res = []
for n in liste_internationale:
    res.append(cls.is_phone_number(n, check_only=False))
print(res)  # affichera ['+33 6 89 97 21 31', '', '+44 1289 972132', '', '+1 510-748-8230', '']


# %%
# extraction des n° de téléphone
def _():
    res = []
    for phone_number in liste_internationale:
        res.append(cls.is_phone_number(phone_number, check_only=False, extraction=True))

    return res


phones_number = _()
print(phones_number)  # affichera
# [
#   PhoneNumber(country_code=33, phone_number=689972131, national_number='06 89 97 21 31', international_number='+33 6 89 97 21 31', e164_number='+33689972131', given_number='+3306 89 97.21-31'),
#   PhoneNumber(country_code='', phone_number='', national_number='', international_number='', e164_number='', given_number='+3306 89 97.21-31 0'),
#   PhoneNumber(country_code=44, phone_number=1289972132, national_number='01289 972132', international_number='+44 1289 972132', e164_number='+441289972132', given_number='+4412 89.97.21-3------------------2'),
#   PhoneNumber(country_code='', phone_number='', national_number='', international_number='', e164_number='', given_number='+4412 89.97.21-3------------------2 0'),
#   PhoneNumber(country_code=1, phone_number=5107488230, national_number='(510) 748-8230', international_number='+1 510-748-8230', e164_number='+15107488230', given_number='+1510 - 748 - 8230'),
#   PhoneNumber(country_code='', phone_number='', national_number='', international_number='', e164_number='', given_number='+1510 - 748 - 8230 - 0')
# ]


# %%
# dumping pour une meilleure visualisation
@log.dict_dumping
def dump(tuple_2_dump):
    return tuple_2_dump


for phone in phones_number:
    dump(phone)  # affichage plus lisible pour notre regard, au format YAML (mode DEBUG seulement)
