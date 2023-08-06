import moment
from datetime import datetime

# Create a moment from a string
print(moment.date("12-18-2012"))

# Create a moment with a specified strftime format
print(moment.date("12-18-2012", "%m-%d-%Y"))

# Moment uses the awesome dateparser library behind the scenes
print(moment.date("2012-12-18"))

# Create a moment with words in it
print(moment.date("December 18, 2012"))

# Create a moment that would normally be pretty hard to do
print(moment.date("2 weeks ago"))

# Create a moment from the current datetime
print(moment.now())

# The moment can also be UTC-based
print(moment.utcnow())

# Create a moment with the UTC time zone
print(moment.utc("2012-12-18"))

# Create a moment from a Unix timestamp
# print(moment.unix(1355875153626))

# Create a moment from a Unix UTC timestamp
# print(moment.unix(1355875153626, utc=True))

# Return a datetime instance
print(moment.date(2012, 12, 18).date)

# We can do the same thing with the UTC method
print(moment.utc(2012, 12, 18).date)

# Create and format a moment using Moment.js semantics
print(moment.now().format("YYYY-M-D"))

# Create and format a moment with strftime semantics
print(moment.date(2012, 12, 18).strftime("%Y-%m-%d"))

# Use the special `%^` combo to add a date suffix (1st, 2nd, 3rd, 4th, etc)
print(moment.date(2012, 12, 18).strftime("%B %d, %Y"))

# Update your moment's time zone
print(moment.date(datetime(2012, 12, 18)).locale("US/Central").date)

# Alter the moment's UTC time zone to a different time zone
print(moment.utcnow().timezone("US/Eastern").date)

# Set and update your moment's time zone. For instance, I'm on the
# west coast, but want NYC's current time.
print(moment.now().locale("US/Pacific").timezone("US/Eastern"))

# In order to manipulate time zones, a locale must always be set or
# you must be using UTC.
print(moment.utcnow().timezone("US/Eastern").date)

# You can also clone a moment, so the original stays unaltered
now = moment.utcnow().timezone("US/Pacific")
print(now)
future = now.clone().add(weeks=2)
print(future)


# Sub
now = moment.date("12-18-2012")
print("*"*31, now.format("D/M/YYYY"))
past = now.clone().sub(years=2, months=2)
print("*"*31, past.format("D/M/YYYY"))

print("now >= past", now >= past)
print("now < past", now < past)
print("now == past", now == past)

diff = now.diff(past).days
print("diff", diff)
print("diff - 92", diff - 92)

print(moment.date("lun., 31 août 2020 15:57:43").format("D/M/YYYY HH:mm:ss"))
print(moment.date("lun., 31 août 2020 15:57:43").strftime("%d/%m/%Y %H:%M:%S"))
