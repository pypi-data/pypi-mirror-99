import time

import enlighten


import platform
import random
import time

import enlighten


def initialize(manager, initials=15):
    """
    Simple progress bar example
    """

    # Simulated preparation
    pbar = manager.counter(total=initials, desc='Initializing:', unit='initials')
    for _ in range(initials):
        time.sleep(random.uniform(0.05, 0.25))  # Random processing time
        pbar.update()
    pbar.close()


def status_animation(manager):
    phases = ['֍', '֍ ֍', '֍ ֍ ֍', '֍ ֍ ֍ ֍', '֍ ֍ ֍ ֍ ֍', '֍ ֍ ֍ ֍', '֍ ֍ ֍', '֍ ֍', '֍']
    cursor = 0

    status_animation_phase = manager.status_bar(
        status_format='•( {phases} )•',
        phases=phases[cursor],
        position=2,
        fill=' ',
        justify=enlighten.Justify.CENTER
    )
    time.sleep(0.5)

    total_phases = len(phases)
    while True:
        time.sleep(0.5)
        cursor = (cursor + 1) % total_phases
        status_animation_phase.update(
            status_format='•( {phases} )•',
            phases=phases[cursor],
            position=2,
            fill=' ',
            justify=enlighten.Justify.CENTER
        )


def main():
    """
    Main function
    """

    with enlighten.get_manager() as manager:
        status = manager.status_bar(status_format=u'Enlighten{fill}Stage: {demo}{fill}{elapsed}',
                                    color='bold_underline_bright_black_on_lightslategray',
                                    justify=enlighten.Justify.CENTER, demo='Initializing',
                                    autorefresh=True, min_delta=0.5)
        docs = manager.term.link('https://python-enlighten.readthedocs.io/en/stable/examples.html',
                                 'Read the Docs')
        manager.status_bar(' More examples on %s! ' % docs, position=1, fill='-',
                           justify=enlighten.Justify.CENTER)

        initialize(manager, 15)
        initialize(manager, 30)
        status_animation(manager)


if __name__ == '__main__':
    main()
