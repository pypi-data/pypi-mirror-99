import os
import re
import subprocess
import sys
from subprocess import Popen, PIPE

import PySimpleGUI as sg

from corelibs import config, lazy as lz, tools, cleanse
from corelibs.gui import theme

conda_env = {}
current_selected_env_sh256 = current_selected_env_conda_sh256 = current_selected_env_pip_sh256 = \
    current_selected_env_revision_sh256 = active_env = conda_requirement_path = pip_requirement_path = revision_path = \
    ""

ansi_escape = re.compile(r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])")

def list_conda_path():
    # os.system('cmd /k "color a & date"')
    os.system('cmd /c "where /R C: Anaconda"')


def _check_conda_path():
    if not lz.is_file_exists(config.UI_CONDA_PATH, is_dir=True):
        msg = f"\nLe chemin Conda \"{config.UI_CONDA_PATH}\" n'existe pas" \
              f"\n\nVeuillez indiquer le bon chemin dans votre fichier de configuration \"user_config.py\" " \
              f"(constante UI_CONDA_PATH)" \
              f"\n\nReportez vous à la documentation pour plus de précisions...\n"
        sg.popup_ok(msg, title="Alerte", icon=theme.corelibs_path_ico, grab_anywhere=True)
        sys.exit(1)


def get_conda_env():
    global conda_env

    command = "\"" + lz.get_abspath(config.UI_CONDA_PATH, "conda") + "\" env list"
    _check_conda_path()

    pipe = Popen(command, stdout=PIPE, encoding="utf-8")

    while True:
        line = pipe.stdout.readline()
        if not line:
            break

        if not line.rstrip().startswith("#"):
            rec = re.compile(r"([\w\-]*)( {5,})(.*)", re.IGNORECASE)
            try:
                groups = rec.search(line.rstrip()).groups()
            except AttributeError:
                pass

            if groups[0]:
                conda_env.update({groups[0]: groups[2].replace("*  ", "")})


def get_conda_env_list(env):
    if str(env) == "":
        return ""

    command = "\"" + lz.get_abspath(config.UI_CONDA_PATH, "conda") + "\" list -n " + str(env)
    _check_conda_path()

    pipe = Popen(command, stdout=PIPE, encoding="utf-8")
    text = pipe.communicate()[0]
    packages_list = ""

    packages_list += f"Liste des packages installés sur l'environnement \"{str(env)}\"\n\n"

    for i, t in enumerate(text.splitlines()):
        if i == 2:
            header = [h for h in t.split(" ") if h]
            packages_list += header[0].rjust(5, " ") + " Nom package (version)\n\n"
            # + header[1].ljust(123, " ") \
            # + header[2].rjust(31, " ") + "\n"
            # + header[3].rjust(23, " ") \
            # + header[4].rjust(23, " ") + "\n"
        elif i > 2:
            body = [b for b in t.split(" ") if b]
            if len(body) > 1:
                packages_list += str(i - 2).rjust(5, " ") + " " + body[0] + " (" + body[1] + ")\n"
                # + body[2].rjust(23, " ") \
                # + (body[3].rjust(23, " ") if len(body) == 4 else "") + "\n"

    return packages_list


def extract_requirement(requirement_file_path, env, conda=True):
    if not isinstance(conda, bool):
        return None

    if conda:
        command = "\"" + lz.get_abspath(config.UI_CONDA_PATH, "conda") + "\" list -n " + str(env) + " -e"
    else:
        command = f"pip list --format=freeze --path \"{env}\\Lib\\site-packages\""

    pipe = Popen(command, stdout=PIPE, encoding="utf-8")
    with open(requirement_file_path, "w") as f_out:
        # f_out.write(pipe.communicate()[0])
        while True:
            line = pipe.stdout.readline()
            if not line:
                break
            if not ansi_escape.search(line.rstrip()):
                f_out.write(line.rstrip() + "\n")


def extract_revision(revision_file_path, env):
    command = "\"" + lz.get_abspath(config.UI_CONDA_PATH, "conda") + "\" list -n " + str(env) + " --revision"

    pipe = Popen(command, stdout=PIPE, encoding="utf-8")
    with open(revision_file_path, "w") as f_out:
        # f_out.write(pipe.communicate()[0])
        while True:
            line = pipe.stdout.readline()
            if not line:
                break
            if not ansi_escape.search(line.rstrip()):
                f_out.write(line.rstrip() + "\n")


def get_requirement(requirement_file_path, multiline):
    f_in = open(requirement_file_path, "r")
    multiline.update(f_in.read())
    f_in.close()


def clone_env(env, new_env_name, window):
    _new_env_name = cleanse.is_str(new_env_name, strip_accented_char=True,
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

    if sg.popup(f"\nL'environnement nommé \"{env}\" sera clôné avec le nouveau nom \"{_new_env_name}\".\n"
                "\n\nMerci de confirmer le clônage et de patienter (selon le nombre de packages installés dans "
                "l'environnement source, cette action peut prendre un peu de temps).\n",
                icon=theme.corelibs_path_ico,
                title="Confirmation",
                grab_anywhere=True,
                custom_text=("Oui", "Non")) == "Oui":
        command = "\"" + lz.get_abspath(config.UI_CONDA_PATH, "conda") + "\" create -n \"" \
                  + _new_env_name + "\" --clone \"" + str(env) + "\" -y"
        subprocess.run(command, shell=True, encoding="utf-8")

        get_conda_env()
        window["-COMBO_ENV-"].update(values=[conda for conda in conda_env.keys()])
        window["-INPUT_NEW_ENV_NAME_2_CLONE-"]("Nom environnement")
        sg.popup_ok(f"L'environnement \"{_new_env_name}\" a été clôné avec succès à "
                    f"partir de l'environnement \"{env}\"",
                    title="Succès", icon=theme.corelibs_path_ico, grab_anywhere=True)


def conda_update(env):
    command = "\"" + lz.get_abspath(config.UI_CONDA_PATH, "conda") + "\" update -n \"" + str(env) + "\" --all -y"
    subprocess.run(command, shell=True, encoding="utf-8")


def conda_remove(env):
    command = "\"" + lz.get_abspath(config.UI_CONDA_PATH, "conda") + "\" remove -n \"" + str(env) + "\" --all -y"
    subprocess.run(command, shell=True, encoding="utf-8")


def conda_restore(env, revision, get_revision_numbers=False):
    global revision_path

    regex_sequence = r"(.*)(rev )(\d+)(.*)?"
    res = re.compile(regex_sequence, re.I)

    _groups = []
    with open(revision_path, "r", encoding="utf-8") as f_in:
        for line in f_in:
            _ = res.search(line)
            if _ is not None:
                _groups.append(_.groups()[2])

    if get_revision_numbers:
        return _groups

    command = "\"" + lz.get_abspath(config.UI_CONDA_PATH, "conda") + "\" install --revision \"" \
              + str(revision) + "\" -n \"" + env + "\" --force-reinstall -q -y"
    subprocess.run(command, shell=True, encoding="utf-8")


def show_window(_theme):
    global current_selected_env_sh256, current_selected_env_conda_sh256, current_selected_env_pip_sh256, \
        current_selected_env_revision_sh256, conda_requirement_path, pip_requirement_path, revision_path

    revision_groups = []

    get_conda_env()

    sg.theme(_theme)

    tab_active_layout_actions = [
        [
            sg.Input("Nom environnement", size=(58, 1),
                     tooltip="Nom du nouveau environnement clôné à partir de l'environnement actif choisi",
                     key="-INPUT_NEW_ENV_NAME_2_CLONE-"),
            sg.Button("Clôner", key="-BUTTON_CLONE-", size=(13, 1)),
            sg.Button("Sauvegarder", key="-BUTTON_BACKUP-", size=(13, 1)),
            sg.Button("Mettre à jour", key="-BUTTON_UPDATE-", size=(13, 1))
        ],
    ]

    tab_active_layout = [
        [sg.Multiline("", key="-MULTILINE_ACTIVE-", size=(108, 31))],
        [sg.Column(tab_active_layout_actions, visible=False, key='-ACTIVE_LAYOUT_ACTIONS-')],
    ]

    tab_revision_layout_actions = [
        [
            # sg.Text("", size=(81, 1)),
            # sg.Input("N° révision", size=(93, 1),
            #          tooltip="Choisir un numéro de révision antérieur pour la restauration",
            #          key="-INPUT_REVISION_NUMBER-"),
            sg.Combo(["N° révision"],
                     readonly=True,
                     default_value="N° révision",
                     size=(93, 1),
                     tooltip="Sélectionner un numéro de révision antérieur pour la restauration...",
                     key="-COMBO_REVISION_NUMBER-"),
            sg.Button("Restaurer", key="-BUTTON_RESTORE-", size=(13, 1))
        ],
    ]

    tab_revision_layout = [
        [sg.Multiline("", key="-MULTILINE_REVISION-", size=(108, 31))],
        [sg.Column(tab_revision_layout_actions, visible=False, key='-REVISION_LAYOUT_ACTIONS-')],
    ]

    tab_requirement_conda_layout_actions = [
        [
            sg.Input("", key="-INPUT_REQUIREMENT_CONDA-", visible=False, change_submits=True),
            sg.Text("", size=(81, 1)),
            sg.FileSaveAs(
                target="-INPUT_REQUIREMENT_CONDA-",
                button_text="Enregistrer sous",
                tooltip="Enregistrer le fichier requirement (vision Conda)",
                file_types=(("Fichiers Texte", "*.txt"),),
                size=(13, 1),
                key="-FILE_BROWSE_CONDA_REQUIREMENT-")
        ],
    ]

    tab_requirement_conda_layout = [
        [sg.Multiline("", key="-MULTILINE_BCK_CONDA-", size=(108, 31))],
        [sg.Column(tab_requirement_conda_layout_actions, visible=False, key='-BCK_CONDA_LAYOUT_ACTIONS-')],
    ]

    tab_requirement_pip_layout_actions = [
        [
            sg.Input("", key="-INPUT_REQUIREMENT_PIP-", visible=False, change_submits=True),
            sg.Text("", size=(81, 1)),
            sg.FileSaveAs(
                target="-INPUT_REQUIREMENT_PIP-",
                button_text="Enregistrer sous",
                tooltip="Enregistrer le fichier requirement (vision PIP)",
                file_types=(("Fichiers Texte", "*.txt"),),
                size=(13, 1),
                key="-FILE_BROWSE_PIP_REQUIREMENT-")
        ],
    ]

    tab_requirement_pip_layout = [
        [sg.Multiline("", key="-MULTILINE_BCK_PIP-", size=(108, 31))],
        [sg.Column(tab_requirement_pip_layout_actions, visible=False, key='-BCK_PIP_LAYOUT_ACTIONS-')],
    ]

    layout = [
        [
            sg.Combo([conda for conda in conda_env.keys()],
                     readonly=True,
                     size=(75, 1),
                     enable_events=True,
                     tooltip="Sélectionner un environnement conda disponible...",
                     key="-COMBO_ENV-"),
            sg.Button("Supprimer", key="-BUTTON_DELETE-", size=(13, 1)),
            sg.Button("Explorer", key="-BUTTON_EXPLORER-", size=(13, 1))
        ],
        [
            sg.TabGroup([[
                sg.Tab("Packages actifs", tab_active_layout, key="-TAB_ACTIVE_LAYOUT-"),
                sg.Tab("Révisions", tab_revision_layout, key="-TAB_REVISION_LAYOUT-"),
                sg.Tab("Requirements (conda)", tab_requirement_conda_layout, key="-TAB_REQUIREMENT_CONDA_LAYOUT-"),
                sg.Tab("Requirements (pip)", tab_requirement_pip_layout, key="-TAB_REQUIREMENT_PIP_LAYOUT-"),
            ]])
        ],
    ]

    window = sg.Window("Environnements Conda", layout, icon=theme.corelibs_path_ico)

    while True:
        event, values = window.read()
        # print(event, values)
        if event in (None, "Exit"):
            break

        if values["-COMBO_ENV-"] and values["-COMBO_ENV-"] != "gestion environnements conda":
            active_env = values["-COMBO_ENV-"]
            try:
                window["-MULTILINE_ACTIVE-"].update(get_conda_env_list(active_env))

                current_selected_env_sh256 = tools.get_fingerprint(active_env, eval_as_string=True)
                current_selected_env_conda_sh256 = tools.get_fingerprint(current_selected_env_sh256 + "_conda",
                                                                         eval_as_string=True)
                current_selected_env_pip_sh256 = tools.get_fingerprint(current_selected_env_sh256 + "_pip",
                                                                       eval_as_string=True)
                current_selected_env_revision_sh256 = tools.get_fingerprint(current_selected_env_sh256 + "_revision",
                                                                            eval_as_string=True)

                revision_path = lz.get_abspath(
                    theme.user_corelibs_env_requirements_root,
                    current_selected_env_revision_sh256
                )
                extract_revision(revision_path, active_env)
                get_requirement(revision_path, window["-MULTILINE_REVISION-"])

                conda_requirement_path = lz.get_abspath(
                    theme.user_corelibs_env_requirements_root,
                    current_selected_env_conda_sh256
                )
                if not lz.is_file_exists(conda_requirement_path):
                    extract_requirement(conda_requirement_path, active_env, conda=True)
                get_requirement(conda_requirement_path, window["-MULTILINE_BCK_CONDA-"])

                pip_requirement_path = lz.get_abspath(
                    theme.user_corelibs_env_requirements_root,
                    current_selected_env_pip_sh256
                )
                if not lz.is_file_exists(pip_requirement_path):
                    extract_requirement(pip_requirement_path, conda_env[active_env], conda=False)
                get_requirement(pip_requirement_path, window["-MULTILINE_BCK_PIP-"])

                for w in ("-ACTIVE_LAYOUT_ACTIONS-", "-REVISION_LAYOUT_ACTIONS-",
                          "-BCK_CONDA_LAYOUT_ACTIONS-", "-BCK_PIP_LAYOUT_ACTIONS-"):
                    window[w].update(visible=True)

                revision_groups = conda_restore(active_env, None, get_revision_numbers=True)
                window["-COMBO_REVISION_NUMBER-"].update(
                    values=[rev for rev in revision_groups]
                )
            except KeyError:
                msg = f"\nL'environnement \"{active_env}\" n'existe pas\n"
                sg.popup_ok(msg, title="Alerte", icon=theme.corelibs_path_ico, grab_anywhere=True)

            if event == "-BUTTON_EXPLORER-":
                active_env = values["-COMBO_ENV-"]
                try:
                    lz.open_explorer(conda_env[active_env])
                except KeyError:
                    msg = f"\nL'environnement \"{active_env}\" n'existe pas\n"
                    sg.popup_ok(msg, title="Alerte", icon=theme.corelibs_path_ico, grab_anywhere=True)

            if event == "-BUTTON_CLONE-" and (values["-INPUT_NEW_ENV_NAME_2_CLONE-"]
                                              and values["-INPUT_NEW_ENV_NAME_2_CLONE-"] != "Nom environnement"):
                clone_env(values["-COMBO_ENV-"], values["-INPUT_NEW_ENV_NAME_2_CLONE-"], window)

            if event == "-BUTTON_BACKUP-":
                extract_requirement(conda_requirement_path, values["-COMBO_ENV-"], conda=True)
                get_requirement(conda_requirement_path, window["-MULTILINE_BCK_CONDA-"])
                extract_requirement(pip_requirement_path, conda_env[values["-COMBO_ENV-"]], conda=False)
                get_requirement(pip_requirement_path, window["-MULTILINE_BCK_PIP-"])
                sg.popup_ok(f"La sauvegarde de l'environnement \"{values['-COMBO_ENV-']}\" a été réalisée avec succès",
                            title="Succès", icon=theme.corelibs_path_ico, grab_anywhere=True)

            if event == "-BUTTON_UPDATE-":
                if sg.popup(f"\nSouhaitez vous faire une sauvegarde de votre environnement \"{values['-COMBO_ENV-']}\" "
                            f"avant de le mettre à jour ?\n"
                            "\n\nMerci de patienter (selon le nombre de packages installés dans "
                            "l'environnement source, la mise à jour peut prendre un peu de temps).\n",
                            icon=theme.corelibs_path_ico,
                            title="Confirmation",
                            grab_anywhere=True,
                            custom_text=("Oui", "Non")) == "Oui":
                    extract_requirement(conda_requirement_path, values["-COMBO_ENV-"], conda=True)
                    get_requirement(conda_requirement_path, window["-MULTILINE_BCK_CONDA-"])
                    extract_requirement(pip_requirement_path, conda_env[values["-COMBO_ENV-"]], conda=False)
                    get_requirement(pip_requirement_path, window["-MULTILINE_BCK_PIP-"])

                conda_update(values["-COMBO_ENV-"])
                window["-MULTILINE_ACTIVE-"].update(get_conda_env_list(values["-COMBO_ENV-"]))
                extract_revision(revision_path, values["-COMBO_ENV-"])
                get_requirement(revision_path, window["-MULTILINE_REVISION-"])
                sg.popup_ok(f"L'environnement \"{values['-COMBO_ENV-']}\" a été mis à jour avec succès",
                            title="Succès", icon=theme.corelibs_path_ico, grab_anywhere=True)

            if event == "-BUTTON_DELETE-":
                if sg.popup(f"\nSouhaitez vous supprimer l'environnement \"{values['-COMBO_ENV-']}\"?\n",
                            icon=theme.corelibs_path_ico,
                            title="Confirmation",
                            grab_anywhere=True,
                            custom_text=("Oui", "Non")) == "Oui":
                    conda_remove(values["-COMBO_ENV-"])
                    for w in ("-COMBO_ENV-", "-MULTILINE_ACTIVE-", "-MULTILINE_BCK_CONDA-", "-MULTILINE_BCK_PIP-"):
                        window[w].update("")
                    get_conda_env()
                    window["-COMBO_ENV-"].update(
                        values=[conda for conda in conda_env.keys() if conda != values["-COMBO_ENV-"]]
                    )
                    # lz.delete_files(conda_env[values["-COMBO_ENV-"]], remove_empty_dir=True, verbose=False)
                    sg.popup_ok(f"L'environnement \"{values['-COMBO_ENV-']}\" a été supprimé avec succès",
                                title="Succès", icon=theme.corelibs_path_ico, grab_anywhere=True)

            if event == "-BUTTON_RESTORE-" and values["-COMBO_REVISION_NUMBER-"] != "N° révision":
                try:
                    revision = int(values["-COMBO_REVISION_NUMBER-"])

                    if sg.popup(f"\nSouhaitez vous restaurer l'environnement \"{values['-COMBO_ENV-']}\" en revenant à"
                                f" la révision \"{revision}\"?\n"
                                "\n\nMerci de patienter (selon le nombre de packages installés dans "
                                "l'environnement source, la restauration peut prendre un peu de temps).\n",
                                icon=theme.corelibs_path_ico,
                                title="Confirmation",
                                grab_anywhere=True,
                                custom_text=("Oui", "Non")) == "Oui":
                        if str(revision) not in revision_groups:
                            sg.popup_ok(
                                f"Le n° de révision \"{revision}\" n'appartient pas à la liste des révisions disponibles"
                                f" pour l'environnement \"{values['-COMBO_ENV-']}\"",
                                title="Erreur", icon=theme.corelibs_path_ico, grab_anywhere=True)
                        else:
                            conda_restore(values['-COMBO_ENV-'], revision)
                            window["-MULTILINE_ACTIVE-"].update(get_conda_env_list(values['-COMBO_ENV-']))
                            extract_revision(revision_path, values["-COMBO_ENV-"])
                            get_requirement(revision_path, window["-MULTILINE_REVISION-"])
                            sg.popup_ok(f"L'environnement \"{values['-COMBO_ENV-']}\" a été restauré avec succès",
                                        title="Succès", icon=theme.corelibs_path_ico, grab_anywhere=True)
                except ValueError:
                    sg.popup_ok(f"Le n° révision \"{values['-COMBO_REVISION_NUMBER-']}\" n'est pas un entier",
                                title="Erreur", icon=theme.corelibs_path_ico, grab_anywhere=True)

            if event == "-INPUT_REQUIREMENT_CONDA-" and values["-INPUT_REQUIREMENT_CONDA-"]:
                lz.copy(conda_requirement_path, values["-INPUT_REQUIREMENT_CONDA-"])
                sg.popup_ok(f"Le fichier requirement conda \"{values['-INPUT_REQUIREMENT_CONDA-']}\" a été enregistré "
                            f"avec succès", title="Succès", icon=theme.corelibs_path_ico, grab_anywhere=True)

            if event == "-INPUT_REQUIREMENT_PIP-" and values["-INPUT_REQUIREMENT_PIP-"]:
                lz.copy(pip_requirement_path, values["-INPUT_REQUIREMENT_PIP-"])
                sg.popup_ok(f"Le fichier requirement pip \"{values['-INPUT_REQUIREMENT_PIP-']}\" a été enregistré avec "
                            f"succès", title="Succès", icon=theme.corelibs_path_ico, grab_anywhere=True)
