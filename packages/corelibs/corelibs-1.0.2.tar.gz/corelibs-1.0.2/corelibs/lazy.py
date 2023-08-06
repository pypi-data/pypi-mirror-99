r"""
.. module:: lazy.py
    :synopsis: Module de base avec des fonctions, décorateurs utiles, etc...

.. moduleauthor:: Michel TRUONG <michel.truong@gmail.com>

.. topic:: Description générale

    Module de base avec des fonctions, décorateurs utiles, etc...

"""
import datetime as dt
import getpass
import glob
import inspect
import os
import pathlib
import platform
import re
import shutil
import subprocess
import sys
from calendar import timegm
from collections import namedtuple

import yaml

import corelibs
from corelibs import _corelibs as _c, config

log = _c.log

try:
    import coloredlogs as cl
except ImportError:
    raise Exception(_c._print_import_exception("coloredlogs"))

try:
    from IPython import get_ipython
except ImportError:
    raise Exception(_c._print_import_exception("ipython"))

try:
    import schema as sc
except ImportError:
    raise Exception(_c._print_import_exception("schema"))

try:
    import yamale
except ImportError:
    raise Exception(_c._print_import_exception("yamale"))

try:
    import numba
except ImportError:
    raise Exception(_c._print_import_exception("numba"))

EPOCH_AS_FILETIME = 116444736000000000  # January 1, 1970 as MS file time
HUNDREDS_OF_NANOSECONDS = 10000000
CORELIBS_TMP_COPY_FOLDER = "__CORELIBS_TCF__"


def get_username():
    r"""
    .. admonition:: Description

        | Récupère le nom de l'utilisateur courant

    :return:
        | :magenta:`nom de l'utilisateur courant`

    :green:`Exemple` :

    .. literalinclude:: ..\\..\\tests\\lazy\\get_username.py
        :language: python

    """
    return getpass.getuser()


def get_hostname():
    r"""
    .. admonition:: Description

        | Récupère le nom de l'ordinateur courant

    :return:
        | :magenta:`nom de l'ordinateur courant`

    :green:`Exemple` :

    .. literalinclude:: ..\\..\\tests\\lazy\\get_hostname.py
        :language: python

    """
    return os.environ['COMPUTERNAME']


def is_validated_schema(data_2_validate,
                        schema,
                        is_dict_schema=True,
                        verbose=config.DEFAULT_VERBOSE,
                        ignore_errors=config.DEFAULT_IGNORE_ERROR):
    r"""
    .. admonition:: Description

        | Vérifie si une donnée est conforme au schéma descriptif. La donnée à éprouver est par défaut un dictionnaire
            autrement, c'est un fichier de configuration YAML.

    :param data_2_validate: donnée à valider

        | :magenta:`dictionnaire ou tuple` (si :red:`is_dict_schema` == :magenta:`True`)
        | ou
        | :magenta:`chemin absolu du fichier YAML à valider` (si :red:`is_dict_schema` == :magenta:`False`)

    :param schema: nom du schéma de référence

        | :magenta:`schéma` (si :red:`is_dict_schema` == :magenta:`True`)
        | ou
        | :magenta:`chemin absolu du schéma YAML permettant la validation` (si :red:`is_dict_schema` == :magenta:`False`)

    :param is_dict_schema: indique si le schéma est un dictionnaire ou un fichier YAML

        | :magenta:`valeurs possibles`: `False/True`
        | :magenta:`valeur par défaut`: `True`

    :param verbose: afficher ou non les messages d'info/alertes

        | :magenta:`valeurs possibles`: `False/True`
        | :magenta:`valeur par défaut`: `DEFAULT_VERBOSE` (cf. :ref:`reference-label-config`)

    :param ignore_errors: forcer l'exécution lorsqu'une erreur est levée

        | :magenta:`valeurs possibles`: `False/True`
        | :magenta:`valeur par défaut`: `False` (cf. `DEFAULT_IGNORE_ERROR` dans :ref:`reference-label-config`)

    :return:
        | :magenta:`Booléen`: `False/True`

    :green:`Exemple` :

    .. literalinclude:: ..\\..\\tests\\lazy\\is_validated_schema.py
        :language: python

    :green:`Exemple Schéma YAML` :

    .. literalinclude:: ..\\..\\tests\\lazy\\schema_conf_test.yaml
        :language: yaml

    :green:`Exemple fichier YAML à valider avec le schéma descriptif YAML` :

    .. literalinclude:: ..\\..\\tests\\lazy\\conf_test.yaml
        :language: yaml

    :green:`Terminal` :

    .. code-block:: bash

        $ python is_validated_schema.py  #illustration indicative non nécessairement représentative du code en exemple

    .. image:: ..\\ss\\is_well_formatted_schema_log.png

    """
    if is_dict_schema:
        if isinstance(data_2_validate, dict):
            msg = "Le dictionnaire passé"
        elif isinstance(data_2_validate, str):
            msg = "La chaine passée"
        elif isinstance(data_2_validate, (int, float)):
            msg = "Le nombre passé"
        else:
            msg = "La donnée passée"

        try:
            schema.validate(data_2_validate)
            if verbose:
                cl.install(level=config.DEFAULT_LOG_LEVEL)
                log.info(f"-[{config.PACKAGE_NAME}]- {msg} en argument est conforme par rapport au schéma descriptif "
                         f"requis")
            return True

        except sc.SchemaError as e:
            log.error(f"-[{config.PACKAGE_NAME}]- {msg} en argument n'est pas conforme par rapport au schéma descriptif"
                      f" requis")
            log.error(e)
            log.error("Argument en paramètre : ")
            log.error(data_2_validate)
            return False
    else:
        _data_2_validate_info = get_file_extension(data_2_validate)
        if ".yaml" not in _data_2_validate_info.file_extension and ".yml" not in _data_2_validate_info.file_extension:
            if not ignore_errors:
                log.error(f"-[{config.PACKAGE_NAME}]- Fichier de configuration YAML \"{data_2_validate}\" non reconnu "
                          f"pour la validation")
                sys.exit(1)

        _schema_info = get_file_extension(schema)
        if ".yaml" not in _schema_info.file_extension and ".yml" not in _schema_info.file_extension:
            if not ignore_errors:
                log.error(f"-[{config.PACKAGE_NAME}]- Fichier schéma YAML \"{schema}\" non reconnu pour la validation")
                sys.exit(1)

        if not is_file_exists(data_2_validate):
            if not ignore_errors:
                log.error(f"-[{config.PACKAGE_NAME}]- Fichier de configuration YAML \"{data_2_validate}\" non trouvé "
                          f"pour la validation")
                sys.exit(1)

        if not is_file_exists(schema):
            if not ignore_errors:
                log.error(f"-[{config.PACKAGE_NAME}]- Fichier schéma YAML \"{schema}\" non trouvé pour la validation")
                sys.exit(1)

        _schema = yamale.make_schema(schema)
        _data_2_validate = yamale.make_data(data_2_validate)
        try:
            yamale.validate(_schema, _data_2_validate)
            if verbose:
                cl.install(level=config.DEFAULT_LOG_LEVEL)
                log.info(f"-[{config.PACKAGE_NAME}]- Le fichier YAML \"{data_2_validate}\" est conforme au fichier de "
                         f"schéma descriptif YAML \"{schema}\"")

            return True
        except yamale.YamaleError as e:
            log.error(f"-[{config.PACKAGE_NAME}]- Le fichier YAML \"{data_2_validate}\" n'est pas conforme au fichier "
                      f"de schéma descriptif YAML \"{schema}\"")
            for result in e.results:
                for error in result.errors:
                    log.error("\t%s" % error)

            return False


def merge_dictionaries(merged_dictionary, dictionary_2_merge):
    r"""
    .. admonition:: Description

        | Permet de fusionner 2 dictionnaires ensemble
        | :red:`\/!\\ ATTENTION \/!\\` L'ordre des dictionnaires en argument est important!

    :param merged_dictionary: dictionnaire conteneur destiné à recevoir le résultat de la fusion

    :param dictionary_2_merge: dictionnaire à fusionner

    :return:
        | :magenta:`dictionnaire résultat de la fusion`
        | ou
        | :magenta:`None`

    :green:`Exemple` :

    .. literalinclude:: ..\\..\\tests\\lazy\\merge_dictionaries.py
        :language: python

    """
    try:
        if merged_dictionary is None or isinstance(merged_dictionary, (str, int, float)):
            # effet bord ou si a est une primitive
            merged_dictionary = dictionary_2_merge
        elif isinstance(merged_dictionary, list):
            # si liste, alors on ne peut qu'ajouter à la suite
            if isinstance(dictionary_2_merge, list):
                merged_dictionary.extend(dictionary_2_merge)
            else:
                merged_dictionary.append(dictionary_2_merge)
        elif isinstance(merged_dictionary, dict):
            if isinstance(dictionary_2_merge, dict):
                for key in dictionary_2_merge:
                    if key in merged_dictionary:
                        merged_dictionary[key] = merge_dictionaries(merged_dictionary[key], dictionary_2_merge[key])
                    else:
                        merged_dictionary[key] = dictionary_2_merge[key]
            else:
                # non dictionnaire avec dictionnaire
                return None
        else:
            # inconnu...
            return None
    except TypeError:
        return None

    return merged_dictionary


def get_timestamp(timestamp_format="DT", display_ms=False, only_ms=False):
    r"""
    .. admonition:: Description

        | Retourne un timestamp normalisé ; utile pour suffixer les noms des fichiers

    :param timestamp_format: timestamp_format souhaité du timestamp
        | :magenta:`valeurs possibles`: `DT, D, T, NOW, GD ou GT`
        | :magenta:`valeur par défaut`: `DT`

    :param display_ms: afficher ou non les milli secondes

        | :magenta:`valeurs possibles`: `False/True`
        | :magenta:`valeur par défaut`: `False`

    :param only_ms: récupère seulement les millièmes de secondes (pratique si besoin d'un `seed`)

        | :magenta:`valeurs possibles`: `False/True`
        | :magenta:`valeur par défaut`: `False`

    :return:
        | :magenta:`timestamp`, selon timestamp_format :
        |    * YYYYMMDD_HHMMSS.SSSSSS
        |    * YYYYMMDD_HHMMSS
        |    * ou SSSSSS

    :green:`Exemple` :

    .. literalinclude:: ..\\..\\tests\\lazy\\get_timestamp.py
        :language: python

    :green:`Terminal` :

    .. code-block:: bash

        $ python get_timestamp.py
        Le timestamp sans milli secondes est 20201025_182141
        Le timestamp en milli secondes est 457668
        Le timestamp avec milli secondes est 20201025_182141.457668
        Le timestamp avec la date seulement est 20201025
        Le timestamp avec l'heure seulement est 182141
        Le timestamp avec la date et l'heure sans retraitement est 2020-10-25 18:21:41
        Le timestamp avec la date sans retraitement est 2020-10-25
        Le timestamp avec l'heure sans retraitement est 18:21:41

    """
    date_time = str(dt.datetime.now()).split()
    date = date_time[0]
    time_ms = date_time[1]
    time = time_ms.split(".")[0]
    ms = time_ms.split(".")[1]
    time_stamp = None

    if only_ms:
        return ms

    if timestamp_format == "DT":
        time_stamp = "".join(date.split("-")) + "_" + "".join(time.split(":"))
    elif timestamp_format == "D":
        time_stamp = "".join(date.split("-"))
    elif timestamp_format == "T":
        time_stamp = "".join(time.split(":"))
    elif timestamp_format == "NOW":
        time_stamp = date + " " + time
    elif timestamp_format == "GD":
        time_stamp = date
    elif timestamp_format == "GT":
        time_stamp = time

    if display_ms:
        time_stamp = time_stamp + "." + ms

    return time_stamp


def is_file_exists(file_path, is_dir=False, ignore_errors=config.DEFAULT_IGNORE_ERROR):
    r"""
    .. admonition:: Description

        | Vérifie si le fichier existe ou non

    :param file_path: chemin du fichier/répertoire

    :param is_dir: indique si la vérification porte sur un dossier ou non

        | :magenta:`valeurs possibles`: `False/True`
        | :magenta:`valeur par défaut`: `False` (la vérification se fait sans distinction)

    :param ignore_errors: forcer l'exécution lorsqu'une erreur est levée

        | :magenta:`valeurs possibles`: `False/True`
        | :magenta:`valeur par défaut`: `False` (cf. `DEFAULT_IGNORE_ERROR` dans :ref:`reference-label-config`)

    :return:
        | :magenta:`True/False`


    :green:`Exemple` :

    .. literalinclude:: ..\\..\\tests\\lazy\\is_file_exists.py
        :language: python


    :green:`Terminal` :

    .. code-block:: bash

        $ python get_abspath.py
        Le fichier "D:\OneDrive\Documents\_TEST_\__LOGS__" existe
        Le fichier "D:\OneDrive\Documents\_TEST_\__LOGS__\Fichier.txt" existe
        Le fichier "D:\OneDrive\Documents\_TEST_\__LOGS__\Fichier.txt" existe et est un répertoire
        Le fichier "D:\OneDrive\Documents\_TEST_\__LOGS__\Fichier.txt" existe et n'est pas un répertoire

    """
    if file_path == "":
        return False

    file = pathlib.Path(file_path)

    if is_dir:
        try:
            if file.is_dir() and file.exists():
                return True
        except OSError:
            if not ignore_errors:
                log.error(f"-[{config.PACKAGE_NAME}]- Le nom du fichier est incorrect \"{file_path}\"")
                sys.exit(1)
            else:
                return False
    else:
        try:
            if file.exists():
                return True
        except OSError:
            if not ignore_errors:
                log.error(f"-[{config.PACKAGE_NAME}]- Le nom du fichier est incorrect \"{file_path}\"")
                sys.exit(1)
            else:
                return False

    return False


def _delete_files(file_path, verbose=config.DEFAULT_VERBOSE):
    try:
        pathlib.Path(file_path).unlink()

        if verbose:
            dir_path, file = get_dir_n_basename(file_path)
            cl.install(level=config.DEFAULT_LOG_LEVEL)
            log.info(f"-[{config.PACKAGE_NAME}]- Le fichier \"{file}\" a été correctement supprimé à l'emplacement "
                     f"\"{dir_path}\"")
    except FileNotFoundError:
        log.warning(f"-[{config.PACKAGE_NAME}]- Fichier ou répertoire inexistant")
    except PermissionError:
        log.critical(f"-[{config.PACKAGE_NAME}]- Habilitations insuffisantes ou chemin incorrect")
    except OSError:
        log.error(f"-[{config.PACKAGE_NAME}]- Le nom contient des caractères interdits")


def delete_files(file_path, extension="", remove_empty_dir=True, verbose=config.DEFAULT_VERBOSE):
    r"""
    .. admonition:: Description

        | Permet de supprimer des fichiers ou répertoires récursivement. La suppression peut se faire également en se
            basant sur plusieurs extensions différentes (cf. exemple)

    :param file_path: le chemin absolu du fichier ou du répertoire à supprimer

    :param extension: le(s) extension(s) ou modèle des fichiers à supprimer

        | :magenta:`valeurs possibles`: `expression régulière` pour désigner des extensions/modèles de nom de fichiers
        | :magenta:`valeur par défaut`: `rien` (pour éviter les erreurs...)

    :param remove_empty_dir: indique si il faut supprimer ou non le répertoire vidé

        | :magenta:`valeurs possibles`: `False/True`
        | :magenta:`valeur par défaut`: `True`

    :param verbose: afficher ou non les messages d'info/alertes

        | :magenta:`valeurs possibles`: `False/True`
        | :magenta:`valeur par défaut`: `DEFAULT_VERBOSE` (cf. :ref:`reference-label-config`)

    :return:
        | :magenta:`rien...`

    :green:`Exemple` :

    .. literalinclude:: ..\\..\\tests\\lazy\\delete_files.py
        :language: python

    """
    for _file_extensions in extension.split(","):
        if is_file_exists(file_path, is_dir=True) and _file_extensions:
            path = pathlib.Path(file_path)
            for _f in path.glob(_file_extensions):
                if _f.is_dir():
                    delete_files(_f, _file_extensions, remove_empty_dir, verbose)
                else:
                    _delete_files(_f, verbose)
        elif is_file_exists(file_path):
            _delete_files(file_path, verbose)

    if remove_empty_dir:
        try:
            pathlib.Path(file_path).rmdir()

            if verbose:
                cl.install(level=config.DEFAULT_LOG_LEVEL)
                log.info(f"-[{config.PACKAGE_NAME}]- Le dossier \"{file_path}\" a été correctement supprimé")
        except FileNotFoundError:
            log.warning(f"-[{config.PACKAGE_NAME}]- Fichier ou répertoire inexistant")
        except PermissionError:
            log.critical(f"-[{config.PACKAGE_NAME}]- Habilitations insuffisantes ou chemin incorrect")
        except OSError:
            log.error(f"-[{config.PACKAGE_NAME}]- Le dossier \"{file_path}\" n'est pas vide et ne peut pas être "
                      f"supprimé")


def get_abspath(root_dir_path, dir_2_join):
    r"""
    .. admonition:: Description

        | Retourne le chemin absolu normalisé à partir d'un couple (chemin, dossier)

    :param root_dir_path: le chemin absolu

    :param dir_2_join: le dosssier à concaténer au chemin absolu

    :return:
        | :magenta:`le chemin normalisé`

    :green:`Exemple` :

    .. literalinclude:: ..\\..\\tests\\lazy\\get_abspath.py
        :language: python

    :green:`Terminal` :

    .. code-block:: bash

        $ python get_abspath.py
        Le chemin absolu normalisé est "C:\documents\dir\toto"

    """
    return os.path.abspath(os.path.join(root_dir_path, dir_2_join))


def get_dir_n_basename(path):
    r"""
    .. admonition:: Description

        | Retourne un tuple (chemin, nom fichier ou nom répertoire) à partir d'un chemin absolu normalisé
            (e.g. "C:\\documents\\dir" retournera "dir" et "C:\\documents\\dir\\fichier.txt" retournera "fichier.txt")

    :param path: chemin absolu normalisé

    :return:
        :magenta:`tuple nommé` avec comme attributs :
            * :magenta:`dir_path`
            * :magenta:`base_name`

    :green:`Exemple` :

    .. literalinclude:: ..\\..\\tests\\lazy\\get_dir_n_basename.py
        :language: python

    :green:`Terminal` :

    .. code-block:: bash

        $ python get_dir_n_basename.py
        Le chemin est "C:\Users\M47624\corelibs\tests\lazy"
        Le fichier est "get_dir_n_basename.py"
        Le chemin est "C:\Users\M47624\corelibs\tests\lazy"
        Le fichier est "get_dir_n_basename.py"
        Le chemin est "C:\Users\M47624\corelibs\tests\lazy"
        Le fichier est "get_dir_n_basename.py"

    """
    DirPathnBaseName = namedtuple("DirPathnBaseName", ["dir_path", "base_name"])
    norm_path = os.path.normpath(path)

    return DirPathnBaseName(
        dir_path=os.path.dirname(norm_path),
        base_name=os.path.basename(norm_path)
    )


def get_caller_module_name():
    r"""
    .. admonition:: Description

        | Permet de connaître le nom du module source appelant un autre module.

    :return:
        :magenta:`nom du module appelant`

    :green:`Exemple` :

    .. literalinclude:: ..\\..\\tests\\lazy\\get_caller_module_name.py
        :language: python

    .. literalinclude:: ..\\..\\tests\\lazy\\caller_module_name.py
        :language: python

    :green:`Terminal` :

    .. code-block:: bash

        $ python caller_module_name.py
        Le nom du module python appelant est "caller_module_name.py"

    """
    try:
        frame_info = inspect.currentframe()
        frame_info = frame_info.f_back.f_back
        code = frame_info.f_code

        return get_dir_n_basename(code.co_filename).base_name
    except AttributeError:
        log.error(f"-[{config.PACKAGE_NAME}]- Aucune information disponible.")


def get_caller_line_number(back_level=3, ignore_errors=config.DEFAULT_IGNORE_ERROR):
    r"""
    .. admonition:: Description

        | Permet de connaître la ligne du module source appelant un autre module.

    :param back_level: profondeur d'appel de la fonction parent/enfant

        | :magenta:`valeurs possibles`: `entier`
        | :magenta:`valeur par défaut`: `3`

    :param ignore_errors: forcer l'exécution lorsqu'une erreur est levée

        | :magenta:`valeurs possibles`: `False/True`
        | :magenta:`valeur par défaut`: `False` (cf. `DEFAULT_IGNORE_ERROR` dans :ref:`reference-label-config`)

    :return:
        :magenta:`ligne du module appelant`

    :green:`Exemple` :

    .. literalinclude:: ..\\..\\tests\\lazy\\get_caller_line_number.py
        :language: python

    """
    try:
        frame_info = inspect.currentframe()
        for i in range(back_level):
            frame_info = frame_info.f_back
        return frame_info.f_lineno
    except AttributeError:
        if not ignore_errors:
            log.error(f"-[{config.PACKAGE_NAME}]- Aucune information disponible.")
            sys.exit(1)
    except TypeError:
        if not ignore_errors:
            log.error(f"-[{config.PACKAGE_NAME}]- la profondeur \"{back_level}\" n'est pas un entier")
            sys.exit(1)


def get_module_name():
    r"""
    .. admonition:: Description

        | Retourne le nom du module courant

    :return:
        :magenta:`nom module courant`

    :green:`Exemple` :

    .. literalinclude:: ..\\..\\tests\\lazy\\get_module_name.py
        :language: python

    """
    frame_info = inspect.stack()[1]
    module = inspect.getmodule(frame_info[0])

    return get_dir_n_basename(module.__file__).base_name


def get_file_extension(filename, extensions=True, split_extensions=False):
    r"""
    .. admonition:: Description

        | Retourne un tuple (nom fichier, .extension(s))

    :param filename: nom du fichier avec extension (avec ou sans chemin)

    :param extensions: précise si le fichier comporte des extensions composites ou non (e.g. ".tar.gz")

        | :magenta:`valeurs possibles`: `False/True`
        | :magenta:`valeur par défaut`: `True`

    :param split_extensions: dans le cas d'une extension composite (e.g. ".tar.gz") renvoie soit une chaine de
        caractère (i.e. ".tar.gz"), soit un tableau d'extensions (i.e. [".tar", ".gz"])

        | :magenta:`valeurs possibles`: `False/True`
        | :magenta:`valeur par défaut`: `False` (renvoie par défaut une chaine d'extensions composites)

    :return:
        :magenta:`tuple nommé` avec comme attributs :
            * :magenta:`file_name`
            * :magenta:`file_extension`

    :green:`Exemple` :

    .. literalinclude:: ..\\..\\tests\\lazy\\get_file_extension.py
        :language: python

    """
    if extensions:
        suffix = pathlib.Path(filename).suffixes

        if not split_extensions:
            suffix = "".join(suffix)
    else:
        suffix = pathlib.Path(filename).suffix

    FileExtension = namedtuple("FileExtension", ["file_name", "file_extension"])

    prefix = pathlib.Path(filename).stem.split('.')[0]

    return FileExtension(
        file_name=prefix,
        file_extension=suffix
    )


def get_module_path():
    r"""
    .. admonition:: Description

        | Retourne le chemin du script/programme python courant

    :return:
        | :magenta:`os.path.realpath(sys.argv[0])`
        | ou
        | :magenta:`os.path.dirname(os.path.realpath(sys.argv[0])))`

    :green:`Exemple` :

    .. literalinclude:: ..\\..\\tests\\lazy\\get_module_path.py
        :language: python

    :green:`Terminal` :

    .. code-block:: bash

        $ python get_module_path.py
        Le chemin du programme python est "C:\Users\M47624\corelibs\tests\lazy"

    """
    path = os.path.realpath(sys.argv[0])

    if os.path.isdir(path):
        return path

    return os.path.dirname(path)


def _mkdir(dir_path, verbose=config.DEFAULT_VERBOSE):
    try:
        dir_path, dir_2_make = get_dir_n_basename(dir_path)
        pathlib.Path(get_abspath(dir_path, dir_2_make)).mkdir(parents=True, exist_ok=False)
    except FileExistsError:
        if verbose:
            cl.install(level=config.DEFAULT_LOG_LEVEL)
            log.warning(f"-[{config.PACKAGE_NAME}]- Le dossier \"{dir_2_make}\" existe déjà à l'emplacement "
                        f"\"{dir_path}\"")
    except FileNotFoundError:
        log.warning(f"-[{config.PACKAGE_NAME}]- Fichier ou répertoire inexistant")
    except PermissionError:
        log.critical(f"-[{config.PACKAGE_NAME}]- Habilitations insuffisantes ou chemin incorrect")
    except OSError:
        log.error(f"-[{config.PACKAGE_NAME}]- Le nom contient des caractères interdits")
    else:
        if verbose:
            cl.install(level=config.DEFAULT_LOG_LEVEL)
            log.info(f"-[{config.PACKAGE_NAME}]- Le dossier \"{dir_2_make}\" a été correctement créé à l'emplacement "
                     f"\"{dir_path}\"")


def mkdir(location=None,
          make_scaffolding=True,
          dir_scaffolding=config.DEFAULT_DIR_SCAFFOLDING,
          verbose=config.DEFAULT_VERBOSE,
          ignore_errors=config.DEFAULT_IGNORE_ERROR):
    r"""
    .. admonition:: Description

        | Créer un répertoire standard ou une liste de répertoires de manière récursive ; si le ou les parents
            n'existent pas, ils seront créés (dans le cas d'une liste de répertoires cela permet de factoriser les
            instructions).

        Par défaut, lorsque `corelibs.lazy.mkdir()` est appelé, 4 répertoires en plus sont créés :
            * 1 pour recevoir les fichiers logs, nommé par défaut "__LOGS__"
            * 1 pour recevoir les sorties, nommé par défaut "__OUTPUTS__"
            * 1 pour recevoir les entrées, nommé par défaut "__INPUTS__"
            * 1 pour recevoir les documentations et/ou spécifications, nommé par défaut "__DOCS__"

    .. note::

        Les noms respectifs des répertoires modèles sont gérés par le dictionnaire
            `config.DEFAULT_DIR_SCAFFOLDING` (cf. :ref:`reference-label-config` pour les détails.)

        Il est possible de modifier les noms et/ou la création des répertoires modèles en chargeant un nouveau
        dictionnaire lors de l'appel de :func:`corelibs.lazy.mkdir()`, directement en argument ou via un écrasement de
        la constante ``DEFAULT_DIR_SCAFFOLDING``.

    :param location: la location du répertoire à créer.

        | :magenta:`valeurs possibles`: chemin absolu ou tuple/tableau de chemins absolus
        | :magenta:`valeur par défaut`: le chemin retourné par :func:`corelibs.lazy.get_module_path()`

    :param make_scaffolding: indique s'il faut ou non créer les dossiers "modèle"

        | :magenta:`valeurs possibles`: `Dictionnaire`
        | :magenta:`valeur par défaut`: `DEFAULT_DIR_SCAFFOLDING` (cf. :ref:`reference-label-config`)

    :param dir_scaffolding: dictionnaire définissant les noms des dossiers "modèle" et s'il faut ou non les créer
        unitairement

        | :magenta:`valeurs possibles`: `False/True`
        | :magenta:`valeur par défaut`: `True`

    :param verbose: afficher ou non les messages d'info/alertes

        | :magenta:`valeurs possibles`: `False/True`
        | :magenta:`valeur par défaut`: `DEFAULT_VERBOSE` (cf. :ref:`reference-label-config`)

    :param ignore_errors: forcer l'exécution lorsqu'une erreur est levée

        | :magenta:`valeurs possibles`: `False/True`
        | :magenta:`valeur par défaut`: `False` (cf. `DEFAULT_IGNORE_ERROR` dans :ref:`reference-label-config`)

    :return:
        | :magenta:`rien...`

    :green:`Exemple` :

    .. literalinclude:: ..\\..\\tests\\lazy\\make_directory.py
        :language: python

    :green:`Terminal` :

    .. code-block:: bash

        $ python mkdir.py  #illustration indicative non nécessairement représentative du code en exemple

    .. image:: ..\\ss\\mkdir_log.png

    """
    if location is None:
        dir_path = get_module_path()
    else:
        dir_path = location

    # dir_path_db = get_dir_n_basename(dir_path)
    # if not is_file_exists(dir_path_db.dir_path, is_dir=True):
    #     log.error(f"-[{config.PACKAGE_NAME}]- Le chemin \"{dir_path_db.dir_path}\" n'existe pas")
    #     sys.exit(1)

    if not is_validated_schema(dir_scaffolding, config.SCHEMA_DIR_SCAFFOLDING):
        if not ignore_errors:
            sys.exit(1)

    if not make_scaffolding:
        if isinstance(dir_path, str):
            _mkdir(dir_path, verbose)
        elif isinstance(dir_path, (list, tuple)):
            for dir in dir_path:
                _mkdir(dir, verbose)
    else:
        dir_scaffolding = merge_dictionaries(config.DEFAULT_DIR_SCAFFOLDING, dir_scaffolding)
        for key, val in dir_scaffolding.items():
            if val["make"]:
                if isinstance(dir_path, str):
                    _mkdir(get_abspath(dir_path, val["name"]), verbose)
                elif isinstance(dir_path, (list, tuple)):
                    for dir in dir_path:
                        _mkdir(get_abspath(dir, val["name"]), verbose)


def get_path_scaffold_directories(location=None):
    r"""
    .. admonition:: Description

        | Retourne les chemins absolus de tous les répertoires créés cf. :func:`corelibs.lazy.mkdir()`
            pour plus de détails.

    :param location: la location du répertoire racine contenant les répertoires modèles.

        | :magenta:`valeur par défaut`: le chemin retourné par :func:`corelibs.lazy.get_module_path()`

    :return:
        :magenta:`tuple nommé` avec comme attributs :
            * :magenta:`docs : chemin absolu du répertoire "__DOCS__"` (si existe)
            * :magenta:`input : chemin absolu du répertoire "__INPUTS__"` (si existe)
            * :magenta:`output : chemin absolu du répertoire "__OUTPUTS__"` (si existe)
            * :magenta:`logs : chemin absolu du répertoire "__LOGS__"` (si existe)

    :green:`Exemple` :

    .. literalinclude:: ..\\..\\tests\\lazy\\get_path_scaffold_directories.py
        :language: python

    """
    if location is None:
        dir_path = get_module_path()
    else:
        dir_path = location

    dirs = {"input": {}, "output": {}, "logs": {}, "docs": {}}
    for key, val in config.DEFAULT_DIR_SCAFFOLDING.items():
        dir_name = val["name"]
        abs_path = get_abspath(dir_path, dir_name)
        dirs[key] = abs_path if os.path.isdir(abs_path) else ""

    ScaffoldDir = namedtuple("ScaffoldDir", ["input", "output", "logs", "docs"])

    return ScaffoldDir(
        input=dirs["input"],
        output=dirs["output"],
        logs=dirs["logs"],
        docs=dirs["docs"]
    )


def get_path_input_dir(location=None):
    r"""
    .. admonition:: Description

        | Retourne le chemin absolu du répertoire des entrées, nommé par défaut "__INPUTS__" cf.
            :func:`corelibs.lazy.mkdir()` pour plus de détails.

    :param location: la location du répertoire racine contenant le répertoire des entrées.

        | :magenta:`valeur par défaut`: le chemin retourné par :func:`corelibs.lazy.get_module_path()`

    :return:
        | :magenta:`chemin absolu du répertoire "__INPUTS__"` (si existe, e.g. "C:\\Users\\M47624\\__INPUTS__")
        | ou
        | :magenta:`chaîne vide` (sinon)

    :green:`Exemple` :

    .. literalinclude:: ..\\..\\tests\\lazy\\get_path_input_dir.py
        :language: python

    """
    scaffold_dir_path = get_path_scaffold_directories(location).input
    if scaffold_dir_path:
        return scaffold_dir_path

    return ""


def get_path_output_dir(location=None):
    r"""
    .. admonition:: Description

        | Retourne le chemin absolu du répertoire des sorties, nommé par défaut "__OUTPUTS__" cf.
            :func:`corelibs.lazy.mkdir()` pour plus de détails.

    :param location: la location du répertoire racine contenant le répertoire des sorties.

        | :magenta:`valeur par défaut`: le chemin retourné par :func:`corelibs.lazy.get_module_path()`

    :return:
        | :magenta:`chemin absolu du répertoire "__OUTPUTS__"` (si existe, e.g. "C:\\Users\\M47624\\__OUTPUTS__")
        | ou
        | :magenta:`chaîne vide` (sinon)

    :green:`Exemple` :

    .. literalinclude:: ..\\..\\tests\\lazy\\get_path_output_dir.py
        :language: python

    """
    scaffold_dir_path = get_path_scaffold_directories(location).output
    if scaffold_dir_path:
        return scaffold_dir_path

    return ""


def get_path_docs_dir(location=None):
    r"""
    .. admonition:: Description

        | Retourne le chemin absolu du répertoire des docs/specs, nommé par défaut "__DOCS__" cf.
            :func:`corelibs.lazy.mkdir()` pour plus de détails.

    :param location: la location du répertoire racine contenant le répertoire des docs/specs.

        | :magenta:`valeur par défaut`: le chemin retourné par :func:`corelibs.lazy.get_module_path()`

    :return:
        | :magenta:`chemin absolu du répertoire "__DOCS__"` (si existe, e.g. "C:\\Users\\M47624\\__DOCS__")
        | ou
        | :magenta:`chaîne vide` (sinon)

    :green:`Exemple` :

    .. literalinclude:: ..\\..\\tests\\lazy\\get_path_docs_dir.py
        :language: python

    """
    scaffold_dir_path = get_path_scaffold_directories(location).docs
    if scaffold_dir_path:
        return scaffold_dir_path

    return ""


def get_path_logs_dir(location=None):
    r"""
    .. admonition:: Description

        | Retourne le chemin absolu du répertoire des logs, nommé par défaut "__LOGS__" cf.
            :func:`corelibs.lazy.mkdir()` pour plus de détails.

    :param location: la location du répertoire racine contenant le répertoire des logs.

        | :magenta:`valeur par défaut`: le chemin retourné par :func:`corelibs.lazy.get_module_path()`

    :return:
        | :magenta:`chemin absolu du répertoire "__LOGS__"` (si existe, e.g. "C:\\Users\\M47624\\__LOGS__")
        | ou
        | :magenta:`chaîne vide` (sinon)

    :green:`Exemple` :

    .. literalinclude:: ..\\..\\tests\\lazy\\get_path_logs_dir.py
        :language: python

    """
    scaffold_dir_path = get_path_scaffold_directories(location).logs
    if scaffold_dir_path:
        return scaffold_dir_path

    return ""


def is_stdin():
    r"""
    .. admonition:: Description

        | Permet de savoir si l'environnement sur lequel est exécuté le script python est un terminal standard ou non

    :return:
        | :magenta:`Booléen`: `False/True`

    """
    if sys.stdin.isatty():
        return True

    return False


def is_jupyter():
    r"""
    .. admonition:: Description

        | Permet de savoir si l'environnement sur lequel est exécuté le script python est Jupyter Notebook ou un
            terminal QTConsole Jupyter

    :return:
        | :magenta:`Booléen`: `False/True`

    :green:`Exemple` :

    .. literalinclude:: ..\\..\\tests\\lazy\\is_jupyter.py
        :language: python

    """
    try:
        ipy_conf = get_ipython().config
        for key, val in ipy_conf.items():
            if key == "IPKernelApp" and "jupyter" in val["connection_file"]:
                return True
    except AttributeError:
        return False


def is_interactive_python():
    r"""
    .. admonition:: Description

        | Permet de savoir si l'environnement sur lequel est exécuté le script python est un terminal Python interactive
            ou non (i.e. vs console ou terminal standard)

    :return:
        | :magenta:`Booléen`: `False/True`

    :green:`Exemple` :

    .. literalinclude:: ..\\..\\tests\\lazy\\is_interactive_python.py
        :language: python

    """
    return hasattr(sys, "ps1") or hasattr(sys, "ps2")


def is_platform(platform_os="Windows", ignore_errors=config.DEFAULT_IGNORE_ERROR):
    r"""
    .. admonition:: Description

        | Permet de vérifier le système d'exploitation sur lequel est lancé le script python

    :param platform_os: indique quel est la plateforme de référence à vérifier .

        | :magenta:`valeurs possibles`: "Windows", "Linux" ou "OSX"
        | :magenta:`valeur par défaut`: "Windows"

    :param ignore_errors: forcer l'exécution lorsqu'une erreur est levée

        | :magenta:`valeurs possibles`: `False/True`
        | :magenta:`valeur par défaut`: `False` (cf. `DEFAULT_IGNORE_ERROR` dans :ref:`reference-label-config`)

    :return:
        | :magenta:`Booléen`: `False/True`

    :green:`Exemple` :

    .. literalinclude:: ..\\..\\tests\\lazy\\is_platform.py
        :language: python

    """
    global current_platform

    os_list = ["Linux", "OSX", "Windows"]

    if sys.platform in "linux":
        current_platform = os_list[0]
    elif sys.platform == "darwin":
        current_platform = os_list[1]
    elif sys.platform == "win32":
        current_platform = os_list[2]

    if platform_os not in os_list:
        if not ignore_errors:
            log.error(f"-[{config.PACKAGE_NAME}]- La valeur \"{platform_os}\" n'existe pas (valeurs possibles : "
                      f"\"{os_list}\")")
            sys.exit(1)

    if platform_os == current_platform:
        return True

    return False


def epoch_2_datetime(seconds, time_format="%d/%m/%Y %H:%M:%S"):
    r"""
    .. admonition:: Description

        | Permet de convertir un nombre de secondes vers un format date/heure spécifié. L'epoch est le temps initial de
            référence, à partir duquel on mesure les secondes écoulées pour calculer les dates/heures. Sous UNIX/POSIX,
            ce temps correspond au 1 janvier 1970 00:00:00 UT et sous Windows NT, 1 janvier 1601 00:00:00 UT.

        | cf. :func:`corelibs.lazy.datetime_2_epoch()` pour la conversion inverse

    :param seconds: indique le nombre de secondes

    :param time_format: indique le format de sortie souhaité

        | :magenta:`valeur par défaut`: "%d/%m/%Y %H:%M:%S" (DD/MM/AAAA HH:MM:SS)

    :return:
        | :magenta:`timestamp`
        | ou
        | :magenta:`None` (si problème)

    :green:`Exemple` :

    .. literalinclude:: ..\\..\\tests\\lazy\\epoch_2_datetime.py
        :language: python

    """
    if is_validated_schema(time_format,
                           config.SCHEMA_DATE_TIME_FORMAT,
                           True,
                           config.DEFAULT_VERBOSE):
        try:
            return dt.datetime.fromtimestamp(seconds).strftime(time_format)
        except OSError as e:
            log.warning(f"-[{config.PACKAGE_NAME}]- Valeur \"{seconds}\" incorrecte \"{e}\"")
            return None

    return None


ZERO = dt.timedelta(0)
HOUR = dt.timedelta(hours=1)


class _UTC(dt.tzinfo):
    def utcoffset(self, _dt):
        return ZERO

    def tzname(self, _dt):
        return "UTC"

    def dst(self, _dt):
        return ZERO


utc = _UTC()


def datetime_2_epoch(date_time,
                     time_format="%d/%m/%Y %H:%M:%S",
                     reference_epoch="Unix",
                     ignore_errors=config.DEFAULT_IGNORE_ERROR):
    r"""
    .. admonition:: Description

        | Permet de convertir une date/heure en nombre de secondes écoulés depuis le temps de référence epoch.

        | cf. :func:`corelibs.lazy.epoch_2_datetime()` pour la conversion inverse

    :param date_time: date à convertir

    :param time_format: indique le format de la date et heure

        | :magenta:`valeur par défaut`: "%d/%m/%Y %H:%M:%S" (DD/MM/AAAA HH:MM:SS)

    :param reference_epoch: indique l'époque de référence

        | :magenta:`valeurs possibles`: "Unix", "Windows"
        | :magenta:`valeur par défaut`: "Unix"

    :param ignore_errors: forcer l'exécution lorsqu'une erreur est levée

        | :magenta:`valeurs possibles`: `False/True`
        | :magenta:`valeur par défaut`: `False` (cf. `DEFAULT_IGNORE_ERROR` dans :ref:`reference-label-config`)

    :return:
        | :magenta:`timestamp` au format epoch

    :green:`Exemple` :

    .. literalinclude:: ..\\..\\tests\\lazy\\datetime_2_epoch.py
        :language: python

    """
    global _dt

    date_time = date_time.strip()
    try:
        _dt = dt.datetime.strptime(date_time, time_format)
    except TypeError:
        if not ignore_errors:
            log.error(f"-[{config.PACKAGE_NAME}]- L'argument \"{date_time}\" n'est pas une date et heure valide")
            sys.exit(1)
    except ValueError:
        if not ignore_errors:
            log.error(f"-[{config.PACKAGE_NAME}]- L'argument \"{date_time}\" n'est pas au format \"{time_format}\"")
            sys.exit(1)

    if reference_epoch == "Unix":
        return int((_dt - dt.datetime.utcfromtimestamp(0)).total_seconds() * 1000)
    else:
        if (_dt.tzinfo is None) or (_dt.tzinfo.utcoffset(_dt) is None):
            _dt = _dt.replace(tzinfo=utc)
        return int(EPOCH_AS_FILETIME + (timegm(_dt.timetuple()) * HUNDREDS_OF_NANOSECONDS))


def reverse_named_tuple(named_tuple, convert_2_dict=False, ignore_errors=config.DEFAULT_IGNORE_ERROR):
    r"""
    .. admonition:: Description

        | Permet d'inverser l'ordre d'un tuple nommé.

    :param named_tuple: indique le tuple nommé à inverser

    :param convert_2_dict: indique s'il faut convertir ou non le tuple nommé en dictionnaire

        | :magenta:`valeurs possibles`: `False/True`
        | :magenta:`valeur par défaut`: `False`

    :param ignore_errors: forcer l'exécution lorsqu'une erreur est levée

        | :magenta:`valeurs possibles`: `False/True`
        | :magenta:`valeur par défaut`: `False` (cf. `DEFAULT_IGNORE_ERROR` dans :ref:`reference-label-config`)

    :return:
        | :magenta:`tuple nommé` avec le nom de classe et attributs tels que passés en argument
        | ou
        | :magenta:`dictionnaire` (conversion du tuple nommé)

    :green:`Exemple` :

    .. literalinclude:: ..\\..\\tests\\lazy\\reverse_named_tuple.py
        :language: python

    """
    if isinstance(named_tuple, tuple):
        if not convert_2_dict:
            nt_class = namedtuple(type(named_tuple).__name__, [name for name in named_tuple._fields][::-1])
            return nt_class(*[getattr(named_tuple, value) for value in named_tuple._fields][::-1])

        return dict(zip(*map(reversed, (named_tuple._fields, named_tuple))))

    log.error(f"-[{config.PACKAGE_NAME}]- L'argument \"{named_tuple}\" n'est pas un tuple")
    if not ignore_errors:
        sys.exit(1)


def get_bytes_size_formats(byte_size):
    r"""
    .. admonition:: Description

        | Permet de lister un tuple nommé contenant toutes les valeurs converties à partir d'une taille en octet.

    :param byte_size: indique le nombre d'octets

    :return:
        :magenta:`tuple nommé` avec comme attributs :
            * :magenta:`byte`
            * :magenta:`kilobyte`
            * :magenta:`megabyte`
            * :magenta:`gigabyte`
            * :magenta:`terabyte`

    :green:`Exemple` :

    .. literalinclude:: ..\\..\\tests\\lazy\\get_bytes_size_formats.py
        :language: python

    """
    ByteSize = namedtuple("ByteSize", [
        "byte", "kilobyte", "megabyte", "gigabyte", "terabyte"
    ])

    if byte_size < 0:
        log.warning(f"-[{config.PACKAGE_NAME}]- Le nombre d'octets \"{byte_size}\" passé en argument est négatif")

        return ByteSize(
            byte=0,
            kilobyte=0,
            megabyte=0,
            gigabyte=0,
            terabyte=0
        )

    return ByteSize(
        byte=byte_size,
        kilobyte=round(byte_size / float(1 << 10), 2),
        megabyte=round(byte_size / float(1 << 20), 2),
        gigabyte=round(byte_size / float(1 << 30), 2),
        terabyte=round(byte_size / float(1 << 40), 2)
    )


def get_bytes_size_4_human(
        byte_size_format,
        default_format=None,
        min_byte_size_format=config.DEFAULT_MIN_BYTE_SIZE_FORMAT,
        size_unit=True,
        ignore_errors=config.DEFAULT_IGNORE_ERROR):
    r"""
    .. admonition:: Description

        | Permet de lister un tuple nommé contenant toutes les valeurs converties à partir d'une taille en octet.

    :param byte_size_format: tuple nommé calculé par :func:`corelibs.lazy.get_bytes_size_formats()`

    :param default_format: format d'affichage souhaité
        | :magenta:`valeur par défaut`: None, laissant le choix à la fonction de retourner la meilleure valeur
        | :magenta:`valeurs possible`: "octet", "Ko", "Mo", "Go" ou "To"

    :param min_byte_size_format: lorsque le format d'affichage `default_format` est à None alors sera calculé
        automatiquement le meilleur format à afficher, dont les seuils minimums sont définis dans
        `DEFAULT_MIN_BYTE_SIZE_FORMAT` (cf. :ref:`reference-label-config`)

    :param size_unit: afficher l'unité de mesure

        | :magenta:`valeurs possibles`: `False/True`
        | :magenta:`valeur par défaut`: `True`

    :param ignore_errors: forcer l'exécution lorsqu'une erreur est levée

        | :magenta:`valeurs possibles`: `False/True`
        | :magenta:`valeur par défaut`: `False` (cf. `DEFAULT_IGNORE_ERROR` dans :ref:`reference-label-config`)

    :return:
        | :magenta:`string` sous la forme XX.XX Unité (où Unité est octet, Ko, Mo, Go ou To)
        | ou
        | :magenta:`float` (si l'unité de mesure n'est pas souhaitée)

    :green:`Exemple` :

    .. literalinclude:: ..\\..\\tests\\lazy\\get_bytes_size_4_human.py
        :language: python

    """
    if not is_validated_schema(min_byte_size_format,
                               config.SCHEMA_DEFAULT_MIN_BYTE_SIZE_FORMAT,
                               True,
                               config.DEFAULT_VERBOSE):
        if not ignore_errors:
            sys.exit(1)

    _b2o = {
        "byte": "octet",
        "kilobyte": "Ko",
        "megabyte": "Mo",
        "gigabyte": "Go",
        "terabyte": "To"
    }

    format_byte_size = merge_dictionaries({
        "octet": {"type": "byte", "min_size": 0},
        "Ko": {"type": "kilobyte", "min_size": 1},
        "Mo": {"type": "megabyte", "min_size": 1},
        "Go": {"type": "gigabyte", "min_size": 1},
        "To": {"type": "terabyte", "min_size": 0.5}
    }, min_byte_size_format)

    if isinstance(byte_size_format, tuple):
        if default_format is not None:
            try:
                val = getattr(byte_size_format, format_byte_size[default_format]["type"])
                val_s = "{0:,}".format(val).replace(",", " ")

                if size_unit:
                    if default_format == "octet":
                        return val_s + " " + default_format + "s" if val > 1 else val_s + " " + default_format

                    return val_s + " " + default_format
                else:
                    return val

            except KeyError:
                log.error(f"-[{config.PACKAGE_NAME}]- L'unité \"{default_format}\" passé en argument n'existe pas "
                          f"(valeurs possibles : octet, Ko, Mo, Go ou To)")
                if not ignore_errors:
                    sys.exit(1)
        else:
            for key, val in reverse_named_tuple(byte_size_format, convert_2_dict=True).items():
                if key == "byte" and val == 0:
                    return str(val) + " " + _b2o[key]

                if val > format_byte_size[_b2o[key]]["min_size"]:
                    val_s = "{0:,}".format(val).replace(",", " ")
                    if size_unit:
                        if _b2o[key] == "octet":
                            return val_s + " " + _b2o[key] + "s" if val > 1 else val_s + " " + _b2o[key]

                        return val_s + " " + _b2o[key]
                    else:
                        return val
    else:
        log.error(f"-[{config.PACKAGE_NAME}]- L'argument passé n'est pas un tuple nommé "
                  f"(cf. corelibs.lazy.get_bytes_size_formats()).")
        if not ignore_errors:
            sys.exit(1)


def is_namedtuple_instance(obj):
    r"""
    .. admonition:: Description

        | Permet de déterminer si l'objet passé en argument est une instance de tuple nommé.

    :param obj: un tuple nommé

    :return:
        | :magenta:`Booléen`: `False/True`

    :green:`Exemple` :

    .. literalinclude:: ..\\..\\tests\\lazy\\is_namedtuple_instance.py
        :language: python

    """
    _type = type(obj)
    bases = _type.__bases__

    if len(bases) != 1 or bases[0] != tuple:
        return False
    fields = getattr(_type, '_fields', None)
    if not isinstance(fields, tuple):
        return False

    return all(type(i) == str for i in fields)


def convert_2_dict(obj):
    r"""
    .. admonition:: Description

        | Permet de convertir tous les objets (convertissables) en dictionnaire de manière récursive.

    :param obj: objet à convertir

    :return:
        | :magenta:`dictionnaire`
        | ou
        | :magenta:`objet contenant un dictionnaire imbriqué converti`

    :green:`Exemple` :

    .. literalinclude:: ..\\..\\tests\\lazy\\convert_2_dict.py
        :language: python

    """
    if isinstance(obj, dict):
        return {key: convert_2_dict(value) for key, value in obj.items()}
    elif isinstance(obj, list):
        return [convert_2_dict(value) for value in obj]
    elif is_namedtuple_instance(obj):
        return {key: convert_2_dict(value) for key, value in obj._asdict().items()}
    elif isinstance(obj, tuple):
        return tuple(convert_2_dict(value) for value in obj)

    return obj


def _get_corelibs_path():
    return get_dir_n_basename(corelibs.__file__).dir_path


def _get_corelibs_abs_path(_dir="bin"):
    return get_abspath(_get_corelibs_path(), _dir)


def get_closest_value_in_list(value, list_of_values, ignore_errors=config.DEFAULT_IGNORE_ERROR):
    r"""
    .. admonition:: Description

        | Permet de récupérer la valeur la plus proche (en delta absolu) dans une liste de valeurs pour une valeur
            donnée.

    :param value: indique la valeur de référence

    :param list_of_values: liste de valeurs (tuples ou tableaux)

    :param ignore_errors: forcer l'exécution lorsqu'une erreur est levée

        | :magenta:`valeurs possibles`: `False/True`
        | :magenta:`valeur par défaut`: `False` (cf. `DEFAULT_IGNORE_ERROR` dans :ref:`reference-label-config`)

    :return:
        | :magenta:`valeur la plus proche trouvée`

    :green:`Exemple` :

    .. literalinclude:: ..\\..\\tests\\lazy\\get_closest_value_in_list.py
        :language: python

    """
    if not isinstance(value, (int, float)):
        log.error(f"-[{config.PACKAGE_NAME}]- L'argument \"{value}\" n'est pas une valeur numérique")
        if not ignore_errors:
            sys.exit(1)

    if not isinstance(list_of_values, (list, tuple)):
        log.error(f"-[{config.PACKAGE_NAME}]- L'argument \"{list_of_values}\" n'est pas une liste de valeurs")
        if not ignore_errors:
            sys.exit(1)

    for val in list_of_values:
        if not isinstance(val, (int, float)):
            log.error(f"-[{config.PACKAGE_NAME}]- La liste \"{list_of_values}\" contient des valeurs non numériques")
            if not ignore_errors:
                sys.exit(1)

    curr = list_of_values[0]
    for index in range(len(list_of_values)):
        if abs(value - list_of_values[index]) < abs(value - curr):
            curr = list_of_values[index]

    return curr


def get_home():
    r"""
    .. admonition:: Description

        | Permet de retrouver le chemin de l'utilisateur ("home")

    :return:
        | :magenta:`le chemin absolu du home`

    :green:`Exemple` :

    .. literalinclude:: ..\\..\\tests\\lazy\\get_home.py
        :language: python

    """
    return str(pathlib.Path.home())


def open_explorer(path):
    r"""
    .. admonition:: Description

        | Permet d'ouvrir dans l'explorateur en pointant directement sur le chemin passé en argument.

    :param path: indique le chemin à pointer

    :return:
        | :magenta:`rien...`

    :green:`Exemple` :

    .. literalinclude:: ..\\..\\tests\\lazy\\open_explorer.py
        :language: python

    """
    try:
        if platform.system() == "Windows":
            os.startfile(path)
        elif platform.system() == "Darwin":
            subprocess.Popen(["open", path])
        else:
            subprocess.Popen(["xdg-open", path])
    except FileNotFoundError:
        log.error(f"-[{config.PACKAGE_NAME}]- Le chemin \"{path}\" n'existe pas")
        sys.exit(1)


def _move(source, destination):
    if not is_file_exists(source):
        log.error(f"-[{config.PACKAGE_NAME}]- Le fichiers source \"{source}\" n'existe pas")
        sys.exit(1)

    source_db_name = get_dir_n_basename(source)
    destination_db_name = get_dir_n_basename(destination)

    if is_file_exists(get_abspath(destination_db_name.dir_path, destination_db_name.base_name), is_dir=True):
        if not is_file_exists(source, is_dir=True):
            destination = get_abspath(destination, source_db_name.base_name)

    try:
        if _is_validated_renamed_file_name(get_dir_n_basename(destination).base_name):
            shutil.move(source, destination)
    except OSError as e:
        log.error(f"-[{config.PACKAGE_NAME}]- {e}")


def _get_glob_from_source(source, destination):
    files = glob.glob(source)

    if not isinstance(destination, str):
        log.error(f"-[{config.PACKAGE_NAME}]- Le fichier de destination \"{destination}\" doit être un dossier pour "
                  f"recevoir les fichiers sources \"{files}\" (ayant pour modèle \"{source}\")")
        sys.exit(1)

    if not is_file_exists(destination, is_dir=True):
        mkdir(destination, make_scaffolding=False)

    return files


def move(source, destination):
    r"""
    .. admonition:: Description

        | Permet de déplacer un ou des fichiers vers une nouvelle destination ou des nouvelles destinations. Les
            fichiers sont au sens Unix du terme (i.e. soit fichier régulier, soit répertoire)

    :param source: indique l'emplacement source du ou des fichiers à déplacer avec le(s) chemin(s) absolu(s), avec ou
        sans schéma.

    :param destination: indique l'emplacement destination du ou des fichiers à déplacer avec le(s) chemin(s) absolu(s).

    :return:
        | :magenta:`rien...`

    :green:`Exemple` :

    .. literalinclude:: ..\\..\\tests\\lazy\\move.py
        :language: python

    """
    if isinstance(source, (list, tuple)) and isinstance(destination, (list, tuple)):
        if len(source) != len(destination):
            log.error(f"-[{config.PACKAGE_NAME}]- Les fichiers sources \"{source}\" et les fichiers \"{destination}\" "
                      f"doivent être 2 listes de même longueur")
            sys.exit(1)
        else:
            for s in range(len(source)):
                if "*" in source[s] and not is_file_exists(destination[s], is_dir=True):
                    log.warning(f"-[{config.PACKAGE_NAME}]- Le fichier source \"{source[s]}\" avec un schéma dans le "
                                f"nom doit être déplacé dans un dossier et \"{destination[s]}\" n'en est pas. Aucune "
                                f"action ne sera effectuée sur ce fichier...")
                else:
                    if "*" in source[s]:
                        files = glob.glob(source[s])
                        for f in files:
                            _move(f, destination[s])
                    else:
                        _move(source[s], destination[s])
    else:
        if isinstance(source, (list, tuple)):
            if not is_file_exists(destination, is_dir=True):
                mkdir(destination, make_scaffolding=False)

            for s in range(len(source)):
                if "*" in source[s]:
                    files = glob.glob(source[s])
                    for f in files:
                        _move(f, destination)
                else:
                    _move(source[s], destination)
        else:
            if "*" in source:
                files = _get_glob_from_source(source, destination)

                for f in files:
                    _move(f, destination)
            else:
                _move(source, destination)


def _copy(source, destination):
    if not is_file_exists(source):
        log.error(f"-[{config.PACKAGE_NAME}]- Le fichiers source \"{source}\" n'existe pas")
        sys.exit(1)

    destination_db_name = get_dir_n_basename(destination)
    destination_tmp = get_abspath(destination_db_name.dir_path, CORELIBS_TMP_COPY_FOLDER)

    try:
        if is_file_exists(source, is_dir=True):
            if not is_file_exists(destination, is_dir=True):
                try:
                    shutil.copytree(source, destination)
                except OSError as e:
                    log.error(f"-[{config.PACKAGE_NAME}]- {e}")
            else:
                shutil.copytree(source, destination_tmp)
                move(destination_tmp + "\\*", destination)
        else:
            shutil.copy2(source, destination)
    except OSError as e:
        log.error(f"-[{config.PACKAGE_NAME}]- {e}")

    try:
        shutil.rmtree(destination_tmp)
    except OSError:
        pass


def copy(source, destination):
    r"""
    .. admonition:: Description

        | Permet de copier un ou des fichiers vers une nouvelle destination ou des nouvelles destinations. Les
            fichiers sont au sens Unix du terme (i.e. soit fichier régulier, soit répertoire)

    .. warning::

        | La copie lèvera une alerte si des sous répertoires destinations existent et portent les mêmes noms que les
            sous répertoire sources.

    :param source: indique l'emplacement source du ou des fichiers à copier avec le(s) chemin(s) absolu(s), avec ou sans
        schéma.

    :param destination: indique l'emplacement destination du ou des fichiers à copier avec le(s) chemin(s) absolu(s).

    :return:
        | :magenta:`rien...`

    :green:`Exemple` :

    .. literalinclude:: ..\\..\\tests\\lazy\\copy_files.py
        :language: python

    """
    if isinstance(source, (list, tuple)) and isinstance(destination, (list, tuple)):
        if len(source) != len(destination):
            log.error(f"-[{config.PACKAGE_NAME}]- Les fichiers sources \"{source}\" et les fichiers \"{destination}\" "
                      f"doivent être 2 listes de même longueur")
            sys.exit(1)
        else:
            for s in range(len(source)):
                if "*" in source[s] and not is_file_exists(destination[s], is_dir=True):
                    log.warning(f"-[{config.PACKAGE_NAME}]- Le fichier source \"{source[s]}\" avec un schéma dans le "
                                f"nom doit être copié dans un dossier et \"{destination[s]}\" n'en est pas. Aucune "
                                f"action ne sera effectuée sur ce fichier...")
                else:
                    if "*" in source[s]:
                        files = glob.glob(source[s])
                        for f in files:
                            _copy(f, destination[s])
                    else:
                        _copy(source[s], destination[s])
    else:
        if isinstance(source, (list, tuple)):
            if not is_file_exists(destination, is_dir=True):
                mkdir(destination, make_scaffolding=False)

            for s in range(len(source)):
                if "*" in source[s]:
                    files = glob.glob(source[s])
                    for f in files:
                        _copy(f, destination)
                else:
                    _copy(source[s], destination)
        else:
            if "*" in source:
                files = _get_glob_from_source(source, destination)

                for f in files:
                    _copy(f, destination)
            else:
                _copy(source, destination)


def _has_sequence(file_name, total_index=1):
    try:
        regex_sequence = r"(%{)(\d+)(})"
        res = re.compile(regex_sequence)
        _groups = res.search(file_name).groups()

        if int(_groups[1]) == 0:
            new_file_name = re.sub(regex_sequence, str(total_index), file_name)
        else:
            new_file_name = re.sub(regex_sequence, str(total_index).rjust(int(_groups[1]), "0"), file_name)

        return new_file_name
    except AttributeError:
        return file_name


def _is_validated_renamed_file_name(replace):
    forbidden_char = r"[\\\/:*?\"<>\|]"
    rec = re.compile(forbidden_char)
    if rec.search(replace):
        log.error(f"-[{config.PACKAGE_NAME}]- Le nouveau nom \"{replace}\" contient des caractères interdits "
                  f"\"\\/:*?\"<>|\". Aucune action sera appliquée.")

        return False

    return True


def _has_regex_pattern(pattern, replace):
    regex_p_char = r"[(\\)]"  # r"[\\\/:*?^$\-<>,|+()\[\]]"
    recp = re.compile(regex_p_char)
    regex_r_char = r"[\\]"
    recr = re.compile(regex_r_char)
    if recp.search(pattern) and recr.search(replace):
        return True

    if not recp.search(pattern):
        log.error(f"-[{config.PACKAGE_NAME}]- Aucun schéma avec sous groupes détecté dans les noms des fichiers "
                  f"sources \"{pattern}\". Aucune action sera appliquée.")
        return False

    if not recr.search(pattern):
        log.error(f"-[{config.PACKAGE_NAME}]- Aucun schéma de regroupement détecté dans les noms des fichiers finaux "
                  f"\"{replace}\". Aucune action sera appliquée.")
        return False

    log.error(f"-[{config.PACKAGE_NAME}]- Aucun schéma détecté dans les noms \"{pattern}\" et \"{replace}\". Aucune "
              f"action sera appliquée.")

    return False


def _str_transformation(group_array, index, transformation):
    if transformation == "U":
        new_name = group_array[int(index) - 1].upper()
    elif transformation == "L":
        new_name = group_array[int(index) - 1].lower()
    elif transformation == "C":
        new_name = group_array[int(index) - 1].capitalize()
    elif transformation == "T":
        new_name = group_array[int(index) - 1].title()
    elif transformation == "S":
        new_name = group_array[int(index) - 1].swapcase()

    return new_name


def _regex_transform(pattern, replace, file_name, transform):
    rec = re.compile(pattern, re.IGNORECASE)
    _groups = rec.search(file_name).groups()

    _transformation_group = {}
    _transform = transform.upper().split("\\")
    ret = re.compile(r"([ULCTS])\d+")
    for _t in _transform:
        if ret.search(_t):
            _transformation_group.update({_t[1:]: _t[0:1]})

    new_name = ""
    _replace = replace.split("\\")
    rer = re.compile(r"^(\d+)(.*)$")
    for _r in _replace:
        if _r and rer.match(_r):
            _sub_r = rer.search(_r).groups()
            if _sub_r[1] == "":
                if _r in _transformation_group:
                    new_name += _str_transformation(_groups, _r, _transformation_group[_r])
                else:
                    new_name += _groups[int(_sub_r[0]) - 1]
            elif _sub_r[1]:
                if _sub_r[0] in _transformation_group:
                    new_name += _str_transformation(_groups, _sub_r[0], _transformation_group[_sub_r[0]])
                    new_name += _sub_r[1]
                else:
                    new_name += _groups[int(_sub_r[0]) - 1] + _sub_r[1]
            else:
                new_name += _groups[int(_r) - 1]
        else:
            new_name += _r

    return new_name


def _rename(path, pattern, replace, transform=None, debug=False, verbose=config.DEFAULT_VERBOSE):
    files = glob.glob(path + r"\*")
    rep = re.compile(pattern, re.IGNORECASE)
    sequence_index = 0

    for f in files:
        if rep.search(f):
            _f = get_dir_n_basename(f)
            sequence_index += 1
            if transform is not None:
                new_name = _has_sequence(
                    _regex_transform(pattern, replace, _f.base_name, transform),
                    sequence_index
                )
            else:
                new_name = _has_sequence(
                    re.sub(pattern, replace, _f.base_name),
                    sequence_index
                )

            if debug:
                if _is_validated_renamed_file_name(new_name):
                    log.debug(f"-[{config.PACKAGE_NAME}]- \"{_f.base_name}\" -> \"{new_name}\"")
                else:
                    log.error(f"-[{config.PACKAGE_NAME}]- \"{_f.base_name}\" -> None")
            else:
                _move(get_abspath(path, _f.base_name), get_abspath(path, new_name))
        else:
            if verbose:
                log.info(f"-[{config.PACKAGE_NAME}]- Le fichier \"{f}\" ne correspond pas au schéma \"{pattern}\"")


def rename(path, pattern, replace, transform=None, debug=True, verbose=config.DEFAULT_VERBOSE):
    r"""
    .. admonition:: Description

        | Permet de renommer à la volée des fichiers selon des schémas regex.

    .. note::

        | Cette fonction est un emballage de la fonction :func:`corelibs.lazy.move()`. A l'utiliser de préférence si
            c'est un renommage simple.

    .. warning::

        | Compte tenu des possibles dégâts liés aux erreurs de schéma regex, par défaut, la fonction s'exécute en mode
            :red:`debug` = :magenta:`True`

        | Pour que la fonction s'applique, il faut donc que le :red:`debug` soit positionné à :magenta:`False`
            **explicitement**.

    :param path: indique l'emplacement des fichiers sources à renommer en chemin absolu.

    :param pattern: indique le schéma regex des fichiers sources. Le schéma source doit contenir à minima des :red:`()`,
        listant les différents sous groupes. Un séquençace est possible également via les directives suivantes :

            * %{0} pour un séquençage sans padding
            * %{n} où n est un entier indiquant le nombre de 0 en padding

    :param replace: indique le schéma regex final de remplacement. Le schéma cible doit contenir à minima des :red:`\\n`
        où n est un entier représentant les sous groupes trouvés à partir du schéma source.

    :param transform: indique s'il y a des transformations à opérer ou non. Les transformations possibles sur le nom des
        fichiers cibles sont :

            * \\U\\n pour Uppercase sur le sous groupe identifié \n
            * \\L\\n pour Lowercase sur le sous groupe identifié \n
            * \\C\\n pour Capitalize (Premier mot en capitalizing) sur le sous groupe identifié \n
            * \\T\\n pour Title (Premier Mot En Title) sur le sous groupe identifié \n
            * \\S\\n pour Swapcase sur le sous groupe identifié \n

    :param debug: indique si la fonction doit s'appliquer ou tourner à blanc

        | :magenta:`valeurs possibles`: `False/True`
        | :magenta:`valeur par défaut`: `True`

    :param verbose: afficher ou non les messages d'info/alertes. Dans le cadre d'une utilisation regex, le verbose
        peut se comporter comme un véritable spam...!!! =þ

        | :magenta:`valeurs possibles`: `False/True`
        | :magenta:`valeur par défaut`: `DEFAULT_VERBOSE` (cf. :ref:`reference-label-config`)

    :return:
        | :magenta:`rien...`

    :green:`Exemple` :

    .. literalinclude:: ..\\..\\tests\\lazy\\rename.py
        :language: python

    """
    if not is_file_exists(path, is_dir=True):
        log.error(f"-[{config.PACKAGE_NAME}]- Le chemin \"{path}\" n'existe pas")
        sys.exit(1)

    old_log_level = config.DEFAULT_LOG_LEVEL
    if debug:
        cl.install(level=10)

    if is_file_exists(get_abspath(path, pattern), ignore_errors=True):
        replace = _has_sequence(replace)
        if debug:
            if _is_validated_renamed_file_name(replace):
                log.debug(f"-[{config.PACKAGE_NAME}]- \"{pattern}\" -> \"{replace}\"")
            else:
                log.error(f"-[{config.PACKAGE_NAME}]- \"{pattern}\" -> None")
        else:
            _move(get_abspath(path, pattern), get_abspath(path, replace))
    else:
        if _has_regex_pattern(pattern, replace):
            _rename(path, pattern, replace, transform, debug, verbose)

    cl.install(level=old_log_level)


def add_dir_path_2_project(path):
    r"""
    .. admonition:: Description

        | Permet d'inclure dans le projet actuel des programmes python tiers, enregistrés dans un emplacement différent.

    .. warning::

        | En principe, il est très rare de faire appel à cette fonction. Si cela se répète, il faudrait éventuellement
            revoir la structure du projet.

    :param path: indique l'emplacement en chemin absolu du **dossier** contenant le ou les programmes python à inclure
        dans le projet actuel.

    :return:
        | :magenta:`rien...`

    :green:`Exemple` :

    .. literalinclude:: ..\\..\\tests\\lazy\\_programme_importe.py
        :language: python

    .. literalinclude:: ..\\..\\tests\\lazy\\add_dir_path_2_project.py
        :language: python

    """
    if not is_file_exists(path, is_dir=True):
        log.error(f"-[{config.PACKAGE_NAME}]- Le chemin \"{path}\" n'existe pas")
        sys.exit(1)

    sys.path.append(os.path.abspath(path))


def _is_base_dir_path_existed_n_validated_file_name(dir_path, ignore_errors=config.DEFAULT_IGNORE_ERROR):
    _db = get_dir_n_basename(dir_path)
    if not is_file_exists(_db.dir_path):
        if not ignore_errors:
            log.error(f"-[{config.PACKAGE_NAME}]- Le répertoire de sortie \"{_db.dir_path}\" pour enregistrer "
                      f"le fichier \"{_db.base_name}\" n'existe pas")
            sys.exit(1)
        else:
            return None
    if not _is_validated_renamed_file_name(_db.base_name):
        if not ignore_errors:
            sys.exit(1)
        else:
            return None

    return get_abspath(_db.dir_path, _db.base_name)


def get_locale_tab(platform_os=None, yaml_dumping=True):
    r"""
    .. admonition:: Description

        | Liste l'ensemble des codes langues disponibles pour l'internationalisation (utilisé par
            :func:`corelibs.cleanse.is_datetime()` ou par le builtin :magenta:`locale.setlocale(...)` => cf.
            documentation officielle python)

    :param platform_os: indique quel est la plateforme de référence à vérifier

        | :magenta:`valeurs possibles`: "Windows", "Unix", "All" ou "None"
        | :magenta:`valeur par défaut`: "None"

    :param yaml_dumping: indique s'il faut afficher de manière lisible ou retourner la liste

    :return:
        | :magenta:`liste des codes` si :red:`yaml_dumping` == :magenta:`False`

    :green:`Exemple` :

    .. literalinclude:: ..\\..\\tests\\lazy\\get_locale_tab.py
        :language: python

    """
    _ = ""
    if platform_os is None:
        if is_platform("Windows"):
            _ = "Windows"
            data = config.LOCAL_TAB["Windows"]
        else:
            _ = "Unix"
            data = config.LOCAL_TAB["Unix"]
    else:
        if "all" in str(platform_os).lower():
            data = config.LOCAL_TAB
        elif platform_os == "Windows":
            _ = "Windows"
            data = config.LOCAL_TAB["Windows"]
        else:
            _ = "Unix"
            data = config.LOCAL_TAB["Unix"]

    if yaml_dumping:
        if _:
            log.info(f"\nListe des codes langues disponibles pour la plateforme {_}"
                     f"\n\n{yaml.dump(data, allow_unicode=True)}")
        else:
            log.info(f"\nListe des codes langues disponibles pour toutes les plateformes confondues"
                     f"\n\n{yaml.dump(data, allow_unicode=True)}")
    else:
        return data
