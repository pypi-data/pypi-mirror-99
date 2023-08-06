# args_dumping.py
from corelibs import config, log
from random import randrange

my_dict = {
    0: {
        "nom": "MARIE ADÉLIE",
        "prénom": "Kim",
        "age": 7
    },
    1: {
        "arg1": "Hello",
        "arg2": "Kim"
    },
    2: {
        "msg": "I ❤  U",
        "from": "papa"
    }
}


# le niveau d'alerte par défaut est à INFO, correspondant à la valeur 20...
# 10 correspond à DEBUG, ce qui a pour effet d'afficher le dumping...
config.DEFAULT_LOG_LEVEL = 10  # décommenter pour baisser le niveau d'alerte à DEBUG


# décoration pour lister dynamiquement les arguments passés en paramétrage de la fonction `test_dumping(...)
@log.args_dumping
def test_dumping(iteration, *args, **kwargs):
    pass


total_dict = len(my_dict)
for i in range(7):  # appel dynamique aléatoire d'arguments dans la fonction `test_dumping()`
    rand_number = randrange(total_dict)
    test_dumping(
        i,
        rand_number,
        "itération {i} et nb aléatoire {rand_number}".format(i="{:0>3}".format(i), rand_number=rand_number),
        sub_dict=my_dict[rand_number]
    )
