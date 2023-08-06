import sys
import subprocess
from corelibs import log

exe = r"D:\OneDrive\Documents\_TEST_\x64\7za.exe"
target = r"D:\OneDrive\Documents\_TEST_\test.7z"
source = r"D:\OneDrive\Documents\_TEST_\Zatoichi.avi"
command = exe + " a -t7z \"" + target + "\" \"" + source + "\" -mx9"


@log.status_bar(status_bar_title="Compression...")
def execute(command):
    try:
        subprocess.check_call(
            command,
            bufsize=0,
            shell=True,
            stdout=sys.stdout,  # subprocess.PIPE
            stderr=subprocess.STDOUT,
            universal_newlines=True
        )
    except subprocess.CalledProcessError as e:
        print(e.returncode)
    finally:
        print("OK")


execute(command)
