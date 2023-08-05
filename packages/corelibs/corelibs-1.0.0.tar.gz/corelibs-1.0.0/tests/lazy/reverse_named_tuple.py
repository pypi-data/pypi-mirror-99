# reverse_named_tuple.py
# %%
from corelibs import lazy as lz


# %%
# création d'un tuple nommé
byte_size = lz.get_bytes_size_formats(1739886085)
print(byte_size)
# ByteSize(byte=1739886085, kilobyte=1699107.5, megabyte=1659.28, gigabyte=1.62, terabyte=0.0)

# %%
# renverser le tuple nommé
reverse_nt = lz.reverse_named_tuple(byte_size)
print(reverse_nt)
# ByteSize(terabyte=0.0, gigabyte=1.62, megabyte=1659.28, kilobyte=1699107.5, byte=1739886085.0)

# %%
# comme la classe originale existe lors de l'inversion, il est toujours possible d'accéder à un des attributs
print(reverse_nt.megabyte)  # affichera 1659.28

# %%
# renverser le tuple nommé avec conversion en dictionnaire
reverse_nt = lz.reverse_named_tuple(byte_size, convert_2_dict=True)
print(reverse_nt)
# {'terabyte': 0.0, 'gigabyte': 1.62, 'megabyte': 1659.28, 'kilobyte': 1699107.5, 'byte': 1739886085}

# %%
# exemple avec dir_n_basename()
dir_n_basename = lz.get_dir_n_basename(r"C:\Users\M47624\corelibs\tests\lazy\get_dir_n_basename.py")
print(dir_n_basename)
# DirPathnBaseName(dir_path='C:\\Users\\M47624\\corelibs\\tests\\lazy', base_name='get_dir_n_basename.py')

# %%
print(lz.reverse_named_tuple(dir_n_basename))
# DirPathnBaseName(base_name='get_dir_n_basename.py', dir_path='C:\\Users\\M47624\\corelibs\\tests\\lazy')

# %%
print(dir_n_basename.base_name)  # get_dir_n_basename.py
