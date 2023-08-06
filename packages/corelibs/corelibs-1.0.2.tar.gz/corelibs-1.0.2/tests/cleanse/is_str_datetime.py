# is_datetime.py
# %%
import datetime as dt

from corelibs import cleanse as cls

# %%
# forcer le traitement des instructions suivantes même en erreur...
print(cls.is_datetime("Hello Kim", ignore_errors=True))  # retourne vide...

# %%
# Datetime en chaine de caractère
# forcer le retour à vide (utile pour les données loufoques de la morkitu)
print(cls.is_datetime("2020-08-31", "%Y-%m-%d", out_format=""))  # retourne vide...

# %%
print(cls.is_datetime("2020-08-31", "%Y-%m-%d"))  # retourne 31/08/2020 00:00:00
print(cls.is_datetime("lun., 31 août 2020 15:57:43", "%a, %d %b %Y %H:%M:%S"))  # 31/08/2020 15:57:43

# %%
# format entrée en anglais, avec une sortie française (par défaut)...
print(cls.is_datetime("Mon, 31 Aug 2020 15:57:43",
                      in_format="%a, %d %b %Y %H:%M:%S",
                      out_format="le %A %d %b %Y à %H h et %M min",
                      in_locale_time="en"))  # le lundi 31 août 2020 à 15 h et 57 min

# %%
# format entrée en anglais, avec une sortie suédoise...
print(cls.is_datetime("Mon, 30 Oct 2020 15:57:43",
                      in_format="%a, %d %b %Y %H:%M:%S",
                      out_format="%A %d %b %Y • %H:%M:%S",
                      in_locale_time="en",
                      out_locale_time="sv"))  # fredag 30 okt 2020 • 15:57:43

# %%
# format entrée en français (par défaut), avec une sortie anglaise...
print(cls.is_datetime("lun., 31 août 2020 15:57:43",
                      in_format="%a, %d %b %Y %H:%M:%S",
                      out_format="%A %d %b %Y @ %HH n %Mmin",
                      out_locale_time="en"))  # Monday 31 Aug 2020 @ 15H n 57min

# %%
# Instance datetime
_now = dt.datetime.now()
# sortie par défaut quand c'est une date...
print(cls.is_datetime(_now))  # retourne 15/12/2020 23:58:08

# %%
# sortie avec conversion format
print(cls.is_datetime(_now, out_format="le %A %d %b %Y à %H h et %M min"))  # le mardi 15 déc. 2020 à 23 h et 58 min
