# get_timestamp.py
# %%
from corelibs import lazy as lz


# %%
timestamp = lz.get_timestamp()
print("Le timestamp sans milli secondes est {timestamp}".format(timestamp=timestamp))
# Le timestamp sans milli secondes est 20201209_181434

# %%
timestamp = lz.get_timestamp(only_ms=True)
print("Le timestamp en milli secondes est {timestamp}".format(timestamp=timestamp))
# Le timestamp en milli secondes est 096248

# %%
timestamp = lz.get_timestamp(display_ms=True)
print("Le timestamp avec milli secondes est {timestamp}".format(timestamp=timestamp))
# Le timestamp avec milli secondes est 20201209_181434.097248

# %%
timestamp = lz.get_timestamp(timestamp_format="D")
print("Le timestamp avec la date seulement est {timestamp}".format(timestamp=timestamp))
# Le timestamp avec la date seulement est 20201209

# %%
timestamp = lz.get_timestamp(timestamp_format="T")
print("Le timestamp avec l'heure seulement est {timestamp}".format(timestamp=timestamp))
# Le timestamp avec l'heure seulement est 181434

# %%
timestamp = lz.get_timestamp(timestamp_format="NOW")
print("Le timestamp avec la date et l'heure sans retraitement est {timestamp}".format(timestamp=timestamp))
# Le timestamp avec la date et l'heure sans retraitement est 2020-12-09 18:14:34

# %%
timestamp = lz.get_timestamp(timestamp_format="GD")
print("Le timestamp avec la date sans retraitement est {timestamp}".format(timestamp=timestamp))
# Le timestamp avec la date sans retraitement est 2020-12-09

# %%
timestamp = lz.get_timestamp(timestamp_format="GT")
print("Le timestamp avec l'heure sans retraitement est {timestamp}".format(timestamp=timestamp))
# Le timestamp avec l'heure sans retraitement est 18:14:34
