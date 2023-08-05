import os
import subprocess

import corelibs
from corelibs import lazy

dir_path, file_name = lazy.get_dir_n_basename(corelibs.__file__)
# URL = str(dir_path) + r"\docs\build\html\index.html"
URL = str(dir_path) + r"\docs\index.html"


def webdoc():
    try:  # should work on Windows
        os.startfile(URL)
    except AttributeError:
        pass
    except FileNotFoundError:
        pass
    else:
        try:  # should work on MacOS and most Linux versions
            subprocess.call(['open', URL])
        except FileNotFoundError:
            pass


if __name__ == "__main__":
    webdoc()
