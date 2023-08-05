# replace_chaining_AL.py
# exemple programme pour gérer le mailing list d'Alex L.
from corelibs import cleanse as cls

# %%
with open(r"D:\OneDrive\Desktop\Alex_L_LD.txt") as f_in:
    string = f_in.read()


def name_2_upper(m):
    return m.groups()[1] + " " + m.groups()[0].upper()[:-1] + " " + m.groups()[2]


def mail_2_name(m):
    return m.groups()[0].title() + " " + m.groups()[1].upper() + \
           " <" + m.groups()[0].lower() + "." + m.groups()[1].lower() + m.groups()[2].lower() + ">"


res = cls.replace_chaining(
    string,
    udf_0=lambda x: cls.is_str(x, chars_2_replace={  # nettoyage caractères zarbioïdes
        "Ã©": "é",
        "Ã´": "ô",
        "Ã§": "ç",
        "Ã‡": "C"
    }),
    udf_1=lambda x: cls.replace(x, r"((([-\w',çéô Ç]* )*(<[-\w.@]*>)|([\w .@]*)))(;)", r"\1\n"),  # séparer en liste
    udf_2=lambda x: cls.replace(x, r"(^[ ]+)?(.*)", r"\2"),  # suppression démarrage par espace(s)
    udf_3=lambda x: cls.replace(x, r"'(.*),? (.*)' (.*)", name_2_upper),  # gestion modèle sous forme "Prénoms Composés NOMS COMPOSÉS <email>"
    udf_4=lambda x: cls.replace(x, r"^(?!(?:DOCUMENTATION).*$)(\w*).(\w*)(@[\w.]*)", mail_2_name),  # gestion modèle sous forme "prenom.nom@bpifrance.fr" sans prendre en compte le cas particulier "DOCUMENTATION documentation@bpifrance.fr"
    udf_5=lambda x: cls.replace(x, r"(([A-Z][-,a-zéèôç. ']+[ ]*)+) (([-A-Z ]+) ?)+ <(.*)>", r"\1;\3;\5"),  # formatage final Prénom Composé;NOMS COMPOSÉS;email@domain
    udf_6=lambda x: cls.replace(x, r"^(?!(.*;){2}(.*))([\w\- ]+) <?([\w.@]*)>?", r"\3;;\4;VALIDATION MANUELLE"),  # tout le reste, à surveiller manuellement car les formatages n'ont pas été identifiés par les schémas ci-dessus...
)

# affichage sortie standard
print(res)


# ou sortie vers fichier
with open(r"D:\OneDrive\Desktop\Alex_L_LD_FORMATED.txt", "w") as f_out:
    f_out.write(res)
