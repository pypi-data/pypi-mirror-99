# jupytercolorlog.py
from corelibs import config, log

# écrasement de la config par défaut de corelibs
# config.DEFAULT_VERBOSE = True
# config.DEFAULT_STACK_TRACE = True
# config.DEFAULT_STYLE_STACK_TRACE = "color"
# config.DEFAULT_CONTEXT_SOURCE_LINES = 7

# instanciation par défaut pour Jupyter Notebooks seuleemnt
cl = log.JupyterColorLog()

cl.debug("Bonjour, ceci est un test niveau DEBUG")
cl.info("Bonjour, ceci est un test niveau INFO", trace_back=True)
cl.warning("Bonjour, ceci est un test niveau WARNING")
cl.error("Bonjour, ceci est un test niveau ERROR")
cl.critical("Bonjour, ceci est un test niveau CRITIQUE")


# Création log dynamiquement selon contexte terminal standard ou Jupyter Notebooks
xcl = log.ColorLog()

xcl.debug("Bonjour, ceci est un test dynamique niveau DEBUG")
xcl.info("Bonjour, ceci est un test dynamique niveau INFO")
xcl.warning("Bonjour, ceci est un test dynamique niveau WARNING")
xcl.error("Bonjour, ceci est un test dynamique niveau ERROR")
xcl.critical("Bonjour, ceci est un test dynamique niveau CRITIQUE")
