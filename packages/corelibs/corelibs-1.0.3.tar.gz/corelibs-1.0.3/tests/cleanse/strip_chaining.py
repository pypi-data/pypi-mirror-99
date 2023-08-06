# replace_chaining.py
# %%
from corelibs import cleanse as cls, lazy as lz


# %%
# enchainement (plus lisible)
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
res = cls.strip_chaining(
    string,
    arg_dynamique="Coucou",  # ne sera pas traité car n'est pas un callable
    function_dynamique=lz.get_home,  # callable mais ne sera pas non plus traité car n'est pas un strip()
    # liste infinie dynamique des fonctions appelables à la suite... (si utile et pertinent)
    udf_1=lambda x: cls.strip(x, search=r"\d{9};00[1-9]{3};.*", non_printable_char=False),  # suppression de tous les siren avec un NIC 00XXXX (en ne gardant plus que les NIC à 000XX)
    udf_2=lambda x: cls.strip(x, search=b"\x3B", non_printable_char=False, replace=b"\x2C"),
    udf_3=lambda x: cls.strip(x, search=r".*,(NAFRev\d*|NAP).*", non_printable_char=False)  # suppression de tous les NAF non définitifs ou les valeurs NAP qui semblent être incorrects
)
print(res)
# affiche
# 999990609,00011,99999060900011,O,,NN,,,,true,1,,4,,PL,DE,LA,PYRAMIDE,92800,PUTEAUX,,,92062,,,,,,,,,,,,,,,,,,,1991-12-30,F,,,,,73.1Z,NAF1993,N
# 999990625,00025,99999062500025,O,,NN,,,,true,1,,,,RTE,DE,MANOM,57100,THIONVILLE,,,57672,,,,,,,,,,,,,,,,,,,1995-11-30,F,,,,,27.3C,NAF1993,O
# 999990666,00011,99999066600011,O,1986-05-15,,,,,false,4,,10,,RUE,CHAUCHAT,75009,PARIS,9,,,75109,,,,,,,,,,,,,,,,,,,1997-12-03,F,,,,,66.0A,NAF1993,N
# 999990666,00029,99999066600029,O,1997-12-03,,,,,false,3,,2,,RUE,PILLET,WILL,75009,PARIS,9,,,75109,,,,,,,,,,,,,,,,,,,2000-07-01,F,,,,,66.0A,NAF1993,N


# %%
# sinon en version non enchainée, 1ère possibilité (imbrication)
print(
    cls.strip(
        cls.strip(
            cls.strip(
                string,
                search=r"\d{9};00[1-9]{3};.*",  # suppression de tous les siren avec un NIC 00XXXX (en ne gardant plus que les NIC à 000XX)
                non_printable_char=False
            ),
            search=b"\x3B",
            replace=b"\x2C",
            non_printable_char=False
        ),
        search=r".*,(NAFRev\d*|NAP).*",  # suppression de tous les NAF non définitifs ou les valeurs NAP qui semblent être incorrects
        non_printable_char=False
    )
)
# affiche bien l'attendu
# 999990609,00011,99999060900011,O,,NN,,,,true,1,,4,,PL,DE,LA,PYRAMIDE,92800,PUTEAUX,,,92062,,,,,,,,,,,,,,,,,,,1991-12-30,F,,,,,73.1Z,NAF1993,N
# 999990625,00025,99999062500025,O,,NN,,,,true,1,,,,RTE,DE,MANOM,57100,THIONVILLE,,,57672,,,,,,,,,,,,,,,,,,,1995-11-30,F,,,,,27.3C,NAF1993,O
# 999990666,00011,99999066600011,O,1986-05-15,,,,,false,4,,10,,RUE,CHAUCHAT,75009,PARIS,9,,,75109,,,,,,,,,,,,,,,,,,,1997-12-03,F,,,,,66.0A,NAF1993,N
# 999990666,00029,99999066600029,O,1997-12-03,,,,,false,3,,2,,RUE,PILLET,WILL,75009,PARIS,9,,,75109,,,,,,,,,,,,,,,,,,,2000-07-01,F,,,,,66.0A,NAF1993,N


# %%
# sinon en version non enchainée, 2ème possibilité (avec étapes intermédiaires)
etape_1 = cls.strip(
    string,
    search=r"\d{9};00[1-9]{3};.*",  # suppression de tous les siren avec un NIC 00XXXX (en ne gardant plus que les NIC à 000XX)
    non_printable_char=False
)

etape_2 = cls.strip(
    etape_1,
    search=b"\x3B",
    replace=b"\x2C",
    non_printable_char=False
)

print(
    cls.strip(
        etape_2,
        search=r".*,(NAFRev\d*|NAP).*",  # suppression de tous les NAF non définitifs ou les valeurs NAP qui semblent être incorrects
        non_printable_char=False
    )
)
# affiche bien l'attendu
# 999990609,00011,99999060900011,O,,NN,,,,true,1,,4,,PL,DE,LA,PYRAMIDE,92800,PUTEAUX,,,92062,,,,,,,,,,,,,,,,,,,1991-12-30,F,,,,,73.1Z,NAF1993,N
# 999990625,00025,99999062500025,O,,NN,,,,true,1,,,,RTE,DE,MANOM,57100,THIONVILLE,,,57672,,,,,,,,,,,,,,,,,,,1995-11-30,F,,,,,27.3C,NAF1993,O
# 999990666,00011,99999066600011,O,1986-05-15,,,,,false,4,,10,,RUE,CHAUCHAT,75009,PARIS,9,,,75109,,,,,,,,,,,,,,,,,,,1997-12-03,F,,,,,66.0A,NAF1993,N
# 999990666,00029,99999066600029,O,1997-12-03,,,,,false,3,,2,,RUE,PILLET,WILL,75009,PARIS,9,,,75109,,,,,,,,,,,,,,,,,,,2000-07-01,F,,,,,66.0A,NAF1993,N
