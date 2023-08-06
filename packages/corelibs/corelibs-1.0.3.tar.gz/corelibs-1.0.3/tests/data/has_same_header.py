# has_same_header.py
# %%
from corelibs import data

# %%
# Test OK
_ = data.has_same_header(
    r"C:\Users\miki\AppData\Local\Temp\tmpa1trgjyy_corelibs",
    r"C:\Users\miki\AppData\Local\Temp\tmpzhoxgdc2_corelibs"
)
print(f"Résultat : {_.result}", f" - Infos : {_.cause}")
# Résultat : True  - Infos : {'hype': 'o(^  ^ o) Tout est OK, YEAH!!! (o ^  ^)o'}


# %%
# Test KO 1ère possibilité
_ = data.has_same_header(
    r"C:\Users\miki\AppData\Local\Temp\tmpa1trgjyy_corelibs",
    r"C:\Users\miki\AppData\Local\Temp\tmpzhoxgdc2_corelibs"
)
print(f"Résultat : {_.result}", f" - Infos : {_.cause}")
# Résultat : False  - Infos : {
#    'cause': 'Différence format',
#    'columns difference': ['owner', 'Created Time', 'Finger Print'],
#    'file': [
#        '#',
#        'File Type',
#        'File Name',
#        'Technical ID',
#        'owner',
#        'Last Access',
#        'Last Modification',
#        'Created Time',
#        'Bytes',
#        'KiloBytes',
#        'MegaBytes',
#        'GigaBytes',
#        'Finger Print'
#    ],
#    'file 2 compare': [
#        '#',
#        'File Type',
#        'File Name',
#        'Technical ID',
#        'Owner',
#        'Last Access',
#        'Last Modification',
#        'OS Time',
#        'Bytes',
#        'KiloBytes',
#        'MegaBytes',
#        'GigaBytes',
#        'Fingerprint'
#    ]
# }


# %%
# Test KO 2ème possibilité
_ = data.has_same_header(
    r"C:\Users\miki\AppData\Local\Temp\tmpa1trgjyy_corelibs",
    r"C:\Users\miki\AppData\Local\Temp\tmpzhoxgdc2_corelibs"
)
print(f"Résultat : {_.result}", f" - Infos : {_.cause}")
# Résultat : False  - Infos : {'cause': 'Longueur différente', 'file': '14 colonnes', 'file 2 compare': '13 colonnes'}
