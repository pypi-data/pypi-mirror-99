# rename.py
# %%
from corelibs import lazy as lz


# %%
# Renommage simple
lz.rename(
    path=r"D:\OneDrive\Documents\_TEST_\_TEST_RENOMMAGE_",
    pattern=r"_cars.sas7bdat",
    replace=r"nouveau_RS_cars.sas7bdat",
    debug=False
)  # équivalent à lz.move(r"D:\OneDrive\Documents\_TEST_\_TEST_RENOMMAGE_\_cars.sas7bdat", r"D:\OneDrive\Documents\_TEST_\_TEST_RENOMMAGE_\nouveau_RS_cars.sas7bdat")

# %%
# Renommage simple par modèle
lz.rename(
    r"D:\OneDrive\Documents\_TEST_\_TEST_RENOMMAGE_\__R2D2-LOGS__",
    r"(termcolorlog)_(\d{4})(\d{2})(\d{2})_(\d{2})(\d{2})(\d{2})(.LOG)",  # Schéma source avec 8 sous groupes, (termcolorlog)_(\d{4})(\d{2})(\d{2})_(\d{2})(\d{2})(\d{2})(.LOG)
    r"\1_\4\3\2_\5\6.log",  # Schéma cible décrivant "termcolorlog_JJMMAAAA_HHMM.log"
    debug=False
)
# résultats :
# termcolorlog_20201208_222147.LOG -> termcolorlog_08122020_2221.log
# termcolorlog_20201208_222351.LOG -> termcolorlog_08122020_2223.log
# termcolorlog_20201208_222452.LOG -> termcolorlog_08122020_2224.log
# termcolorlog_20201208_222839.LOG -> termcolorlog_08122020_2228.log
# termcolorlog_20201208_223739.LOG -> termcolorlog_08122020_2237.log
# termcolorlog_20201208_223834.LOG -> termcolorlog_08122020_2238.log
# termcolorlog_20201208_223920.LOG -> termcolorlog_08122020_2239.log
# termcolorlog_20201208_224058.LOG -> termcolorlog_08122020_2240.log
# termcolorlog_20201208_224116.LOG -> termcolorlog_08122020_2241.log
# termcolorlog_20201208_224144.LOG -> termcolorlog_08122020_2241.log

# %%
# Renommage simple par modèle avec transformation 1er exemple
lz.rename(
    r"D:\OneDrive\Documents\_TEST_\_TEST_RENOMMAGE_\__R2D2-LOGS__\__R2D2-LOGS__",
    r"(termcolorlog)_(\d{4})(\d{2})(\d{2})_(\d{2})(\d{2})(\d{2})(.LOG)",  # Schéma source avec 8 sous groupes, (termcolorlog)_(\d{4})(\d{2})(\d{2})_(\d{2})(\d{2})(\d{2})(.LOG)
    r"\1_\4\3\2_\5\6\8",  # Schéma cible décrivant "termcolorlog_JJMMAAAA_HHMM(.LOG)"
    transform=r"\U1\T8",  # Upper sur le premier groupe et Title sur le dernier groupe
    debug=False
)
# résultats :
# termcolorlog_20201208_222147.LOG -> TERMCOLORLOG_08122020_2221.Log
# termcolorlog_20201208_222351.LOG -> TERMCOLORLOG_08122020_2223.Log
# termcolorlog_20201208_222452.LOG -> TERMCOLORLOG_08122020_2224.Log
# termcolorlog_20201208_222839.LOG -> TERMCOLORLOG_08122020_2228.Log
# termcolorlog_20201208_223739.LOG -> TERMCOLORLOG_08122020_2237.Log
# termcolorlog_20201208_223834.LOG -> TERMCOLORLOG_08122020_2238.Log
# termcolorlog_20201208_223920.LOG -> TERMCOLORLOG_08122020_2239.Log
# termcolorlog_20201208_224058.LOG -> TERMCOLORLOG_08122020_2240.Log
# termcolorlog_20201208_224116.LOG -> TERMCOLORLOG_08122020_2241.Log
# termcolorlog_20201208_224144.LOG -> TERMCOLORLOG_08122020_2241.Log


# %%
# Renommage simple par modèle avec transformation 2ème exemple
lz.rename(
    r"D:\OneDrive\Documents\_TEST_\_TEST_RENOMMAGE_",
    r"_(cars)(.*)(.sas7bdat)",  # Schéma source avec 3 sous groupes
    r"NOUVEAU_NOM_\1_AVEC_TRANSFO\2.nouvelle_extension",  # Schéma cible décrivant "NOUVEAU_NOM_(cars)_AVEC_TRANSFO(.*).nouvelle_extension"
    transform=r"\S1\T2",  # Swapcase sur le premier groupe et Title sur le 2ème groupe
    debug=False
)
# résultats :
# _CaRS.sas7bdat -> NOUVEAU_NOM_cArs_AVEC_TRANSFO.nouvelle_extension
# _cars_asia.sas7bdat -> NOUVEAU_NOM_CARS_AVEC_TRANSFO_Asia.nouvelle_extension


# %%
# Renommage simple par modèle avec transformation et séquences sans padding 1er exemple
lz.rename(
    r"D:\OneDrive\Documents\_TEST_\_TEST_RENOMMAGE_\__R2D2__",
    r"(termcolorlog)_(\d{4})(\d{2})(\d{2})_(\d{2})(\d{2})(\d{2})(.LOG)",  # Schéma source avec 8 sous groupes, (termcolorlog)_(\d{4})(\d{2})(\d{2})_(\d{2})(\d{2})(\d{2})(.LOG)
    r"\1_\4\3\2_%{0}_\8",  # Schéma cible décrivant "TERMCOLORLOG_JJMMAAAA_%SEQUENCE_(.LOG)"
    transform=r"\U1\T8",  # Upper sur le premier groupe et Title sur le dernier groupe
    debug=False,
    verbose=True
)
# résultats :
# termcolorlog_20201208_222147.LOG -> TERMCOLORLOG_08122020_1_.Log
# termcolorlog_20201208_222351.LOG -> TERMCOLORLOG_08122020_2_.Log
# termcolorlog_20201208_222452.LOG -> TERMCOLORLOG_08122020_3_.Log
# termcolorlog_20201208_222839.LOG -> TERMCOLORLOG_08122020_4_.Log
# termcolorlog_20201208_223739.LOG -> TERMCOLORLOG_08122020_5_.Log
# termcolorlog_20201208_223834.LOG -> TERMCOLORLOG_08122020_6_.Log
# termcolorlog_20201208_223920.LOG -> TERMCOLORLOG_08122020_7_.Log
# termcolorlog_20201208_224058.LOG -> TERMCOLORLOG_08122020_8_.Log
# termcolorlog_20201208_224116.LOG -> TERMCOLORLOG_08122020_9_.Log
# termcolorlog_20201208_224144.LOG -> TERMCOLORLOG_08122020_10_.Log

# %%
# Renommage simple par modèle avec transformation et séquences avec padding 2ème exemple
lz.rename(
    r"D:\OneDrive\Documents\_TEST_\_TEST_RENOMMAGE_\__R2D2__\__R2D2-LOGS__",
    r"(termcolorlog)_(\d{4})(\d{2})(\d{2})_(\d{2})(\d{2})(\d{2})(.LOG)",  # Schéma source avec 8 sous groupes, (termcolorlog)_(\d{4})(\d{2})(\d{2})_(\d{2})(\d{2})(\d{2})(.LOG)
    r"_%{10}_\1_\4\3\2_%{0}_\8",  # Schéma cible décrivant "_%SEQUENCE_PADDING10_TERMCOLORLOG_JJMMAAAA_%SEQUENCE_PADDING_(.LOG)"
    transform=r"\U1\T8",  # Upper sur le premier groupe et Title sur le dernier groupe
    debug=False
)
# résultats :
# termcolorlog_20201208_182147.LOG -> _0000000001_TERMCOLORLOG_08122020_0000000001_.Log
# termcolorlog_20201208_182351.LOG -> _0000000002_TERMCOLORLOG_08122020_0000000002_.Log
# termcolorlog_20201208_182452.LOG -> _0000000003_TERMCOLORLOG_08122020_0000000003_.Log
# termcolorlog_20201208_182839.LOG -> _0000000004_TERMCOLORLOG_08122020_0000000004_.Log
# termcolorlog_20201208_183739.LOG -> _0000000005_TERMCOLORLOG_08122020_0000000005_.Log
# termcolorlog_20201208_183834.LOG -> _0000000006_TERMCOLORLOG_08122020_0000000006_.Log
# termcolorlog_20201208_183920.LOG -> _0000000007_TERMCOLORLOG_08122020_0000000007_.Log
# termcolorlog_20201208_184058.LOG -> _0000000008_TERMCOLORLOG_08122020_0000000008_.Log
# termcolorlog_20201208_184116.LOG -> _0000000009_TERMCOLORLOG_08122020_0000000009_.Log
# termcolorlog_20201208_184144.LOG -> _0000000010_TERMCOLORLOG_08122020_0000000010_.Log
