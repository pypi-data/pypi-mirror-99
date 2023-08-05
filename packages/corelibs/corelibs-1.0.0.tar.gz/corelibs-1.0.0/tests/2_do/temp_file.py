# https://stackabuse.com/the-python-tempfile-module/
# https://stackoverflow.com/questions/23212435/permission-denied-to-write-to-my-temporary-file
import os
import tempfile  # 1

print("Creating one temporary file...")

temp = tempfile.NamedTemporaryFile(mode="wb", suffix="_corelibs", delete=False)  # 2

try:
    print("Created file is:", temp)  # 3
    print("Name of the file is:", temp.name)  # 4

    temp.write(b"Hello\x09\x3B\x09Kim")
finally:
    print("Closing the temp file")
    temp.close()  # 5
    os.unlink(temp.name)
