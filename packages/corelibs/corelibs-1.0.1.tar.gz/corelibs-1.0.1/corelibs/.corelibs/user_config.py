import logging as log
########################################################################################################################
# Bienvenue à...                                                                                                       #
#                                      ______                ___ __                                                    #
#                                     / ____/___  ________  / (_) /_  _____                                            #
#                                    / /   / __ \/ ___/ _ \/ / / __ \/ ___/                                            #
#                                   / /___/ /_/ / /  /  __/ / / /_/ (__  )                                             #
#                                   \____/\____/_/   \___/_/_/_.___/____/                              #################
#                                                                                                     # user_config.py #
########################################################################################################################


########################################################################################################################
# // * CONFIGURATION UTILISATEUR #######################################################################################
########################################################################################################################
# //? ici les nouvelles définitions/constantes utilisateur...
MA_CONSTANTE_UTILISATEUR = "Hello! =}"
########################################################################################################################
# /CONFIGURATION UTILISATEUR ###########################################################################################
########################################################################################################################


####################################
# DÉBUT CONFIGURATION CORELIBS... ###
########################################################################################################################
# // * CONFIGURATION INTERFACE UI ######################################################################################
########################################################################################################################
# //? Chemin pour le script Conda
# //? Windows 10: C:\Users\<your-username>\Anaconda3\
# //? macOS: /Users/<your-username>/anaconda3 for the shell install, ~/opt for the graphical install.
# //? Linux: /home/<your-username>/anaconda3
# //? cf. https://docs.anaconda.com/anaconda/user-guide/faq/ pour plus de détail
UI_CONDA_PATH = r"C:\ProgramData\Anaconda3\Scripts"

# //? Par défaut, le thème est aléatoire, pour connaitre le nom du thème affiché, mettre à Oui
UI_DISPLAY_THEME_NAME = False

# //? Nom du thème à afficher
UI_THEME_NAME = "Sandy Beach"  # None pour un affichage aléatoire parmi la liste des thèmes ci-dessous
# Nom thèmes disponibles :
# "Black" "Blue Mono" "Blue Purple" "Bright Colors" "Brown Blue" "Dark" "Dark 2" "Dark Amber" "Dark Black"
# "Dark Black 1" "Dark Blue" "Dark Blue 1" "Dark Blue 2" "Dark Blue 3" "Dark Blue 4" "Dark Blue 5" "Dark Blue 6"
# "Dark Blue 7" "Dark Blue 8" "Dark Blue 9" "Dark Blue 10" "Dark Blue 11" "Dark Blue 12" "Dark Blue 13" "Dark Blue 14"
# "Dark Blue 15" "Dark Blue 16" "Dark Blue 17" "Dark Brown" "Dark Brown 1" "Dark Brown 2" "Dark Brown 3" "Dark Brown 4"
# "Dark Brown 5" "Dark Brown 6" "Dark Brown 7" "Dark Green" "Dark Green 1" "Dark Green 2" "Dark Green 3" "Dark Green 4"
# "Dark Green 5" "Dark Green 6" "Dark Green 7" "Dark Grey" "Dark Grey 1" "Dark Grey 2" "Dark Grey 3" "Dark Grey 4"
# "Dark Grey 5" "Dark Grey 6" "Dark Grey 7" "Dark Grey 8" "Dark Grey 9" "Dark Grey 10" "Dark Grey 11" "Dark Grey 12"
# "Dark Grey 13" "Dark Grey 14" "Dark Purple" "Dark Purple 1" "Dark Purple 2" "Dark Purple 3" "Dark Purple 4"
# "Dark Purple 5" "Dark Purple 6" "Dark Purple 7" "Dark Red" "Dark Red 1" "Dark Red 2" "Dark Tan Blue" "Dark Teal"
# "Dark Teal 1" "Dark Teal 2" "Dark Teal 3" "Dark Teal 4" "Dark Teal 5" "Dark Teal 6" "Dark Teal 7" "Dark Teal 8"
# "Dark Teal 9" "Dark Teal 10" "Dark Teal 11" "Dark Teal 12" "Default" "Default 1" "Default No More Nagging" "Green"
# "Green Mono" "Green Tan" "Hot Dog Stand" "Kayak" "Light Blue" "Light Blue 1" "Light Blue 2" "Light Blue 3"
# "Light Blue 4" "Light Blue 5" "Light Blue 6" "Light Blue 7" "Light Brown" "Light Brown 1" "Light Brown 2"
# "Light Brown 3" "Light Brown 4" "Light Brown 5" "Light Brown 6" "Light Brown 7" "Light Brown 8" "Light Brown 9"
# "Light Brown 10" "Light Brown 11" "Light Brown 12" "Light Brown 13" "Light Gray 1" "Light Green" "Light Green 1"
# "Light Green 2" "Light Green 3" "Light Green 4" "Light Green 5" "Light Green 6" "Light Green 7" "Light Green 8"
# "Light Green 9" "Light Green 10" "Light Grey" "Light Grey 1" "Light Grey 2" "Light Grey 3" "Light Grey 4"
# "Light Grey 5" "Light Grey 6" "Light Purple" "Light Teal" "Light Yellow" "Material 1" "Material 2" "Neutral Blue"
# "Purple" "Python" "Reddit" "Reds" "Sandy Beach" "System Default" "System Default 1" "System Default For Real" "Tan"
# "Tan Blue" "Teal Mono" "Topanga"
########################################################################################################################
# /CONFIGURATION INTERFACE UI ##########################################################################################
########################################################################################################################

########################################################################################################################
# // * CONFIGURATION LOCALE ############################################################################################
########################################################################################################################
# //? buffer de lecture/écriture en nombres d'octets
DEFAULT_BYTE_CHUNK_SIZE = 1048576 * 64  # 1048576 bytes <=> 1024KB <=> 1MB

# //? buffer de prévisualisation/lecture/écriture en nombre de lignes
DEFAULT_BUFFER_CHUNK_SIZE = 65536  # <=> max lignes Excel < 2007, sinon 1048576 lignes

# //? encodage par défaut des fichiers
DEFAULT_ENCODING_FILE = "latin-1"  # //! Western Europe latin-1 pour les français, sinon choisir "utf-8" ou "ISO-8859-1"

# //? format français par défaut
DEFAULT_LOCALE_TIME = "fr"  # //! en pour l'anglais => voir corelibs.lazy.get_locale_tab() pour la liste complète

# //? code page encoding pour les retour terminal des appels commandes DOS
DEFAULT_DOS_CMD_CP_ENCODING = "cp850"  # cf. https://en.wikipedia.org/wiki/Code_page_850

# //? format des tailles avec leur valeur minimale pour l'affichage automatisé
DEFAULT_MIN_BYTE_SIZE_FORMAT = {
    "octet": {"min_size": 0},
    "Ko": {"min_size": 1},
    "Mo": {"min_size": 1},
    "Go": {"min_size": 1},
    "To": {"min_size": 0.5}
}
########################################################################################################################
# /CONFIGURATION LOCALE ################################################################################################
########################################################################################################################


########################################################################################################################
# // * CONFIGURATION PROJET ############################################################################################
########################################################################################################################
# //? nom structures modèles de répertoires par défaut
DEFAULT_DIR_SCAFFOLDING = {
    "input": {  # dossier contenant toutes les données "entrées"
        "name": "__INPUTS__",
        "make": True
    },
    "output": {  # dossier contenant toutes les données "sorties"
        "name": "__OUTPUTS__",
        "make": True
    },
    "logs": {  # dossier contenant toutes les sorties "logs"
        "name": "__LOGS__",
        "make": True
    },
    "docs": {  # dossier contenant toutes les documentations/specs liées au projet
        "name": "__DOCS__",
        "make": True
    },
}
########################################################################################################################
# /CONFIGURATION PROJET ################################################################################################
########################################################################################################################


########################################################################################################################
# // * CONFIGURATION LOG ###############################################################################################
########################################################################################################################
# //? forcer l'exécution des instructions suivantes même quand une erreur est levée (Attention à son emploi...)
DEFAULT_IGNORE_ERROR = False

# //? affichage détaillé de la pile d'exécution
DEFAULT_STACK_TRACE = False

# //? redirection de l'affichage détaillé de la pile d'exécution vers la log
DEFAULT_STACK_TRACE_2_FILE = False

# //? affichage détaillé de la pile d'exécution
# par défaut, le style de couleur sera :
# • "lightbg" si environnement Jupyter, sinon "darkbg2" si DEFAULT_STACK_TRACE_2_FILE est faux
# • "plaintext" si DEFAULT_STACK_TRACE_2_FILE est vrai
DEFAULT_STYLE_STACK_TRACE = "default"  # valeur possibles : plaintext, color, darkbg2 ou lightbg

# //? contexte du code source pour les affichage détaillés des logs
DEFAULT_CONTEXT_SOURCE_LINES = 3

# //? affichage informations en provenance du package corelibs
DEFAULT_VERBOSE = False

# //? nom fichier log par défaut dans le cas des entrées standards
DEFAULT_STDIN_LOGS_NAME = "__STDIN_"

# //? extension par défaut des fichiers logs
DEFAULT_LOGS_EXTENSION = ".log"

# //? niveau d"affichage des logs, valeurs possibles :
# * log.DEBUG <=> 10
# * log.INFO <=> 20 (valeur par défaut)
# * log.WARNING <=> 30
# * log.ERROR <=> 40
# * log.CRITICAL <=> 50
#
# //! pour désactiver une alerte, on augmente son niveau, par exemple WARNING (30)
# et dans ce cas, les alertes de niveau DEBUG et INFO seront ignorées.
DEFAULT_LOG_LEVEL = log.INFO  # ou 20

# //? le style par défaut des LOG affichées dans la sortie standard
DEFAULT_FIELD_STYLES = {
    "asctime": {"color": 242, "bright": True},
    "hostname": {"color": "magenta"},
    "username": {"color": "yellow"},
    "levelname": {"color": 242, "bright": True},
    "levelno": {"color": 242, "bright": True},
    "lineno": {"color": "white"},
    "process": {"color": "white"},
    "name": {"color": "blue"},
    "module": {"color": "blue"},
    "programname": {"color": "cyan"},
    "thread": {"color": "white"},
    "filename": {"color": "blue"},
    "funcName": {"color": "blue"},
}

# //? les couleurs par défaut selon le niveau
DEFAULT_LEVEL_STYLES = {
    "critical": {
        "color": 255,
        "background": "red",
    },
    "error": {"color": "red"},
    "warning": {"color": "yellow"},
    "debug": {"color": "green"},
    "info": {"color": "cyan"},
    "notice": {"color": "magenta"},
    "spam": {"color": "green"},
    "success": {"color": "green"},
    "verbose": {"color": "blue"},
}

# //? le label par défaut de la log
# si DEFAULT_SHORT_LOG_LABEL alors affiche simplement le nom du programme qui a généré la log
# sinon affichera le chemin complet avec le nom du programme source et cible qui ont levé l"info ou l"alerte
DEFAULT_SHORT_LOG_LABEL = True

# //? le format par défaut de la log
DEFAULT_LOG_FORMAT = \
    "%(asctime)s %(username)s@%(hostname)s - %(name)s" \
    + " [P%(process)d - T%(thread)d - %(filename)s:%(lineno)05d] • %(levelname)13s : %(message)s"

# //? le timestamp par défaut de la log
DEFAULT_LOG_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
########################################################################################################################
# /CONFIGURATION LOG ###################################################################################################
########################################################################################################################
