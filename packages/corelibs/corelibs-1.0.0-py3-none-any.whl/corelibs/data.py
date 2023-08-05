r"""
.. module:: data.py
    :synopsis: Module pour gérer tout ce qui se rapporte à la manipulation des données

.. moduleauthor:: Michel TRUONG <michel.truong@gmail.com>

.. topic:: Description générale

    Module pour gérer tout ce qui se rapporte à la manipulation des données

"""
import math
import os
import re
import shutil
import sys
import tempfile
from collections import namedtuple

import dask.dataframe as ddf
import dtale
import pandas as pd

from corelibs import _corelibs as _c, config, lazy as lz, tools

log = _c.log


def replace_in_file(path,
                    pattern,
                    replace,
                    regex_flag=None,
                    out_file_path=None,
                    ignore_errors=False,
                    encoding=config.DEFAULT_ENCODING_FILE,
                    out_encoding=config.DEFAULT_ENCODING_FILE):
    r"""
    .. admonition:: Description

        | Permet de scanner un fichier et de remplacer tout son contenu.

    :param path: indique l'emplacement en chemin absolu du fichier plat à traiter.

    :param pattern: indique la chaine de caractères ou le modèle regex à chercher.

    :param replace: indique la chaine de caractères ou le modèle regex en remplacement.

    :param regex_flag: indique les flags à utiliser. cf. :ref:`reference-label-liens-utiles`, **Librairie regex** pour
        plus de détails

    :param out_file_path: indique le fichier de sortie si nécessaire.

    :param ignore_errors: indique si l'ouverture des fichiers doit ignorer ou non les erreurs d'encodage de type
        "byte 0xff in position 0" qui survient lors d'un décodage caractère encodé en utf-16 alors que la lecture du
        fichier se fait avec le code utf-8.

        | :magenta:`valeurs possibles`: `False/True`
        | :magenta:`valeur par défaut`: `False`

    :param encoding: indique l'encodage à la lecture

    :param encoding: indique l'encodage à l'écriture (identique à l'encoding de lecture par défaut)

    :return:
        | :magenta:`rien...`

    :green:`Exemple` :

    .. literalinclude:: ..\\..\\tests\\data\\replace_in_file.py
        :language: python

    """
    if not lz.is_file_exists(path):
        log.error(f"-[{config.PACKAGE_NAME}]- Le fichier en entrée \"{path}\" n'existe pas")
        sys.exit(1)

    if lz.is_file_exists(path, is_dir=True):
        log.error(f"-[{config.PACKAGE_NAME}]- Le fichier en entrée \"{path}\" ne peut pas être un répertoire")
        sys.exit(1)

    if (isinstance(pattern, bytes) and not isinstance(replace, bytes)) \
            or (not isinstance(pattern, bytes) and isinstance(replace, bytes)):
        log.error(f"-[{config.PACKAGE_NAME}]- Le modèle de recherche \"{pattern}\" et le modèle de remplacement "
                  f"\"{replace}\" doivent être tous les 2 des modèles binaires")
        sys.exit(1)

    if out_file_path is not None:
        lz._is_base_dir_path_existed_n_validated_file_name(out_file_path)

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

    error_options = "ignore" if ignore_errors else None

    rec = re.compile(pattern, flags)
    if out_file_path is None:
        if isinstance(pattern, bytes):
            temp_file = tempfile.NamedTemporaryFile(
                mode="wb",
                suffix=config.PACKAGE_SUFFIX_TMP_NAME,
                delete=False)

            with open(path, "rb") as in_file:
                for line in in_file:
                    replaced_contents = rec.sub(replace, line)
                    temp_file.write(replaced_contents)
        else:
            temp_file = tempfile.NamedTemporaryFile(
                encoding=out_encoding,
                mode="w",
                suffix=config.PACKAGE_SUFFIX_TMP_NAME,
                delete=False)

            with open(path, "r", encoding=encoding, errors=error_options) as in_file:
                for line in in_file:
                    replaced_contents = rec.sub(replace, line)
                    temp_file.write(replaced_contents)

        temp_file.close()
        shutil.move(temp_file.name, path)
    else:
        if isinstance(pattern, bytes):
            with open(path, "rb") as in_file, open(out_file_path, "wb") as out_file:
                for line in in_file:
                    replaced_contents = rec.sub(replace, line)
                    out_file.write(replaced_contents)
        else:
            with open(path, "r", encoding=encoding, errors=error_options) as in_file, \
                    open(out_file_path, "w", encoding=out_encoding) as out_file:
                for line in in_file:
                    replaced_contents = rec.sub(replace, line)
                    out_file.write(replaced_contents)


def tail(file_path,
         chunk=config.DEFAULT_BUFFER_CHUNK_SIZE,
         skip_header=False,
         start_file=False,
         encoding=config.DEFAULT_ENCODING_FILE,
         out_encoding=config.DEFAULT_ENCODING_FILE):
    r"""
    .. admonition:: Description

        | Permet d'extraire les dernières lignes d'un gros fichier plat.

    :param file_path: indique l'emplacement en chemin absolu du fichier plat à traiter.

    :param chunk: indique le nombre de lignes à extraire
        cf. `DEFAULT_BUFFER_CHUNK_SIZE` dans :ref:`reference-label-config`

    :param skip_header: indique si l'extraction doit écarter l'entête du fichier.

        | :magenta:`valeurs possibles`: `False/True`
        | :magenta:`valeur par défaut`: `False`

    :param start_file: indique s'il faut lancer l'application liée par défaut au format du fichier, après extraction.

        | :magenta:`valeurs possibles`: `False/True`
        | :magenta:`valeur par défaut`: `False`

    :param encoding: indique l'encodage à la lecture

    :param out_encoding: indique l'encodage à l'écriture (identique à l'encoding de lecture par défaut)

    :return:
        | :magenta:`le chemin du fichier extrait` (à la même racine, avec le suffixe ":green:`_tail_preview`")

    :green:`Exemple` :

    .. literalinclude:: ..\\..\\tests\\data\\tail.py
        :language: python

    """
    if chunk is not None and not isinstance(chunk, int):
        log.error(f"-[{config.PACKAGE_NAME}]- Le nombre de lignes \"{chunk}\" à découper doit être un entier")
        sys.exit(1)

    if not lz.is_file_exists(file_path):
        log.error(f"-[{config.PACKAGE_NAME}]- Le fichier \"{file_path}\" n'existe pas")
        sys.exit(1)

    file_path_db = lz.get_dir_n_basename(file_path)
    file_path_db_ext = lz.get_file_extension(file_path_db.base_name)

    fsize = os.stat(file_path).st_size

    i = 0
    with open(file_path, "r", encoding=encoding) as f:
        if config.DEFAULT_BYTE_CHUNK_SIZE > fsize:
            config.DEFAULT_BYTE_CHUNK_SIZE = fsize - 1
        data = []

        if not skip_header:
            header = f.readline()

        while True:
            i += 1
            f.seek(fsize - config.DEFAULT_BYTE_CHUNK_SIZE * i)
            data.extend(f.readlines())
            if len(data) >= chunk or f.tell() == 0:
                tail_2_print = "".join(data[-chunk:])

                out_file_path = lz.get_abspath(
                    file_path_db.dir_path,
                    file_path_db_ext.file_name + "_tail_preview" + file_path_db_ext.file_extension
                )
                with open(out_file_path, "w", encoding=out_encoding) as out_file:
                    if not skip_header:
                        out_file.write(header)

                    out_file.write(tail_2_print)

                if start_file:
                    os.startfile(out_file_path)

                break

    return out_file_path


def head(file_path,
         chunk=config.DEFAULT_BUFFER_CHUNK_SIZE,
         skip_header=False,
         start_file=False,
         encoding=config.DEFAULT_ENCODING_FILE,
         out_encoding=config.DEFAULT_ENCODING_FILE):
    r"""
    .. admonition:: Description

        | Permet d'extraire les premières lignes d'un gros fichier plat.

    :param file_path: indique l'emplacement en chemin absolu du fichier plat à traiter.

    :param chunk: indique le nombre de lignes à extraire
        cf. `DEFAULT_BUFFER_CHUNK_SIZE` dans :ref:`reference-label-config`

    :param skip_header: indique si l'extraction doit écarter l'entête du fichier.

        | :magenta:`valeurs possibles`: `False/True`
        | :magenta:`valeur par défaut`: `False`

    :param start_file: indique s'il faut lancer l'application liée par défaut au format du fichier, après extraction.

        | :magenta:`valeurs possibles`: `False/True`
        | :magenta:`valeur par défaut`: `False`

    :param encoding: indique l'encodage à la lecture

    :param out_encoding: indique l'encodage à l'écriture (identique à l'encoding de lecture par défaut)

    :return:
        | :magenta:`le chemin du fichier extrait` (à la même racine, avec le suffixe ":green:`_head_preview`")
        | ou
        | :magenta:`None` si problème

    :green:`Exemple` :

    .. literalinclude:: ..\\..\\tests\\data\\head.py
        :language: python

    """
    if chunk is not None and not isinstance(chunk, int):
        log.error(f"-[{config.PACKAGE_NAME}]- Le nombre de lignes \"{chunk}\" à découper doit être un entier")
        sys.exit(1)

    if not lz.is_file_exists(file_path):
        log.error(f"-[{config.PACKAGE_NAME}]- Le fichier \"{file_path}\" n'existe pas")
        sys.exit(1)

    file_path_db = lz.get_dir_n_basename(file_path)
    file_path_db_ext = lz.get_file_extension(file_path_db.base_name)

    with open(file_path, encoding=encoding) as in_file:
        head_2_print = [next(in_file) for line in range(chunk + 1)]

    if skip_header:
        head_2_print = head_2_print[1:]

    out_file_path = lz.get_abspath(
        file_path_db.dir_path,
        file_path_db_ext.file_name + "_head_preview" + file_path_db_ext.file_extension
    )

    try:
        with open(out_file_path, "w", encoding=out_encoding) as out_file:
            for line in head_2_print:
                out_file.write(line)

        if start_file:
            os.startfile(out_file_path)

        return out_file_path
    except PermissionError:
        log.error(f"-[{config.PACKAGE_NAME}]- Permissions insuffisantes pour écrire dans \"{out_file_path}\"")
        sys.exit(1)

    return None


def preview(obj, separator=";", allow_cell_edits=True, subprocess=True):
    r"""
    .. admonition:: Description

        | Permet de visionner et manipuler rapidement les données extraites ou des données agrégées dans une application
            web.

    .. warning::

        | Attention aux erreurs de type Mémoire insuffisante. La manipulation des données sur l'application web devrait
            se faire sur un nombre restreint d'observations et spécialement en fonction des ressources propres au PC sur
            lequel est lancé les traitements python.

    :param obj: indique l'emplacement en chemin absolu du fichier plat ou le dataframe pandas à prévisualiser.

    :param separator: indique le caractère séparateur.

    :param allow_cell_edits: indique la possibilité d'éditer les cellules lues.

        | :magenta:`valeurs possibles`: `False/True`
        | :magenta:`valeur par défaut`: `True`

    :param subprocess: indique si l'exécution se fait en mode threading ou non. Le comportement par défaut va tuer
        automatiquement le process si il n'est plus utilisé ou si l'exécution de la pile principale est finie (ce
        paramétrage fonctionne sous iPython, Jupyter & la console Python mais ne fontionne pas sur un terminal standard
        ou un terminal émulé - PyCharm par exemple - où il faudrait désactiver le threading)

        | :magenta:`valeurs possibles`: `False/True`
        | :magenta:`valeur par défaut`: `True`

    :return:
        | :magenta:`rien`

    :green:`Exemple` :

    .. literalinclude:: ..\\..\\tests\\data\\preview.py
        :language: python

    .. image:: ..\\ss\\dtale_preview.png

    """
    if isinstance(obj, pd.DataFrame):
        dt = dtale.show(obj, ignore_duplicate=True, allow_cell_edits=allow_cell_edits, subprocess=subprocess)
        dt.open_browser()
    else:
        if not lz.is_file_exists(obj):
            log.error(f"-[{config.PACKAGE_NAME}]- Le fichier \"{obj}\" n'existe pas")
            sys.exit(1)

        col_names = pd.read_csv(obj, sep=separator, nrows=0, engine="python").columns
        data_type_dict = {}
        data_type_dict.update({col: "str" for col in col_names if col not in data_type_dict})

        df = ddf.read_csv(obj, sep=separator, dtype=data_type_dict)
        df = df.fillna("").compute()

        dt = dtale.show(df, ignore_duplicate=True, allow_cell_edits=allow_cell_edits, subprocess=subprocess)
        dt.open_browser()


def split_file(file_path,
               skip_header=False,
               start=None,
               chunk=config.DEFAULT_BUFFER_CHUNK_SIZE,
               suffix="_part_"):
    r"""
    .. admonition:: Description

        | Permet de scinder un fichier plat volumineux en plusieurs petits fichiers

    :param file_path: indique l'emplacement en chemin absolu du fichier plat à scinder.

    :param skip_header: indique s'il faut ou non écarter la ligne d'entête.

        | :magenta:`valeurs possibles`: `False/True`
        | :magenta:`valeur par défaut`: `False`

    :param start: indique si besoin, la première ligne à partir de laquelle l'extraction va démarrer

    :param chunk: indique le nombre de lignes à scinder par fichier
        cf. `DEFAULT_BUFFER_CHUNK_SIZE` dans :ref:`reference-label-config`. Utilisé conjointement avec :red:`start` cet
        argument sera pris comme l'offset d'arrêt pour extraire le fichier

        | :magenta:`valeurs possibles`: `entier/None`
        | :magenta:`valeur par défaut`: `DEFAULT_BUFFER_CHUNK_SIZE`

    :param suffix: indique le suffix à appliquer aux fichiers scindés

    :return:
        | :magenta:`rien`

    :green:`Exemple` :

    .. literalinclude:: ..\\..\\tests\\data\\split_file.py
        :language: python

    """
    if not lz.is_file_exists(file_path):
        log.error(f"-[{config.PACKAGE_NAME}]- Le fichier \"{file_path}\" n'existe pas")
        sys.exit(1)

    if start is not None:
        if not isinstance(start, int):
            log.error(f"-[{config.PACKAGE_NAME}]- L'offset de départ \"{start}\" doit être un entier")
            sys.exit(1)

        if start < 0:
            log.error(f"-[{config.PACKAGE_NAME}]- L'offset de départ {start} doit être un entier positif")
            sys.exit(1)

    if chunk is not None and not isinstance(chunk, int):
        log.error(f"-[{config.PACKAGE_NAME}]- Le nombre de lignes \"{chunk}\" à découper doit être un entier")
        sys.exit(1)

    if start is None and chunk is None:
        chunk = config.DEFAULT_BUFFER_CHUNK_SIZE

    total_lines = tools.get_total_lines_in_file(file_path)

    file_path_db = lz.get_dir_n_basename(file_path)
    file_path_name_ext = lz.get_file_extension(file_path_db.base_name)

    with open(file_path, "rb") as fin:
        header = fin.readline()

        if start:
            output_file_name = file_path_name_ext.file_name + str(suffix) + file_path_name_ext.file_extension
        else:
            output_file_name = file_path_name_ext.file_name + str(suffix) + "0" + file_path_name_ext.file_extension

        fout = open(lz.get_abspath(
            file_path_db.dir_path,
            output_file_name
        ), "wb")

        if not skip_header:
            fout.write(header)

        for i, line in enumerate(fin):
            if start:
                if i >= start - 1 and (chunk is None or i < chunk + start - 1):
                    fout.write(line)
                elif i >= chunk + start - 1:
                    fout.close()
                    break
            else:
                fout.write(line)

                if (i + 1) % chunk == 0:
                    fout.close()

                    if i < total_lines - 1:
                        fout = open(lz.get_abspath(
                            file_path_db.dir_path,
                            file_path_name_ext.file_name + str(suffix) + f"{math.floor(i/chunk+1)}"
                            + file_path_name_ext.file_extension
                        ), "wb")

                        if not skip_header:
                            fout.write(header)

        fout.close()


def _append_files(files_2_append, fout, index, skip_header=True, chunk=config.DEFAULT_BUFFER_CHUNK_SIZE):
    if files_2_append:
        with open(files_2_append, "rb") as fin:
            header = fin.readline()
            if index == 0:
                fout.write(header)
            else:
                if not skip_header:
                    fout.write(header)

            while True:
                data = fin.read(chunk)
                if data:
                    fout.write(data)
                else:
                    break


def append_files(files_2_append,
                 out_file_path,
                 source_dir_path=None,
                 skip_header=True,
                 chunk=config.DEFAULT_BUFFER_CHUNK_SIZE):
    r"""
    .. admonition:: Description

        | Permet de concaténer des fichiers plats

    :param files_2_append: indique les fichiers à concaténer

    :param out_file_path: indique le nom du fichier de sortie avec son chemin absolu

    :param source_dir_path: indique le chemin absolu des fichiers sources (optionnel pour factoriser l'argument
        **files_2_append**)

    :param skip_header: indique s'il faut ou non écarter la ligne d'entête

        | :magenta:`valeurs possibles`: `False/True`
        | :magenta:`valeur par défaut`: `True`

    :param chunk: indique le nombre de lignes à lire par cycle de lecture
        cf. `DEFAULT_BUFFER_CHUNK_SIZE` dans :ref:`reference-label-config`

        | :magenta:`valeurs possibles`: `entier/None`
        | :magenta:`valeur par défaut`: `DEFAULT_BUFFER_CHUNK_SIZE`

    :return:
        | :magenta:`rien`

    :green:`Exemple` :

    .. literalinclude:: ..\\..\\tests\\data\\append_files.py
        :language: python

    """
    if not isinstance(files_2_append, (list, tuple)):
        log.error(f"-[{config.PACKAGE_NAME}]- La concaténation ne peut se faire que sur une liste ou tuple de fichiers "
                  f"et \"{files_2_append}\" n'en est pas.")
        sys.exit(1)

    out_file_path_db = lz.get_dir_n_basename(out_file_path)
    if not lz.is_file_exists(out_file_path_db.dir_path, is_dir=True):
        log.error(f"-[{config.PACKAGE_NAME}]- Le chemin du fichier agrégé \"{out_file_path_db.dir_path}\" n'existe pas")
        sys.exit(1)

    if source_dir_path is not None and not lz.is_file_exists(source_dir_path, is_dir=True):
        log.error(f"-[{config.PACKAGE_NAME}]- Le chemin des fichiers sources à agréger \"{source_dir_path}\" n'existe "
                  f"pas")
        sys.exit(1)

    fout = open(out_file_path, "wb")

    for i, f in enumerate(files_2_append):
        if not lz.is_file_exists(f, ignore_errors=True):
            if source_dir_path is not None:
                f_path = lz.get_abspath(source_dir_path, f)
            else:
                f_path = f

            if not lz.is_file_exists(f_path, ignore_errors=True):
                log.error(f"-[{config.PACKAGE_NAME}]- Fichier \"{f}\" non trouvé, aucune action ne sera appliquée")
                f_path = ""
        else:
            f_path = f

        _append_files(f_path, fout, i, skip_header, chunk)

    fout.close()


def has_same_header(file_path, file_2_compare, separator=";"):
    r"""
    .. admonition:: Description

        | Permet de vérifier si 2 fichiers plats ont la même entête

    :param file_path: indique le fichier de référence avec son chemin absolu.

    :param file_2_compare: indique le fichier à comparer avec son chemin absolu.

    :param separator: indique le caractère séparateur.

    :return:
        :magenta:`tuple nommé` avec comme attributs :
            * :magenta:`result` (booléen)
            * :magenta:`cause` (motif)

    :green:`Exemple` :

    .. literalinclude:: ..\\..\\tests\\data\\has_same_header.py
        :language: python

    """
    if not lz.is_file_exists(file_path):
        log.error(f"-[{config.PACKAGE_NAME}]- Le fichier \"{file_path}\" n'existe pas")
        sys.exit(1)

    if not lz.is_file_exists(file_2_compare):
        log.error(f"-[{config.PACKAGE_NAME}]- Le fichier à comparer \"{file_2_compare}\" n'existe pas")
        sys.exit(1)

    if lz.is_file_exists(file_path, is_dir=True) or lz.is_file_exists(file_2_compare, is_dir=True):
        log.error(f"-[{config.PACKAGE_NAME}]- La comparaison ne peut pas se faire sur un dossier")
        sys.exit(1)

    file_cols = pd.read_csv(file_path, sep=separator, nrows=0, engine="python").columns.tolist()
    file_2_compare_cols = pd.read_csv(file_2_compare, sep=separator, nrows=0, engine="python").columns.tolist()

    HasSameHeader = namedtuple("HasSameHeader", ["result", "cause"])

    if len(file_cols) != len(file_2_compare_cols):
        return HasSameHeader(
            result=False,
            cause={
                "cause": "Longueur différente",
                "file": f"{len(file_cols)} colonnes",
                "file 2 compare": f"{len(file_2_compare_cols)} colonnes"
            }
        )

    diff = [i for i, j in zip(file_cols, file_2_compare_cols) if i != j]
    if diff:
        return HasSameHeader(
            result=False,
            cause={
                "cause": "Différence format",
                "columns difference": diff,
                "file": file_cols,
                "file 2 compare": file_2_compare_cols
            }
        )

    return HasSameHeader(
            result=True,
            cause={"hype": "o(^  ^ o) Tout est OK, YEAH!!! (o ^  ^)o"}
        )
