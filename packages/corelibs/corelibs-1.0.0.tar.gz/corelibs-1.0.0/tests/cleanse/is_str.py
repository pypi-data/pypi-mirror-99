# is_str.py
# %%
from corelibs import cleanse as cls


# test si chaine caractères
print(cls.is_str(123))  # affichera une chaîne vide ""

# suppression de tous les caractères non imprimables
# \x00 <=> NULL (NUL)
# \x01 <=> START OF HEADING (SOH)
# \x02 <=> START OF TEXT (STX)
# \x03 <=> END OF TEXT (ETX)
# \x04 <=> END OF TRANSMISSION (EOT)
# \x05 <=> END OF QUERY (ENQ)
# \x06 <=> ACKNOWLEDGE (ACK)
# \x07 <=> BEEP (BEL)
# \x08 <=> BACKSPACE (BS)
# \x09 <=> HORIZONTAL TAB (HT)
# \x0A <=> LINE FEED (LF)
# \x0B <=> VERTICAL TAB (VT)
# \x0C <=> FF (FORM FEED)
# \x0D <=> CR (CARRIAGE RETURN)
# \x0E <=> SO (SHIFT OUT)
# \x0F <=> SI (SHIFT IN)
# \x10 <=> DATA LINK ESCAPE (DLE)
# \x11 <=> DEVICE CONTROL 1 (DC1)
# \x12 <=> DEVICE CONTROL 2 (DC2)
# \x13 <=> DEVICE CONTROL 3 (DC3)
# \x14 <=> DEVICE CONTROL 4 (DC4)
# \x15 <=> NEGATIVE ACKNOWLEDGEMENT (NAK)
# \x16 <=> SYNCHRONIZE (SYN)
# \x17 <=> END OF TRANSMISSION BLOCK (ETB)
# \x18 <=> CANCEL (CAN)
# \x19 <=> END OF MEDIUM (EM)
# \x1A <=> SUBSTITUTE (SUB)
# \x1B <=> ESCAPE (ESC)
# \x1C <=> FILE SEPARATOR (FS) RIGHT ARROW
# \x1D <=> GROUP SEPARATOR (GS) LEFT ARROW
# \x1E <=> RECORD SEPARATOR (RS) UP ARROW
# \x1F <=> UNIT SEPARATOR (US) DOWN ARROW
chaine = """
\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0A\x0B\x0C\x0D\x0E\x0F\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19
\x1A\x1B\x1C\x1D\x1E\x1F Hello, je suis la chaîne qui ne sera pas nettoyée... \x12\x13\x14\x15\x16\x17\x18
❤ =}
"""
print(cls.is_str(chaine))  # affiche " Hello, je suis la chaîne qui ne sera pas nettoyée...  ❤ =}"

# %%
# Supression via des classes de caractères Unicode
# Cc => Caractères de contrôles (non imprimables)
# Lu => Caractères majuscules
# Zs => espace
print(cls.is_str(chaine, unicode_categories_2_remove=("Cc", "Lu", "Zs"))) # affiche "ello,jesuislachaînequineserapasnettoyée...❤=}"

# %%
# suppression des caractères accentués en les ramplaçant par leurs équivalents non accentués
chaine = "Hello, voici ma liste de caractères accentués ÀÁÂÃÄÅÆÇÈÉÊËÌÍÎÏÐÑÒÓÔÕÖØÙÚÛÜÝÞßàáâãäåæçèéêëìíîïðñòóôõöøùúûüýþÿŒœŠšŸƒ"
print(cls.is_str(chaine, strip_accented_char=True))  # affiche "Hello, voici ma liste de caracteres accentues AAAAAAÆCEEEEIIIIÐNOOOOOØUUUUYÞßaaaaaaæceeeeiiiiðnoooooøuuuuyþyŒœSsYƒ"

# %%
# suppression des caractères numériques avec les signes, opérateurs et séparateurs
chaine = "Hello, voici ma liste avec des caractères numériques : date(28/11/2013) heure(19:31) normal(123456) " \
         "séparateur (012.2345.12) signe + 12.2345.12 separateur 12,123,456 - 123 separateur 10 123 456 " \
         "signe - 123.12 signe et sep -12,123 signe et sep -10 012,123 1456"
print(cls.is_str(chaine, strip_num_char=True))  # affiche "Hello, voici ma liste avec des caractères numériques : date() heure() normal() séparateur () signe separateur separateur signe signe et sep signe et sep"

# %%
# remplacement des caractères, K -> A, i -> n et m -> T 3 -> 7
# 1er exemple avec une liste de caractères
chaine = "Hello, ma \x12\x13\x14\x15\x16\x17\x18 chaine avec des caractères à remplacer : Kim Marie Adélie, ma petite choupinette a 3 ans (casse prise en coMpte...)"
print(cls.is_str(chaine, chars_2_replace="Kim3", replaced_chars="AnT7"))  # affiche "Hello, Ta  channe avec des caractères à reTplacer : AnT Marne Adélne, Ta petnte choupnnette a 7 ans (casse prnse en coMpte...)"

# %%
# 2ème exemple avec un dictionnaire
print(cls.is_str(chaine,
                 chars_2_replace={
                     "Kim Marie Adélie": "Kim Marie Adélie TRUONG",  # multi char
                     "3": "7",  # single char
                     "M": "m"
                 }))  # Hello, ma  chaine avec des caractères à remplacer : Kim Marie Adélie TRUONG, ma petite choupinette a 7 ans (casse prise en compte...)
