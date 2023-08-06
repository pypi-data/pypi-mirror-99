def sum_numbers(number):
    if number >= 10:
        return sum([int(x) for x in str(number)])

    return number


def is_siret(str_siret):
    reversed_siret = str_siret[::-1]
    val_2_check = []

    for i, pos in enumerate(reversed_siret):
        if "356000000"[::-1] in reversed_siret:
            if sum([int(s) for s in reversed_siret]) % 5 == 0:
                print("Siret POSTE OK")
                return True
            else:
                print("Siret POSTE KO")
                return False
        else:
            if (i + 1) % 2 == 0:
                even = int(pos) * 2
                val_2_check.append(sum_numbers(even))
            else:
                odd = int(pos) * 1
                val_2_check.append(sum_numbers(odd))

    if sum(val_2_check) % 5 == 0:
        print("Siren {siret} is correctly formatted".format(siret=str_siret))
        return True

    print("Siren {siret} is not correctly formatted".format(siret=str_siret))
    return False


sirets = ["05680142600018", "30366398300011", "31822879800019", "63200149100018", "96250496500048", "30230683200023",
          "30230683200031", "30230683200023", "30230683200015", "35600000049837", "35600000052135"]
for siret in sirets:
    is_siret(siret)
