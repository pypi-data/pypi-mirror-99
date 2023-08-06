# is_file_exists.py
# %%
from corelibs import lazy as lz


def test(file_test):
    if lz.is_file_exists(file_test):
        print("Le fichier \"{file_test}\" existe".format(file_test=file_test))
    else:
        print("Le fichier \"{file_test}\" n'existe pas".format(file_test=file_test))


file = r"D:\OneDrive\Documents\_TEST_"
test(file)

file = r"D:\OneDrive\Documents\_TEST_\__LOGS__\Fichier.txt"
test(file)

# %%
file = r"D:\OneDrive\Documents\_TEST_"
if lz.is_file_exists(file, is_dir=True):
    print("Le fichier \"{file}\" existe et est un répertoire".format(file=file))

# %%
file = r"D:\OneDrive\Documents\_TEST_\Fichier.txt"
if lz.is_file_exists(file):
    print("Le fichier \"{file}\" existe".format(file=file))

# %%
file = r"D:\OneDrive\Documents\_TEST_\Fichier.txt"
if not lz.is_file_exists(file, is_dir=True):
    print("Le fichier \"{file}\" n'est pas un répertoire".format(file=file))
