# get_bytes_size_formats.py
# %%
from corelibs import lazy as lz


print(lz.get_bytes_size_formats(0))
# affiche ByteSize(byte=0, kilobyte=0.0, megabyte=0.0, gigabyte=0.0, terabyte=0.0)
print(lz.get_bytes_size_formats(153800565))
# affiche ByteSize(byte=153800565, kilobyte=150195.86, megabyte=146.68, gigabyte=0.14, terabyte=0.0)
print(lz.get_bytes_size_formats(1739886085))
# affiche ByteSize(byte=1739886085, kilobyte=1699107.5, megabyte=1659.28, gigabyte=1.62, terabyte=0.0)

