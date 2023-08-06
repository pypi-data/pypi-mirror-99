# get_file_properties.py
# %%
from corelibs import tools as to


# %%
# récupération des informations par défaut (affichange la taille dynamiquement, à la valeur la plus appropriée)
filename = r"D:\OneDrive\Documents\_TEST_\2020-11-11.jpg"
filename_properties = to.get_file_properties(filename)
print(filename_properties)
# affiche l'objet FileProperties(
#   st_mode=33206,
#   st_ino=11540474045256220,
#   st_dev=3199390331,
#   st_nlink=1,
#   st_uid='Invités',
#   st_gid=0,
#   st_size='96.26 Ko',  # la taille est exprimée en Ko pour une petite image
#   st_atime='13/11/2020 22:22:21',
#   st_mtime='11/11/2020 22:10:46',
#   st_ctime='11/11/2020 22:10:39')

# %%
# récupération des informations par défaut (affichange la taille dynamiquement, à la valeur la plus appropriée)
filename = r"D:\OneDrive\Documents\_TEST_\Zatoichi.avi"
filename_properties = to.get_file_properties(filename)
print(filename_properties)
# affiche l'objet FileProperties(
#   st_mode=33206,
#   st_ino=1125899906961926,
#   st_dev=3199390331,
#   st_nlink=1, st_uid='miche',
#   st_gid=0,
#   st_size='699.78 Mo',  # la taille est exprimée en Mo pour le film Zatoichi.avi
#   st_atime='13/11/2020 22:19:27',
#   st_mtime='22/03/2013 20:17:02',
#   st_ctime='10/11/2020 15:56:52')

# %%
# récupération des informations avec la taille ventilée par unité de mesure (jusqu'au To)
# fichier plus gros
filename = r"D:\OneDrive\Documents\_TEST_\Zatoichi.avi"
filename_properties = to.get_file_properties(filename, pretty_byte_size=False)
print(filename_properties)
# affiche l'objet FileProperties(
#   st_mode=33206,
#   st_ino=1125899906961926,
#   st_dev=3199390331,
#   st_nlink=1,
#   st_uid='miche',
#   st_gid=0,
#   st_size=ByteSize(  # objet ByteSize contenant toutes les tailles converties depuis le nb d'octets
#       byte=733775872,
#       kilobyte=716578.0,
#       megabyte=699.78,
#       gigabyte=0.68,
#       terabyte=0.0),
#   st_atime='13/11/2020 22:19:27',
#   st_mtime='22/03/2013 20:17:02',
#   st_ctime='10/11/2020 15:56:52')
# pour accéder à la taille en gigaoctet (gigabyte) par exemple récupérer directement son attribut
print(
    "La faille en Go du fichier Zatoichi.avi est de {taille} Go"
    .format(taille=filename_properties.st_size.gigabyte)
)  # affichera "La faille en Go du fichier Zatoichi.avi est de 0.68 Go"

# %%
# récupération des informations par défaut (affichange la taille dynamiquement, à la valeur la plus appropriée)
filename = r"D:\OneDrive\Documents\_TEST_"
filename_properties = to.get_file_properties(filename)
print(filename_properties)
# affiche l'objet FileProperties(
#   st_mode=16895,
#   st_ino=281474976804077,
#   st_dev=3199390331,
#   st_nlink=1,
#   st_uid='miche',
#   st_gid=0,
#   st_size='4.12 Go',  # la taille est exprimée en Go pour le répertoire _TEST_
#   st_atime='14/11/2020 18:23:11',
#   st_mtime='14/11/2020 17:58:08',
#   st_ctime='07/10/2020 22:17:12')
