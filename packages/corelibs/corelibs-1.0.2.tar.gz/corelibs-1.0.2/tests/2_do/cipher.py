# %%
# https://stackoverflow.com/questions/2490334/simple-way-to-encode-a-string-according-to-a-password
import zlib
import secrets
from base64 import urlsafe_b64encode as b64e, urlsafe_b64decode as b64d

from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

BACKEND = default_backend()
ITERATIONS = 100_000


def _derive_key(password: bytes, salt: bytes, iterations: int = ITERATIONS) -> bytes:
    """Derive a secret key from a given password and salt"""
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(), length=32, salt=salt,
        iterations=iterations, backend=BACKEND)
    return b64e(kdf.derive(password))


def password_encrypt(message: bytes, password: str, iterations: int = ITERATIONS) -> bytes:
    salt = secrets.token_bytes(16)
    key = _derive_key(password.encode(), salt, iterations)
    return b64e(
        b'%b%b%b' % (
            salt,
            iterations.to_bytes(4, 'big'),
            b64d(Fernet(key).encrypt(message)),
        )
    )


def password_decrypt(token: bytes, password: str) -> bytes:
    decoded = b64d(token)
    salt, iter, token = decoded[:16], decoded[16:20], b64e(decoded[20:])
    iterations = int.from_bytes(iter, 'big')
    key = _derive_key(password.encode(), salt, iterations)
    return Fernet(key).decrypt(token)


# %%
# message = {
#     "msg": "Hello Kim",
#     "from": "papa"
# }
message = """
import corelibs
message = {"msg": "Hello Kim", "from": "papa"}
print("message encapsulé", "•"*31, message, message["msg"], corelibs)
"""
pwd = "28Nov2013KT"

print(str(message))

_c = zlib.compress(password_encrypt(str(message).encode(), pwd))
print(_c)

# %%
_d = password_decrypt(zlib.decompress(_c), pwd + "Hello").decode()
print(_d, type(_d))
exec(_d)
print("message interne", message)

# import ast
# _ = ast.literal_eval(_)
#
# print(_, type(_))
# print(_["msg"])


# %%
import zlib

a = b"this string needs compressing"
a = zlib.compress(a)
print("*"*31, a)
print("+"*31, zlib.decompress(a))
