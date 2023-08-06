# is_schema.py
# %%
from corelibs import cleanse as cls


chaine = """
Somewhere, something incredible is waiting to be known.

For small creatures such as we the vastness is bearable only through love.

We're made of star stuff. We are a way for the cosmos to know itself.

If you want to make an apple pie from scratch, you must first create the universe.

Science is a way of thinking much more than it is a body of knowledge.

Imagination will often carry us to worlds that never were. But without it we go nowhere.

Every one of us is, in the cosmic perspective, precious. If a human disagrees with you, let him live. In a hundred billion galaxies, you will not find another.

Science is not only compatible with spirituality; it is a profound source of spirituality.

Absence of evidence is not evidence of absence.

We live in a society exquisitely dependent on science and technology, in which hardly anyone knows anything about science and technology.

===

Quelque part, quelque chose d'incroyable attend d'être connu.

Pour les petites créatures comme nous, l'immensité n'est supportable que par l'amour.

Nous sommes faits de poussières d'étoiles. Nous sommes un moyen pour le cosmos de se connaître.

Si vous voulez faire une tarte aux pommes à partir de rien, vous devez d'abord créer l'univers.

La science est une façon de penser bien plus qu’un ensemble de connaissances.

L'imagination nous transportera souvent dans des mondes qui ne l'ont jamais été. Mais sans elle, nous allons nulle part.

Chacun de nous est, dans la perspective cosmique, précieux. Si une personne n'est pas d'accord avec vous, laissez la vivre. Dans un rayon de cent milliards de galaxies, vous n'en trouverez pas d'autres.

La science n'est pas seulement compatible avec la spiritualité; c'est une source profonde de spiritualité.

L'absence de preuve n'est pas une preuve d'absence.

Nous vivons dans une société extrêmement dépendante de la science et de la technologie, dans laquelle presque personne ne sait rien de la science et de la technologie.

Carl SAGAN
"""

# recherche début de chaîne...
print(cls.is_schema(chaine, schema=r"^somewhere.*", regex_flag=None))  # affichera False car Somewhere ne commence qu'à la 2ème ligne

# recherche du mot somewhere sans distinction
print(cls.is_schema(chaine, schema=r"somewhere"))  # affichera True

# recherche début de chaîne en "cassant" la chaîne principale
for s in chaine.split("\n"):
    if cls.is_schema(s, schema=r"^somewhere.*"):
        print(s)  # affichera Somewhere, something incredible is waiting to be known.

# recherche si signé par Carl SAGAN
print(cls.is_schema(chaine, schema=r"Carl SAGAN$"))  # affichera True


# %%
# Exemple plus concrète et sérieuse =þ
# validation d'un format de fichier avec ID, Prénom et Date anniversaire sous la forme JJ/MM/AAAA, séparé par des ;
# ce format est traduit par le schéma suivant ^[0-9]{2};\w+;([0-9]{2}\/){2}[0-9]{4}
chaine = """
ID;Prénom;Date Anniversaire
01;Kim;28/11/2013
02,Mickey,18/11/1928
XX;YODA;1980
"""

_chaine = chaine.split("\n")
res = _chaine[0:2]

for s in _chaine[2:-1]:
    if cls.is_schema(s, r"^[0-9]{2};\w+;([0-9]{2}\/){2}[0-9]{4}"):
        res.append(s + "OK".rjust(31 - len(s)))
    else:
        res.append(s + "KO".rjust(31 - len(s)))

res.append("".join(_chaine[-1:]))  # inutile mais pour être rigoureux, il y a la dernière chaine à blanc qui doit être prise en compte...
print("\n".join(res))
# ce qui affichera, avec la 2ème ligne validée et les autres lignes non validées
# ID;Prénom;Date Anniversaire
# 01;Kim;28/11/2013            OK
# 02,Mickey,18/11/1928         KO
# XX;YODA;1980                 KO
