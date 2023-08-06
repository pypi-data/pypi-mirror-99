########################################################################################################################
# Bienvenue à...                                                                                                       #
#                                      ______                ___ __                                                    #
#                                     / ____/___  ________  / (_) /_  _____                                            #
#                                    / /   / __ \/ ___/ _ \/ / / __ \/ ___/                                            #
#                                   / /___/ /_/ / /  /  __/ / / /_/ (__  )                                             #
#                                   \____/\____/_/   \___/_/_/_.___/____/                                   ############
#                                                                                                          # config.py #
########################################################################################################################
import ctypes
import logging as log

import phonenumbers
import schema as sc


def _import_user_corelibs_root():
    try:
        import os
        import sys
        import pathlib
        import shutil
        import corelibs

        CORELIBS_FOLDER = ".corelibs"
        CORELIBS_USER_CONFIG = "user_config.py"

        corelibs_root = os.path.dirname(corelibs.__file__) + "\\" + CORELIBS_FOLDER
        user_corelibs_root = os.path.abspath(str(pathlib.Path.home()) + "\\" + CORELIBS_FOLDER)

        if not pathlib.Path(user_corelibs_root).is_dir():
            shutil.copytree(corelibs_root, user_corelibs_root)
            ctypes.windll.kernel32.SetFileAttributesW(user_corelibs_root, 2)

        if not pathlib.Path(user_corelibs_root + "\\" + CORELIBS_USER_CONFIG).is_file():
            shutil.copy2(corelibs_root + "\\" + CORELIBS_USER_CONFIG, user_corelibs_root + "\\" + CORELIBS_USER_CONFIG)
    finally:
        sys.path.append(user_corelibs_root)


_import_user_corelibs_root()
import user_config as _uc

PACKAGE_NAME = "֍( corelibs )֎"
PACKAGE_VERSION = "1.0.1"

PACKAGE_SUFFIX_TMP_NAME = "_corelibs"

########################################################################################################################
# CONFIGURATION INTERFACE UI ###########################################################################################
########################################################################################################################
# Chemin pour le script Conda
# Windows 10: C:\Users\<your-username>\Anaconda3\
# macOS: /Users/<your-username>/anaconda3 for the shell install, ~/opt for the graphical install.
# Linux: /home/<your-username>/anaconda3
# cf. https://docs.anaconda.com/anaconda/user-guide/faq/ pour plus de détail
try:
    UI_CONDA_PATH = _uc.UI_CONDA_PATH
except AttributeError:
    UI_CONDA_PATH = r"C:\ProgramData\Anaconda3\Scripts"

# Par défaut, le thème est aléatoire, pour connaitre le nom du thème affiché, mettre à Oui
try:
    UI_DISPLAY_THEME_NAME = _uc.UI_DISPLAY_THEME_NAME

    if not isinstance(UI_DISPLAY_THEME_NAME, bool):
        UI_DISPLAY_THEME_NAME = False
except AttributeError:
    UI_DISPLAY_THEME_NAME = False

# Nom du thème à afficher
try:
    UI_THEME_NAME = _uc.UI_THEME_NAME

    if not isinstance(UI_THEME_NAME, str) or UI_THEME_NAME not in (
            "Black", "Blue Mono", "Blue Purple", "Bright Colors", "Brown Blue", "Dark", "Dark 2", "Dark Amber",
            "Dark Black", "Dark Black 1", "Dark Blue", "Dark Blue 1", "Dark Blue 2", "Dark Blue 3", "Dark Blue 4",
            "Dark Blue 5", "Dark Blue 6", "Dark Blue 7", "Dark Blue 8", "Dark Blue 9", "Dark Blue 10", "Dark Blue 11",
            "Dark Blue 12", "Dark Blue 13", "Dark Blue 14", "Dark Blue 15", "Dark Blue 16", "Dark Blue 17",
            "Dark Brown", "Dark Brown 1", "Dark Brown 2", "Dark Brown 3", "Dark Brown 4", "Dark Brown 5",
            "Dark Brown 6", "Dark Brown 7", "Dark Green", "Dark Green 1", "Dark Green 2", "Dark Green 3",
            "Dark Green 4", "Dark Green 5", "Dark Green 6", "Dark Green 7", "Dark Grey", "Dark Grey 1", "Dark Grey 2",
            "Dark Grey 3", "Dark Grey 4", "Dark Grey 5", "Dark Grey 6", "Dark Grey 7", "Dark Grey 8", "Dark Grey 9",
            "Dark Grey 10", "Dark Grey 11", "Dark Grey 12", "Dark Grey 13", "Dark Grey 14", "Dark Purple",
            "Dark Purple 1", "Dark Purple 2", "Dark Purple 3", "Dark Purple 4", "Dark Purple 5", "Dark Purple 6",
            "Dark Purple 7", "Dark Red", "Dark Red 1", "Dark Red 2", "Dark Tan Blue", "Dark Teal", "Dark Teal 1",
            "Dark Teal 2", "Dark Teal 3", "Dark Teal 4", "Dark Teal 5", "Dark Teal 6", "Dark Teal 7", "Dark Teal 8",
            "Dark Teal 9", "Dark Teal 10", "Dark Teal 11", "Dark Teal 12", "Default", "Default 1",
            "Default No More Nagging", "Green", "Green Mono", "Green Tan", "Hot Dog Stand", "Kayak", "Light Blue",
            "Light Blue 1", "Light Blue 2", "Light Blue 3", "Light Blue 4", "Light Blue 5", "Light Blue 6",
            "Light Blue 7", "Light Brown", "Light Brown 1", "Light Brown 2", "Light Brown 3", "Light Brown 4",
            "Light Brown 5", "Light Brown 6", "Light Brown 7", "Light Brown 8", "Light Brown 9", "Light Brown 10",
            "Light Brown 11", "Light Brown 12", "Light Brown 13", "Light Gray 1", "Light Green", "Light Green 1",
            "Light Green 2", "Light Green 3", "Light Green 4", "Light Green 5", "Light Green 6", "Light Green 7",
            "Light Green 8", "Light Green 9", "Light Green 10", "Light Grey", "Light Grey 1", "Light Grey 2",
            "Light Grey 3", "Light Grey 4", "Light Grey 5", "Light Grey 6", "Light Purple", "Light Teal",
            "Light Yellow", "Material 1", "Material 2", "Neutral Blue", "Purple", "Python", "Reddit", "Reds",
            "Sandy Beach", "System Default", "System Default 1", "System Default For Real", "Tan", "Tan Blue",
            "Teal Mono", "Topanga"):
        UI_THEME_NAME = None
except AttributeError:
    UI_THEME_NAME = None
########################################################################################################################
# /CONFIGURATION INTERFACE UI ##########################################################################################
########################################################################################################################

########################################################################################################################
# CONFIGURATION LOCALE #################################################################################################
########################################################################################################################
# Format Phone number
PHONE_NUMBER_FORMAT_NATIONAL = phonenumbers.PhoneNumberFormat.NATIONAL
PHONE_NUMBER_FORMAT_INTERNATIONAL = phonenumbers.PhoneNumberFormat.INTERNATIONAL
PHONE_NUMBER_FORMAT_E164 = phonenumbers.PhoneNumberFormat.E164

# buffer de lecture/écriture en nombres d'octets
try:
    DEFAULT_BYTE_CHUNK_SIZE = _uc.DEFAULT_BYTE_CHUNK_SIZE
except AttributeError:
    DEFAULT_BYTE_CHUNK_SIZE = 1048576 * 64  # 1048576 exprimé en bytes <=> 1024KB <=> 1MB

# buffer de prévisualisation/lecture/écriture en nombre de lignes
try:
    DEFAULT_BUFFER_CHUNK_SIZE = _uc.DEFAULT_BUFFER_CHUNK_SIZE
except AttributeError:
    DEFAULT_BUFFER_CHUNK_SIZE = 65536  # <=> max lignes Excel < 2007, sinon 1048576 lignes

# encodage par défaut des fichiers
try:
    DEFAULT_ENCODING_FILE = _uc.DEFAULT_ENCODING_FILE
except AttributeError:
    DEFAULT_ENCODING_FILE = "latin-1"  # Western Europe latin-1 pour les français, sinon choisir "utf-8" ou "ISO-8859-1"

# les formats français par défaut
try:
    DEFAULT_LOCALE_TIME = _uc.DEFAULT_LOCALE
except AttributeError:
    DEFAULT_LOCALE_TIME = "fr"

# code page encoding pour les retour terminal des appels commandes DOS
try:
    DEFAULT_DOS_CMD_CP_ENCODING = _uc.DEFAULT_DOS_CMD_CP_ENCODING
except AttributeError:
    DEFAULT_DOS_CMD_CP_ENCODING = "cp850"  # cf. https://en.wikipedia.org/wiki/Code_page_850

# format des tailles avec leur valeur minimale pour l'affichage automatisé
try:
    DEFAULT_MIN_BYTE_SIZE_FORMAT = _uc.DEFAULT_MIN_BYTE_SIZE_FORMAT
except AttributeError:
    DEFAULT_MIN_BYTE_SIZE_FORMAT = {
        "octet": {"min_size": 0},
        "Ko": {"min_size": 1},
        "Mo": {"min_size": 1},
        "Go": {"min_size": 1},
        "To": {"min_size": 0.5}
    }

# schéma de contrôle pour valider DEFAULT_MIN_BYTE_SIZE_FORMAT
SCHEMA_DEFAULT_MIN_BYTE_SIZE_FORMAT = sc.Schema({
    sc.Optional(sc.And(str, lambda s: s in (
        # clé parmi les noms définis ci-dessous
        "octet", "Ko", "Mo", "Go", "To"
    ))): {
        "min_size": sc.Or(int, float)
    }
})

# schéma de contrôle pour valider les flags regex au niveau recherche
SCHEMA_REGEX_FLAGS = sc.Regex(
    r"^(\b(((re|RegexFlag).)?((A(SCII)?)|(DEBUG)|(I(GNORECASE)?)|(L(OCALE)?)|(M(ULTILINE)?)|(S)|(DOTALL)|(X)|("
    r"VERBOSE)))((\ )*\|(\ )*)?)+$"
)
########################################################################################################################
# /CONFIGURATION LOCALE ################################################################################################
########################################################################################################################


########################################################################################################################
# CONFIGURATION PROJET #################################################################################################
########################################################################################################################
# nom structures modèles de répertoires par défaut
try:
    DEFAULT_DIR_SCAFFOLDING = _uc.DEFAULT_DIR_SCAFFOLDING
except AttributeError:
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

# schéma de contrôle pour valider DEFAULT_DIR_SCAFFOLDING
SCHEMA_DIR_SCAFFOLDING = sc.Schema({
    sc.Optional(sc.And(str, lambda s: s in (
        # clé parmi les noms définis ci-dessous
        "input", "output", "logs", "docs"
    ))): {
        "name": sc.Regex(
            r"^__[a-zA-Z0-9 _-]+__$"
        ),
        "make": bool
    }
})
########################################################################################################################
# /CONFIGURATION PROJET ################################################################################################
########################################################################################################################


########################################################################################################################
# CONFIGURATION LOG ####################################################################################################
########################################################################################################################
# forcer l'exécution des instructions suivantes même quand une erreur est levée (Attention à son emploi...)
try:
    DEFAULT_IGNORE_ERROR = _uc.DEFAULT_IGNORE_ERROR
except AttributeError:
    DEFAULT_IGNORE_ERROR = False

# affichage détaillé de la pile d'exécution
try:
    DEFAULT_STACK_TRACE = _uc.DEFAULT_STACK_TRACE
except AttributeError:
    DEFAULT_STACK_TRACE = False

# redirection de l'affichage détaillé de la pile d'exécution vers la log
try:
    DEFAULT_STACK_TRACE_2_FILE = _uc.DEFAULT_STACK_TRACE_2_FILE
except AttributeError:
    DEFAULT_STACK_TRACE_2_FILE = False

# affichage détaillé de la pile d'exécution
# par défaut, le style de couleur sera :
# • "lightbg" si environnement Jupyter, sinon "darkbg2" si DEFAULT_STACK_TRACE_2_FILE est faux
# • "plaintext" si DEFAULT_STACK_TRACE_2_FILE est vrai
try:
    DEFAULT_STYLE_STACK_TRACE = _uc.DEFAULT_STYLE_STACK_TRACE
except AttributeError:
    DEFAULT_STYLE_STACK_TRACE = "default"  # valeur possibles : plaintext, color, darkbg2 ou lightbg

# contexte du code source pour les affichage détaillés des logs
try:
    DEFAULT_CONTEXT_SOURCE_LINES = _uc.DEFAULT_CONTEXT_SOURCE_LINES
except AttributeError:
    DEFAULT_CONTEXT_SOURCE_LINES = 3

# affichage informations en provenance du package corelibs
try:
    DEFAULT_VERBOSE = _uc.DEFAULT_VERBOSE
except AttributeError:
    DEFAULT_VERBOSE = False

# nom fichier log par défaut dans le cas des entrées standards
try:
    DEFAULT_STDIN_LOGS_NAME = _uc.DEFAULT_STDIN_LOGS_NAME
except AttributeError:
    DEFAULT_STDIN_LOGS_NAME = "__STDIN_"

# extension par défaut des fichiers logs
try:
    DEFAULT_LOGS_EXTENSION = _uc.DEFAULT_LOGS_EXTENSION
except AttributeError:
    DEFAULT_LOGS_EXTENSION = ".log"

# niveau d"affichage des logs, valeurs possibles :
# * log.DEBUG <=> 10
# * log.INFO <=> 20 (valeur par défaut)
# * log.WARNING <=> 30
# * log.ERROR <=> 40
# * log.CRITICAL <=> 50
#
# pour désactiver une alerte, on augmente son niveau, par exemple WARNING (30)
# et dans ce cas, les alertes de niveau DEBUG et INFO seront ignorées.
try:
    DEFAULT_LOG_LEVEL = _uc.DEFAULT_LOG_LEVEL
except AttributeError:
    DEFAULT_LOG_LEVEL = log.INFO  # ou 20

# le style par défaut des LOG affichées dans la sortie standard
try:
    DEFAULT_FIELD_STYLES = _uc.DEFAULT_FIELD_STYLES
except AttributeError:
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

# schéma de contrôle pour valider DEFAULT_FIELD_STYLES
SCHEMA_FIELD_STYLES = sc.Schema({
    sc.Optional(sc.And(str, lambda s: s in (
        # clé parmi les noms définis ci-dessous
        "asctime", "hostname", "username", "created", "filename", "funcName", "levelname", "levelno", "lineno",
        "message", "module", "msecs", "name", "pathname", "process", "processName", "relativeCreated", "thread",
        "threadName", "programname"
    ))): {
        # clé "color" accepte comme valeur :
        # • soit un entier entre 0 et 255
        # • soit une des 8 couleurs prédéfinies ci-dessous
        "color": sc.Or(sc.And(int, lambda n: 0 <= n <= 255),
                       sc.And(str, lambda s: s in (
                           "black", "blue", "cyan", "green",
                           "magenta", "red", "white", "yellow"
                       ))),
        # clé optionnelle parmi les 3 ci-dessous, avec comme valeur un booléen True/False
        sc.Optional(sc.And(str, sc.Use(str.lower), lambda s: s in (
            "bold", "bright", "faint"
        ))): bool,
    }
})

# les couleurs par défaut selon le niveau
try:
    DEFAULT_LEVEL_STYLES = _uc.DEFAULT_LEVEL_STYLES
except AttributeError:
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

# schéma de contrôle pour valider DEFAULT_LEVEL_STYLES
SCHEMA_LEVEL_STYLES = sc.Schema({
    sc.Optional(sc.And(str, lambda s: s in (
        # clé parmi les noms définis ci-dessous
        "critical", "error", "warning", "debug", "info"
    ))): {
        # clé "color" accepte comme valeur :
        # • soit un entier entre 0 et 255
        # • soit une des 8 couleurs prédéfinies ci-dessous
        "color": sc.Or(sc.And(int, lambda n: 0 <= n <= 255),
                       sc.And(str, lambda s: s in (
                           "black", "blue", "cyan", "green",
                           "magenta", "red", "white", "yellow"
                       ))),
        sc.Optional(sc.And(str, sc.Use(str.lower), lambda s: s in (
            # clé optionnelle qui accepte seulelment une couleur comme valeur
            "background"
        ))): sc.Or(sc.And(int, lambda n: 0 <= n <= 255),
                   sc.And(str, lambda s: s in (
                       "black", "blue", "cyan", "green",
                       "magenta", "red", "white", "yellow"
                   ))),
    }
})

# le label par défaut de la log
# si DEFAULT_SHORT_LOG_LABEL alors affiche simplement le nom du programme qui a généré la log
# sinon affichera le chemin complet avec le nom du programme source et cible qui ont levé l"info ou l"alerte
try:
    DEFAULT_SHORT_LOG_LABEL = _uc.DEFAULT_SHORT_LOG_LABEL
except AttributeError:
    DEFAULT_SHORT_LOG_LABEL = True

# le format par défaut de la log
try:
    DEFAULT_LOG_FORMAT = _uc.DEFAULT_LOG_FORMAT
except AttributeError:
    DEFAULT_LOG_FORMAT = \
        "%(asctime)s %(username)s@%(hostname)s - %(name)s" \
        + " [P%(process)d - T%(thread)d - %(filename)s:%(lineno)05d] • %(levelname)13s : %(message)s"

# schéma de contrôle pour valider DEFAULT_LOG_FORMAT
SCHEMA_LOG_FORMAT = sc.Regex(
    # le format de la log doit être une combinaison de %(nom)s où nom doit être parmi la liste ci-dessous
    r"^([ <>•@:=$~{}\(\)\[\]\w\d\-\.]*"
    + r"%\((\b(asctime|created|filename|funcName|levelname|levelno|lineno|message|module|msecs|name"
    + r"|pathname|process|processName|relativeCreated|thread|threadName|username|hostname)\b)\)"
    + r"\d*[sd]{1,1}[ <>•@:=$~{}\(\)\[\]\w\d\-\.]*)*$"
)

# le timestamp par défaut de la log
try:
    DEFAULT_LOG_DATE_FORMAT = _uc.DEFAULT_LOG_DATE_FORMAT
except AttributeError:
    DEFAULT_LOG_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

# schéma de contrôle pour valider DEFAULT_LOG_DATE_FORMAT
SCHEMA_LOG_DATE_FORMAT = SCHEMA_DATE_TIME_FORMAT = sc.Regex(
    # le format de la date log doit être une combinaison de %X où X doit être une lettre parmi la liste ci-dessous
    r"^(%(%|\b[aAwdbBmyYHIpMSfzZjUWcxXGuV]\b)[ \/\-:]*)*$"
)

# LOCALE TAB
LOCAL_TAB = {
    "Windows": {
        "af": "africain",
        "ar-ae": "arabe (Émirats Arabes Unis)",
        "ar-bh": "arabe (Bahreïn)",
        "ar-dz": "arabe (Algérie)",
        "ar-eg": "arabe (Égypte)",
        "ar-iq": "arabe (Irak)",
        "ar-jo": "arabe (Jordanie)",
        "ar-kw": "arabe (Koweït)",
        "ar-lb": "arabe (Liban)",
        "ar-ly": "arabe (Libye)",
        "ar-ma": "arabe (Maroc)",
        "ar-om": "arabe (Oman)",
        "ar-qa": "arabe (Qatar)",
        "ar-sa": "arabe (Arabie Saoudite)",
        "ar-sy": "arabe (Syrie)",
        "ar-tn": "arabe (Tunisie)",
        "ar-ye": "arabe (Yemen)",
        "ar": "arabe",
        "as": "assamais",
        "az": "azéri",
        "be": "biélorusse",
        "bg": "bulgare",
        "bn": "bengali",
        "ca": "catalan",
        "cs": "tchèque",
        "da": "danois",
        "de-at": "allemand (Autriche)",
        "de-ch": "allemand (Suisse)",
        "de-li": "allemand (Liechtenstein)",
        "de-lu": "allemand (Luxembourg)",
        "de": "allemand (Allemagne)",
        "div": "divehi (Maldives)",
        "el": "grec",
        "en-au": "anglais (Australie)",
        "en-bz": "anglais (Belize)",
        "en-ca": "anglais (Canada)",
        "en-gb": "anglais (Royaume-Uni)",
        "en-ie": "anglais (Irlande)",
        "en-jm": "anglais (Jamaïque)",
        "en-nz": "anglais (Nouvelle-Zélande)",
        "en-ph": "anglais (Philippines)",
        "en-tt": "anglais (Trinité-et-Tobago)",
        "en-us": "anglais (États-Unis)",
        "en-za": "anglais (Afrique du Sud)",
        "en-zw": "anglais (Zimbabwe)",
        "en": "anglais",
        "es-ar": "espagnol (Argentine)",
        "es-bo": "espagnol (Bolivie)",
        "es-cl": "espagnol (Chili)",
        "es-co": "espagnol (Colombie)",
        "es-cr": "espagnol (Costa Rica)",
        "es-do": "espagnol (République dominicaine)",
        "es-ec": "espagnol (Équateur)",
        "es-gt": "espagnol (Guatemala)",
        "es-hn": "espagnol (Honduras)",
        "es-mx": "espagnol (Mexique)",
        "es-ni": "espagnol (Nicaragua)",
        "es-pa": "espagnol (Panama)",
        "es-pe": "espagnol (Pérou)",
        "es-pr": "espagnol (Porto Rico)",
        "es-py": "espagnol (Paraguay)",
        "es-sv": "espagnol (El Salvador)",
        "es-us": "espagnol (États-Unis)",
        "es-uy": "espagnol (Uruguay)",
        "es-ve": "espagnol (Venezuela)",
        "es": "espagnol",
        "et": "estonien",
        "eu": "basque (Basque)",
        "fa": "persan",
        "fi": "finnois",
        "fo": "féroïen",
        "fr-be": "français (Belgique)",
        "fr-ca": "français (Canada)",
        "fr-ch": "français (Suisse)",
        "fr-lu": "français (Luxembourg)",
        "fr-mc": "français (Monaco)",
        "fr": "français (France)",
        "gd": "gaélique écossais",
        "gl": "galicien",
        "gu": "gujarati",
        "he": "hébreu",
        "hi": "hindi",
        "hr": "croate",
        "hu": "hongrois",
        "hy": "arménien",
        "id": "indonésien",
        "is": "islandais",
        "it-ch": "italien (Suisse)",
        "it": "italien (Italie)",
        "ja": "japonais",
        "ka": "géorgien",
        "kk": "kazakh",
        "kn": "kannada",
        "ko": "coréen",
        "kok": "konkani",
        "kz": "kyrgyz",
        "lt": "lituanien",
        "lv": "letton",
        "mk": "macédonien",
        "ml": "malayalam",
        "mn": "mongol",
        "mr": "marathe",
        "ms": "malais",
        "mt": "maltais",
        "nb-no": "norvégien bokmål (Norvège)",
        "ne": "népalais",
        "nl-be": "néerlandais (Belgique)",
        "nl": "néerlandais (Pays-Bas)",
        "nn-no": "norvégien nynorsk (Norvège)",
        "no": "norvégien",
        "or": "oriya",
        "pa": "pendjabi",
        "pl": "polonais",
        "pt-br": "portugais (Brésil)",
        "pt": "portugais (Portugal)",
        "rm": "romanche",
        "ro-md": "roumain (Moldavie)",
        "ro": "roumain",
        "ru-md": "russe (Moldavie)",
        "ru": "russe",
        "sa": "sanskrit",
        "sb": "serbien",
        "sk": "slovaque",
        "sl": "slovène",
        "sq": "albanais",
        "sr": "serbe",
        "sv-fi": "suédois (Finlande)",
        "sv": "suédois",
        "sw": "swahili",
        "sx": "sutu",
        "syr": "syriaque",
        "ta": "tamoul",
        "te": "télougou",
        "th": "thaï",
        "tn": "tswana",
        "tr": "turc",
        "ts": "tsonga",
        "tt": "Tatar",
        "uk": "ukrainien",
        "ur": "ourdou",
        "uz": "ouzbek",
        "vi": "vietnamien",
        "xh": "xhosa",
        "yi": "yiddish",
        "zh-cn": "Chinese (China)",
        "zh-hk": "Chinese (Hong Kong SAR)",
        "zh-mo": "Chinese (Macao SAR)",
        "zh-sg": "Chinese (Singapore)",
        "zh-tw": "Chinese (Taiwan)",
        "zh": "Chinese",
        "zu": "Zulu",
    },
    "Unix": {
        "af": "africain",
        "af_ZA": "africain (Afrique du Sud)",
        "af_NA": "africain (Namibie)",
        "ak": "akan",
        "ak_GH": "akan (Ghana)",
        "sq": "albanais",
        "sq_AL": "albanais (Albanie)",
        "sq_XK": "albanais (Kosovo)",
        "sq_MK": "albanais (Macédoine)",
        "de": "allemand",
        "de_DE": "allemand (Allemagne)",
        "de_AT": "allemand (Autriche)",
        "de_BE": "allemand (Belgique)",
        "de_LI": "allemand (Liechtenstein)",
        "de_LU": "allemand (Luxembourg)",
        "de_CH": "allemand (Suisse)",
        "am": "amharique",
        "am_ET": "amharique (Éthiopie)",
        "en": "anglais",
        "en_ZA": "anglais (Afrique du Sud)",
        "en_AI": "anglais (Anguilla)",
        "en_AG": "anglais (Antigua-et-Barbuda)",
        "en_AU": "anglais (Australie)",
        "en_BS": "anglais (Bahamas)",
        "en_BB": "anglais (Barbade)",
        "en_BE": "anglais (Belgique)",
        "en_BZ": "anglais (Belize)",
        "en_BM": "anglais (Bermudes)",
        "en_BW": "anglais (Botswana)",
        "en_CM": "anglais (Cameroun)",
        "en_CA": "anglais (Canada)",
        "en_DG": "anglais (Diego Garcia)",
        "en_DM": "anglais (Dominique)",
        "en_ER": "anglais (Érythrée)",
        "en_FM": "anglais (États fédérés de Micronésie)",
        "en_US": "anglais (États-Unis)",
        "en_FJ": "anglais (Fidji)",
        "en_GM": "anglais (Gambie)",
        "en_GH": "anglais (Ghana)",
        "en_GI": "anglais (Gibraltar)",
        "en_GD": "anglais (Grenade)",
        "en_GU": "anglais (Guam)",
        "en_GG": "anglais (Guernesey)",
        "en_GY": "anglais (Guyana)",
        "en_CX": "anglais (Île Christmas)",
        "en_IM": "anglais (Île de Man)",
        "en_NF": "anglais (Île Norfolk)",
        "en_KY": "anglais (Îles Caïmans)",
        "en_CC": "anglais (Îles Cocos)",
        "en_CK": "anglais (Îles Cook)",
        "en_FK": "anglais (Îles Malouines)",
        "en_MP": "anglais (Îles Mariannes du Nord)",
        "en_MH": "anglais (Îles Marshall)",
        "en_UM": "anglais (Îles mineures éloignées des États-Unis)",
        "en_SB": "anglais (Îles Salomon)",
        "en_TC": "anglais (Îles Turques-et-Caïques)",
        "en_VG": "anglais (Îles Vierges britanniques)",
        "en_VI": "anglais (Îles Vierges des États-Unis)",
        "en_IN": "anglais (Inde)",
        "en_IE": "anglais (Irlande)",
        "en_JM": "anglais (Jamaïque)",
        "en_JE": "anglais (Jersey)",
        "en_KE": "anglais (Kenya)",
        "en_KI": "anglais (Kiribati)",
        "en_LS": "anglais (Lesotho)",
        "en_LR": "anglais (Libéria)",
        "en_MG": "anglais (Madagascar)",
        "en_MY": "anglais (Malaisie)",
        "en_MW": "anglais (Malawi)",
        "en_MT": "anglais (Malte)",
        "en_MU": "anglais (Maurice)",
        "en_MS": "anglais (Montserrat)",
        "en_NA": "anglais (Namibie)",
        "en_NR": "anglais (Nauru)",
        "en_NG": "anglais (Nigéria)",
        "en_NU": "anglais (Niue)",
        "en_NZ": "anglais (Nouvelle-Zélande)",
        "en_UG": "anglais (Ouganda)",
        "en_PK": "anglais (Pakistan)",
        "en_PW": "anglais (Palaos)",
        "en_PG": "anglais (Papouasie-Nouvelle-Guinée)",
        "en_PH": "anglais (Philippines)",
        "en_PN": "anglais (Pitcairn)",
        "en_PR": "anglais (Porto Rico)",
        "en_HK": "anglais (R.A.S. chinoise de Hong Kong)",
        "en_MO": "anglais (R.A.S. chinoise de Macao)",
        "en_GB": "anglais (Royaume-Uni)",
        "en_RW": "anglais (Rwanda)",
        "en_KN": "anglais (Saint-Christophe-et-Niévès)",
        "en_SX": "anglais (Saint-Martin (partie néerlandaise))",
        "en_VC": "anglais (Saint-Vincent-et-les-Grenadines)",
        "en_SH": "anglais (Sainte-Hélène)",
        "en_LC": "anglais (Sainte-Lucie)",
        "en_AS": "anglais (Samoa américaines)",
        "en_WS": "anglais (Samoa)",
        "en_SC": "anglais (Seychelles)",
        "en_SL": "anglais (Sierra Leone)",
        "en_SG": "anglais (Singapour)",
        "en_SS": "anglais (Soudan du Sud)",
        "en_SD": "anglais (Soudan)",
        "en_SZ": "anglais (Swaziland)",
        "en_TZ": "anglais (Tanzanie)",
        "en_IO": "anglais (Territoire britannique de l’océan Indien)",
        "en_TK": "anglais (Tokelau)",
        "en_TO": "anglais (Tonga)",
        "en_TT": "anglais (Trinité-et-Tobago)",
        "en_TV": "anglais (Tuvalu)",
        "en_VU": "anglais (Vanuatu)",
        "en_ZM": "anglais (Zambie)",
        "en_ZW": "anglais (Zimbabwe)",
        "ar": "arabe",
        "ar_DZ": "arabe (Algérie)",
        "ar_SA": "arabe (Arabie saoudite)",
        "ar_BH": "arabe (Bahreïn)",
        "ar_KM": "arabe (Comores)",
        "ar_DJ": "arabe (Djibouti)",
        "ar_EG": "arabe (Égypte)",
        "ar_AE": "arabe (Émirats arabes unis)",
        "ar_ER": "arabe (Érythrée)",
        "ar_IQ": "arabe (Irak)",
        "ar_IL": "arabe (Israël)",
        "ar_JO": "arabe (Jordanie)",
        "ar_KW": "arabe (Koweït)",
        "ar_LB": "arabe (Liban)",
        "ar_LY": "arabe (Libye)",
        "ar_MA": "arabe (Maroc)",
        "ar_MR": "arabe (Mauritanie)",
        "ar_OM": "arabe (Oman)",
        "ar_QA": "arabe (Qatar)",
        "ar_EH": "arabe (Sahara occidental)",
        "ar_SO": "arabe (Somalie)",
        "ar_SS": "arabe (Soudan du Sud)",
        "ar_SD": "arabe (Soudan)",
        "ar_SY": "arabe (Syrie)",
        "ar_TD": "arabe (Tchad)",
        "ar_PS": "arabe (Territoires palestiniens)",
        "ar_TN": "arabe (Tunisie)",
        "ar_YE": "arabe (Yémen)",
        "hy": "arménien",
        "hy_AM": "arménien (Arménie)",
        "as": "assamais",
        "as_IN": "assamais (Inde)",
        "az": "azéri",
        "az_AZ": "azéri (Azerbaïdjan)",
        "az_Cyrl_AZ": "azéri (cyrillique: Azerbaïdjan)",
        "az_Cyrl": "azéri (cyrillique)",
        "az_Latn_AZ": "azéri (latin: Azerbaïdjan)",
        "az_Latn": "azéri (latin)",
        "bm": "bambara",
        "bm_Latn_ML": "bambara (latin: Mali)",
        "bm_Latn": "bambara (latin)",
        "eu": "basque",
        "eu_ES": "basque (Espagne)",
        "bn": "bengali",
        "bn_BD": "bengali (Bangladesh)",
        "bn_IN": "bengali (Inde)",
        "be": "biélorusse",
        "be_BY": "biélorusse (Biélorussie)",
        "my": "birman",
        "my_MM": "birman (Myanmar)",
        "bs": "bosniaque",
        "bs_BA": "bosniaque (Bosnie-Herzégovine)",
        "bs_Cyrl_BA": "bosniaque (cyrillique: Bosnie-Herzégovine)",
        "bs_Cyrl": "bosniaque (cyrillique)",
        "bs_Latn_BA": "bosniaque (latin: Bosnie-Herzégovine)",
        "bs_Latn": "bosniaque (latin)",
        "br": "breton",
        "br_FR": "breton (France)",
        "bg": "bulgare",
        "bg_BG": "bulgare (Bulgarie)",
        "ca": "catalan",
        "ca_AD": "catalan (Andorre)",
        "ca_ES": "catalan (Espagne)",
        "ca_FR": "catalan (France)",
        "ca_IT": "catalan (Italie)",
        "zh": "chinois",
        "zh_CN": "chinois (Chine)",
        "zh_HK": "chinois (R.A.S. chinoise de Hong Kong)",
        "zh_MO": "chinois (R.A.S. chinoise de Macao)",
        "zh_Hans_CN": "chinois (simplifié: Chine)",
        "zh_Hans_HK": "chinois (simplifié: R.A.S. chinoise de Hong Kong)",
        "zh_Hans_MO": "chinois (simplifié: R.A.S. chinoise de Macao)",
        "zh_Hans_SG": "chinois (simplifié: Singapour)",
        "zh_Hans": "chinois (simplifié)",
        "zh_SG": "chinois (Singapour)",
        "zh_TW": "chinois (Taïwan)",
        "zh_Hant_HK": "chinois (traditionnel: R.A.S. chinoise de Hong Kong)",
        "zh_Hant_MO": "chinois (traditionnel: R.A.S. chinoise de Macao)",
        "zh_Hant_TW": "chinois (traditionnel: Taïwan)",
        "zh_Hant": "chinois (traditionnel)",
        "si": "cinghalais",
        "si_LK": "cinghalais (Sri Lanka)",
        "ko": "coréen",
        "ko_KP": "coréen (Corée du Nord)",
        "ko_KR": "coréen (Corée du Sud)",
        "kw": "cornique",
        "kw_GB": "cornique (Royaume-Uni)",
        "hr": "croate",
        "hr_BA": "croate (Bosnie-Herzégovine)",
        "hr_HR": "croate (Croatie)",
        "da": "danois",
        "da_DK": "danois (Danemark)",
        "da_GL": "danois (Groenland)",
        "dz": "dzongkha",
        "dz_BT": "dzongkha (Bhoutan)",
        "es": "espagnol",
        "es_AR": "espagnol (Argentine)",
        "es_BO": "espagnol (Bolivie)",
        "es_EA": "espagnol (Ceuta et Melilla)",
        "es_CL": "espagnol (Chili)",
        "es_CO": "espagnol (Colombie)",
        "es_CR": "espagnol (Costa Rica)",
        "es_CU": "espagnol (Cuba)",
        "es_SV": "espagnol (El Salvador)",
        "es_EC": "espagnol (Équateur)",
        "es_ES": "espagnol (Espagne)",
        "es_US": "espagnol (États-Unis)",
        "es_GT": "espagnol (Guatemala)",
        "es_GQ": "espagnol (Guinée équatoriale)",
        "es_HN": "espagnol (Honduras)",
        "es_IC": "espagnol (Îles Canaries)",
        "es_MX": "espagnol (Mexique)",
        "es_NI": "espagnol (Nicaragua)",
        "es_PA": "espagnol (Panama)",
        "es_PY": "espagnol (Paraguay)",
        "es_PE": "espagnol (Pérou)",
        "es_PH": "espagnol (Philippines)",
        "es_PR": "espagnol (Porto Rico)",
        "es_DO": "espagnol (République dominicaine)",
        "es_UY": "espagnol (Uruguay)",
        "es_VE": "espagnol (Venezuela)",
        "eo": "espéranto",
        "et": "estonien",
        "et_EE": "estonien (Estonie)",
        "ee": "éwé",
        "ee_GH": "éwé (Ghana)",
        "ee_TG": "éwé (Togo)",
        "fo": "féroïen",
        "fo_FO": "féroïen (Îles Féroé)",
        "fi": "finnois",
        "fi_FI": "finnois (Finlande)",
        "fr": "français",
        "fr_DZ": "français (Algérie)",
        "fr_BE": "français (Belgique)",
        "fr_BJ": "français (Bénin)",
        "fr_BF": "français (Burkina Faso)",
        "fr_BI": "français (Burundi)",
        "fr_CM": "français (Cameroun)",
        "fr_CA": "français (Canada)",
        "fr_KM": "français (Comores)",
        "fr_CG": "français (Congo-Brazzaville)",
        "fr_CD": "français (Congo-Kinshasa)",
        "fr_CI": "français (Côte d’Ivoire)",
        "fr_DJ": "français (Djibouti)",
        "fr_FR": "français (France)",
        "fr_GA": "français (Gabon)",
        "fr_GP": "français (Guadeloupe)",
        "fr_GQ": "français (Guinée équatoriale)",
        "fr_GN": "français (Guinée)",
        "fr_GF": "français (Guyane française)",
        "fr_HT": "français (Haïti)",
        "fr_RE": "français (La Réunion)",
        "fr_LU": "français (Luxembourg)",
        "fr_MG": "français (Madagascar)",
        "fr_ML": "français (Mali)",
        "fr_MA": "français (Maroc)",
        "fr_MQ": "français (Martinique)",
        "fr_MU": "français (Maurice)",
        "fr_MR": "français (Mauritanie)",
        "fr_YT": "français (Mayotte)",
        "fr_MC": "français (Monaco)",
        "fr_NE": "français (Niger)",
        "fr_NC": "français (Nouvelle-Calédonie)",
        "fr_PF": "français (Polynésie française)",
        "fr_CF": "français (République centrafricaine)",
        "fr_RW": "français (Rwanda)",
        "fr_BL": "français (Saint-Barthélemy)",
        "fr_MF": "français (Saint-Martin (partie française))",
        "fr_PM": "français (Saint-Pierre-et-Miquelon)",
        "fr_SN": "français (Sénégal)",
        "fr_SC": "français (Seychelles)",
        "fr_CH": "français (Suisse)",
        "fr_SY": "français (Syrie)",
        "fr_TD": "français (Tchad)",
        "fr_TG": "français (Togo)",
        "fr_TN": "français (Tunisie)",
        "fr_VU": "français (Vanuatu)",
        "fr_WF": "français (Wallis-et-Futuna)",
        "fy": "frison occidental",
        "fy_NL": "frison occidental (Pays-Bas)",
        "gd": "gaélique écossais",
        "gd_GB": "gaélique écossais (Royaume-Uni)",
        "gl": "galicien",
        "gl_ES": "galicien (Espagne)",
        "cy": "gallois",
        "cy_GB": "gallois (Royaume-Uni)",
        "lg": "ganda",
        "lg_UG": "ganda (Ouganda)",
        "ka": "géorgien",
        "ka_GE": "géorgien (Géorgie)",
        "el": "grec",
        "el_CY": "grec (Chypre)",
        "el_GR": "grec (Grèce)",
        "kl": "groenlandais",
        "kl_GL": "groenlandais (Groenland)",
        "gu": "gujarati",
        "gu_IN": "gujarati (Inde)",
        "ha": "haoussa",
        "ha_GH": "haoussa (Ghana)",
        "ha_Latn_GH": "haoussa (latin: Ghana)",
        "ha_Latn_NE": "haoussa (latin: Niger)",
        "ha_Latn_NG": "haoussa (latin: Nigéria)",
        "ha_Latn": "haoussa (latin)",
        "ha_NE": "haoussa (Niger)",
        "ha_NG": "haoussa (Nigéria)",
        "he": "hébreu",
        "he_IL": "hébreu (Israël)",
        "hi": "hindi",
        "hi_IN": "hindi (Inde)",
        "hu": "hongrois",
        "hu_HU": "hongrois (Hongrie)",
        "ig": "igbo",
        "ig_NG": "igbo (Nigéria)",
        "id": "indonésien",
        "id_ID": "indonésien (Indonésie)",
        "ga": "irlandais",
        "ga_IE": "irlandais (Irlande)",
        "is": "islandais",
        "is_IS": "islandais (Islande)",
        "it": "italien",
        "it_IT": "italien (Italie)",
        "it_SM": "italien (Saint-Marin)",
        "it_CH": "italien (Suisse)",
        "ja": "japonais",
        "ja_JP": "japonais (Japon)",
        "kn": "kannada",
        "kn_IN": "kannada (Inde)",
        "ks": "kashmiri",
        "ks_Arab_IN": "kashmiri (arabe: Inde)",
        "ks_Arab": "kashmiri (arabe)",
        "ks_IN": "kashmiri (Inde)",
        "kk": "kazakh",
        "kk_Cyrl_KZ": "kazakh (cyrillique: Kazakhstan)",
        "kk_Cyrl": "kazakh (cyrillique)",
        "kk_KZ": "kazakh (Kazakhstan)",
        "km": "khmer",
        "km_KH": "khmer (Cambodge)",
        "ki": "kikuyu",
        "ki_KE": "kikuyu (Kenya)",
        "ky": "kirghize",
        "ky_Cyrl_KG": "kirghize (cyrillique: Kirghizistan)",
        "ky_Cyrl": "kirghize (cyrillique)",
        "ky_KG": "kirghize (Kirghizistan)",
        "lo": "lao",
        "lo_LA": "lao (Laos)",
        "lv": "letton",
        "lv_LV": "letton (Lettonie)",
        "ln": "lingala",
        "ln_AO": "lingala (Angola)",
        "ln_CG": "lingala (Congo-Brazzaville)",
        "ln_CD": "lingala (Congo-Kinshasa)",
        "ln_CF": "lingala (République centrafricaine)",
        "lt": "lituanien",
        "lt_LT": "lituanien (Lituanie)",
        "lu": "luba-katanga",
        "lu_CD": "luba-katanga (Congo-Kinshasa)",
        "lb": "luxembourgeois",
        "lb_LU": "luxembourgeois (Luxembourg)",
        "mk": "macédonien",
        "mk_MK": "macédonien (Macédoine)",
        "ms": "malais",
        "ms_BN": "malais (Brunéi Darussalam)",
        "ms_Latn_BN": "malais (latin: Brunéi Darussalam)",
        "ms_Latn_MY": "malais (latin: Malaisie)",
        "ms_Latn_SG": "malais (latin: Singapour)",
        "ms_Latn": "malais (latin)",
        "ms_MY": "malais (Malaisie)",
        "ms_SG": "malais (Singapour)",
        "ml": "malayalam",
        "ml_IN": "malayalam (Inde)",
        "mg": "malgache",
        "mg_MG": "malgache (Madagascar)",
        "mt": "maltais",
        "mt_MT": "maltais (Malte)",
        "gv": "manx",
        "gv_IM": "manx (Île de Man)",
        "mr": "marathe",
        "mr_IN": "marathe (Inde)",
        "mn": "mongol",
        "mn_Cyrl_MN": "mongol (cyrillique: Mongolie)",
        "mn_Cyrl": "mongol (cyrillique)",
        "mn_MN": "mongol (Mongolie)",
        "nd": "ndébélé du Nord",
        "nd_ZW": "ndébélé du Nord (Zimbabwe)",
        "nl": "néerlandais",
        "nl_AW": "néerlandais (Aruba)",
        "nl_BE": "néerlandais (Belgique)",
        "nl_CW": "néerlandais (Curaçao)",
        "nl_BQ": "néerlandais (Pays-Bas caribéens)",
        "nl_NL": "néerlandais (Pays-Bas)",
        "nl_SX": "néerlandais (Saint-Martin (partie néerlandaise))",
        "nl_SR": "néerlandais (Suriname)",
        "ne": "népalais",
        "ne_IN": "népalais (Inde)",
        "ne_NP": "népalais (Népal)",
        "no": "norvégien",
        "no_NO": "norvégien (Norvège)",
        "nb": "norvégien bokmål",
        "nb_NO": "norvégien bokmål (Norvège)",
        "nb_SJ": "norvégien bokmål (Svalbard et Jan Mayen)",
        "nn": "norvégien nynorsk",
        "nn_NO": "norvégien nynorsk (Norvège)",
        "or": "oriya",
        "or_IN": "oriya (Inde)",
        "om": "oromo",
        "om_ET": "oromo (Éthiopie)",
        "om_KE": "oromo (Kenya)",
        "os": "ossète",
        "os_GE": "ossète (Géorgie)",
        "os_RU": "ossète (Russie)",
        "ug": "ouïghour",
        "ug_Arab_CN": "ouïghour (arabe: Chine)",
        "ug_Arab": "ouïghour (arabe)",
        "ug_CN": "ouïghour (Chine)",
        "ur": "ourdou",
        "ur_IN": "ourdou (Inde)",
        "ur_PK": "ourdou (Pakistan)",
        "uz": "ouzbek",
        "uz_AF": "ouzbek (Afghanistan)",
        "uz_Arab_AF": "ouzbek (arabe: Afghanistan)",
        "uz_Arab": "ouzbek (arabe)",
        "uz_Cyrl_UZ": "ouzbek (cyrillique: Ouzbékistan)",
        "uz_Cyrl": "ouzbek (cyrillique)",
        "uz_Latn_UZ": "ouzbek (latin: Ouzbékistan)",
        "uz_Latn": "ouzbek (latin)",
        "uz_UZ": "ouzbek (Ouzbékistan)",
        "ps": "pachto",
        "ps_AF": "pachto (Afghanistan)",
        "pa": "pendjabi",
        "pa_Arab_PK": "pendjabi (arabe: Pakistan)",
        "pa_Arab": "pendjabi (arabe)",
        "pa_Guru_IN": "pendjabi (gourmoukhî: Inde)",
        "pa_Guru": "pendjabi (gourmoukhî)",
        "pa_IN": "pendjabi (Inde)",
        "pa_PK": "pendjabi (Pakistan)",
        "fa": "persan",
        "fa_AF": "persan (Afghanistan)",
        "fa_IR": "persan (Iran)",
        "ff": "peul",
        "ff_CM": "peul (Cameroun)",
        "ff_GN": "peul (Guinée)",
        "ff_MR": "peul (Mauritanie)",
        "ff_SN": "peul (Sénégal)",
        "pl": "polonais",
        "pl_PL": "polonais (Pologne)",
        "pt": "portugais",
        "pt_AO": "portugais (Angola)",
        "pt_BR": "portugais (Brésil)",
        "pt_CV": "portugais (Cap-Vert)",
        "pt_GW": "portugais (Guinée-Bissau)",
        "pt_MZ": "portugais (Mozambique)",
        "pt_PT": "portugais (Portugal)",
        "pt_MO": "portugais (R.A.S. chinoise de Macao)",
        "pt_ST": "portugais (Sao Tomé-et-Principe)",
        "pt_TL": "portugais (Timor oriental)",
        "qu": "quechua",
        "qu_BO": "quechua (Bolivie)",
        "qu_EC": "quechua (Équateur)",
        "qu_PE": "quechua (Pérou)",
        "rm": "romanche",
        "rm_CH": "romanche (Suisse)",
        "ro": "roumain",
        "ro_MD": "roumain (Moldavie)",
        "ro_RO": "roumain (Roumanie)",
        "rn": "roundi",
        "rn_BI": "roundi (Burundi)",
        "ru": "russe",
        "ru_BY": "russe (Biélorussie)",
        "ru_KZ": "russe (Kazakhstan)",
        "ru_KG": "russe (Kirghizistan)",
        "ru_MD": "russe (Moldavie)",
        "ru_RU": "russe (Russie)",
        "ru_UA": "russe (Ukraine)",
        "rw": "rwanda",
        "rw_RW": "rwanda (Rwanda)",
        "se": "sami du Nord",
        "se_FI": "sami du Nord (Finlande)",
        "se_NO": "sami du Nord (Norvège)",
        "se_SE": "sami du Nord (Suède)",
        "sg": "sangho",
        "sg_CF": "sangho (République centrafricaine)",
        "sr": "serbe",
        "sr_BA": "serbe (Bosnie-Herzégovine)",
        "sr_Cyrl_BA": "serbe (cyrillique: Bosnie-Herzégovine)",
        "sr_Cyrl_XK": "serbe (cyrillique: Kosovo)",
        "sr_Cyrl_ME": "serbe (cyrillique: Monténégro)",
        "sr_Cyrl_RS": "serbe (cyrillique: Serbie)",
        "sr_Cyrl": "serbe (cyrillique)",
        "sr_XK": "serbe (Kosovo)",
        "sr_Latn_BA": "serbe (latin: Bosnie-Herzégovine)",
        "sr_Latn_XK": "serbe (latin: Kosovo)",
        "sr_Latn_ME": "serbe (latin: Monténégro)",
        "sr_Latn_RS": "serbe (latin: Serbie)",
        "sr_Latn": "serbe (latin)",
        "sr_ME": "serbe (Monténégro)",
        "sr_RS": "serbe (Serbie)",
        "sh": "serbo-croate",
        "sh_BA": "serbo-croate (Bosnie-Herzégovine)",
        "sn": "shona",
        "sn_ZW": "shona (Zimbabwe)",
        "sk": "slovaque",
        "sk_SK": "slovaque (Slovaquie)",
        "sl": "slovène",
        "sl_SI": "slovène (Slovénie)",
        "so": "somali",
        "so_DJ": "somali (Djibouti)",
        "so_ET": "somali (Éthiopie)",
        "so_KE": "somali (Kenya)",
        "so_SO": "somali (Somalie)",
        "sv": "suédois",
        "sv_FI": "suédois (Finlande)",
        "sv_AX": "suédois (Îles Åland)",
        "sv_SE": "suédois (Suède)",
        "sw": "swahili",
        "sw_KE": "swahili (Kenya)",
        "sw_UG": "swahili (Ouganda)",
        "sw_TZ": "swahili (Tanzanie)",
        "tl": "tagalog",
        "tl_PH": "tagalog (Philippines)",
        "ta": "tamoul",
        "ta_IN": "tamoul (Inde)",
        "ta_MY": "tamoul (Malaisie)",
        "ta_SG": "tamoul (Singapour)",
        "ta_LK": "tamoul (Sri Lanka)",
        "cs": "tchèque",
        "cs_CZ": "tchèque (République tchèque)",
        "te": "télougou",
        "te_IN": "télougou (Inde)",
        "th": "thaï",
        "th_TH": "thaï (Thaïlande)",
        "bo": "tibétain",
        "bo_CN": "tibétain (Chine)",
        "bo_IN": "tibétain (Inde)",
        "ti": "tigrigna",
        "ti_ER": "tigrigna (Érythrée)",
        "ti_ET": "tigrigna (Éthiopie)",
        "to": "tonguien",
        "to_TO": "tonguien (Tonga)",
        "tr": "turc",
        "tr_CY": "turc (Chypre)",
        "tr_TR": "turc (Turquie)",
        "uk": "ukrainien",
        "uk_UA": "ukrainien (Ukraine)",
        "vi": "vietnamien",
        "vi_VN": "vietnamien (Vietnam)",
        "ii": "yi du Sichuan",
        "ii_CN": "yi du Sichuan (Chine)",
        "yi": "yiddish",
        "yo": "yoruba",
        "yo_BJ": "yoruba (Bénin)",
        "yo_NG": "yoruba (Nigéria)",
        "zu": "zoulou",
        "zu_ZA": "zoulou (Afrique du Sud)",
    }
}
########################################################################################################################
# /CONFIGURATION LOG ###################################################################################################
########################################################################################################################
