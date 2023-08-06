# scan_dir.py
# %%
from corelibs import tools

# scan initial
tools.scan_dir(r"D:\OneDrive\Documents\_TEST_\__LOGS__ - Copie", duplicated_files_indicator=True)

# affichage sans recalcul (si cache existe)
tools.scan_dir(r"D:\OneDrive\Documents\_TEST_\__LOGS__ - Copie", skip_pre_scan=True, render="Excel")

# scan delta
# à partir de maintenant, le dossier "D:\OneDrive\Documents\_TEST_\__LOGS__ - Copie" existe en cache et seuls les deltas
# détectés seront calculés...
tools.scan_dir(r"D:\OneDrive\Documents\_TEST_\__LOGS__ - Copie", duplicated_files_indicator=True)
