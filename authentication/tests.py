from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, SignatureExpired, BadSignature, BadData

from StudentManageSys.settings import SECURE_KEY


def decrypt(token):
    s = Serializer(secret_key=SECURE_KEY['SECRET_KEY'], salt=SECURE_KEY['AUTH_SALT'])
    try:
        data = s.loads(token)
    except SignatureExpired:
        msg = 'token expired'
        print(msg)
    except BadSignature as e:
        encoded_payload = e.payload
        if encoded_payload is not None:
            try:
                s.load_payload(encoded_payload)
            except BadData:
                msg = 'token tampered'
                print(msg)
        msg = 'badSignature of token'
        print(msg)
    except:
        msg = 'wrong token with unknown reason'
        print(msg)

    return data


print(decrypt(
    'eyJhbGciOiJIUzI1NiIsImlhdCI6MTUzNjA0NDYzNSwiZXhwIjoxNTM2MDQ4MjM1fQ.eyJ1c2VyX2lkIjo1LCJpYXQiOjE1MzYwNDQ2MzUuNDA1OTA4OCwiaXNfc3R1ZGVudCI6MX0.dha5eO7QI2uTn7ozutsXf565Nivzy8go825fAPXKxVs'))
