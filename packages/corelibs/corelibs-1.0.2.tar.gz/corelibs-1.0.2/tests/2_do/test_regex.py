import re


def upper_repl(match):
    return 'GOO' + match.group(1).upper() + 'GAR'


print(re.sub(r'foo([a-z]+)bar', upper_repl, 'foobazbar'))
