# get_caller_module_name.py
from corelibs import lazy as lz


def get_module_info():
    caller_name = lz.get_caller_module_name()
    print(f"Le nom du module python appelant est \"{caller_name}\"")
