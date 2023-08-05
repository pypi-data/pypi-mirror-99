# stack_trace.py
from corelibs import log, config

# config.DEFAULT_STACK_TRACE = True  # on force globalement l'affichage détaillé des piles d'exécution


def palindrome(mot):
    mots = list(mot)
    len_mot = len(mots)
    for i in range(int(len_mot / 2) + 1):
        if mot[i].lower() != mot[(len_mot - 1) - i].lower():
            return False

    return True


@log.stack_trace(force=True)  # on force localement l'affichage détaillé des piles d'exécution
def is_palindrome(mot):
    if palindrome(mot):
        print("\"{mot}\" est un palindrome".format(mot=mot))
    else:
        print("\"{mot}\" n'est pas un palindrome".format(mot=mot))


is_palindrome("Hello Kim, c'est papa =}")  # False
is_palindrome("saippuakauppias")  # True
