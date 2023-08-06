import datetime as dt
import locale

locale.setlocale(locale.LC_TIME, "")  # explicit empty locale arg will return the environment var =)

now = dt.datetime.now()
# print(now)
date_time = str(now).split()
# print(date_time)
date_ = "".join(date_time[0].split("-"))
# print(date_)
time_ = "".join(date_time[1].split(":"))
# print(time_)
print(date_ + "_" + time_)
# print(time.strftime("%a, %d %b %Y %H:%M:%S"))
# print(time.strftime("%a, %Y-%m-%d %H:%M:%S"))


def is_str_datetime(dt_str, in_format="%Y-%m-%d"):
    """
         check if given string is a formatted datetime

         :param dt_str: datetime string
         :param in_format: datetime input format, default : "%Y-%m-%d" => https://docs.python.org/3/library/datetime.html

         :return: None
     """
    try:
        assert dt_str == dt.datetime.strptime(dt_str, in_format).strftime(in_format)
    except AssertionError:
        raise AssertionError("Incorrect date format")


is_str_datetime("2020-08-31", "%Y-%m-%d")
is_str_datetime("2020/08/31", "%Y/%m/%d")
is_str_datetime("2020-8-1", "%Y-%m-%d")
is_str_datetime("20200801", "%Y%m%d")
is_str_datetime("2020-08-31 15", "%Y-%m-%d %H")
is_str_datetime("lun., 31 août 2020 15:57:43", "%a, %d %b %Y %H:%M:%S")
is_str_datetime("lun., 2020-08-31 16:23:26", "%a, %Y-%m-%d %H:%M:%S")
