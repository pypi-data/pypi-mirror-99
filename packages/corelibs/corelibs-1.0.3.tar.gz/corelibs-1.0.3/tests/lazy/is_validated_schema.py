# is_validated_schema.py
# %%
import schema as sc

from corelibs import lazy as lz

########################################################################################################################
# TEST Schéma DICT (défaut)
########################################################################################################################
# Test schéma byte format size
SCHEMA_DEFAULT_BYTE_SIZE_FORMAT = sc.Schema({
    sc.Optional(sc.And(str, lambda s: s in (
        # clé parmi les noms définis ci-dessous
        "octet", "Ko", "Mo", "Go", "To"
    ))): {
        "min_size": sc.Or(int, float)
    }
})
# Test valide
DEFAULT_BYTE_SIZE_FORMAT_OK = {
    "octet": {"min_size": 0},
    "Ko": {"min_size": 1},
    "Mo": {"min_size": 1},
    "Go": {"min_size": 1},
    "To": {"min_size": 0.5}
}
lz.is_validated_schema(DEFAULT_BYTE_SIZE_FORMAT_OK, SCHEMA_DEFAULT_BYTE_SIZE_FORMAT, verbose=True)
# Test invalide
DEFAULT_BYTE_SIZE_FORMAT_KO = {
    "octet": {"min_size": "Hello"},
    "Ko": {"min_size": "Kim"},
    "Mo": {"min_size": "Marie"},
    "Go": {"min_size": "Adélie"},
    "To": {"min_size": 7}
}
lz.is_validated_schema(DEFAULT_BYTE_SIZE_FORMAT_KO, SCHEMA_DEFAULT_BYTE_SIZE_FORMAT, verbose=True)

# %%
# Test schéma scaffolding
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
# Test valide
DIR_SCAFFOLDING_OK = {
    "input": {  # dossier contenant toutes les données "entrées"
        "name": "__MY_INPUTS__",
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
}
lz.is_validated_schema(DIR_SCAFFOLDING_OK, SCHEMA_DIR_SCAFFOLDING, verbose=True)
# Test invalide
DIR_SCAFFOLDING_KO = {
    "input": {  # dossier contenant toutes les données "entrées"
        "name": "__R2 D2__",
        "make": False
    },
    "output": {  # dossier contenant toutes les données "sorties"
        "name": "__MY_OUTPUTS__",
        "make": "Coucou"
    },
    "logs": {  # dossier contenant toutes les sorties "logs"
        "name": "__MY-LOGS__",
        "make": True
    },
}
lz.is_validated_schema(DIR_SCAFFOLDING_KO, SCHEMA_DIR_SCAFFOLDING)

# %%
# Test schéma styles des champs
SCHEMA_FIELD_STYLES = sc.Schema({
    sc.Optional(sc.And(str, lambda s: s in (
        "asctime", "hostname", "username", "levelname", "name", "programname"
    ))): {
        "color": sc.Or(sc.And(int, lambda n: 0 <= n <= 255),
                       sc.And(str, lambda s: s in (
                           "black", "blue", "cyan", "green",
                           "magenta", "red", "white", "yellow"
                       ))),
        sc.Optional(sc.And(str, sc.Use(str.lower), lambda s: s in (
            "bold", "bright", "faint"
        ))): bool,
    }
})
# Test valide...
FIELD_STYLES_OK = {
    "asctime": {"color": 242, "bright": True},
    "hostname": {"color": "magenta"},
    "username": {"color": "yellow"},
    "levelname": {"color": 242, "bright": True},
    "name": {"color": "blue"},
    "programname": {"color": "cyan"}
}
lz.is_validated_schema(FIELD_STYLES_OK, SCHEMA_FIELD_STYLES)
# Test invalide...
FIELD_STYLES_KO = {
    "asctimeZ": {"color": 242, "bright": True},
    "hostname": {"color": "white"},
    "username": {"color": "yellow"},
    "levelname": {"color": 242, "bright": False},
    "name": {"color": "blue"},
    "programname": {"color": "cyan"}
}
lz.is_validated_schema(FIELD_STYLES_KO, SCHEMA_FIELD_STYLES)

# %%
# Test schéma styles des niveaux d'alertes
SCHEMA_LEVEL_STYLES = sc.Schema({
    sc.Optional(sc.And(str, lambda s: s in (
        "critical", "error", "warning", "debug", "info", "notice", "spam", "success", "verbose"
    ))): {
        "color": sc.Or(sc.And(int, lambda n: 0 <= n <= 255),
                       sc.And(str, lambda s: s in (
                           "black", "blue", "cyan", "green",
                           "magenta", "red", "white", "yellow"
                       ))),
        sc.Optional(sc.And(str, sc.Use(str.lower), lambda s: s in (
            "background"
        ))): sc.Or(sc.And(int, lambda n: 0 <= n <= 255),
                   sc.And(str, lambda s: s in (
                       "black", "blue", "cyan", "green",
                       "magenta", "red", "white", "yellow"
                   ))),
    }
})
# Test valide...
LEVEL_STYLES_OK = {
    "critical": {"color": "white", "background": "red"},
    "verbose": {"color": "white"},
}
lz.is_validated_schema(LEVEL_STYLES_OK, SCHEMA_LEVEL_STYLES)
# Test invalide...
LEVEL_STYLES_KO = {
    "WRONG_KEY_critical": {"color": "white", "background": "red"}
}
lz.is_validated_schema(LEVEL_STYLES_KO, SCHEMA_LEVEL_STYLES)

# %%
# Test schéma format d'affichage des logs
SCHEMA_LOG_FORMAT = sc.Regex(
    r"^([ <>•@:=$~{}\(\)\[\]\w\d\-\.]*"
    + r"%\((\b(asctime|created|filename|funcName|levelname|levelno|lineno|message|module|msecs|name"
    + r"|pathname|process|processName|relativeCreated|thread|threadName|username|hostname)\b)\)"
    + r"\d*[sd]{1,1}[ <>•@:=$~{}\(\)\[\]\w\d\-\.]*)*$"
)
# Test valide...
LOG_FORMAT_OK = \
    "> %(asctime)s %(username)s@%(hostname)s - %(name)s" \
    + "[P.%(process)d - T.%(thread)d - L.%(lineno)05d] • %(levelname)13s %(message)s"
lz.is_validated_schema(LOG_FORMAT_OK, SCHEMA_LOG_FORMAT)
# Test invalide...
LOG_FORMAT_KO = "%(asctime)s %(username)s@%(hostname)s %(name)s[%(process)d] • %(_levelname_)13s %(message)s"
lz.is_validated_schema(LOG_FORMAT_KO, SCHEMA_LOG_FORMAT)

# %%
# Test schéma format d'affichage timestamp des logs
SCHEMA_LOG_DATE_FORMAT = sc.Regex(r"^(%(%|\b[aAwdbBmyYHIpMSfzZjUWcxXGuV]\b)[ \/\-:]*)*$")
# Test valide...
LOG_DATE_FORMAT_OK = "%Y/%m/%d %H:%M:%S"
lz.is_validated_schema(LOG_DATE_FORMAT_OK, SCHEMA_LOG_DATE_FORMAT)
# Test invalide...
LOG_DATE_FORMAT_KO = "%Y-%m-%d %HH : %M : %S"
lz.is_validated_schema(LOG_DATE_FORMAT_KO, SCHEMA_LOG_DATE_FORMAT)

# %%
########################################################################################################################
# TEST Schéma YAML
########################################################################################################################
lz.is_validated_schema(
    r"D:\OneDrive\Documents\[PYTHON_PROJECTS]\corelibs\tests\lazy\conf_test.yaml",
    r"D:\OneDrive\Documents\[PYTHON_PROJECTS]\corelibs\tests\lazy\schema_conf_test.yaml",
    is_dict_schema=False
)
