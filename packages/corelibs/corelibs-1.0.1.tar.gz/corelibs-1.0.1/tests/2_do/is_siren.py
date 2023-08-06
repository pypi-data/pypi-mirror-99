def sum_numbers(number):
    """
    internal use...

    :param number:
    :return: int
    """
    if number >= 10:
        return sum([int(x) for x in str(number)])
    return number


def is_siren(str_siren):
    """
    check if a SIREN number is correctly formatted
    :param str_siren:
    :return: str
    """
    reversed_siren = str_siren[::-1]
    val_2_check = []
    for i, pos in enumerate(reversed_siren):
        if (i + 1) % 2 == 0:
            even = int(pos) * 2
            val_2_check.append(sum_numbers(even))
        else:
            odd = int(pos) * 1
            val_2_check.append(sum_numbers(odd))

    if sum(val_2_check) % 10 == 0:
        print(f"Siren {str_siren} is correctly formatted")
        return True

    print(f"Siren {str_siren} is not correctly formatted")
    return False


sirens = ["732829320",
          "303663983",
          "303663981",
          "318228798",
          "632001491",
          "962504965",
          "302306832",
          "969510197",
          "624800579",
          "337180905",
          "782413744",
          "958807703",
          "957810146",
          "385720040",
          "935880245",
          "571850056",
          "425780434",
          "581621091",
          "475750337",
          "475450102",
          "563720283",
          "60801487",
          "46020202",
          "15753320",
          "56801426",
          "16150815"]
for siren in sirens:
    is_siren(siren)
