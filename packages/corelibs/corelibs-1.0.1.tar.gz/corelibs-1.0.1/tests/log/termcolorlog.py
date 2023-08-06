# termcolorlog.py
from corelibs import config, log

# écrasement de la config par défaut de corelibs
# config.DEFAULT_VERBOSE = True
config.DEFAULT_LOGS_EXTENSION = ".LOG"
# config.DEFAULT_SHORT_LOG_LABEL = False
# config.DEFAULT_STACK_TRACE_2_FILE = True
# config.DEFAULT_STYLE_STACK_TRACE = "plaintext"
# config.DEFAULT_STACK_TRACE = True
# config.DEFAULT_CONTEXT_SOURCE_LINES = 7

# instanciation par défaut pour la sortie standard terminal seulement
cl = log.TermColorLog()

cl.debug("Bonjour, ceci est un test niveau DEBUG")
cl.info("Bonjour, ceci est un test niveau INFO", True)
cl.warning("Bonjour, ceci est un test niveau WARNING")
cl.error("Bonjour, ceci est un test niveau ERROR", trace_back=True)
cl.critical("Bonjour, ceci est un test niveau CRITIQUE")


# redéfinition du nom du dossier logs
# /!\ IMPORTANT /!\
#    il n'y a que le dossier des logs qui est pris en compte, définir les autres dossiers ici est inutile
config.DEFAULT_DIR_SCAFFOLDING = {
    "logs": {  # dossier contenant toutes les sorties "logs"
        "name": "__R2D2-LOGS__",
        "make": True
    },
}

# instanciation personnalisée
user_cl = log.TermColorLog(
    name="Ma log à moi que j'ai",
    log_level=None,
    output_2_log_file=True,
    location=r"D:\OneDrive\Documents\_TEST_\T32020",
    log_file_name=None,
    field_styles={
        "asctime": {"color": "black"},
        "name": {"color": "green"},
    },
    level_styles={
        "info": {
            "color": "white",
            "background": "cyan"
        },
    },
    log_format="%(asctime)s - %(name)s [%(filename)s:%(lineno)07d] <> %(levelname)13s : %(message)s",
    log_date_format="%A %d %B %Y"
)

user_cl.debug("Bonjour, ceci est un test personnalisé niveau DEBUG")
user_cl.info("Bonjour, ceci est un test personnalisé niveau INFO")
user_cl.warning("Bonjour, ceci est un test personnalisé niveau WARNING")
user_cl.error("Bonjour, ceci est un test personnalisé niveau ERROR", trace_back=True)
user_cl.critical("Bonjour, ceci est un test personnalisé niveau CRITIQUE", trace_back=True)


# Création log dynamiquement selon contexte terminal standard ou Jupyter Notebooks
xcl = log.ColorLog(log_file_name="KIM")
xcl.debug("Bonjour, ceci est un test dynamique niveau DEBUG")
xcl.info("Bonjour, ceci est un test dynamique niveau INFO")
xcl.warning("Bonjour, ceci est un test dynamique niveau WARNING")
xcl.error("Bonjour, ceci est un test dynamique niveau ERROR", trace_back=True)
xcl.critical("Bonjour, ceci est un test dynamique niveau CRITIQUE", trace_back=True)
