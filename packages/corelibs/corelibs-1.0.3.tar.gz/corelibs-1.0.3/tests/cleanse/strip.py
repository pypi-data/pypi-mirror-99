# strip.py
# %%
from corelibs import cleanse as cls

# %%
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
# \x0C <=> FORM FEED (FF)
# \x0D <=> CARRIAGE RETURN (CR)
# \x0E <=> SHIFT OUT (SO)
# \x0F <=> SHIFT IN (SI)
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
string = """
\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0A\x0B\x0C\x0D\x0E\x0F\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19
\x1A\x1B\x1C\x1D\x1E\x1F Hello, je suis la chaîne qui va rester après nettoyage... \x12\x13\x14\x15\x16\x17\x18
❤ =}
"""
print(cls.strip(string))
# affiche " Hello, je suis la chaîne qui va rester après nettoyage... ❤ =}"


# %%
# supression de tous les caractères non imprimables, avec un remplacement différent
print(cls.strip(string, replace="-"))
# affiche "-----------------------------------Hello,-je-suis-la-chaîne-qui-va-rester-après-nettoyage...---------❤-=}-"


# %%
# Supression via des classes de caractères Unicode
# Cc => Caractères de contrôles (non imprimables)
# Lu => Caractères majuscules
# Zs => espace
print(cls.strip(string, unicode_categories=("Cc", "Lu", "Zs")))
# affiche "ello,jesuislachaînequivaresteraprèsnettoyage...❤=}"


# %%
# Supression multiple espaces (comportement par défaut)
string = """
\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0A\x0B\x0C\x0D\x0E\x0F\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19
o( ^   ^ o)     Hello Kim !!!     (o ^   ^ )o   
\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0A\x0B\x0C\x0D\x0E\x0F\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19
"""
print(cls.strip(string))
# affiche "o( ^ ^ o) Hello Kim !!! (o ^ ^ )o"

# %%
# Supression espace insécable
string = "Cette chaine contient 3 espaces -(\xA0\xA0\xA0)- insécables"
print(string)  # affiche "Cette chaine contient 3 espaces -(   )- insécables"
print(cls.strip(string))  # affiche "Cette chaine contient 3 espaces -()- insécables"


# %%
# suppression des caractères accentués en les ramplaçant par leurs équivalents non accentués
string = "Hello, voici ma liste de caractères accentués ÀÁÂÃÄÅÆÇÈÉÊËÌÍÎÏÐÑÒÓÔÕÖØÙÚÛÜÝÞßàáâãäåæçèéêëìíîïðñòóôõöøùúûüýþÿŒœŠšŸƒ"
print(cls.strip(string, accented_char=True))
# affiche "Hello, voici ma liste de caracteres accentues AAAAAAÆCEEEEIIIIÐNOOOOOØUUUUYÞßaaaaaaæceeeeiiiiðnoooooøuuuuyþyŒœSsYƒ"


# %%
# suppression des caractères numériques avec les signes, opérateurs et séparateurs
string = """
Hello, voici ma liste avec des caractères numériques : 
date -(28/11/2013)- 
heure -(19:31)- 
normal -(123456)- 
signe -(+ 12.2345.12)- ou -(- 12.2345.12)- 
séparateur -(012.2345.12)- ou -(12,123,456)- ou -( 10 123 456)- 
signe et sep -(-10 012,123 1456)- 
"""
print(cls.strip(string, num_char=True, non_printable_char=False))
# affiche "
# Hello, voici ma liste avec des caractères numériques :
# date -()-
# heure -()-
# normal -()-
# signe -()- ou -()-
# séparateur -()- ou -()- ou -()-
# signe et sep -()-
# "


# %%
# suppression par recherche standard (on enlève ici tout ce qui est entre les ; - juste pour le fun car aucun intérêt...)
string = """
999990583;00133;99999058300133;O;1993-01-01;NN;;;2006-11-25T22:25:28;false;4;CENTRALE DE MIJANES;;;;;09120;VARILHES;;;09324;;;;;;;;;;;;;;;;;;;2004-06-30;F;;;;;40.1A;NAFRev1;N
999990583;00158;99999058300158;O;1998-09-07;NN;;;2019-11-14T14:00:51;true;3;PARC TECHNOL LA PARDIEU;6;;RUE;CONDORCET;63000;CLERMONT-FERRAND;;;63113;;;;;;;;;;;;;;;;;;;2004-06-30;F;;;;;28.4A;NAFRev1;N
999990609;00011;99999060900011;O;;NN;;;;true;1;;4;;PL;DE LA PYRAMIDE;92800;PUTEAUX;;;92062;;;;;;;;;;;;;;;;;;;1991-12-30;F;;;;;73.1Z;NAF1993;N
999990625;00025;99999062500025;O;;NN;;;;true;1;;;;RTE;DE MANOM;57100;THIONVILLE;;;57672;;;;;;;;;;;;;;;;;;;1995-11-30;F;;;;;27.3C;NAF1993;O
999990641;00014;99999064100014;O;;NN;;;;true;1;;99;;BD;DE GRENELLE;75015;PARIS 15;;;75115;;;;;;;;;;;;;;;;;;;1986-06-15;F;;;;;65.01;NAP;N
999990666;00011;99999066600011;O;1986-05-15;;;;;false;4;;10;;RUE;CHAUCHAT;75009;PARIS 9;;;75109;;;;;;;;;;;;;;;;;;;1997-12-03;F;;;;;66.0A;NAF1993;N
999990666;00029;99999066600029;O;1997-12-03;;;;;false;3;;2;;RUE;PILLET WILL;75009;PARIS 9;;;75109;;;;;;;;;;;;;;;;;;;2000-07-01;F;;;;;66.0A;NAF1993;N
999990666;00037;99999066600037;O;2000-07-01;NN;;;2020-05-20T03:34:55;true;3;8 A 10;8;;RUE;D'ASTORG;75008;PARIS 8;;;75108;;;;;;;;;;;;;;;;;;;2008-01-01;A;;;;;65.11Z;NAFRev2;N
999990682;00034;99999068200034;O;2001-09-18;NN;;;;true;3;LE PONANT DE PARIS;27;;RUE;LEBLANC;75015;PARIS 15;;;75115;;;;;;;;;;;;;;;;;;;2003-12-18;F;;;;;65.2E;NAFRev1;N
999992357;00015;99999235700015;O;2003-12-31;01;2017;;2019-06-24T14:13:19;true;5;;6;;RUE;DE L ETOILE;80090;AMIENS;;;80021;;;;;;;;;;;;;;;;;;;2012-01-22;A;;;;;81.10Z;NAFRev2;O
"""
print(cls.strip(string, search=r"[^;\n]+", non_printable_char=False))
# affiche "
# ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
# ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
# ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
# ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
# ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
# ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
# ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
# ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
# ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
# ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
# "


# %%
# suppression des ;  avec remplacement par , (en binaire)
print(cls.strip(string, search=b"\x3B", non_printable_char=False, replace=b"\x2C"))
# affiche "
# 999990583,00133,99999058300133,O,1993-01-01,NN,,,2006-11-25T22:25:28,false,4,CENTRALE,DE,MIJANES,,,,,09120,VARILHES,,,09324,,,,,,,,,,,,,,,,,,,2004-06-30,F,,,,,40.1A,NAFRev1,N
# 999990583,00158,99999058300158,O,1998-09-07,NN,,,2019-11-14T14:00:51,true,3,PARC,TECHNOL,LA,PARDIEU,6,,RUE,CONDORCET,63000,CLERMONT-FERRAND,,,63113,,,,,,,,,,,,,,,,,,,2004-06-30,F,,,,,28.4A,NAFRev1,N
# 999990609,00011,99999060900011,O,,NN,,,,true,1,,4,,PL,DE,LA,PYRAMIDE,92800,PUTEAUX,,,92062,,,,,,,,,,,,,,,,,,,1991-12-30,F,,,,,73.1Z,NAF1993,N
# 999990625,00025,99999062500025,O,,NN,,,,true,1,,,,RTE,DE,MANOM,57100,THIONVILLE,,,57672,,,,,,,,,,,,,,,,,,,1995-11-30,F,,,,,27.3C,NAF1993,O
# 999990641,00014,99999064100014,O,,NN,,,,true,1,,99,,BD,DE,GRENELLE,75015,PARIS,15,,,75115,,,,,,,,,,,,,,,,,,,1986-06-15,F,,,,,65.01,NAP,N
# 999990666,00011,99999066600011,O,1986-05-15,,,,,false,4,,10,,RUE,CHAUCHAT,75009,PARIS,9,,,75109,,,,,,,,,,,,,,,,,,,1997-12-03,F,,,,,66.0A,NAF1993,N
# 999990666,00029,99999066600029,O,1997-12-03,,,,,false,3,,2,,RUE,PILLET,WILL,75009,PARIS,9,,,75109,,,,,,,,,,,,,,,,,,,2000-07-01,F,,,,,66.0A,NAF1993,N
# 999990666,00037,99999066600037,O,2000-07-01,NN,,,2020-05-20T03:34:55,true,3,8,A,10,8,,RUE,D'ASTORG,75008,PARIS,8,,,75108,,,,,,,,,,,,,,,,,,,2008-01-01,A,,,,,65.11Z,NAFRev2,N
# 999990682,00034,99999068200034,O,2001-09-18,NN,,,,true,3,LE,PONANT,DE,PARIS,27,,RUE,LEBLANC,75015,PARIS,15,,,75115,,,,,,,,,,,,,,,,,,,2003-12-18,F,,,,,65.2E,NAFRev1,N
# 999992357,00015,99999235700015,O,2003-12-31,01,2017,,2019-06-24T14:13:19,true,5,,6,,RUE,DE,L,ETOILE,80090,AMIENS,,,80021,,,,,,,,,,,,,,,,,,,2012-01-22,A,,,,,81.10Z,NAFRev2,O
# "


# %%
# suppression lignes vides
string = """

999990609,00011,99999060900011,O,,NN,,,,true,1,,4,,PL,DE,LA,PYRAMIDE,92800,PUTEAUX,,,92062,,,,,,,,,,,,,,,,,,,1991-12-30,F,,,,,73.1Z,NAF1993,N
999990625,00025,99999062500025,O,,NN,,,,true,1,,,,RTE,DE,MANOM,57100,THIONVILLE,,,57672,,,,,,,,,,,,,,,,,,,1995-11-30,F,,,,,27.3C,NAF1993,O

999990666,00011,99999066600011,O,1986-05-15,,,,,false,4,,10,,RUE,CHAUCHAT,75009,PARIS,9,,,75109,,,,,,,,,,,,,,,,,,,1997-12-03,F,,,,,66.0A,NAF1993,N
999990666,00029,99999066600029,O,1997-12-03,,,,,false,3,,2,,RUE,PILLET,WILL,75009,PARIS,9,,,75109,,,,,,,,,,,,,,,,,,,2000-07-01,F,,,,,66.0A,NAF1993,N



"""
print(cls.strip(string, non_printable_char=False))
# affiche
# 999990609,00011,99999060900011,O,,NN,,,,true,1,,4,,PL,DE,LA,PYRAMIDE,92800,PUTEAUX,,,92062,,,,,,,,,,,,,,,,,,,1991-12-30,F,,,,,73.1Z,NAF1993,N
# 999990625,00025,99999062500025,O,,NN,,,,true,1,,,,RTE,DE,MANOM,57100,THIONVILLE,,,57672,,,,,,,,,,,,,,,,,,,1995-11-30,F,,,,,27.3C,NAF1993,O
# 999990666,00011,99999066600011,O,1986-05-15,,,,,false,4,,10,,RUE,CHAUCHAT,75009,PARIS,9,,,75109,,,,,,,,,,,,,,,,,,,1997-12-03,F,,,,,66.0A,NAF1993,N
# 999990666,00029,99999066600029,O,1997-12-03,,,,,false,3,,2,,RUE,PILLET,WILL,75009,PARIS,9,,,75109,,,,,,,,,,,,,,,,,,,2000-07-01,F,,,,,66.0A,NAF1993,N
