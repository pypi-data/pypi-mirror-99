import json
import random
import shutil
import sys
import threading
import time

import PySimpleGUI as sg

from corelibs import config, lazy as lz, webdoc, cleanse, tools
from corelibs.gui import theme, gui_conda

TOTAL_PROCESSING_ANIMATION_GIF = 7
rand_processing_gif_number = random.choice(range(TOTAL_PROCESSING_ANIMATION_GIF))


def _open_user_folder():
    if not lz.is_file_exists(theme.user_corelibs_root, is_dir=True):
        lz.copy(
            theme.corelibs_root,
            theme.user_corelibs_root
        )

    lz.open_explorer(theme.user_corelibs_root)


def _display_layout(_layout):
    list_of_layout = {
        "gestion projet": "PROJECT",
        "purifier les fichiers plats": "CLEANSE",
        "scan & analyse": "ANALYSIS",
        "gestion environnements conda": "CONDA",
    }

    for key, value in list_of_layout.items():
        window[f"-{value}_LAYOUT-"].update(visible=False)
        if key == _layout:
            window[f"-{value}_LAYOUT-"].update(visible=True)


def _create_folder(path_2_create, _type="python"):
    global event, values

    msg = f"\nDossier {_type} créé à l'emplacement indiqué\n "

    window_closable = False
    if path_2_create not in ("Nouveau projet python", "Nouveau dossier modèle", ""):
        if ("/" in path_2_create or "\\" in path_2_create) \
                and lz.is_file_exists(path_2_create, is_dir=True, ignore_errors=True):
            msg = f"\nDossier \"{path_2_create}\" existe déjà..." \
                  f"\n\nVeuillez saisir un nom pour le dossier projet python et/ou dossier modèle\n "
            sg.popup_ok(msg, title="Alerte", icon=theme.corelibs_path_ico, grab_anywhere=True)
            return None

        path_2_create_bd = lz.get_dir_n_basename(path_2_create)
        if not lz._is_validated_renamed_file_name(path_2_create_bd.base_name):
            msg = f"\nLe nom du dossier \"{path_2_create_bd.base_name}\" n'est pas valide" \
                  f"\n\nVeuillez saisir un nom approprié\n "
            sg.popup_ok(msg, title="Alerte", icon=theme.corelibs_path_ico, grab_anywhere=True)
            return None

        if _type == "python":
            base_name = cleanse.is_str(path_2_create_bd.base_name,
                                       strip_accented_char=True,
                                       chars_2_replace={
                                           " ": "_",
                                           "!": "",
                                           "@": "",
                                           "#": "",
                                           "{": "",
                                           "}": "",
                                           "(": "",
                                           ")": "",
                                           "[": "",
                                           "]": "",
                                           "=": "",
                                           "+": "",
                                           "$": "",
                                           "£": "",
                                           "€": "",
                                           "ç": "c",
                                           "\"": "",
                                           "'": "",
                                           "°": "",
                                           "¤": "",
                                           "µ": "",
                                           "§": ""
                                       }).lower()
            try:
                from pyscaffold import cli

                new_py_project_path = lz.get_abspath(path_2_create_bd.dir_path, base_name)
                if not lz.is_file_exists(path_2_create_bd.dir_path, is_dir=True, ignore_errors=True):
                    lz.mkdir(path_2_create_bd.dir_path, make_scaffolding=False)

                for options in [new_py_project_path, "--force", "--package", base_name]:
                    sys.argv.append(options)
                cli.run()
                lz.open_explorer(new_py_project_path)
                window["-INPUT_PATH_PYTHON-"]("Nouveau projet python")
            except ImportError:
                msg = f"\nLe package \"pyscaffold\" ne semble pas être installé dans l'environnement actuel." \
                      f"\n\nVeuillez l'installer d'abord :" \
                      f"\n\t$ pip install pyscaffold\n "
                sg.popup_ok(msg, title="Alerte", icon=theme.corelibs_path_ico, grab_anywhere=True)
        else:
            folder_2_make = lz.get_abspath(path_2_create_bd.dir_path, path_2_create_bd.base_name)
            lz.mkdir(folder_2_make, ignore_errors=True)
            lz.open_explorer(folder_2_make)
            window["-INPUT_PATH_DIR_SCAFFOLDING-"]("Nouveau dossier modèle")
            window_closable = True

        sg.popup_ok(msg, title="Succès", icon=theme.corelibs_path_ico, grab_anywhere=True)
        if values["-INPUT_PATH_DIR_SCAFFOLDING-"] in ("Nouveau dossier modèle", "") or window_closable:
            window.close()


end_cleanse_file = False


def _run_cleanse_file(file_2_clean):
    global end_cleanse_file

    cleanse.cleanse_file(file_path=file_2_clean, time_stamp="D")

    end_cleanse_file = True


def _cleanse_file(file_2_clean):
    global end_cleanse_file

    if not lz.is_file_exists(file_2_clean):
        msg = f"\nLe fichier à nettoyer \"{file_2_clean}\" n'existe pas." \
              f"\n\nVeuillez soumettre un nouveau fichier\n "
        sg.popup_ok(msg, title="Alerte", icon=theme.corelibs_path_ico, grab_anywhere=True)
        return None

    first = True
    while True:
        if end_cleanse_file:
            sg.popup_animated(None)
            window.close()
            break
        else:
            sg.popup_animated(
                image_source=theme.corelibs_path + f"\\gui\\processing_0{rand_processing_gif_number}.gif",
                message="En cours d'exécution...",
                background_color="white"
            )
            if first:
                threading.Thread(target=_run_cleanse_file, kwargs=dict(file_2_clean=file_2_clean), daemon=True).start()
            first = False
        time.sleep(.05)

    sg.popup_ok(f"Le traitement du fichier \"{file_2_clean}\" est terminé avec succès",
                title="Succès", icon=theme.corelibs_path_ico, grab_anywhere=True)
    file_2_clean_db = lz.get_dir_n_basename(file_2_clean)
    lz.open_explorer(file_2_clean_db.dir_path)


def _get_scan_history():
    _history_file = lz.get_abspath(theme.user_corelibs_cache_root, "history.json")
    if not lz.is_file_exists(_history_file, ignore_errors=True):
        return 0, {}

    with open(_history_file, "r") as f_in:
        try:
            history = json.load(f_in)
        except json.decoder.JSONDecodeError:
            return 0, {}

        if len(history) == 0:
            return 0, {}
        else:
            return len(history), history


def _get_scan_dir_path_hash(dir_path):
    scan_out_file_name = tools.get_fingerprint(
        str(dir_path).replace("\\", "_").replace("/", "_").lower(), eval_as_string=True
    )

    _cache_file = lz.get_abspath(theme.user_corelibs_cache_root, scan_out_file_name)

    return _cache_file


_tkam_suffix = "_TKAM"


def _scan_window(dir_path):
    _hash = _get_scan_dir_path_hash(dir_path)
    if _hash is None:
        return None

    prescan_frame_layout = [
        [
            sg.Checkbox("Calculer les doublons", key="-CHECKBOX_CHECK_DUP_FILE-", default=False),
            sg.Checkbox("Récupérer les propriétés dossiers", key="-CHECKBOX_GET_DIR_PROPERTIES-", default=False),
            sg.Checkbox("Utiliser le cache", key="-CHECKBOX_SCAN_CACHING-", default=True)
        ],
        [sg.Output(size=(171, 43))],
    ]
    scan_frame_layout = [
        [sg.Text("", key="-TEXT_SCAN_INFO-", visible=False, size=(152, 1))],
        [sg.ProgressBar(max_value=0, orientation="h", size=(111, 19), key="-PROGRESS_BAR-", visible=False)],
    ]
    layout_scan = [
        [sg.Frame(f"Pré-Scan Dossier/Disque • {dir_path}", prescan_frame_layout, key="-PRESCAN_FRAME_LAYOUT-")],
        [sg.Frame("Empreinte Digitale Fichiers", scan_frame_layout, key="-SCAN_FRAME_LAYOUT-", visible=False)],
        [
            sg.Text("", size=(138, 1)),
            sg.Button("Scanner", key="-BUTTON_SCAN-", size=(13, 1))
        ],
    ]

    scan_window = sg.Window("Scan & Analyse", layout_scan, icon=theme.corelibs_path_ico, grab_anywhere=False)
    while True:
        event, values = scan_window.read()

        if event in (sg.WIN_CLOSED, None, "Exit"):
            break

        shutil.move(
            tools._pre_scan(dir_path,
                            encoding="utf-8",
                            std_print=True,
                            skip_directories_properties=not values["-CHECKBOX_GET_DIR_PROPERTIES-"]),
            _hash + _tkam_suffix
        )

        tools.scan_dir(
            dir_path,
            duplicated_files_indicator=values["-CHECKBOX_CHECK_DUP_FILE-"],
            skip_pre_scan=True,
            std_print=True,
            gui_instance=scan_window,
            caching=values["-CHECKBOX_SCAN_CACHING-"],
            force_excel_2_refresh=True
        )


def _scan_dir_path(dir_path, refresh=True):
    if refresh:
        _scan_window(dir_path)
    else:
        scan_out_file_name = tools.get_fingerprint(
            str(dir_path).replace("\\", "_").replace("/", "_").lower(), eval_as_string=True
        )

        _cache_file = lz.get_abspath(theme.user_corelibs_cache_root, scan_out_file_name)

        if not lz.is_file_exists(_cache_file, ignore_errors=True):
            if sg.popup("\nLe fichier cache sélectionné n'existe pas ou est corrompu\n"
                        "Souhaitez-vous rafraichir les données ?\n",
                        icon=theme.corelibs_path_ico,
                        title="Confirmation",
                        grab_anywhere=True,
                        custom_text=("Oui", "Non")) == "Oui":
                window.close()
                _scan_window(dir_path)
            else:
                return None
        else:
            tools.scan_dir(dir_path, skip_pre_scan=True)


theme.set_theme()
sg.theme(theme.active_theme)

main_layout = [
    [sg.Image(theme.corelibs_path + r"\gui\corelibs.png", size=(370, 108))],
    [sg.Combo([
        "documentation",
        "afficher dossier utilisateur",
        "purger dossier utilisateur",
        "gestion projet",
        "purifier les fichiers plats",
        "scan & analyse",
        "gestion environnements conda",
    ],
        readonly=True,
        size=(50, 1),
        enable_events=True,
        tooltip="Sélectionner une action dans la liste...",
        key="-COMBO-")]
]

project_layout = [
    [
        sg.Input("Nouveau projet python", size=(42, 1),
                 # change_submits=True,
                 key="-INPUT_PATH_PYTHON-"),
        sg.FolderBrowse(
            button_text="Parcourir",
            tooltip="Créer un nouveau projet python à l'emplacement indiqué",
            key="-FOLDER_BROWSE_PYTHON-")
    ],
    [
        sg.Input("Nouveau dossier modèle", size=(42, 1),
                 # change_submits=True,
                 key="-INPUT_PATH_DIR_SCAFFOLDING-"),
        sg.FolderBrowse(
            button_text="Parcourir",
            tooltip="Créer un nouveau dossier modèle à l'emplacement indiqué",
            key="-FOLDER_BROWSE_DIR_SCAFFOLDING-")
    ],
    [sg.Text("")],
    [sg.Button("OK", key="-BUTTON_OK_PROJECT-", size=(5, 1))]
]

cleanse_layout = [
    [
        sg.Input("", size=(33, 1), key="-INPUT_PATH_CLEANSE_FILE-"),
        sg.FileBrowse(
            file_types=(("Fichiers plats", "*.csv *.tsv *.txt"), ("Tous les fichiers", "*.*")),
            button_text="Parcourir",
            tooltip="Sélectionner un fichier plat à purifier",
            key="-FILE_BROWSE_CLEANSE-",
        ),
        sg.Button("OK", key="-BUTTON_OK_CLEANSE-", size=(5, 1))
    ]
]

total_history, history = _get_scan_history()
analysis_hitory_frame_layout = [
    [sg.Combo([v for k, v in history.items()],
              readonly=True,
              size=(48, 1),
              enable_events=True,
              tooltip="Sélectionner un scan existant",
              key="-COMBO_HISTORY-")],
    [sg.Text("")],
    [sg.Text("", size=(13, 1)),
     sg.Button("Rafraichir", key="-BUTTON_REFRESH_HISTORY-", size=(13, 1)),
     sg.Button("Afficher", key="-BUTTON_DISPLAY_HISTORY-", size=(13, 1))],
]

analysis_frame_layout = [
    [
        sg.Input("", size=(40, 1), enable_events=True, key="-INPUT_PATH_DIR_2_SCAN-"),
        sg.FolderBrowse(
            button_text="Parcourir",
            tooltip="Sélectionner un dossier à analyser",
            key="-FOLDER_BROWSE_DIR_2_SCAN-", target="-INPUT_PATH_DIR_2_SCAN-")
    ],
]

analysis_layout = [
    [sg.Frame("Nouveau Scan & Analyses...", analysis_frame_layout, key="-ANALYSIS_FRAME_LAYOUT-")],
    [sg.Text("")],
    [sg.Frame("Historiques Scan & Analyses...",
              analysis_hitory_frame_layout,
              visible=True if total_history > 0 else False,
              key="-ANALYSIS_HISTORY_FRAME_LAYOUT-")],
]

conda_layout = [
    [sg.Text("Hello CONDA =)")],
    [sg.Text("", size=(38, 1)), sg.Button("OK", key="-TEXT_OK_CONDA-", size=(5, 1))]
]

layout = [
    [sg.Column(main_layout, key="-MAIN_LAYOUT-")],
    [sg.Text("")],
    [
        sg.Column(project_layout, visible=False, key="-PROJECT_LAYOUT-"),
        sg.Column(cleanse_layout, visible=False, key="-CLEANSE_LAYOUT-"),
        sg.Column(analysis_layout, visible=False, key="-ANALYSIS_LAYOUT-"),
        sg.Column(conda_layout, visible=False, key="-CONDA_LAYOUT-"),
    ],
    [sg.Text(f"Thème \"{theme.active_theme_name}\"")] if config.UI_DISPLAY_THEME_NAME else ""
]

window = sg.Window(config.PACKAGE_NAME + " • V" + config.PACKAGE_VERSION,
                   layout, icon=theme.corelibs_path_ico, grab_anywhere=True)


event = values = None


def _main():
    global event, values

    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, None, "Exit"):
            break

        if values["-COMBO-"] == "documentation":
            webdoc.webdoc()
            window.close()
        elif values["-COMBO-"] == "afficher dossier utilisateur":
            _open_user_folder()
            window.close()
        elif values["-COMBO-"] == "purger dossier utilisateur":
            if sg.popup("\nSouhaitez-vous poursuivre la suppression de votre dossier utilisateur ?\n"
                        "\n\nNote: ce dossier sera reconstruit automatiquement au prochain appel "
                        "de la bibliothèque corelibs.\n ",
                        icon=theme.corelibs_path_ico,
                        title="Confirmation",
                        grab_anywhere=True,
                        custom_text=("Oui", "Non")) == "Oui":
                lz.delete_files(theme.user_corelibs_root, extension="*")
                window.close()
        elif values["-COMBO-"] == "gestion environnements conda":
            window.close()
            gui_conda.show_window(theme.active_theme)
        else:
            _display_layout(values["-COMBO-"])

        if event == "-BUTTON_OK_PROJECT-":
            _create_folder(values["-INPUT_PATH_PYTHON-"])
            _create_folder(values["-INPUT_PATH_DIR_SCAFFOLDING-"], "dir scaffolding")

        if event == "-BUTTON_OK_CLEANSE-" and values["-INPUT_PATH_CLEANSE_FILE-"]:
            _cleanse_file(values["-INPUT_PATH_CLEANSE_FILE-"])

        if values["-COMBO_HISTORY-"]:
            if event == "-BUTTON_REFRESH_HISTORY-":
                window.close()
                _scan_dir_path(values["-COMBO_HISTORY-"], refresh=True)
            elif event == "-BUTTON_DISPLAY_HISTORY-":
                _scan_dir_path(values["-COMBO_HISTORY-"], refresh=False)

        if event == "-INPUT_PATH_DIR_2_SCAN-" and values["-FOLDER_BROWSE_DIR_2_SCAN-"]:
            window.close()
            _scan_window(lz.get_abspath(values["-FOLDER_BROWSE_DIR_2_SCAN-"], ""))


_main()
