from passlib.context import CryptContext

class Hash:
    def bcrypt(request):
        return CryptContext(schemes=["bcrypt"],deprecated="auto").hash(request)

    def verify(hashed_password,plain_password):
        return CryptContext(schemes=["bcrypt"],deprecated="auto").verify(plain_password,hashed_password)
