import time

import enlighten


with enlighten.get_manager() as manager:
    status_bar = manager.status_bar(status_format='{fill} Exécution : {program} {fill} Statut : {status}',
                                    color='bold_underline_bright_black_on_lightslategray',
                                    program='Demo',
                                    status='INITIALISATION')
    manager.status_bar(' corelibs@timing ', position=1, fill='-',
                       justify=enlighten.Justify.CENTER)

    time.sleep(1)
    status_bar.update(status='EN COURS...')
    for _ in range(400):
        print(_)
    time.sleep(1)
    status_bar.update(status='TERMINÉE')
