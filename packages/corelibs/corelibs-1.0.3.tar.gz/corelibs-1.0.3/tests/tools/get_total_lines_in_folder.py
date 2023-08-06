# get_total_lines_in_folder.py
# %%
from corelibs import tools as to

# %%
# Scan standard...
wcl = to.get_total_lines_in_folder(r"\\wsl$\Ubuntu-20.04\root", "*history")
print(wcl)  # affiche un objet Wcl(total_files=3, total_lines=431)

# %%
########################################################################################################################

# Scan avec multiple schéma et exclusion répertoires et/ou fichiers
# étalon *.sas
wcl = to.get_total_lines_in_folder(
    dir_2_scan=r"D:\OneDrive\Documents\_TEST_\SAS_ADD",
    files_pattern="*.sas"
)
print(wcl)  # affiche Wcl(total_files=95, total_lines=20943)
#
# étalon *.log
wcl = to.get_total_lines_in_folder(
    dir_2_scan=r"D:\OneDrive\Documents\_TEST_\SAS_ADD",
    files_pattern="*.log"
)
print(wcl)  # affiche Wcl(total_files=3, total_lines=587)
#
# scan multiple
wcl = to.get_total_lines_in_folder(
    dir_2_scan=r"D:\OneDrive\Documents\_TEST_\SAS_ADD",
    files_pattern=("*.sas", "*.log")
)
print(wcl)  # affiche Wcl(total_files=98, total_lines=21530) qui est bien le total des 2 sous ensembles étalons =)

# %%
########################################################################################################################

# Scan multiple avec exclusions
# étalon 1
wcl = to.get_total_lines_in_folder(
    dir_2_scan=r"D:\OneDrive\Documents\_TEST_\SAS_ADD\_QUAL_",
    files_pattern=("*.sas", "*.log")
)
print(wcl)  # Wcl(total_files=93, total_lines=20869)

# %%
# étalon 2
wcl = to.get_total_lines_in_folder(
    dir_2_scan=r"D:\OneDrive\Documents\_TEST_\SAS_ADD\[ _BACKUP_POINT_0 ]",
    files_pattern=("*.sas", "*.log")
)
print(wcl)  # Wcl(total_files=4, total_lines=654)

# %%
# étalon 3
print(
    "Total lignes lues :",
    to.get_total_lines_in_file(r"D:\OneDrive\Documents\_TEST_\SAS_ADD\hello.sas")
)  # Total lignes lues : 7

# %%
# étalon 4
wcl = to.get_total_lines_in_folder(
    dir_2_scan=r"D:\OneDrive\Documents\_TEST_\SAS_ADD",
    files_pattern=("*.sas", "*.log")
)
print(wcl)  # Wcl(total_files=98, total_lines=21530)
# 98 = 93 + 4 + 1
# 21530 = 20869 + 654 + 7

# %%
# exclusions étalon
wcl = to.get_total_lines_in_folder(
    dir_2_scan=r"D:\OneDrive\Documents\_TEST_\SAS_ADD",
    files_pattern=("*.sas", "*.log"),
    to_exclude=r"*_BACKUP_POINT_0*"
)
print(wcl)  # Wcl(total_files=94, total_lines=20876)
# 94 = 98 - 4
# 20876 = 21530 - 654

# %%
# exclusions finales
wcl = to.get_total_lines_in_folder(
    dir_2_scan=r"D:\OneDrive\Documents\_TEST_\SAS_ADD",
    files_pattern=("*.sas", "*.log"),
    to_exclude=(r"*_BACKUP_POINT_0*", r"*SAS_ADD\hello.sas")
)
print(wcl)  # Wcl(total_files=93, total_lines=20869)
# 93 = 98 - 4 - 1
# 20869 = 21530 - 654 - 7

# le compte y est! =}
