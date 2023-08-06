import click

from corelibs.gui import gui


@click.command()
def main():
    gui._main()


if __name__ == "__main__":
    main()
