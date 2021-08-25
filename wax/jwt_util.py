import jwt


class JWTUtil:
    salt: str

    def __init__(self, app):
        self.salt = 'ajifajifeji'

    def encrypt(self, user_id: int, subject: str, expire_at: int) -> str:
        payload = {'uid': user_id, 'sub': subject, 'exp': expire_at}
        return jwt.encode(payload, self.salt, algorithm='HS256')

    def decrypt(self, token: str) -> dict:
        """
        get payload dict, raise jwt.exceptions.ExpiredSignatureError if token has expired.
        """
        return jwt.decode(token, self.salt, algorithms='HS256')
