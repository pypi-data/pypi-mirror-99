r"""
.. module:: log.py
    :synopsis: Module permettant de manipuler tout ce qui est relatif à la gestion des logs

.. moduleauthor:: Michel TRUONG <michel.truong@gmail.com>

.. topic:: Description générale

    Module permettant de manipuler tout ce qui est relatif à la gestion des logs

"""
import inspect
import logging
import re
import sys
from collections import namedtuple
from functools import wraps
from time import time, sleep
from typing import Optional, Dict

from corelibs import _corelibs as _c, config, lazy as lz

log = _c.log

try:
    import enlighten
except ImportError:
    raise Exception(_c._print_import_exception("enlighten"))

try:
    import coloredlogs as cl
except ImportError:
    raise Exception(_c._print_import_exception("coloredlogs"))

try:
    import yaml

    yaml.Dumper.ignore_aliases = lambda *args: True
except ImportError:
    raise Exception(_c._print_import_exception("yaml"))

try:
    import stackprinter as tb
except ImportError:
    raise Exception(_c._print_import_exception("stackprinter"))


def _style_trace_back():
    if config.DEFAULT_STYLE_STACK_TRACE == "plaintext" or config.DEFAULT_STACK_TRACE_2_FILE:
        return "plaintext"

    if config.DEFAULT_STYLE_STACK_TRACE == "default":
        if lz.is_jupyter():
            return "lightbg"
        else:
            return "darkbg2"
    elif config.DEFAULT_STYLE_STACK_TRACE in ["plaintext", "color", "darkbg2", "lightbg"]:
        return config.DEFAULT_STYLE_STACK_TRACE
    else:
        cl.install(level=config.DEFAULT_LOG_LEVEL)
        log.error(f"-[{config.PACKAGE_NAME}]- Le style \"{config.DEFAULT_STYLE_STACK_TRACE}\" pour les traces backs "
                  f"n'est pas reconnu. Valeurs possibles \"plaintext\", \"color\", \"darkbg2\" ou \"lightbg\".")
        sys.exit(1)


status_bar_manager = None
decorator_return = {
    "duration": {
        "status_bar": None,
        "progress_bar": None,
        "total": None
    }
}


class TermColorLog:
    r"""
    .. admonition:: Description

        | Classe de base pour manipuler les logs colorées dans la sortie standard du terminal.

        cf. :ref:`reference-label-config` pour la configuration par défaut
        (modifiable lors de l'instanciation de la classe)

    """
    _lz = None

    def _set_name(self, name):
        if name:
            return name
        else:
            if config.DEFAULT_SHORT_LOG_LABEL:
                return self._lz.get_file_extension(
                    self._caller_name
                )[0]
            else:
                return self._caller_name + "\\" + self._lz.get_caller_module_name()

    def _set_log_level(self, level):
        if level:
            self._log_level = level
        else:
            self._log_level = config.DEFAULT_LOG_LEVEL

        return self._log_level

    def _set_output_2_log_file(self, output_2_log_file):
        self._output_2_log_file = output_2_log_file

        return self._output_2_log_file

    def _set_location(self, location):
        global scaffolding
        default_dir_scaffolding = {
            "input": {  # dossier contenant toutes les données "entrées"
                "name": "__INPUTS__",
                "make": False
            },
            "output": {  # dossier contenant toutes les données "sorties"
                "name": "__OUTPUTS__",
                "make": False
            },
            "logs": {  # dossier contenant toutes les sorties "logs"
                "name": "__LOGS__",
                "make": True
            },
            "docs": {  # dossier contenant toutes les documentations/specs liées au projet
                "name": "__DOCS__",
                "make": False
            },
        }

        scaffolding = self._lz.merge_dictionaries(default_dir_scaffolding, {})

        if location:
            user_dir_scaffolding = config.DEFAULT_DIR_SCAFFOLDING
            if self._lz.is_validated_schema(user_dir_scaffolding,
                                            config.SCHEMA_DIR_SCAFFOLDING,
                                            True,
                                            config.DEFAULT_VERBOSE):
                scaffolding = self._lz.merge_dictionaries(config.DEFAULT_DIR_SCAFFOLDING, user_dir_scaffolding)

            self._lz.mkdir(location, dir_scaffolding=scaffolding, verbose=config.DEFAULT_VERBOSE)

            return self._lz.get_path_logs_dir(location)
        else:
            if self._output_2_log_file:
                self._lz.mkdir(dir_scaffolding=scaffolding)

            return self._lz.get_path_logs_dir()

    def _set_log_file_name(self, log_file_name):
        if log_file_name:
            return log_file_name + config.DEFAULT_LOGS_EXTENSION
        else:
            return self._lz.get_file_extension(
                self._caller_name
            )[0] + "_" + self._lz.get_timestamp() + config.DEFAULT_LOGS_EXTENSION

    def _set_field_styles(self, field_styles):
        self._field_styles = config.DEFAULT_FIELD_STYLES
        if field_styles:
            if self._lz.is_validated_schema(field_styles, config.SCHEMA_FIELD_STYLES, True, config.DEFAULT_VERBOSE):
                self._field_styles = self._lz.merge_dictionaries(config.DEFAULT_FIELD_STYLES, field_styles)
            else:
                sys.exit(1)

        return self._field_styles

    def _set_level_styles(self, level_styles):
        self._level_styles = config.DEFAULT_LEVEL_STYLES
        if level_styles:
            if self._lz.is_validated_schema(level_styles, config.SCHEMA_LEVEL_STYLES, True, config.DEFAULT_VERBOSE):
                self._level_styles = self._lz.merge_dictionaries(config.DEFAULT_LEVEL_STYLES, level_styles)
            else:
                sys.exit(1)

        return self._level_styles

    def _set_log_format(self, log_format):
        self._log_format = config.DEFAULT_LOG_FORMAT
        if log_format:
            if self._lz.is_validated_schema(log_format, config.SCHEMA_LOG_FORMAT, True, config.DEFAULT_VERBOSE):
                self._log_format = log_format
            else:
                sys.exit(1)

        return self._log_format

    def _set_log_date_format(self, log_date_format):
        self._log_date_format = config.DEFAULT_LOG_DATE_FORMAT
        if log_date_format:
            if self._lz.is_validated_schema(log_date_format,
                                            config.SCHEMA_LOG_DATE_FORMAT,
                                            True,
                                            config.DEFAULT_VERBOSE):
                self._log_date_format = log_date_format
            else:
                sys.exit(1)

        return self._log_date_format

    def _set_logger(self, line_no, init=False):
        # Create a filehandler object
        if line_no == 1 and init and self._output_2_log_file:
            try:
                self._fh = logging.FileHandler(self._location + "\\" + self._log_file_name, encoding="UTF-8")
            except OSError:  # gestion STDIN
                self._fh = logging.FileHandler(
                    self._location + "\\"
                    + config.DEFAULT_STDIN_LOGS_NAME + "_" + self._lz.get_timestamp() + config.DEFAULT_LOGS_EXTENSION,
                    encoding="UTF-8"
                )

            self._fh.setLevel(self._log_level)

        cl.DEFAULT_FIELD_STYLES = self._field_styles
        cl.DEFAULT_LEVEL_STYLES = self._level_styles
        cl.DEFAULT_LOG_FORMAT = self._log_format
        cl.DEFAULT_DATE_FORMAT = self._log_date_format

        # Create a ColoredFormatter to use as formatter for the FileHandler
        if not init and self._output_2_log_file:
            formatter = cl.BasicFormatter(
                re.sub(
                    r"%\(\bhostname\b\)\d*s",
                    cl.find_hostname(),
                    re.sub(
                        r"%\(\busername\b\)\d*s",
                        cl.find_username(),
                        re.sub(
                            r"%\(\blineno\b\)\d*d",
                            str(line_no),
                            re.sub(
                                r"%\(\bfilename\b\)\d*s",
                                self._caller_name,
                                self._log_format
                            )
                        )
                    )
                )
            )
            self._fh.setFormatter(formatter)

        self._regex_match = re.match(r".*(%\(\blineno\b\))(\d+)(d).*", self._log_format)
        cl.install(
            level=self._log_level,
            fmt=re.sub(
                r"%\(\blineno\b\)\d*d",
                "{:0>{width}d}".format(line_no, width=self._regex_match.group(2)),
                re.sub(
                    r"%\(\bfilename\b\)\d*s",
                    self._caller_name,
                    self._log_format
                )
            )
        )

        self._logger = logging.getLogger(self._name)

        if init and self._output_2_log_file:
            self._logger.addHandler(self._fh)

    def _print_log_msg(self, print_log_level, message, trace_back):
        self._set_logger(self._lz.get_caller_line_number())
        print_log_level(message)

        style_2_apply = _style_trace_back()
        if config.DEFAULT_STACK_TRACE or trace_back:
            if config.DEFAULT_STACK_TRACE_2_FILE:
                print_log_level(tb.format(style=style_2_apply, source_lines=config.DEFAULT_CONTEXT_SOURCE_LINES))
            else:
                print(tb.show(style=style_2_apply, source_lines=config.DEFAULT_CONTEXT_SOURCE_LINES))

    def debug(self, message, trace_back=config.DEFAULT_STACK_TRACE):
        self._print_log_msg(self._logger.debug, message, trace_back)

    def info(self, message, trace_back=config.DEFAULT_STACK_TRACE):
        self._print_log_msg(self._logger.info, message, trace_back)

    def warning(self, message, trace_back=config.DEFAULT_STACK_TRACE):
        self._print_log_msg(self._logger.warning, message, trace_back)

    def error(self, message, trace_back=config.DEFAULT_STACK_TRACE):
        self._print_log_msg(self._logger.error, message, trace_back)

    def critical(self, message, trace_back=config.DEFAULT_STACK_TRACE):
        self._print_log_msg(self._logger.critical, message, trace_back)

    def __init__(self,
                 name=None, log_level=config.DEFAULT_LOG_LEVEL,
                 output_2_log_file=True,
                 location=None, log_file_name=None,
                 field_styles=None, level_styles=None,
                 log_format=None, log_date_format=None
                 ):
        r"""
        :param name: indique le nom de la log en cours

            | :magenta:`valeur possibles`: `None/nom de la log`
            | :magenta:`valeur par défaut`: `None`

        :param log_level: indique le niveau minimum d'alerte pour l'affichage des logs

            | :magenta:`valeur possibles`: `None/niveau d'alerte`
            | :magenta:`valeur par défaut`: `config.DEFAULT_LOG_LEVEL`

        :param output_2_log_file: indique s'il faut ou non écrire les logs dans un fichier en sortie

            | :magenta:`valeur possibles`: `False/True`
            | :magenta:`valeur par défaut`: `True`

        :param location: indique l'emplacement des fichiers logs de sortie

            | :magenta:`valeur possibles`: `None/chemin dossier logs`
            | :magenta:`valeur par défaut`: `None`

                * Si `location` non renseigné, par défaut, les logs seront enregistrés dans le dossier retourné par
                    :func:`corelibs.lazy.mkdir()`
                * Sinon les logs seront enregistrés dans le dossier `location\\DEFAULT_DIR_SCAFFOLDING["logs"]["name"]`

        :param log_file_name: indique le nom de la log

            | :magenta:`valeur possibles`: `None/nom de la log`
            | :magenta:`valeur par défaut`: `None`

                * Si `log_file_name` non renseigné, par défaut, le nom sera la concaténation des retours de :
                    * :func:`corelibs.lazy.get_module_name()`
                    * :func:`corelibs.lazy.get_file_extension()`
                    * :func:`corelibs.lazy.get_timestamp()`

                    i.e. :magenta:`nom_programme_AAAAMMDD_HHMMDD.log`, résultat de
                    :grey:`corelibs.lazy.get_file_extension(corelibs.lazy.get_module_name())[0]  + "_"
                    + corelibs.lazy.get_timestamp() + ".log"`


        :param field_styles: permet de définir le style d'affichage des logs dans la sortie standard

            | :magenta:`valeur possibles`: `None/dictionnaire`
            | :magenta:`valeur par défaut`: `None`

        :param level_styles: permet de définir le style d'affichage des niveaux d'alerte des logs dans la sortie
            standard

            | :magenta:`valeur possibles`: `None/dictionnaire`
            | :magenta:`valeur par défaut`: `None`

        :param log_format: permet de définir le format d'affichage de la log

            | :magenta:`valeur possibles`: `None/format d'affichage de la log`
            | :magenta:`valeur par défaut`: `None`

        :param log_date_format: permet de définir le format d'affichage horodaté de la log

            | :magenta:`valeur possibles`: `None/format d'affichage horodaté de la log`
            | :magenta:`valeur par défaut`: `None`

        .. note ::

            cf. :ref:`reference-label-config` :
                * `DEFAULT_LOG_LEVEL`
                * `DEFAULT_FIELD_STYLES`
                * `DEFAULT_LEVEL_STYLES`
                * `DEFAULT_DIR_SCAFFOLDING`
                * `DEFAULT_LOGS_EXTENSION`
                * `DEFAULT_LOG_FORMAT`
                * `DEFAULT_LOG_DATE_FORMAT`

        :green:`Exemple` :

        .. literalinclude:: ..\\..\\tests\\log\\termcolorlog.py
            :language: python

        """
        self._lz = lz

        self._caller_name = self._lz.get_caller_module_name()

        self._name = self._set_name(name)
        self._log_level = self._set_log_level(log_level)
        self._output_2_log_file = self._set_output_2_log_file(output_2_log_file)
        self._location = self._set_location(location)
        self._log_file_name = self._set_log_file_name(log_file_name)
        self._field_styles = self._set_field_styles(field_styles)
        self._level_styles = self._set_level_styles(level_styles)
        self._log_format = self._set_log_format(log_format)
        self._log_date_format = self._set_log_date_format(log_date_format)

        self._line_no = 1
        self._set_logger(self._line_no, init=True)

    @property
    def name(self):
        return self._name

    # @name.setter
    # def name(self, value):
    #     self._name = self._set_name(value)

    @property
    def log_level(self):
        return self._log_level

    # @log_level.setter
    # def log_level(self, value):
    #     self._log_level = self._set_log_level(value)

    @property
    def output_2_log_file(self):
        return self._output_2_log_file

    # @output_2_log_file.setter
    # def output_2_log_file(self, value):
    #     self._output_2_log_file = self._set_output_2_log_file(value)

    @property
    def location(self):
        return self._location

    # @location.setter
    # def location(self, value):
    #     self._location = self._set_location(value)

    @property
    def log_file_name(self):
        return self._log_file_name

    # @log_file_name.setter
    # def log_file_name(self, value):
    #     self._log_file_name = self._set_log_file_name(value)

    @property
    def field_styles(self):
        return self._field_styles

    # @field_styles.setter
    # def field_styles(self, value):
    #     self._field_styles = self._set_field_styles(value)

    @property
    def level_styles(self):
        return self._level_styles

    # @level_styles.setter
    # def level_styles(self, value):
    #     self._level_styles = self._set_level_styles(value)

    @property
    def log_format(self):
        return self._log_format

    # @log_format.setter
    # def log_format(self, value):
    #     self._log_format = self._set_log_format(value)

    @property
    def log_date_format(self):
        return self._log_date_format

    # @log_date_format.setter
    # def log_date_format(self, value):
    #     self._log_date_format = self._set_log_date_format(value)


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
    r"""
    .. admonition:: Description

        | Classe de base pour manipuler les logs colorées sur les sorties web Jupyter Notebooks.

        cf. :ref:`reference-label-config` pour la configuration par défaut (modifiable lors de l'instanciation de la
        classe)
    """

    def _print_log_msg(self, print_log_level, message, trace_back):
        print_log_level(message)

        style_2_apply = _style_trace_back()
        if config.DEFAULT_STACK_TRACE or trace_back:
            if config.DEFAULT_STACK_TRACE_2_FILE:
                print_log_level(tb.format(style=style_2_apply, source_lines=config.DEFAULT_CONTEXT_SOURCE_LINES))
            else:
                print(tb.show(style=style_2_apply, source_lines=config.DEFAULT_CONTEXT_SOURCE_LINES))

    def debug(self, message, trace_back=config.DEFAULT_STACK_TRACE):
        self._print_log_msg(self._logger.debug, message, trace_back)

    def info(self, message, trace_back=config.DEFAULT_STACK_TRACE):
        self._print_log_msg(self._logger.info, message, trace_back)

    def warning(self, message, trace_back=config.DEFAULT_STACK_TRACE):
        self._print_log_msg(self._logger.warning, message, trace_back)

    def error(self, message, trace_back=config.DEFAULT_STACK_TRACE):
        self._print_log_msg(self._logger.error, message, trace_back)

    def critical(self, message, trace_back=config.DEFAULT_STACK_TRACE):
        self._print_log_msg(self._logger.critical, message, trace_back)

    def __init__(self, log_level=config.DEFAULT_LOG_LEVEL):
        r"""
        :param log_level: indique le niveau minimum d'alerte pour l'affichage des logs

            | :magenta:`valeur possibles`: `None/niveau d'alerte`
            | :magenta:`valeur par défaut`: `config.DEFAULT_LOG_LEVEL`

        .. note ::

            cf. :ref:`reference-label-config` :
                * `DEFAULT_LOG_LEVEL`

        :green:`Exemple` :

        .. literalinclude:: ..\\..\\tests\\log\\jupytercolorlog.py
            :language: python

        .. image:: ..\\ss\\jupyter_color_log.png

        """
        try:
            from colorama import Fore, Back, Style
            self._fore = Fore
            self._back = Back
            self._style = Style

        except ImportError:
            print(_c._print_import_exception("colorama"))
            sys.exit(1)

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


class ColorLog(JupyterColorLog if lz.is_jupyter() else TermColorLog):
    r"""
    .. admonition:: Description

        | Classe de base pour manipuler les logs colorées sans distinctions en sortie terminal ou Jupyter Notebooks.

        cf. :ref:`reference-label-config` pour la configuration par défaut (modifiable lors de l'instanciation de la
        classe)

    .. note:: ColorLog instancie dynamiquement la classe TermColorLog ou JupyterColorLog

        pour plus de détails concernant les arguments :
            * cf. :class:`JupyterColorLog`
            * cf. :class:`TermColorLog`
    """
    if lz.is_jupyter():
        def __init__(self, log_level=config.DEFAULT_LOG_LEVEL):
            JupyterColorLog.__init__(self, log_level=config.DEFAULT_LOG_LEVEL)
    else:
        def __init__(self,
                     name=None, log_level=config.DEFAULT_LOG_LEVEL,
                     output_2_log_file=True,
                     location=None, log_file_name=None,
                     field_styles=None, level_styles=None,
                     log_format=None, log_date_format=None
                     ):
            if log_file_name is None:
                log_file_name = lz.get_file_extension(
                    lz.get_caller_module_name()
                )[0] + "_" + lz.get_timestamp()

            TermColorLog.__init__(self,
                                  name=name, log_level=log_level,
                                  output_2_log_file=output_2_log_file,
                                  location=location,
                                  log_file_name=log_file_name,
                                  field_styles=field_styles, level_styles=level_styles,
                                  log_format=log_format, log_date_format=log_date_format
                                  )


def get_elapsed_time(elapsed_seconds):
    if isinstance(elapsed_seconds, float):
        hours, rem = divmod(elapsed_seconds, 3600)
        minutes, seconds = divmod(rem, 60)

        return "{:0>2}:{:0>2}:{:05.2f}".format(int(hours), int(minutes), seconds)


def timing(log_handler=None):
    r"""
    .. admonition:: Description

        | Décorateur pour chronométrer le temps d'exécution de toutes fonctions cibles

    :param log_handler: indique si le timing doit faire une sortie dans un fichier log, défini via l'instanciation
        de cf. :class:`ColorLog` ou cf. :class:`TermColorLog`.

    :return:
        | :magenta:`rien...`

    :green:`Exemple` :

    .. literalinclude:: ..\\..\\tests\\log\\timing.py
        :language: python

    .. image:: ..\\ss\\decorator_timing.png

    """

    def actual_decorator(wrapped_func):
        @wraps(wrapped_func)
        def wrapper(*args, **kwargs):
            start = time()
            _ = wrapped_func(*args, **kwargs)
            end = time()
            elapsed_time = get_elapsed_time(end - start)

            if isinstance(log_handler, ColorLog) or isinstance(log_handler, TermColorLog):
                log_handler.info("{wrapped_func}() - durée totale exécution : {elapsed_time}"
                                 .format(wrapped_func=wrapped_func.__name__, elapsed_time=elapsed_time))
            else:
                cl.install(level=config.DEFAULT_LOG_LEVEL)
                log.info("{wrapped_func}() - Durée exécution : {elapsed_time}"
                         .format(wrapped_func=wrapped_func.__name__, elapsed_time=elapsed_time))

            return _

        return wrapper

    return actual_decorator


def status_bar(title=None):
    r"""
    .. admonition:: Description

        | Décorateur pour figer sur le terminal, tout en bas, l'état d'avancement.

        La barre de statut n'existe que pendant le temps de l'exécution de la fonction décorée (i.e. lors de
        l'appel d'une autre fonction, cette barre disparait si cette dernière fonction n'est elle-même pas décorée).

    :param title: permet de donner un label à la barre de statut

    :return:
        | :magenta:`rien...`

    :green:`Exemple` :

    .. literalinclude:: ..\\..\\tests\\log\\statusbars_decorator.py
        :language: python

    """
    def actual_decorator(wrapped_func):
        @wraps(wrapped_func)
        def wrapper(*args, **kwargs):
            _w_func_name = wrapped_func.__name__
            sb = StatusBars(title=(title if title else f"{_w_func_name}(...)"))

            _ = wrapped_func(*args, **kwargs)

            sleep(0.5)
            decorator_return["duration"]["status_bar"] = decorator_return["duration"]["total"] = sb.terminate()

            return _

        return wrapper

    return actual_decorator


def args_dumping(wrapped_func):
    r"""
    .. admonition:: Description

        | Décorateur pour lister tous les arguments passés dans une fonction décorée

        Le niveau minimal pour afficher les informations doit être de ``log.DEBUG`` (cf.
        :ref:`reference-label-config` pour plus d'informations `config.DEFAULT_LOG_LEVEL`)

    :green:`Exemple` :

    .. literalinclude:: ..\\..\\tests\\log\\args_dumping.py
        :language: python

    .. image:: ..\\ss\\decorator_args_dumping.png

    """

    def wrapper(*args, **kwargs):
        if config.DEFAULT_LOG_LEVEL == 10:
            func_args = inspect.signature(wrapped_func).bind(*args, **kwargs).arguments
            func_args_str = ", ".join(
                "{} = {!r}".format(*item) for item in func_args.items()
            )

            _ad_msg = f"@args_dumping : {wrapped_func.__module__}.{wrapped_func.__qualname__}({func_args_str})"

            cl.install(level=config.DEFAULT_LOG_LEVEL)
            if lz.is_jupyter():
                _jcl = JupyterColorLog(log_level=config.DEFAULT_LOG_LEVEL)
                _jcl.debug(_ad_msg)
            else:
                log.debug(_ad_msg)

        return wrapped_func(*args, **kwargs)

    return wrapper


def dict_dumping(wrapped_func):
    r"""
    .. admonition:: Description

        | Décorateur pour afficher toutes les fonctions qui retournent un dictionnaire dans un but de vérification.

        Le niveau minimal pour afficher les informations doit être de ``log.DEBUG`` (cf.
        :ref:`reference-label-config` pour plus d'informations `config.DEFAULT_LOG_LEVEL`)

    :green:`Exemple` :

    .. literalinclude:: ..\\..\\tests\\log\\dict_dumping.py
        :language: python

    .. image:: ..\\ss\\dict_dumping.png

    """

    def wrapper(*args, **kwargs):
        _ = wrapped_func(*args, **kwargs)
        if config.DEFAULT_LOG_LEVEL == 10:
            cl.install(level=config.DEFAULT_LOG_LEVEL)
            if isinstance(_, dict):
                log.debug("Dictionnaire détecté\n" + yaml.dump(_, allow_unicode=True))
            elif isinstance(_, tuple):
                log.debug("Tuple détecté\n" + yaml.dump(lz.convert_2_dict(_), allow_unicode=True))

        return wrapped_func(*args, **kwargs)

    return wrapper


class StopWatch:
    r"""
    .. admonition:: Description

        | Classe permettant de chronométrer un programme ou une portion de programme

        Le niveau minimal pour afficher les informations doit être de ``log.INFO`` (cf.
        :ref:`reference-label-config` pour plus d'informations `config.DEFAULT_LOG_LEVEL`)

    """

    def stop(self):
        r"""
        .. admonition:: Description

            | méthode pour arrêter le chronomètre

        :return:
            :magenta:`tuple nommé` avec comme attributs :
                * :magenta:`duration`
                * :magenta:`duration_in_second`
        """
        self._end = time()
        elapsed_time = get_elapsed_time(self._end - self._start)

        print("\n" * 2)
        if isinstance(self._log_handler, ColorLog) or isinstance(self._log_handler, TermColorLog):
            self._log_handler.info("{module_name} - Durée totale exécution : {elapsed_time}"
                                   .format(module_name=self._caller_module_name, elapsed_time=elapsed_time))

        if self._display_status_bar:
            self._sb.terminate()

        TotalDuration = namedtuple("TotalDuration", ["duration", "duration_in_second"])

        return TotalDuration(
            duration=elapsed_time,
            duration_in_second=self._end - self._start
        )

    def __init__(self, log_handler=None, display_status_bar=False):
        r"""
        :param log_handler: indique si le timing doit faire une sortie dans un fichier log, défini via l'instanciation
            de cf. :class:`ColorLog` ou cf. :class:`TermColorLog`.

        :param display_status_bar: indique s'il faut ou non afficher la barre de statut dans la sortie standard

            | :magenta:`valeur possibles`: `False/True`
            | :magenta:`valeur par défaut`: `False`

        :return:
            | :magenta:`rien...`

        :green:`Exemple` :

        .. literalinclude:: ..\\..\\tests\\log\\stopwatch.py
            :language: python

        .. image:: ..\\ss\\stopwatch.png

        """
        self._start = self._end = time()
        self._log_handler = log_handler
        self._caller_module_name = lz.get_caller_module_name()
        self._display_status_bar = display_status_bar

        if self._display_status_bar:
            self._sb = StatusBars(title=self._caller_module_name)

    @property
    def start(self):
        return self._start

    @property
    def end(self):
        return self._end


def stack_trace(force=config.DEFAULT_STACK_TRACE):
    r"""
    .. admonition:: Description

        | Décorateur pour afficher le détail des piles d'exécution (dans le cadre d'un débug).

    :param force: permet de forcer localement l'affichage détaillé

        cf. :ref:`reference-label-config` :
            * `DEFAULT_STACK_TRACE`
            * `DEFAULT_CONTEXT_SOURCE_LINES`

    :return:
        | :magenta:`rien...`

    :green:`Exemple` :

    .. literalinclude:: ..\\..\\tests\\log\\stack_trace.py
        :language: python

    .. image:: ..\\ss\\stack_trace.png

    """
    def actual_decorator(wrapped_func):
        @wraps(wrapped_func)
        def wrapper(*args, **kwargs):
            if config.DEFAULT_STACK_TRACE or force:
                tp = tb.TracePrinter(style="color")
                tp.enable()
                _ = wrapped_func(*args, **kwargs)
                tp.disable()
            else:
                _ = wrapped_func(*args, **kwargs)

            return _

        return wrapper

    return actual_decorator


def _is_valid_string(val):
    if val is not None and not isinstance(val, str):
        log.error(f"-[{config.PACKAGE_NAME}]- L'argument \"{val}\" doit être une chaîne de caractère")
        sys.exit(1)


def _is_valid_justify(justify):
    if not isinstance(justify, str) or not justify.upper() in ("CENTER", "LEFT", "RIGHT"):
        log.error(f"-[{config.PACKAGE_NAME}]- L'argument justify \"{justify}\" n'est pas reconnu. Valeurs possibles "
                  f"center, left ou right")
        sys.exit(1)


def _is_valid_integer(val):
    if not isinstance(val, int):
        log.error(f"-[{config.PACKAGE_NAME}]- L'argument \"{val}\" doit être "
                  f"un entier")
        sys.exit(1)


def _is_valid_statusbar_instance(obj):
    if not isinstance(obj, enlighten._statusbar.StatusBar):
        log.error(f"-[{config.PACKAGE_NAME}]- Le descripteur n'est pas une instance de StatusBars")
        sys.exit(1)


def _is_valid_progress_bar_instance(obj):
    if not isinstance(obj, (enlighten._counter.Counter, enlighten._counter.SubCounter)):
        log.error(f"-[{config.PACKAGE_NAME}]- Le descripteur n'est pas une instance de ProgressBars")
        sys.exit(1)


def _is_sub_process_descriptor_in_dict(sub_process_descriptor, desc_dict):
    if sub_process_descriptor not in desc_dict:
        log.error(f"-[{config.PACKAGE_NAME}]- Le descripteur \"{sub_process_descriptor}\" n'est pas présent dans le "
                  f"dictionnaire")
        sys.exit(1)


class StatusBars:
    r"""
    .. admonition:: Description

        | Classe permettant de créer une barre d'état figée pour afficher dynamiquement les différentes étapes ou
            processus, ainsi que des barres de progression.

        | Chaque barre de progression retour le temps intermédiaire passé par le processus ayant appelé cette barre de
            progression.

        | La classe StatusBars donne également le temps d'exécution total

    .. warning::

        | Les barres d'états ne fonctionnent que sur des terminaux et terminaux émulés (sous PyCharm par exemple
            voir **Run** > **Edit Configurations...** > **Execution** > **Emulate terminal in output console**)

    """
    justify = {
        "CENTER": enlighten.Justify.CENTER,
        "LEFT": enlighten.Justify.LEFT,
        "RIGHT": enlighten.Justify.RIGHT
    }

    def __init__(self, title=None, color="bold_cyan_on_white"):  # bold_black_on_cyan, bold_blue_on_white
        r"""
        :param title: indique le titre à donner à la barre d'état

        :param color: indique la couleur souhaitée pour la barre d'état

            | :magenta:`valeur possibles`: `black`, `red`, `green`, `yellow`, `blue`, `magenta`, `cyan` ou `white`
                (pour la couleur principale, comme pour la couleur du fond)

            * Pour chaque couleur, il y a 3 états possibles, `bold`, `bright` et `normal` (qui est le nom simple de la couleur)
            * Chaque couleur peut être combinée une fois avec un état cité ci-dessus, l'état doit précéder le nom de la couleur
            * La couleur principale et la couleur de fond se combinent avec le mot :red:`on`
            * Les mots sont liés par le caractère underscore `_`
            * Par exemple :green:`bold_black_on_bright_cyan`

        :return:
            | :magenta:`rien...`

        :green:`Exemple` :

        .. literalinclude:: ..\\..\\tests\\log\\statusbars.py
            :language: python

        .. image:: ..\\ss\\status_bar.gif

        .. image:: ..\\ss\\status_bar.png
        """
        _is_valid_string(title)

        self._sb_descriptor_dict = {}
        self._position = 2
        self._caller_module_name = lz.get_caller_module_name()
        self._total_start_time = time()

        self._sb_manager = enlighten.get_manager()
        self._main_sb = self._sb_manager.status_bar(
            status_format="• {title} • {fill} Éxécution : {status}",
            title=f"Programme \"{self._caller_module_name}\"" if title is None else title,
            color=color,
            status="EN COURS..."
        )

        self._sb_manager.status_bar(u"֍( corelibs.log.StatusBars )֎",
                                    position=1,
                                    fill="-",
                                    justify=enlighten.Justify.CENTER)

    def terminate(self):
        r"""
        .. admonition:: Description

            | Permet de terminer l'instance StatusBars et renvoie le temps total d'exécution

        :return:
            :magenta:`tuple nommé` avec comme attributs :
                * :magenta:`duration`
                * :magenta:`duration_in_second`

        """
        elapsed_time = time() - self._total_start_time
        duration = str(get_elapsed_time(elapsed_time))
        TotalDuration = namedtuple("TotalDuration", ["duration", "duration_in_second"])

        sleep(0.03)
        self._main_sb.update(status=f"o(^  ^ o) TERMINÉE • DURÉE TOTALE {duration} (o ^  ^)o")
        self._sb_manager.stop()
        print("\n")

        return TotalDuration(
            duration=duration,
            duration_in_second=elapsed_time
        )

    def _set_descriptor(self, sb_manager, sb_warning_manager=None, sb_error_manager=None):
        self._sb_descriptor_dict.update({
            self._position: {
                "manager": sb_manager,
                "warning": sb_warning_manager,
                "error": sb_error_manager,
                "start_time": time()
            }
        })
        self._position += 1

        return self._position - 1

    def init_sub_process(self, title=None, color="white", fill=" ", justify="center"):
        r"""
        .. admonition:: Description

            | Permet d'initialiser une nouvelle ligne de barre d'état pour gérer un processus enfant. Chaque processus
                enfant peut hériter d'une ou plusieurs barre d'état en utilisatant son descripteur

        .. note::

            | Il n'y a pas de limitations aux nombres de sous-barres d'état. Les affichages et utilisations de ces
                dernières sont ordonnés selon l'ordre d'appel de la méthode décrite ici

        :param title: indique le titre de la nouvelle sous barre d'état

        :param color: indique la couleur souhaitée pour le titre

        :param fill: indique le caractère de remplissage

        :param justify: indique la justification du texte

            | :magenta:`valeur possibles`: `left`, `center` ou `right`

        :return:
            | :magenta:`un descripteur`

        """
        _is_valid_string(title)
        _is_valid_justify(justify)

        _ = self._sb_manager.status_bar(
            status_format="{phases}",
            phases=title,
            position=self._position,
            fill=fill,
            justify=self.justify[justify.upper()],
            color=color
        )

        return self._set_descriptor(_)

    def update_sub_process(self, sub_process_descriptor, phases):
        r"""
        .. admonition:: Description

            | Permet de mettre à jour la sous-barre d'état

        :param sub_process_descriptor: indique le descripteur retourné par la méthode
            :func:`corelibs.log.StatusBars.init_sub_process`

        :param phases: indique et précise l'état si nécessaire

        :return:
            | :magenta:`rien...`

        """
        _is_valid_integer(sub_process_descriptor)
        _is_sub_process_descriptor_in_dict(sub_process_descriptor, self._sb_descriptor_dict)
        _ = self._sb_descriptor_dict[sub_process_descriptor]["manager"]
        _is_valid_statusbar_instance(_)

        sleep(0.3)
        _.update(phases=str(phases))

    def init_progress_bar(self,
                          total=100,
                          desc="Avancement :",
                          status_text="",
                          display_status=True,
                          color="green"):
        r"""
        .. admonition:: Description

            | Permet d'initialiser une nouvelle barre de progression

        .. note::

            | Il n'y a pas de limitations aux nombres de barres de progression. Les affichages et utilisations de ces
                dernières sont ordonnés selon l'ordre d'appel de la méthode décrite ici

        :param total: indique le total des itérations

        :param desc: indique la description à afficher pour la barre de progression

        :param status_text: indique et précise le texte de l'état si nécessaire

        :param display_status: indique l'affichage de l'état Succes/Warning/Error avec leur volumétrie totale

        :param color: indique la couleur de la barre de progression

        :return:
            | :magenta:`un descripteur`

        :green:`Exemple` :

        .. literalinclude:: ..\\..\\tests\\log\\progress_bar.py
            :language: python

        """
        _is_valid_integer(total)
        _is_valid_string(desc)

        bar_swe = self._sb_manager.term.green(u"S:{count_0:{len_total}d}") + " • " + self._sb_manager.term.yellow(
            u"W:{count_1:{len_total}d}") + " • " + self._sb_manager.term.red(u"E:{count_2:{len_total}d}") + " | "

        bar_format = u"{desc}{desc_pad}{percentage:3.0f}% | {bar} {status} " \
                     + (bar_swe if display_status else "") \
                     + u"{elapsed_time}"
        # u"{count_done:{len_total}d}/{count_total_2_process:{len_total}d} • " + \
        # u"(Traités/Total - Reste:{count_remain:{len_total}d}) • " + \
        # u"Temps écoulé {total_elapsed}"
        # u"[{elapsed}<{eta}, {rate:.2f}{unit_pad}{unit}/s]"

        _ = self._sb_manager.counter(total=total, desc=desc, color=color,
                                     status=("|" if status_text == "" else "| " + status_text + " |"),
                                     elapsed_time="Durée 00:00:00",
                                     bar_format=bar_format, position=self._position)
        warning_sb = _.add_subcounter(color="yellow", all_fields=True)
        error_sb = _.add_subcounter(color="red", all_fields=True)

        return self._set_descriptor(_, warning_sb, error_sb)

    def update_progress_bar(self,
                            progress_bar_descriptor,
                            status_text="",
                            status="success",
                            increment=1):
        r"""
        .. admonition:: Description

            | Permet de mettre à jour la barre de progression

        :param progress_bar_descriptor: indique le descripteur retourné par la méthode
            :func:`corelibs.log.StatusBars.init_progress_bar`

        :param status_text: indique et précise le texte de l'état si nécessaire

        :param status: indique et précise l'état d'avancement

            | :magenta:`valeur possibles`: `success`, `warning`, `error`
            | :magenta:`valeur par défaut`: `success`

        :param increment: indique la valeur incrémentale

        :return:
            :magenta:`tuple nommé` avec comme attributs :
                * :magenta:`duration`
                * :magenta:`duration_in_second`

        """
        _is_valid_integer(progress_bar_descriptor)
        _is_sub_process_descriptor_in_dict(progress_bar_descriptor, self._sb_descriptor_dict)

        sleep(0.03)
        elapsed_time = time() - self._sb_descriptor_dict[progress_bar_descriptor]["start_time"]
        duration = str(get_elapsed_time(elapsed_time))

        _ = None
        increment = increment
        if status.lower() in ("warning", "error"):
            increment = 0
            _ = self._sb_descriptor_dict[progress_bar_descriptor][status.lower()]
            _is_valid_progress_bar_instance(_)
            _.update()

        _ = self._sb_descriptor_dict[progress_bar_descriptor]["manager"]
        _is_valid_progress_bar_instance(_)
        _.update(incr=increment,
                 status=("|" if status_text == "" else "| " + status_text + " |"),
                 elapsed_time=f"Durée {duration}")

        StageDuration = namedtuple("StageDuration", ["duration", "duration_in_second"])

        return StageDuration(
            duration=duration,
            duration_in_second=elapsed_time
        )


def progress_bar(title=None, desc=None, desc_padding=32, color="green", terminate=False):
    r"""
    .. admonition:: Description

        | Décorateur pour afficher l'avancement des différentes étapes process sous forme de barre de progression


    :param title: indique le titre de la barre

    :param desc: indique la description à afficher pour la barre de progression

    :param desc_padding: indique la taille de rembourrage

    :param color: indique la couleur de la barre de progression

    :param terminate: indique au décorateur de clore les descripteurs et de libérer le terminal pour un affichage normal

    :return:
        | :magenta:`rien...`

    :green:`Exemple` :

    .. literalinclude:: ..\\..\\tests\\log\\progress_bar_decorator_version.py
        :language: python

    .. image:: ..\\ss\\progress_bar.gif

    .. image:: ..\\ss\\progress_bar.png

    """
    def actual_decorator(wrapped_func):
        @wraps(wrapped_func)
        def wrapper(*args, **kwargs):
            global status_bar_manager
            _w_func_name = wrapped_func.__name__

            if desc:
                _strip_desc = str(desc).strip(" ")

            _desc = (desc.rjust(desc_padding, " ") if desc else f"{_w_func_name}(...)".rjust(desc_padding, " ")) + " :"

            if status_bar_manager is None:
                status_bar_manager = StatusBars(title=(title if title else f"{_w_func_name}(...)"))

            pb_desc = status_bar_manager.init_progress_bar(
                total=1000,
                desc=_desc,
                color=color,
                display_status=False)
            sleep(0.5)
            decorator_return["duration"]["progress_bar"] = \
                decorator_return["duration"]["total"] = status_bar_manager.update_progress_bar(pb_desc, increment=1)

            _ = wrapped_func(*args, **kwargs)

            if terminate is False:
                decorator_return["duration"]["progress_bar"] = \
                    decorator_return["duration"]["total"] = \
                    status_bar_manager.update_progress_bar(pb_desc, increment=999)
            else:
                decorator_return["duration"]["progress_bar"] = \
                    status_bar_manager.update_progress_bar(pb_desc, increment=999)
                decorator_return["duration"]["total"] = status_bar_manager.terminate()

            return _

        return wrapper

    return actual_decorator
