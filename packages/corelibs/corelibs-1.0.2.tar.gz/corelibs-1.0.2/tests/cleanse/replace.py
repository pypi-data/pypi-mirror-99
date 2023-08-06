# replace.py
# %%
import re

from corelibs import config, cleanse as cls

# %%
# remplacement simple
print(
    cls.replace(
        "Coucou Kim, c'est papa ❤ =}",
        "Kim",
        "Kim Marie Adélie"
    )
)  # affiche Coucou Kim Marie Adélie, c'est papa ❤ =}

# remplacement simple (binaire, encodage latin)
print(
    cls.replace(
        "Coucou Kim, c'est papa =}",  # le coeur ne peut pas être utilisé ici car non présent dans l'encodage latin-1... sinon son code est 0xE2 0x99 0xA5
        b"Kim",
        b"Kim Marie Ad\xE9lie",
        encoding=config.DEFAULT_ENCODING_FILE  # "ISO-8859-1"
    )
)  # affiche Coucou Kim Marie Adélie, c'est papa =}

# remplacement simple (binaire, encodage utf-8)
print(
    cls.replace(
        "Coucou Kim, c'est papa ❤ =}",
        b"Kim",
        b"Kim Marie Ad\xC3\xA9lie",
        encoding="utf-8"
    )
)  # affiche Coucou Kim Marie Adélie, c'est papa ❤ =}


# %%
# remplacement avec regex (changement format date, AAAA-MM-DD deviendra DD/MM/AAAA)
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
print(
    cls.replace(
        string,
        search=r"\b(\d{4})-(\d{2})-(\d{2})\b",
        replace=r"\3/\2/\1"
    )
)
# affiche (les champs dates sont bien modifiés comme souhaité, pas les champs horodatés comme AAAA-MM-DDTHH:MM)
# 999990583;00133;99999058300133;O;01/01/1993;NN;;;2006-11-25T22:25:28;false;4;CENTRALE DE MIJANES;;;;;09120;VARILHES;;;09324;;;;;;;;;;;;;;;;;;;30/06/2004;F;;;;;40.1A;NAFRev1;N
# 999990583;00158;99999058300158;O;07/09/1998;NN;;;2019-11-14T14:00:51;true;3;PARC TECHNOL LA PARDIEU;6;;RUE;CONDORCET;63000;CLERMONT-FERRAND;;;63113;;;;;;;;;;;;;;;;;;;30/06/2004;F;;;;;28.4A;NAFRev1;N
# 999990609;00011;99999060900011;O;;NN;;;;true;1;;4;;PL;DE LA PYRAMIDE;92800;PUTEAUX;;;92062;;;;;;;;;;;;;;;;;;;30/12/1991;F;;;;;73.1Z;NAF1993;N
# 999990625;00025;99999062500025;O;;NN;;;;true;1;;;;RTE;DE MANOM;57100;THIONVILLE;;;57672;;;;;;;;;;;;;;;;;;;30/11/1995;F;;;;;27.3C;NAF1993;O
# 999990641;00014;99999064100014;O;;NN;;;;true;1;;99;;BD;DE GRENELLE;75015;PARIS 15;;;75115;;;;;;;;;;;;;;;;;;;15/06/1986;F;;;;;65.01;NAP;N
# 999990666;00011;99999066600011;O;15/05/1986;;;;;false;4;;10;;RUE;CHAUCHAT;75009;PARIS 9;;;75109;;;;;;;;;;;;;;;;;;;03/12/1997;F;;;;;66.0A;NAF1993;N
# 999990666;00029;99999066600029;O;03/12/1997;;;;;false;3;;2;;RUE;PILLET WILL;75009;PARIS 9;;;75109;;;;;;;;;;;;;;;;;;;01/07/2000;F;;;;;66.0A;NAF1993;N
# 999990666;00037;99999066600037;O;01/07/2000;NN;;;2020-05-20T03:34:55;true;3;8 A 10;8;;RUE;D'ASTORG;75008;PARIS 8;;;75108;;;;;;;;;;;;;;;;;;;01/01/2008;A;;;;;65.11Z;NAFRev2;N
# 999990682;00034;99999068200034;O;18/09/2001;NN;;;;true;3;LE PONANT DE PARIS;27;;RUE;LEBLANC;75015;PARIS 15;;;75115;;;;;;;;;;;;;;;;;;;18/12/2003;F;;;;;65.2E;NAFRev1;N
# 999992357;00015;99999235700015;O;31/12/2003;01;2017;;2019-06-24T14:13:19;true;5;;6;;RUE;DE L ETOILE;80090;AMIENS;;;80021;;;;;;;;;;;;;;;;;;;22/01/2012;A;;;;;81.10Z;NAFRev2;O


# %%
# remplacement avec regex (changement format date + format horodaté, AAAA-MM-DD deviendra DD/MM/AAAA et AAAA-MM-DDTHH:MM deviendra DD/MM/AAAA HH:MM)
print(
    cls.replace(
        cls.replace(
            string,
            search=r"\b(\d{4})-(\d{2})-(\d{2})\b",
            replace=r"\3/\2/\1"
        ),
        search=r"\b(\d{4})-(\d{2})-(\d{2})T(\d{2}):(\d{2}):(\d{2})\b",
        replace=r"\3/\2/\1 \4:\5"
    )
)
# affiche (les champs dates et champs horodatés comme 2006-11-25T22 sont bien modifiés comme souhaité)
# 999990583;00133;99999058300133;O;01/01/1993;NN;;;25/11/2006 22:25;false;4;CENTRALE DE MIJANES;;;;;09120;VARILHES;;;09324;;;;;;;;;;;;;;;;;;;30/06/2004;F;;;;;40.1A;NAFRev1;N
# 999990583;00158;99999058300158;O;07/09/1998;NN;;;14/11/2019 14:00;true;3;PARC TECHNOL LA PARDIEU;6;;RUE;CONDORCET;63000;CLERMONT-FERRAND;;;63113;;;;;;;;;;;;;;;;;;;30/06/2004;F;;;;;28.4A;NAFRev1;N
# 999990609;00011;99999060900011;O;;NN;;;;true;1;;4;;PL;DE LA PYRAMIDE;92800;PUTEAUX;;;92062;;;;;;;;;;;;;;;;;;;30/12/1991;F;;;;;73.1Z;NAF1993;N
# 999990625;00025;99999062500025;O;;NN;;;;true;1;;;;RTE;DE MANOM;57100;THIONVILLE;;;57672;;;;;;;;;;;;;;;;;;;30/11/1995;F;;;;;27.3C;NAF1993;O
# 999990641;00014;99999064100014;O;;NN;;;;true;1;;99;;BD;DE GRENELLE;75015;PARIS 15;;;75115;;;;;;;;;;;;;;;;;;;15/06/1986;F;;;;;65.01;NAP;N
# 999990666;00011;99999066600011;O;15/05/1986;;;;;false;4;;10;;RUE;CHAUCHAT;75009;PARIS 9;;;75109;;;;;;;;;;;;;;;;;;;03/12/1997;F;;;;;66.0A;NAF1993;N
# 999990666;00029;99999066600029;O;03/12/1997;;;;;false;3;;2;;RUE;PILLET WILL;75009;PARIS 9;;;75109;;;;;;;;;;;;;;;;;;;01/07/2000;F;;;;;66.0A;NAF1993;N
# 999990666;00037;99999066600037;O;01/07/2000;NN;;;20/05/2020 03:34;true;3;8 A 10;8;;RUE;D'ASTORG;75008;PARIS 8;;;75108;;;;;;;;;;;;;;;;;;;01/01/2008;A;;;;;65.11Z;NAFRev2;N
# 999990682;00034;99999068200034;O;18/09/2001;NN;;;;true;3;LE PONANT DE PARIS;27;;RUE;LEBLANC;75015;PARIS 15;;;75115;;;;;;;;;;;;;;;;;;;18/12/2003;F;;;;;65.2E;NAFRev1;N
# 999992357;00015;99999235700015;O;31/12/2003;01;2017;;24/06/2019 14:13;true;5;;6;;RUE;DE L ETOILE;80090;AMIENS;;;80021;;;;;;;;;;;;;;;;;;;22/01/2012;A;;;;;81.10Z;NAFRev2;O



# %%
# remplacement avec regex & utilisation flags
string = """
Tuesday 08 December 2020 - Ma log à moi que j'ai [termcolorlog.py:1] <>          INFO : Bonjour, ceci est un test personnalisé niveau INFO
Tuesday 08 December 2020 - Ma log à moi que j'ai [termcolorlog.py:1] <>       WARNING : Bonjour, ceci est un test personnalisé niveau WARNING
Tuesday 08 December 2020 - Ma log à moi que j'ai [termcolorlog.py:1] <>         ERROR : Bonjour, ceci est un test personnalisé niveau ERROR
Tuesday 08 December 2020 - Ma log à moi que j'ai [termcolorlog.py:1] <>      CRITICAL : Bonjour, ceci est un test personnalisé niveau CRITIQUE
"""
print(
    cls.replace(
        string,
        search=r"^(tuesday) (08) (december) (2020)(.*)(Bonjour,)(.*)$",  # justification de l'utilisation du flag re.I
        replace=r"\4/12/\2\5Au revoir!\7 - modifié par regex =}",
        regex_flag=re.M | re.I
    )
)
# affiche
# 2020/12/08 - Ma log à moi que j'ai [termcolorlog.py:1] <>          INFO : Au revoir! ceci est un test personnalisé niveau INFO - modifié par regex =}
# 2020/12/08 - Ma log à moi que j'ai [termcolorlog.py:1] <>       WARNING : Au revoir! ceci est un test personnalisé niveau WARNING - modifié par regex =}
# 2020/12/08 - Ma log à moi que j'ai [termcolorlog.py:1] <>         ERROR : Au revoir! ceci est un test personnalisé niveau ERROR - modifié par regex =}
# 2020/12/08 - Ma log à moi que j'ai [termcolorlog.py:1] <>      CRITICAL : Au revoir! ceci est un test personnalisé niveau CRITIQUE - modifié par regex =}


# %%
# remplacement binaire des espace par des ;
print(
    cls.replace(
        string,
        search=b"\x20",
        replace=b"\x3B"
    )
)
# affiche
# Tuesday;08;December;2020;-;Ma;log;à;moi;que;j'ai;[termcolorlog.py:1];<>;;;;;;;;;;INFO;:;Bonjour,;ceci;est;un;test;personnalisé;niveau;INFO
# Tuesday;08;December;2020;-;Ma;log;à;moi;que;j'ai;[termcolorlog.py:1];<>;;;;;;;WARNING;:;Bonjour,;ceci;est;un;test;personnalisé;niveau;WARNING
# Tuesday;08;December;2020;-;Ma;log;à;moi;que;j'ai;[termcolorlog.py:1];<>;;;;;;;;;ERROR;:;Bonjour,;ceci;est;un;test;personnalisé;niveau;ERROR
# Tuesday;08;December;2020;-;Ma;log;à;moi;que;j'ai;[termcolorlog.py:1];<>;;;;;;CRITICAL;:;Bonjour,;ceci;est;un;test;personnalisé;niveau;CRITIQUE
