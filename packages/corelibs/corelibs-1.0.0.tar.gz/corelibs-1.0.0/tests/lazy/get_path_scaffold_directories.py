# get_path_scaffold_directories.py
# %%
from corelibs import config, lazy as lz

root_path = r"D:\OneDrive\Documents\_TEST_\PARENTS\INEXISTANTS"

print(lz.get_path_scaffold_directories(root_path))  # retourne None

lz.mkdir(
    root_path,
    dir_scaffolding={
        "input": {  # dossier contenant toutes les données "entrées"
            "name": "__R2 D2__",
            "make": True
        },
        "output": {  # dossier contenant toutes les données "sorties"
            "name": "__MY_OUTPUTS__",
            "make": True
        },
        "logs": {  # dossier contenant toutes les sorties "logs"
            "name": "__MY-LOGS__",
            "make": True
        },
        "docs": {  # dossier contenant toutes les documentations/specs liées au projet
            "name": "__DOCUMENTATIONS__",
            "make": True
        },
    },
    verbose=False
)

scaffold_dir_path = lz.get_path_scaffold_directories(root_path)
print(scaffold_dir_path)

# récupréer les chemins des docs
print(scaffold_dir_path.docs)

# récupréer les chemins des inputs
print(scaffold_dir_path.input)

# récupréer les chemins des outputs
print(scaffold_dir_path.output)

# récupréer les chemins des logs
print(scaffold_dir_path.logs)

# %%
# si le définition est écrasée, alors le get_path_scaffold_directories() va tenter de retrouver les nouvelles
# informations, par exemple ci-dessous, le nouveau nom du répertoire "input" s'appellera "__R2 D2__" et ainsi de suite
config.DEFAULT_DIR_SCAFFOLDING = {
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
}

print(lz.get_path_scaffold_directories(root_path))  # affichera
# ScaffoldDir(input='D:\\OneDrive\\Documents\\_TEST_\\PARENTS\\INEXISTANTS\\__R2 D2__', output='D:\\OneDrive\\Documents\\_TEST_\\PARENTS\\INEXISTANTS\\__MY_OUTPUTS__', logs='D:\\OneDrive\\Documents\\_TEST_\\PARENTS\\INEXISTANTS\\__MY-LOGS__', docs='')
# "docs" est vide car nous cherchons un nom "__DOCS__" alors que nous avons créé "__DOCUMENTATIONS__"
