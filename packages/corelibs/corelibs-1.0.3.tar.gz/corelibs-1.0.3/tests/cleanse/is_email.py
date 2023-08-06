# is_email.py
# %%
from corelibs import cleanse as cls, log, config


config.DEFAULT_LOG_LEVEL = 10


@log.dict_dumping
def dump(tuple_2_dump):
    return tuple_2_dump


# vérification par défaut
print(cls.is_email("prenom.nom@BPIfrance.fr"))  # affichera True car correctement formaté

# vérification avec l'option déliverabilité avec une erreur typo dans le nom de domaine
print(cls.is_email("prenom.nom@bpi_france.fr", check_deliverability=True))  # affichera False car le nom de domaine bpi_france.fr n'existe pas

# vérification avec normalisation
print(cls.is_email("prenom.nom@BPIfrance.fr", check_only=False))  # affichera prenom.nom@bpifrance.fr

# vérification avec extraction des méta données
res = cls.is_email("prenom.nom@BPIfrance.fr", check_only=False, extraction=True, check_deliverability=True)
print(res)
# affichera l'objet
# Email(
#   email='prenom.nom@bpifrance.fr',
#   local_part='prenom.nom',
#   domain='bpifrance.fr',
#   ascii_email='prenom.nom@bpifrance.fr',
#   ascii_local_part='prenom.nom',
#   ascii_domain='bpifrance.fr',
#   smtp_utf8=False,
#   mx=[
#     (5, 'mail1.bpifrance.fr'),
#     (5, 'mail2.bpifrance.fr'),
#     (10, 'mail1.oseo.fr'),
#     (10, 'mail2.oseo.fr'),
#     (15, 'mail0.bpifrance.fr'),
#     (15, 'mail3.bpifrance.fr')],
#   mx_fallback_type=None
# )

dump(res)  # affichage plus lisible pour notre regard, au format YAML (mode DEBUG seulement)


# %%
# vérification avec un encodage utf8
print(cls.is_email("おはよう@例え.テスト", check_only=False, smtp_utf8=True))  # affichera おはよう@例え.テスト  <=> bonjour@parexemple.test

# extraction utf8
res = cls.is_email("おはよう@例え.テスト", check_only=False, extraction=True, smtp_utf8=True)
print(res)
# affichera l'objet
# Email(
#   email='おはよう@例え.テスト',
#   local_part='おはよう',
#   domain='例え.テスト',
#   ascii_email=None,
#   ascii_local_part=None,
#   ascii_domain='xn--r8jz45g.xn--zckzah',  # domaine ASCII encodé avec sa version Punycode (cf. https://www.rfc-editor.org/rfc/rfc3492.txt)
#   smtp_utf8=True,
#   mx=None,
#   mx_fallback_type=None
# )

dump(res)  # affichage plus lisible pour notre regard, au format YAML (mode DEBUG seulement)
