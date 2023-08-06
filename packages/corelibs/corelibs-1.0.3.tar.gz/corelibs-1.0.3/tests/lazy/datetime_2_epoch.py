# datetime_2_epoch.py
# %%
from corelibs import lazy as lz

# conversion en epoch Unix (https://www.epochconverter.com/#tools)
print(lz.datetime_2_epoch(date_time=" Oct 3 1978       1:33PM  ", time_format="%b %d %Y %I:%M%p"))  # même si ce type de chaîne loufoque est nettoyée avant le calcul, il est préférable d'écrire proprement la donnée...
# 276269580000
print(lz.datetime_2_epoch("28/11/2013 19:23:52"))
# 1385666632000

# conversion en epoch Windows (https://www.epochconverter.com/ldap)
print(lz.datetime_2_epoch(date_time="Oct 3 1978 1:33PM", time_format="%b %d %Y %I:%M%p", reference_epoch="Windows"))
# 119207431800000000
print(lz.datetime_2_epoch(date_time="28/11/2013 19:23:52", reference_epoch="Windows"))
# 130301402320000000
