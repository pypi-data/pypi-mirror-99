# get_closest_value_in_list.py
from corelibs import lazy as lz

print(
    lz.get_closest_value_in_list(1.6, [1, 2, 3])
)  # retourne 2 qui est la valeur la plus proche de 1.6 en delta absolu

print(
    lz.get_closest_value_in_list(74.7, (10, 20, 30, 40, 50, 60, 70, 80, 90, 100))
)  # retourne 70


array = [2, 42, 82, 122, 162, 202, 242, 282, 322, 362]
number = 103
print(lz.get_closest_value_in_list(number, array))  # retourne 122
