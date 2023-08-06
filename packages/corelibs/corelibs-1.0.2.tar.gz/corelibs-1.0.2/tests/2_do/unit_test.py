from corelibs import tools as to

# if not lz.is_file_exists(r"\\wsl$\Ubuntu-20.04\init", is_dir=True, ignore_errors=True):
#     print("bla")


finger_print = to.get_fingerprint(r"\\wsl$\Ubuntu-20.04\init", ignore_errors=True)
print(finger_print)