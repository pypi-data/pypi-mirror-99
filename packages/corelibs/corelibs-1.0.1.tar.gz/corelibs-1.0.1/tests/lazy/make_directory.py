# mkdir.py
# %%
from corelibs import lazy as lz


# %%
# création par défaut où se trouve l'emplacement du programme `mkdir.py`
lz.mkdir()

# %%
# création d'un répertoire standard avec les parents si n'existe pas, sans la structure "modèle"
lz.mkdir(
    location=r"D:\OneDrive\Documents\_TEST_\PARENTS\INEXISTANTS\DOSSIER_STANDARD",
    make_scaffolding=False,
    verbose=True
)

# %%
# création avec 4 dossiers par défaut de la structure "modèle"
# à l'emplacement "D:\OneDrive\Documents\_TEST_\PARENTS\INEXISTANTS\DOSSIER_STANDARD"
lz.mkdir(location=r"D:\OneDrive\Documents\_TEST_\PARENTS\DOSSIERS_SCAFFOLD", verbose=True)

# %%
# création personnalisée avec un seul dossier "__MY-LOGS__"
# à l'emplacement "D:\OneDrive\Documents\_TEST_\PARENTS\INEXISTANTS\DOSSIER_STANDARD"
lz.mkdir(
    location=r"D:\OneDrive\Documents\_TEST_\PARENTS\INEXISTANTS\DOSSIER_STANDARD",
    dir_scaffolding={
        "input": {  # dossier contenant toutes les données "entrées"
            "name": "__R2 D2__",
            "make": False
        },
        "output": {  # dossier contenant toutes les données "sorties"
            "name": "__MY_OUTPUTS__",
            "make": False
        },
        "logs": {  # dossier contenant toutes les sorties "logs"
            "name": "__MY-LOGS__",
            "make": True
        },
        "docs": {  # dossier contenant toutes les documentations/specs liées au projet
            "name": "__DOCS__",
            "make": False
        },
    },
    verbose=True
)

# %%
# création d'une liste de répertoires standards (sans les répertoires modèles) ayant pour structure
# ...DOSSIER_T42020
#    |_Dossier A
#    |_Dossier B
#      |_SDossier B1
#      |_SDossier B2
lz.mkdir(
    location=(
        r"D:\OneDrive\Documents\_TEST_\DOSSIER_T42020\Dossier A",
        r"D:\OneDrive\Documents\_TEST_\DOSSIER_T42020\Dossier B\SDossier B1",
        r"D:\OneDrive\Documents\_TEST_\DOSSIER_T42020\Dossier B\SDossier B2",
    ),
    make_scaffolding=False,
    verbose=True
)  # dans la mesure où les dossiers parents sont créés si n'existent pas, une factorisation est possible...

# %%
# création d'une liste de répertoires standards (avec les répertoires modèles personnalisés) ayant pour structure
# ...DOSSIER_T12021
#    |_Dossier A
#      |__MY_INPUTS__
#      |__MY_OUTPUTS__
#      |__MY_LOGS__
#    |_Dossier B
#      |_SDossier B1
#        |_ +3 DOSSIERS MODELES PERSONNALISÉS
#      |_SDossier B2
#        |_ +3 DOSSIERS MODELES PERSONNALISÉS
lz.mkdir(
    location=(
        r"D:\OneDrive\Documents\_TEST_\DOSSIER_T12021\Dossier A",
        r"D:\OneDrive\Documents\_TEST_\DOSSIER_T12021\Dossier B\SDossier B1",
        r"D:\OneDrive\Documents\_TEST_\DOSSIER_T12021\Dossier B\SDossier B2",
    ),
    dir_scaffolding={
        "input": {  # dossier contenant toutes les données "entrées"
            "name": "__MY_INPUTS__",
            "make": True
        },
        "output": {  # dossier contenant toutes les données "sorties"
            "name": "__MY_OUTPUTS__",
            "make": True
        },
        "logs": {  # dossier contenant toutes les sorties "logs"
            "name": "__MY_LOGS__",
            "make": True
        },
        "docs": {  # dossier contenant toutes les documentations/specs liées au projet
            "name": "__DOCS__",
            "make": False
        },
    },
    verbose=True
)  # cette construction n'a aucun intérêt fonctionnel mais cela est possible...
