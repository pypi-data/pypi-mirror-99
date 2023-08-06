r"""
.. module:: cleanse.py
    :synopsis: Module pour purifier/nettoyer les données

.. moduleauthor:: Michel TRUONG <michel.truong@gmail.com>

.. topic:: Description générale

    Module pour purifier/nettoyer les données

"""
import datetime as dt
import inspect
import itertools
import locale
import re
import sys
from collections import namedtuple

import dask
import phonenumbers
import unicodedata
from email_validator import validate_email, EmailNotValidError

from corelibs import _corelibs as _c, config, lazy as lz

log = _c.log


def cleanse_file(file_path,
                 strip_non_breaking_space=True,
                 out_file_path=None,
                 cleansed_suffix="_CLEANSED",
                 time_stamp="DT",
                 encoding=config.DEFAULT_ENCODING_FILE,
                 ignore_errors=config.DEFAULT_IGNORE_ERROR
                 ):
    r"""
    .. admonition:: Description

        | Permet de purifier le fichier des caractères non imprimables, ainsi que les espaces insécables pouvant générer
            des erreurs lors des imports

    :param file_path: indique le fichier en entrée avec son chemin absolu

    :param strip_non_breaking_space: indique la suppression des espaces insécables

        | :magenta:`valeurs possibles`: `False/True`
        | :magenta:`valeur par défaut`: `True`

    :param out_file_path: indique le fichier en sortie avec son chemin absolu

    :param cleansed_suffix: indique le suffix à utiliser dans le nom de sortie (si :red:`out_file_path`
        == :magenta:`None`)

    :param time_stamp: indique le timestamp à appliquer dans le nom de sortie (si :red:`out_file_path`
        == :magenta:`None`)

        | :magenta:`valeurs possibles`: `DT`, `D`, `T` ou `None`
        | :magenta:`valeur par défaut`: `DT`

    :param encoding: indique l'encodage à la lecture/écriture

    :param ignore_errors: forcer l'exécution lorsqu'une erreur est levée

        | :magenta:`valeurs possibles`: `False/True`
        | :magenta:`valeur par défaut`: `False` (cf. `DEFAULT_IGNORE_ERROR` dans :ref:`reference-label-config`)

    :return:
        | :magenta:`rien...`

    :green:`Exemple` :

    .. literalinclude:: ..\\..\\tests\\cleanse\\cleanse_file.py
        :language: python

    """
    if not lz.is_file_exists(file_path):
        log.error(f"-[{config.PACKAGE_NAME}]- Le fichier \"{file_path}\" n'existe pas")
        sys.exit(1)

    out_file = None
    if out_file_path is not None:
        out_file = lz._is_base_dir_path_existed_n_validated_file_name(out_file_path, ignore_errors=ignore_errors)

    if out_file is None:
        file_path_db = lz.get_dir_n_basename(file_path)
        file_path_ext = lz.get_file_extension(file_path_db.base_name)
        out_file = lz.get_abspath(
            file_path_db.dir_path,
            f"{file_path_ext.file_name}{cleansed_suffix}"
            f"{'_' + lz.get_timestamp(time_stamp) if time_stamp in ('DT', 'D', 'T') else ''}"
            f"{file_path_ext.file_extension}"
        )

    re_np = re.compile("[%s]" % re.escape(control_chars))
    re_nbs = re.compile(r"\xA0+")
    with open(file_path, "r", encoding=encoding, errors="ignore" if ignore_errors else None) as f_in, \
            open(out_file, "w", encoding=encoding) as f_out:
        for line in f_in:
            string = re_np.sub("", line)
            if strip_non_breaking_space:
                string = re_nbs.sub("", string)
            f_out.write(string + "\n")


@dask.delayed
def _dd_replace(string, search, replace, regex_flag=None, encoding=config.DEFAULT_ENCODING_FILE):
    if not isinstance(string, str):
        log.error(f"-[{config.PACKAGE_NAME}]- L'argument string \"{string}\" n'est pas une chaîne de caractères.")
        sys.exit(1)

    if (isinstance(search, bytes) and not isinstance(replace, bytes)) \
            or (not isinstance(search, bytes) and isinstance(replace, bytes)):
        log.error(f"-[{config.PACKAGE_NAME}]- Le modèle de recherche \"{search}\" et le modèle de remplacement "
                  f"\"{replace}\" doivent être tous les 2 des modèles binaires")
        sys.exit(1)

    flags = re.M
    if regex_flag is not None:
        if not isinstance(regex_flag, re.RegexFlag):
            log.error(f"-[{config.PACKAGE_NAME}]- Les flags \"{regex_flag}\" ne sont pas des flags d'une instance "
                      f"regex.")
            sys.exit(1)

        if not lz.is_validated_schema(str(regex_flag), config.SCHEMA_REGEX_FLAGS, True, config.DEFAULT_VERBOSE):
            sys.exit(1)
        else:
            flags = regex_flag

    rec = re.compile(search, flags)
    if isinstance(search, bytes):
        return rec.sub(replace, string.encode(encoding=encoding)).decode(encoding=encoding)

    return rec.sub(replace, string)


def replace(string, search, replace, regex_flag=None, encoding=config.DEFAULT_ENCODING_FILE):
    r"""
    .. admonition:: Description

        | Permet de remplacer la valeur d'une chaine de caractères avec un modèle regex ou une expression simple

    :param string: chaine de caractères à traiter

    :param search: indique la chaine de caractères ou le modèle regex à chercher.

    :param replace: indique la chaine de caractères ou le modèle regex en remplacement.

    :param regex_flag: indique les flags à utiliser. cf. :ref:`reference-label-liens-utiles`, **Librairie regex** pour
        plus de détails

    :param encoding: indique l'encodage à la lecture/écriture

    :return:
        | :magenta:`chaine de caractères transformée`

    :green:`Exemple` :

    .. literalinclude:: ..\\..\\tests\\cleanse\\replace.py
        :language: python

    """
    _ = _dd_replace(string, search, replace, regex_flag=regex_flag, encoding=encoding)
    return _.compute()


def replace_chaining(string, **kwargs):
    r"""
    .. admonition:: Description

        | Wrapper de la fonction :func:`corelibs.cleanse.replace()` permettant de chaîner cette dernière, de manière à
            faciliter la lisibilité et optimiser les traitements de données

    :param string: chaine de caractères à traiter

    :param kwargs: liste dynamique d'arguments nommés. Cette liste accepte toutes les données loufoques. Cependant
        seules les fonctions :func:`corelibs.cleanse.replace()` et :func:`corelibs.cleanse.is_str()` seront traitées
        (cf. :green:`Exemple` pour plus de précisions)

    :return:
        | :magenta:`chaine de caractères transformée`

    :green:`Exemples` :

    .. literalinclude:: ..\\..\\tests\\cleanse\\replace_chaining.py
        :language: python

    .. literalinclude:: ..\\..\\tests\\cleanse\\replace_chaining_AL.py
        :language: python

    :green:`Exemple Appel depuis R` :

    .. literalinclude:: ..\\..\\tests\\cleanse\\treticulate_cleanse.r
        :language: R

    """
    if not isinstance(string, str):
        log.error(f"-[{config.PACKAGE_NAME}]- L'argument string \"{string}\" n'est pas une chaîne de caractères.")
        sys.exit(1)

    for index, (key, val) in enumerate(kwargs.items()):
        if callable(val):
            func_specs = inspect.getfullargspec(val)
            source = inspect.getsource(val)
            _msg = f"-[{config.PACKAGE_NAME}]- L'argument dynamique \"{key}={val.__name__}" \
                   f"({(', '.join(func_specs.args))})\" n'est pas une fonction replace() ou is_str(). " \
                   f"Aucune action ne sera appliquée."

            if val.__name__ == "<lambda>":
                if re.search(r"\b.*(replace|is_str).*\b", source):
                    _ = val
                    string = _(string)
                else:
                    log.warning(_msg)
            else:
                log.warning(_msg)
        else:
            log.warning(f"-[{config.PACKAGE_NAME}]- L'argument dynamique \"{key}={val}\" n'est pas une fonction "
                        f"appelable. Aucune action ne sera appliquée.")

    return string


@dask.delayed
def _dd_get_unicode_chars(unicode_categ=["Cc"]):
    return "".join(c for c in (chr(i) for i in range(sys.maxunicode)) if unicodedata.category(c) in unicode_categ) \
        .join(map(chr, itertools.chain(range(0x00, 0x20), range(0x7f, 0xa0))))


control_chars = _dd_get_unicode_chars().compute()
categ_char = None


@dask.delayed
def _dd_strip(string,
              search=None,
              replace="",
              non_printable_char=True,
              non_breaking_space=True,
              multi_space=True,
              empty_line=True,
              accented_char=False,
              num_char=False,
              unicode_categories=None,
              regex_flag=None,
              encoding=config.DEFAULT_ENCODING_FILE):
    global categ_char

    if not isinstance(string, str):
        log.error(f"-[{config.PACKAGE_NAME}]- L'argument string \"{string}\" n'est pas une chaîne de caractères.")
        sys.exit(1)

    flags = 0
    if regex_flag is not None:
        if not isinstance(regex_flag, re.RegexFlag):
            log.error(f"-[{config.PACKAGE_NAME}]- Les flags \"{regex_flag}\" ne sont pas des flags d'une instance "
                      f"regex.")
            sys.exit(1)

        if not lz.is_validated_schema(str(regex_flag), config.SCHEMA_REGEX_FLAGS, True, config.DEFAULT_VERBOSE):
            sys.exit(1)
        else:
            flags = regex_flag

    if non_printable_char:
        re_np = re.compile("[%s]" % re.escape(control_chars), flags=flags)
        if isinstance(replace, bytes):
            string = re_np.sub(replace.decode(), string)
        else:
            string = re_np.sub(replace, string)

    if non_breaking_space:
        re_nbs = re.compile(r"\xA0+", flags=flags)
        if isinstance(replace, bytes):
            string = re_nbs.sub(replace.decode(), string)
        else:
            string = re_nbs.sub(replace, string)

    if search is not None:
        rec = re.compile(search, flags=flags)
        if isinstance(search, bytes):
            if isinstance(search, bytes):
                if isinstance(replace, str):
                    string = rec.sub(
                        (
                            str.encode(replace)
                            if str.encode(replace) == b""
                            else str.encode(replace)
                        ),
                        string.encode(encoding=encoding)
                    ).decode(encoding=encoding)
                else:
                    string = rec.sub(
                        (
                            replace
                            if replace == b""
                            else replace
                        ),
                        string.encode(encoding=encoding)
                    ).decode(encoding=encoding)
        else:
            if isinstance(replace, bytes):
                string = rec.sub(replace.decode(), string)
            else:
                string = rec.sub(replace, string)

    if unicode_categories is not None and isinstance(unicode_categories, (str, list, tuple)):
        if categ_char is None:
            categ_char = _dd_get_unicode_chars(unicode_categories).compute()
        re_uc = re.compile("[%s]" % re.escape(categ_char), flags=flags)
        if isinstance(replace, bytes):
            string = re_uc.sub(replace.decode(), string)
        else:
            string = re_uc.sub(replace, string)

    if accented_char:
        string = "".join(c for c in unicodedata.normalize("NFD", string) if unicodedata.category(c) != "Mn")

    if num_char:
        re_nc = re.compile(r"([\-\/+* ,.:]*[0-9])", flags=flags)
        if isinstance(replace, bytes):
            string = re_nc.sub(replace.decode(), string)
        else:
            string = re_nc.sub(replace, string)

    if multi_space:
        if isinstance(search, bytes):
            re_ms = re.compile(b" +", flags=flags)
            if isinstance(replace, str):
                string = re_ms.sub((b" " if str.encode(replace) == b"" else str.encode(
                    replace)), string.encode()).decode()
            else:
                string = re_ms.sub((b" " if replace == b"" else replace),
                                   string.encode()).decode()

        else:
            re_ms = re.compile(r" +", flags=flags)
            if isinstance(replace, bytes):
                string = re_ms.sub((" " if replace.decode() == "" else replace.decode()), string)
            else:
                string = re_ms.sub((" " if replace == "" else replace), string)

    if empty_line:
        string = "".join([s for s in string.splitlines(True) if s.strip("\r\n")])

    return string


def strip(string,
          search=None,
          replace="",
          non_printable_char=True,
          non_breaking_space=True,
          multi_space=True,
          empty_line=True,
          accented_char=False,
          num_char=False,
          unicode_categories=None,
          regex_flag=None,
          encoding=config.DEFAULT_ENCODING_FILE):
    r"""
    .. admonition:: Description

        | Permet d'enlever des caractères ou chaines de caractères avec un modèle ou expression

    .. note::

        | strip() a le même comportement que :func:`corelibs.cleanse.replace()` si :red:`replace` prend une valeur
            différente de vide. l'intérêt de strip() est d'avoir des modèles prédéfinis pour purifier les fichiers
            et/ou des chaînes de caractères avec des caractères loufoques

    :param string: chaine de caractères à traiter

    :param search: indique la chaine de caractères ou le modèle regex à chercher (si les autres options ne répondent
        pas aux besoins).

    :param replace: indique le caractère ou la chaîne de caractères de remplacement (rien par
        défaut)

    :param non_printable_char: indique la suppression de tous les caracètres non imprimables

        | :magenta:`valeurs possibles`: `False/True`
        | :magenta:`valeur par défaut`: `True`

    :param non_breaking_space: indique la suppression de tous les espaces insécables (non breaking space)

        | :magenta:`valeurs possibles`: `False/True`
        | :magenta:`valeur par défaut`: `True`

    :param multi_space: indique la suppression des multiple espaces contigüs par un seul espace

        | :magenta:`valeurs possibles`: `False/True`
        | :magenta:`valeur par défaut`: `True`

    :param empty_line: indique la suppression des lignes vides

        | :magenta:`valeurs possibles`: `False/True`
        | :magenta:`valeur par défaut`: `True`

    :param accented_char: indique la suppression des caractères accentués

        | :magenta:`valeurs possibles`: `False/True`
        | :magenta:`valeur par défaut`: `False`

    :param num_char: indique la suppression des caractères contenant des valeurs numériques (formatées ou non)

        | :magenta:`valeurs possibles`: `False/True`
        | :magenta:`valeur par défaut`: `False`

    :param unicode_categories: permet de spécifier une classe de caractères Unicode à supprimer.

        | :magenta:`valeurs possibles`: `Liste ou Tuple de classe Unicode`
            (cf. |unicode_category_url| pour plus de détails sur les classifications des caractères Unicodes)

    :param regex_flag: indique les flags à utiliser. cf. :ref:`reference-label-liens-utiles`, **Librairie regex** pour
        plus de détails

    :param encoding: indique l'encodage à la lecture/écriture

    :return:
        | :magenta:`chaine de caractères transformée`

    :green:`Exemple` :

    .. literalinclude:: ..\\..\\tests\\cleanse\\strip.py
        :language: python

    """
    _ = _dd_strip(string,
                  search=search,
                  replace=replace,
                  non_printable_char=non_printable_char,
                  non_breaking_space=non_breaking_space,
                  multi_space=multi_space,
                  empty_line=empty_line,
                  accented_char=accented_char,
                  num_char=num_char,
                  unicode_categories=unicode_categories,
                  regex_flag=regex_flag,
                  encoding=encoding)
    return _.compute()


def strip_chaining(string, **kwargs):
    r"""
    .. admonition:: Description

        | Wrapper de la fonction :func:`corelibs.cleanse.strip()` permettant de chaîner cette dernière, de manière à
            faciliter la lisibilité et optimiser les traitements de données

    :param string: chaine de caractères à traiter

    :param kwargs: liste dynamique d'arguments nommés. Cette liste accepte toutes les données loufoques. Cependant
        seules les fonctions :func:`corelibs.cleanse.strip()` seront traitées (cf. :green:`Exemple` pour plus de
        précisions)

    :return:
        | :magenta:`chaine de caractères transformée`

    :green:`Exemple` :

    .. literalinclude:: ..\\..\\tests\\cleanse\\strip_chaining.py
        :language: python

    """
    if not isinstance(string, str):
        log.error(f"-[{config.PACKAGE_NAME}]- L'argument string \"{string}\" n'est pas une chaîne de caractères.")
        sys.exit(1)

    for index, (key, val) in enumerate(kwargs.items()):
        if callable(val):
            func_specs = inspect.getfullargspec(val)
            source = inspect.getsource(val)
            _msg = f"-[{config.PACKAGE_NAME}]- L'argument dynamique \"{key}={val.__name__}" \
                   f"({(', '.join(func_specs.args))})\" n'est pas une fonction strip(). Aucune action ne " \
                   f"sera appliquée."

            if val.__name__ == "<lambda>":
                if re.search(r"\b.*strip.*\b", source):
                    _ = val
                    string = _(string)
                else:
                    log.warning(_msg)
            else:
                log.warning(_msg)
        else:
            log.warning(f"-[{config.PACKAGE_NAME}]- L'argument dynamique \"{key}={val}\" n'est pas une fonction "
                        f"appelable. Aucune action ne sera appliquée.")

    return string


@dask.delayed
def _is_datetime(_dt, out_format, out_locale_time=config.DEFAULT_LOCALE_TIME, check_only=False):
    if isinstance(out_locale_time, str):
        try:
            locale.setlocale(locale.LC_TIME, out_locale_time)
        except locale.Error:
            log.error(f"-[{config.PACKAGE_NAME}]- Le paramètre out_locale_time \"{out_locale_time}\" n'est pas reconnu "
                      f"par le système, cf. la liste des codes langues disponibles ci-dessous")
            lz.get_locale_tab()
            sys.exit(1)
    else:
        log.error(f"-[{config.PACKAGE_NAME}]- Le paramètre out_local_time \"{out_locale_time}\" doit être au format "
                  f"chaîne de caractère")
        sys.exit(1)

    return True if check_only else _dt.strftime(out_format)


def is_datetime(dt_str,
                in_format="%d/%m/%Y %H:%M:%S",
                out_format="%d/%m/%Y %H:%M:%S",
                in_locale_time=config.DEFAULT_LOCALE_TIME,
                out_locale_time=config.DEFAULT_LOCALE_TIME,
                ignore_errors=config.DEFAULT_IGNORE_ERROR,
                check_only=False):
    r"""
    .. admonition:: Description

        | Vérifie si une chaîne est un datetime ou non.
        | Permet également de convertir le datetime vers un format souhaité
            (cf. |python_3_time_format_code_url| pour les formats)

    :param dt_str: indique la variable horodatée (datetime ou string)

    :param in_format: indique le format d'entrée (n'est pas nécessaire si le :magenta:`dt_str` est une instance de
        datetime)

    :param out_format: indique le format sortie

    :param in_locale_time: indique la langue de la date en entrée
        (cf. `DEFAULT_LOCALE_TIME` dans :ref:`reference-label-config`). Si chaîne vide, alors la langue utilisée sera
        celle définie par le système d'exploitation sur lequel est exécutée :func:`corelibs.cleanse.is_datetime()`

    :param out_locale_time: indique la langue de la date en sortie
        (cf. `DEFAULT_LOCALE_TIME` dans :ref:`reference-label-config`). Si chaîne vide, alors la langue utilisée sera
        celle définie par le système d'exploitation sur lequel est exécutée :func:`corelibs.cleanse.is_datetime()`

    :param ignore_errors: forcer l'exécution lorsqu'une erreur est levée

        | :magenta:`valeurs possibles`: `False/True`
        | :magenta:`valeur par défaut`: `False` (cf. `DEFAULT_IGNORE_ERROR` dans :ref:`reference-label-config`)

    :param check_only: permet de retourner un booléen au lieu de la chaîne de caractères transformée (utile dans le
        cas où il est seulement souhaité un contrôle, sans nécessairement une transformation pour éventuellement y
        appliquer une règle de gestion propre)

        | :magenta:`valeurs possibles`: `False/True`
        | :magenta:`valeur par défaut`: `False`

    :return:
        | :magenta:`booléen`: `False/True` si :red:`check_only` == :magenta:`True` (comportement par défaut)
        | ou
        | :magenta:`chaine vide` (si forcé)
        | ou
        | :magenta:`None` (si forcé lorsque :red:`dt_str` est une instance de datetime)
        | ou
        | :magenta:(str)`datetime` au format défini via :red:`out_format`

    :green:`Exemple` :

    .. literalinclude:: ..\\..\\tests\\cleanse\\is_str_datetime.py
        :language: python

    """
    if isinstance(dt_str, dt.datetime):
        return _is_datetime(dt_str, out_format, out_locale_time, check_only).compute()

    if isinstance(in_locale_time, str):
        try:
            locale.setlocale(locale.LC_TIME, in_locale_time)
        except locale.Error:
            log.error(f"-[{config.PACKAGE_NAME}]- Le paramètre in_local_time \"{in_locale_time}\" n'est pas reconnu "
                      f"par le système, cf. la liste des codes langues disponibles ci-dessous")
            lz.get_locale_tab()
            sys.exit(1)

    try:
        dt_str = dt.datetime.strptime(dt_str, in_format).strftime(in_format)
    except ValueError:
        if not ignore_errors:
            log.error(f"-[{config.PACKAGE_NAME}]- L'argument \"{dt_str}\" n'est pas au bon format \"{in_format}\"")
            sys.exit(1)
        else:
            return False if check_only else ""

    try:
        if isinstance(dt_str, dt.datetime):
            if out_format is None or out_format == "":
                return False if check_only else None

            return _is_datetime(dt_str, out_format, out_locale_time, check_only).compute()
        else:
            _dt = dt.datetime.strptime(dt_str, in_format)
            assert dt_str == _dt.strftime(in_format)
            if out_format is None or out_format == "":
                return False if check_only else ""

            return _is_datetime(_dt, out_format, out_locale_time, check_only).compute()
    except ValueError:
        if not ignore_errors:
            log.error(f"-[{config.PACKAGE_NAME}]- L'argument \"{dt_str}\" n'est pas au bon format \"{in_format}\"")
            sys.exit(1)
    except TypeError:
        if not ignore_errors:
            log.error(f"-[{config.PACKAGE_NAME}]- L'argument \"{dt_str}\" n'est pas au bon format \"{in_format}\"")
            sys.exit(1)
    except AssertionError:
        raise AssertionError(f"-[{config.PACKAGE_NAME}]- L'argument \"{dt_str}\" n'est pas au bon format "
                             f"\"{in_format}\"")


def is_str(string,
           strip_non_printable_char=True,
           strip_accented_char=False,
           strip_num_char=False,
           chars_2_replace=None,
           replaced_chars=None,
           unicode_categories_2_remove=None,
           check_only=False):
    r"""
    .. admonition:: Description

        | Vérifie si une chaîne de caractères est bien une chaine de caractères.
        | Permet également de faire du nettoyage de caractères

    :param string: chaine de caractères à traiter

    :param strip_non_printable_char: permet de nettoyer la chaine de tous les caractères de contrôles parasites.

        | :magenta:`valeurs possibles`: `False/True`
        | :magenta:`valeur par défaut`: `True`

    :param strip_accented_char: permet de nettoyer la chaine de tous les caractères accentués, avec leurs équivaleuts
        sans accent.

        | :magenta:`valeurs possibles`: `False/True`
        | :magenta:`valeur par défaut`: `False`

    :param strip_num_char: permet de nettoyer la chaine de tous les caractères numériques parasites (avec ou non des
        caractères séparateurs, ainsi que les signes et/ou opérateur comme le "-" ou ":")

        | :magenta:`valeurs possibles`: `False/True`
        | :magenta:`valeur par défaut`: `False`

    :param chars_2_replace: permet de faire du remplacement de caractères unitairement.

        | :magenta:`valeurs possibles`: `Chaine de caractère ou Dictionnaire associatif` (si Dictionnaire, alors
            l'argument :magenta:`replaced_chars` est optionnel, :green:`cf. exemple`)

    :param replaced_chars: indique la liste des caractères de remplacement, si cet argument est renseigné, doit
        fonctionner conjointement avec l'argument :magenta:`chars_2_replace` (:green:`cf. exemple`)

    :param unicode_categories_2_remove: permet de spécifier une classe de caractères Unicode à supprimer. Cet argument
        est optionnel et doit être utilisé avec l'argument :magenta:`strip_non_printable_char`

        | :magenta:`valeurs possibles`: `Liste ou Tuple de classe Unicode`
            (cf. |unicode_category_url| pour plus de détails sur les classifications des caractères Unicodes)
        | :magenta:`valeur par défaut`: `None`

    :param check_only: permet de retourner un booléen au lieu de la chaîne de caractères transformée (utile dans le
        cas où il est seulement souhaité un contrôle, sans nécessairement une transformation pour éventuellement y
        appliquer une règle de gestion propre)

        | :magenta:`valeurs possibles`: `False/True`
        | :magenta:`valeurs par défaut`: `False`

    :return:
        | :magenta:`chaine de caractères transformée` si :red:`check_only` == :magenta:`False` (comportement par défaut)
        | sinon :magenta:`True/False`

    .. note::

        | si :red:`chars_2_replace` est un dictionnaire alors il est possible de remplacer plusieurs caractères d'un
            seul tenant {"ABC": "Nouvelle chaines de caractères"} - ou la suite "ABC" sera remplacée par "Nouvelle
            chaines de caractères" (cf. exemple ci-dessous)

    :green:`Exemple` :

    .. literalinclude:: ..\\..\\tests\\cleanse\\is_str.py
        :language: python

    """
    if not isinstance(string, str):
        return False if check_only else ""

    _str = string
    if strip_non_printable_char:
        all_chars = (chr(i) for i in range(sys.maxunicode))

        categories = ["Cc"]
        if unicode_categories_2_remove is not None \
                and isinstance(unicode_categories_2_remove, (str, list, tuple)):
            categories = unicode_categories_2_remove

        control_chars = \
            "".join(c for c in all_chars if unicodedata.category(c) in categories) \
                .join(map(chr, itertools.chain(range(0x00, 0x20), range(0x7f, 0xa0))))

        re_np = re.compile("[%s]" % re.escape(control_chars))
        _str = re_np.sub("", _str)

        if check_only:
            return True

    if strip_accented_char:
        _str = "".join(c for c in unicodedata.normalize("NFD", _str) if unicodedata.category(c) != "Mn")

        if check_only:
            return True

    if strip_num_char:
        re_num_char = re.compile(r"([\-\/+* ,.:]*[0-9])")
        _str = re_num_char.sub("", _str)

        if check_only:
            return True

    if chars_2_replace is not None and isinstance(chars_2_replace, dict) and replaced_chars is None:
        _str = re.sub("({})".format("|".join(map(re.escape, chars_2_replace.keys()))),
                      lambda m: chars_2_replace[m.group()], _str)

        if check_only:
            return True

    if chars_2_replace is not None and replaced_chars is not None \
            and isinstance(chars_2_replace, str) and isinstance(replaced_chars, str):
        try:
            _str = _str.translate(str.maketrans(chars_2_replace, replaced_chars))

            if check_only:
                return True
        except TypeError:
            log.error(f"-[{config.PACKAGE_NAME}]- Les arguments chars_2_replace \"{chars_2_replace}\" et "
                      f"replaced_chars \"{replaced_chars}\" doivent être une châine de caractères ou un dictionnaire "
                      f"de listes de caractères")
            sys.exit(1)
        except ValueError as e:
            try:
                _str = re.sub(chars_2_replace, replaced_chars, _str)
            except ValueError:
                log.error(f"-[{config.PACKAGE_NAME}]- Les arguments chars_2_replace \"{chars_2_replace}\" et "
                          f"replaced_chars \"{replaced_chars}\" doivent être une châine de caractères de même longueur")
                sys.exit(1)

    return False if check_only else _str


def _luhn_sum_numbers(number):
    if number >= 10:
        return sum([int(x) for x in str(number)])

    return number


def _luhn(reversed_str, is_siret=False):
    val_2_check = []

    for i, pos in enumerate(reversed_str):
        if is_siret and "356000000"[::-1] in reversed_str:
            if sum([int(s) for s in reversed_str]) % 5 == 0:
                return True
            else:
                return False

        if (i + 1) % 2 == 0:
            even = int(pos) * 2
            val_2_check.append(_luhn_sum_numbers(even))
        else:
            odd = int(pos) * 1
            val_2_check.append(_luhn_sum_numbers(odd))

    return val_2_check


def _is_siren(siren, check_only=True, correction=True, new_siren=""):
    reversed_siren = siren[::-1]
    luhn = _luhn(reversed_siren)

    if correction:
        siren = siren.rjust(9, "0")

    if sum(luhn) % 10 == 0:
        if check_only:
            return True
        else:
            return siren
    else:
        if check_only:
            return False
        else:
            if correction:
                return new_siren
            else:
                return siren


def is_siren(siren, check_only=True, correction=True, new_siren=""):
    r"""
    .. admonition:: Description

        | Vérifie si un siren est correctement formaté et est valide au sens technique du terme (cf. alogrithme de
            **Luhn**)

    :param siren: chaine de caractères ou liste de chaînes de caractères à traiter

    :param check_only: permet de retourner un booléen au lieu du siren corrigé (si en erreur) ou consolidé (si il
        manque des caractères 0 devant pour former un siren à 9 caractères)

        | :magenta:`valeurs possibles`: `False/True`
        | :magenta:`valeur par défaut`: `True`

    :param correction: indique s'il faut nettoyer/consolider le siren

        | :magenta:`valeurs possibles`: `False/True`
        | :magenta:`valeur par défaut`: `True`

    :param new_siren: indique la chaîne de remplacement si le siren est faux

        | :magenta:`valeurs possibles`: `chaine de caractères`
        | :magenta:`valeur par défaut`: `chaine vide`

    :return:
        | :magenta:`booléen`: `False/True` si :red:`check_only` == :magenta:`True` (comportement par défaut)
        | ou
        | :magenta:`siren/liste de siren` corrigé/consolidé (si :red:`correction` == :magenta:`True`)

    :green:`Exemple` :

    .. literalinclude:: ..\\..\\tests\\cleanse\\is_siren.py
        :language: python

    """
    msg = f"-[{config.PACKAGE_NAME}]- \"{siren}\" doit être une chaîne de caractères ou une liste de chaînes de " \
          f"caractères"

    if not isinstance(new_siren, str):
        log.error(f"-[{config.PACKAGE_NAME}]- \"{new_siren}\" doit être une chaîne de caractères ")
        sys.exit(1)

    if not isinstance(siren, (str, list, tuple)):
        log.error(msg)
        sys.exit(1)

    if isinstance(siren, (list, tuple)):
        for s in siren:
            if not isinstance(s, str):
                log.error(msg)
                sys.exit(1)

    if isinstance(siren, str):
        return _is_siren(siren, check_only, correction, new_siren)
    else:
        _ = []
        for s in siren:
            _.append(_is_siren(s, check_only, correction, new_siren))

        return _


def _extract_siret(siret, extraction):
    Siret = namedtuple("Siret", ["siren", "nic", "siret"])

    if extraction:
        try:
            return Siret(
                siren=siret[0:9],
                nic=siret[9:14],
                siret=siret
            )
        except Exception as e:
            log.warning(f"-[{config.PACKAGE_NAME}]- {e}")
            return Siret(
                siren="",
                nic="",
                siret=""
            )
    else:
        return siret


def _is_siret(siret, check_only=True, correction=True, new_siret="", extraction=False):
    reversed_siret = siret[::-1]
    luhn = _luhn(reversed_siret, is_siret=True)

    if correction:
        siret = siret.rjust(14, "0")

    if isinstance(luhn, bool):
        if luhn:
            if check_only:
                return True
            else:
                return _extract_siret(siret, extraction)
        else:
            if check_only:
                return False
            else:
                if correction:
                    return _extract_siret(new_siret, extraction)
                else:
                    return _extract_siret(siret, extraction)
    else:
        if sum(luhn) % 5 == 0:
            if check_only:
                return True
            else:
                return _extract_siret(siret, extraction)
        else:
            if check_only:
                return False
            else:
                if correction:
                    return _extract_siret(new_siret, extraction)
                else:
                    return _extract_siret(siret, extraction)


def is_siret(siret, check_only=True, correction=True, new_siret="", extraction=False):
    r"""
    .. admonition:: Description

        | Vérifie si un siret est correctement formaté et est valide au sens technique du terme (cf. alogrithme de
            **Luhn**) - prend également en compte les établissements particuliers de La Poste ayant pour sirène
            **356000000**

    :param siret: chaine de caractères ou liste de chaînes de caractères à traiter

    :param check_only: permet de retourner un booléen au lieu du siret corrigé (si en erreur) ou consolidé (si il
        manque des caractères 0 devant pour former un siret à 15 caractères)

        | :magenta:`valeurs possibles`: `False/True`
        | :magenta:`valeur par défaut`: `True`

    :param correction: indique s'il faut nettoyer/consolider le siret

        | :magenta:`valeurs possibles`: `False/True`
        | :magenta:`valeur par défaut`: `True`

    :param new_siret: indique la chaîne de remplacement si le siret est faux

        | :magenta:`valeurs possibles`: `chaine de caractères`
        | :magenta:`valeur par défaut`: `chaine vide`

    :param extraction: indique s'il faut extraire le siren/nic du siret

        | :magenta:`valeurs possibles`: `False/True`
        | :magenta:`valeur par défaut`: `False`

    :return:
        | :magenta:`booléen`: `False/True` si :red:`check_only` == :magenta:`True` (comportement par défaut)
        | ou
        | :magenta:`siret/liste de siret` corrigé/consolidé (si :red:`correction` == :magenta:`True`)
        | ou
        | :magenta:`tuple nommé` avec comme attributs :

            * :magenta:`siren`
            * :magenta:`nic`
            * :magenta:`siret` (présent ici seulement par commodité)

    :green:`Exemple` :

    .. literalinclude:: ..\\..\\tests\\cleanse\\is_siret.py
        :language: python

    """
    msg = f"-[{config.PACKAGE_NAME}]- \"{siret}\" doit être une chaîne de caractères ou une liste de chaînes de " \
          f"caractères"

    if not isinstance(new_siret, str):
        log.error(f"-[{config.PACKAGE_NAME}]- \"{new_siret}\" doit être une chaîne de caractères ")
        sys.exit(1)

    if not isinstance(siret, (str, list, tuple)):
        log.error(msg)
        sys.exit(1)

    if isinstance(siret, (list, tuple)):
        for s in siret:
            if not isinstance(s, str):
                log.error(msg)
                sys.exit(1)

    if isinstance(siret, str):
        return _is_siret(siret, check_only, correction, new_siret, extraction)
    else:
        _ = []
        for s in siret:
            _.append(_is_siret(s, check_only, correction, new_siret, extraction))

        return _


@dask.delayed
def _is_schema(string, schema, regex_flag):
    if regex_flag is None:
        rec = re.compile(schema)
    else:
        rec = re.compile(schema, regex_flag)

    _ = rec.search
    if schema[0:1] == "^":
        _ = rec.match

    if _(string):
        return True

    return False


def is_schema(string, schema, regex_flag=re.IGNORECASE):
    r"""
    .. admonition:: Description

        | Permet de qualifier une chaîne de caractères par rapport à un schéma regex

    :param string: chaine de caractères à qualifier

    :param schema: schéma regex

    :param regex_flag: indique le flag regex à utiliser. cf. :ref:`reference-label-liens-utiles`, **Librairie regex**
        pour plus de détails

        | :magenta:`valeurs possibles`: `None ou constante regex` (séparée par :magenta:`|` si plusieurs constantes,
            par exemple **re.M** | **re.I**)
        | :magenta:`valeur par défaut`: `re.IGNORECASE`

    :return:
        | :magenta:`booléen`: `False/True`

    :green:`Exemple` :

    .. literalinclude:: ..\\..\\tests\\cleanse\\is_schema.py
        :language: python

    """
    if not isinstance(string, str) or not isinstance(schema, str):
        log.error(f"-[{config.PACKAGE_NAME}]- \"{string}\" et \"{schema}\" doivent être des chaînes de caractères")
        sys.exit(1)

    if regex_flag != re.IGNORECASE and regex_flag is not None:
        if not isinstance(regex_flag, re.RegexFlag):
            log.error(f"-[{config.PACKAGE_NAME}]- Les flags \"{regex_flag}\" ne sont pas des flags d'une instance "
                      f"regex.")
            sys.exit(1)

    _ = _is_schema(string, schema, regex_flag)
    return _.compute()


def is_phone_number(phone_number,
                    check_only=True,
                    normalize=True,
                    country_code="FR",
                    phone_number_format=config.PHONE_NUMBER_FORMAT_INTERNATIONAL,
                    correction=True,
                    new_phone="",
                    extraction=False):
    r"""
    .. admonition:: Description

        | Permet de qualifier un n° de téléphone au format international, national ou E164

    :param phone_number: n° de téléphone à traiter

    :param check_only: permet de retourner un booléen au lieu du n° de téléphone normalisé

        | :magenta:`valeurs possibles`: `False/True`
        | :magenta:`valeur par défaut`: `True`

    :param normalize: indique s'il faut normaliser le n° de téléphone

        | :magenta:`valeurs possibles`: `False/True`
        | :magenta:`valeur par défaut`: `True`

    :param country_code: indique le code du pays (code ISO sur 2 caractères)

        | :magenta:`valeurs possibles`: `Code ISO pays ou None` (si :magenta:`None` alors le n° de téléphone
            **doit être** au **format international**, +XX??????????)
        | :magenta:`valeur par défaut`: `FR`

    :param phone_number_format: indique le format de sortie

        | :magenta:`valeurs possibles`: `config.PHONE_NUMBER_FORMAT_INTERNATIONAL`,
            `config.PHONE_NUMBER_FORMAT_NATIONAL` ou `config.PHONE_NUMBER_FORMAT_E164`
        | :magenta:`valeur par défaut`: `config.PHONE_NUMBER_FORMAT_INTERNATIONAL`

    :param correction: indique s'il faut nettoyer/consolider le n° de téléphone

        | :magenta:`valeurs possibles`: `False/True`
        | :magenta:`valeur par défaut`: `True`

    :param new_phone: indique la chaîne de remplacement si le n° de téléphone est faux

        | :magenta:`valeurs possibles`: `chaine de caractères`
        | :magenta:`valeur par défaut`: `chaine vide`

    :param extraction: indique s'il faut extraire le n° passé en argument via :red:`phone_number`

        | :magenta:`valeurs possibles`: `False/True`
        | :magenta:`valeur par défaut`: `False`

    :return:
        | :magenta:`booléen`: `False/True` si :red:`check_only` == :magenta:`True` (comportement par défaut)
        | ou
        | :magenta:`n° de téléphone` normalisé au format :red:`phone_number_format` et consolidé si :red:`correction`
             == :magenta:`True`
        | ou
        | :magenta:`tuple nommé` avec comme attributs :

            * :magenta:`country_code`
            * :magenta:`phone_number`
            * :magenta:`national_number` (présent ici seulement par commodité)
            * :magenta:`international_number` (présent ici seulement par commodité)
            * :magenta:`e164_number` (présent ici seulement par commodité)
            * :magenta:`given_number`

    :green:`Exemple` :

    .. literalinclude:: ..\\..\\tests\\cleanse\\is_phone_number.py
        :language: python

    .. image:: ..\\ss\\is_phone_number.png

    """
    if not isinstance(phone_number, str):
        log.error(f"-[{config.PACKAGE_NAME}]- Le n° de téléphone \"{phone_number}\" doit être une chaîne de caractères")
        sys.exit(1)

    try:
        phone = phonenumbers.parse(phone_number, country_code)
    except phonenumbers.phonenumberutil.NumberParseException:
        if country_code is None and phone_number[0:1] != "+":
            log.error(f"-[{config.PACKAGE_NAME}]- Le n° \"{phone_number}\" doit être au format internationnal ou E164 "
                      f"si le code du pays est à None")
            sys.exit(1)
        else:
            try:
                phone = phonenumbers.parse(phone_number, None)
            except phonenumbers.phonenumberutil.NumberParseException as e:
                log.error(f"-[{config.PACKAGE_NAME}]- {e}")
                sys.exit(1)

    is_valid_phone_number = phonenumbers.is_valid_number(phone)
    if check_only:
        return is_valid_phone_number
    else:
        if normalize:
            _phone = phonenumbers.format_number(phone, phone_number_format)
        else:
            _phone = phone_number

        if extraction:
            PhoneNumber = namedtuple("PhoneNumber", [
                "country_code",
                "phone_number",
                "national_number",
                "international_number",
                "e164_number",
                "given_number"])

            if correction and is_valid_phone_number is False:
                return PhoneNumber(
                    country_code="",
                    phone_number="",
                    national_number="",
                    international_number="",
                    e164_number="",
                    given_number=phone_number
                )
            else:
                return PhoneNumber(
                    country_code=phone.country_code,
                    phone_number=phone.national_number,
                    national_number=phonenumbers.format_number(phone, config.PHONE_NUMBER_FORMAT_NATIONAL),
                    international_number=phonenumbers.format_number(phone, config.PHONE_NUMBER_FORMAT_INTERNATIONAL),
                    e164_number=phonenumbers.format_number(phone, config.PHONE_NUMBER_FORMAT_E164),
                    given_number=phone_number
                )
        else:
            if correction and is_valid_phone_number is False:
                _phone = new_phone

            return _phone


def is_email(email,
             check_only=True,
             check_deliverability=False,
             normalize=True,
             correction=True,
             new_email="",
             extraction=False,
             smtp_utf8=False):
    r"""
    .. admonition:: Description

        | Permet de valider et d'uniformiser un email

    :param email: email à traiter

    :param check_only: permet de retourner un booléen au lieu de l'email normalisé

        | :magenta:`valeurs possibles`: `False/True`
        | :magenta:`valeur par défaut`: `True`

    :param check_deliverability: indique s'il faut vérifier la délivrabilité de l'email (si son format est valide).

        | :magenta:`valeurs possibles`: `False/True`
        | :magenta:`valeur par défaut`: `False`

    :param normalize: indique s'il faut normaliser l'email en sortie

        | :magenta:`valeurs possibles`: `False/True`
        | :magenta:`valeur par défaut`: `True`

    :param correction: indique s'il faut corriger l'email faut avec la valeur passée via :red:`new_email`

    :param new_email: indique la chaîne de remplacement si l'email est faux

        | :magenta:`valeurs possibles`: `chaine de caractères`
        | :magenta:`valeur par défaut`: `chaine vide`

    :param extraction: indique s'il faut extraire l':red:`email` passé en argument

        | :magenta:`valeurs possibles`: `False/True`
        | :magenta:`valeur par défaut`: `False`

    :param smtp_utf8: indique si l':red:`email` passé en argument est encodé en utf8

        | :magenta:`valeurs possibles`: `False/True`
        | :magenta:`valeur par défaut`: `False`

    :return:
        | :magenta:`booléen`: `False/True` si :red:`check_only` == :magenta:`True` (comportement par défaut)
        | ou
        | :magenta:`email` normalisé avec un encodage **ASCII** ou en **UTF8** (si :red:`smtp_utf8` == :magenta:`True`)
        | ou
        | :magenta:`tuple nommé` avec comme attributs :

            * :magenta:`email` (email complet normalisé en UTF8)
            * :magenta:`local_part`  (préfixe du @ en UTF8)
            * :magenta:`domain` (suffixe du @ en UTF8)
            * :magenta:`ascii_email` (email complet normalisé en ASCII)
            * :magenta:`ascii_local_part` (préfixe du @ en ASCII ou :magenta:`None` si :red:`smtp_utf8` == :magenta:`True`)
            * :magenta:`ascii_domain` (suffixe du @ en ASCII ou |punnycode_url| si :red:`smtp_utf8` == :magenta:`True`)
            * :magenta:`smtp_utf8`
            * :magenta:`mx` (entrée MX du/des serveurs DNS)
            * :magenta:`mx_fallback_type` (:magenta:`None` si tout est OK, sinon les possibles erreurs levées)

    :green:`Exemple` :

    .. literalinclude:: ..\\..\\tests\\cleanse\\is_email.py
        :language: python

    .. image:: ..\\ss\\is_email.png

    """
    if not isinstance(email, str):
        log.error(f"-[{config.PACKAGE_NAME}]- L'email \"{email}\" doit être une chaîne de caractères")
        sys.exit(1)
    if not isinstance(new_email, str):
        log.error(f"-[{config.PACKAGE_NAME}]- L'email de remplacement \"{new_email}\" doit être une chaîne de "
                  f"caractères")
        sys.exit(1)

    try:
        _ = validate_email(email, check_deliverability=check_deliverability, allow_smtputf8=smtp_utf8)

        if check_only:
            return True
        else:
            if extraction:
                Email = namedtuple("Email", [
                    "email",
                    "local_part",
                    "domain",
                    "ascii_email",
                    "ascii_local_part",
                    "ascii_domain",
                    "smtp_utf8",
                    "mx",
                    "mx_fallback_type"])

                return Email(
                    email=_.email,
                    local_part=_.local_part,
                    domain=_.domain,
                    ascii_email=_.ascii_email,
                    ascii_local_part=_.ascii_local_part,
                    ascii_domain=_.ascii_domain,
                    smtp_utf8=_.smtputf8,
                    mx=_.mx,
                    mx_fallback_type=_.mx_fallback_type
                )
            else:
                if normalize:
                    if smtp_utf8:
                        return _.email
                    else:
                        return _.ascii_email
                else:
                    return email
    except EmailNotValidError:
        if check_only:
            return False
        else:
            if correction:
                return new_email

    return email

