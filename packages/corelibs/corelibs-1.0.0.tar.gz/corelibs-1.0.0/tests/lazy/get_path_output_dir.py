# get_path_output_dir.py
from corelibs import config, lazy as lz

root_path = r"D:\OneDrive\Documents\_TEST_\PARENTS\INEXISTANTS"

print(lz.get_path_output_dir(root_path))  # retourne rien

lz.mkdir(
    root_path,
    dir_scaffolding={
        "input": {  # dossier contenant toutes les données "entrées"
            "name": "__R2 D2__",
            "make": False
        },
        "output": {  # dossier contenant toutes les données "sorties"
            "name": "__MY_OUTPUTS__",
            "make": True
        },
        "logs": {  # dossier contenant toutes les sorties "logs"
            "name": "__MY-LOGS__",
            "make": False
        },
        "docs": {  # dossier contenant toutes les documentations/specs liées au projet
            "name": "__DOCS__",
            "make": False
        },
    },
    verbose=False
)
print(lz.get_path_output_dir(root_path))  # retourne "D:\OneDrive\Documents\_TEST_\PARENTS\INEXISTANTS\__MY_OUTPUTS__"
