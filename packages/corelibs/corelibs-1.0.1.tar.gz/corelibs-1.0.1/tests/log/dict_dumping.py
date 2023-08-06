# dict_dumping.py
from corelibs import config, log, tools as to

# le niveau d'alerte par défaut est à INFO, correspondant à la valeur 20...
# 10 correspond à DEBUG, ce qui a pour effet d'afficher le dumping...
config.DEFAULT_LOG_LEVEL = 10  # décommenter pour baisser le niveau d'alerte à DEBUG


@log.dict_dumping
def test_namedtuple():
    filename = r"D:\OneDrive\Documents\_TEST_\2020-11-11.jpg"
    file_properties = to.get_file_properties(filename, pretty_byte_size=False)
    return file_properties


# affichage simple du tuple nommé pas toujours évident à lire selon complexcité
print(test_namedtuple())  # FileProperties(st_mode=33206, st_ino=11540474045256220, st_dev=3199390331, st_nlink=1, st_uid='Invités', st_gid=0, st_size=ByteSize(byte=98569, kilobyte=96.26, megabyte=0.09, gigabyte=0.0, terabyte=0.0), st_atime='14/11/2020 22:27:01', st_mtime='11/11/2020 22:10:46', st_ctime='11/11/2020 22:10:39')
test_namedtuple()
