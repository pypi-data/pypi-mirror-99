import logging
import sys
from typing import Optional, Dict

from corelibs import config


def _print_import_exception(package_name):
    return f"\n\n-[{config.PACKAGE_NAME} • ImportError]- Impossible d'importer le package {package_name} - " \
           f"veuillez l'installer d'abord\n\t$conda/pip install {package_name}"


# config pour utilisation interne de la log ---------------------------------------------------------------------------#
def _is_jupyter():
    try:
        try:
            from IPython import get_ipython
        except ImportError:
            raise Exception(_print_import_exception("ipython"))

        ipy_conf = get_ipython().config
        for key, val in ipy_conf.items():
            if key == "IPKernelApp" and "jupyter" in val["connection_file"]:
                return True
    except AttributeError:
        return False


if _is_jupyter():
    try:
        from colorama import Fore, Back, Style

    except ImportError:
        raise Exception(_print_import_exception("colorama"))


    class ColoredFormatter(logging.Formatter):
        def __init__(self,
                     *args,
                     colors: Optional[Dict[str, str]] = None,
                     **kwargs) -> None:
            super().__init__(*args, **kwargs)

            self.colors = colors if colors else {}

        def format(self, record) -> str:
            record.esc_color = "\x1b[37m"
            record.color = self.colors.get(record.levelname, "")
            record.esc_reset = "\x1b[0m"

            return super().format(record)


    class JupyterColorLog(ColoredFormatter):
        def debug(self, message):
            self._logger.debug(message)

        def info(self, message):
            self._logger.info(message)

        def warning(self, message):
            self._logger.warning(message)

        def error(self, message):
            self._logger.error(message)

        def critical(self, message):
            self._logger.critical(message)

        def __init__(self, log_level=config.DEFAULT_LOG_LEVEL):
            try:
                from colorama import Fore, Back, Style
                self._fore = Fore
                self._back = Back
                self._style = Style

            except ImportError:
                raise Exception(_print_import_exception("colorama"))

            super(ColoredFormatter, self).__init__()

            formatter = ColoredFormatter(
                "{esc_color}{asctime} [{name}:{esc_reset}{lineno:05}{esc_color}] •{esc_reset}"
                + " {color}{levelname:13}{esc_reset} {esc_color}:{esc_reset} {message}",
                style='{', datefmt="%Y-%m-%d %H:%M:%S",
                colors={
                    'DEBUG': self._fore.GREEN,
                    'INFO': self._fore.CYAN,
                    'WARNING': self._fore.YELLOW,
                    'ERROR': self._fore.RED,
                    'CRITICAL': self._fore.RED + self._back.WHITE,
                }
            )

            handler = logging.StreamHandler(sys.stdout)
            handler.setFormatter(formatter)

            self._logger = logging.getLogger()
            self._logger.handlers[:] = []
            self._logger.addHandler(handler)
            self._logger.setLevel(log_level)

    log = JupyterColorLog(config.DEFAULT_LOG_LEVEL)
else:
    try:
        import coloredlogs as cl
    except ImportError:
        raise Exception(_print_import_exception("coloredlogs"))

    cl.DEFAULT_FIELD_STYLES = config.DEFAULT_FIELD_STYLES
    cl.DEFAULT_LEVEL_STYLES = config.DEFAULT_LEVEL_STYLES
    cl.DEFAULT_LOG_FORMAT = config.DEFAULT_LOG_FORMAT
    cl.DEFAULT_DATE_FORMAT = config.DEFAULT_LOG_DATE_FORMAT

    default_log_label = config.PACKAGE_NAME
    if not config.DEFAULT_SHORT_LOG_LABEL:
        default_log_label = __file__

    cl.install(
        level=config.DEFAULT_LOG_LEVEL,
        fmt=cl.DEFAULT_LOG_FORMAT
    )
    log = logging.getLogger(default_log_label)
# config pour utilisation interne de la log /--------------------------------------------------------------------------#
