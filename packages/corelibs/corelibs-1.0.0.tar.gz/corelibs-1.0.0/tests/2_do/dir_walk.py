import os


# traverse root directory, and list directories as dirs and files as files
def scan_dir(dir_path):
    index = 0
    for root, dirs, files in os.walk(dir_path):
        # path = root.split(os.sep)
        # print((len(path) - 1) * '---', root, os.path.basename(root))
        dirs.sort()
        # print("d", root, to.get_file_properties(root, pretty_byte_size=False))
        print(index, "d", root)

        for file in sorted(files):
            index += 1
            # print(len(path) * '-', root, "\\", file)
            _file = root + "\\" + file
            # print('-', _file, to.get_file_properties(_file, pretty_byte_size=False))
            print(index, '-', _file)

        index += 1


# scan_dir(r"D:\OneDrive\Documents\_TEST_")


# for f in os.listdir(r"\\wsl$\Ubuntu-20.04"):
#     print(f)


d = [os.path.join(dp, f) for dp, dn, fn in os.walk(os.path.expanduser(r"\\wsl$\Ubuntu-20.04")) for f in fn]
print(d)
