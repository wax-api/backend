import jwt
from wax.utils import eafp, randstr
import string


class JWTUtil:
    refname = 'wax.JWTUtil'
    salt: str

    def __init__(self, config):
        salt_file = eafp(lambda: config['lessweb']['jwt']['salt_file'])
        if not salt_file:
            seq = string.ascii_letters + string.digits
            self.salt = randstr(seq, length=30)
        else:
            self.salt = open(salt_file).read().strip()

    def encrypt(self, user_id: int, subject: str, expire_at: int) -> str:
        payload = {'uid': user_id, 'sub': subject, 'exp': expire_at}
        return jwt.encode(payload, self.salt, algorithm='HS256')

    def decrypt(self, token: str) -> dict:
        """
        return payload dict or raises jwt.ExpiredSignatureError if the expiration time is in the past
        """
        return jwt.decode(token, self.salt, algorithms='HS256')

    @classmethod
    def from_(cls, app) -> 'JWTUtil':
        if cls.refname not in app:
            app[cls.refname] = JWTUtil(app['config'])
        return app[cls.refname]
