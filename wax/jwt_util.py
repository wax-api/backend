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
        return payload dict or raises jwt.ExpiredSignatureError if the expiration time is in the past
        """
        return jwt.decode(token, self.salt, algorithms='HS256')
