import jwt

def crearToken(data: dict):
    token : str = jwt.encode(payload=data, key='secreto', algorithm='HS256')
    return token

def validarToken(token: str):
    data : dict = jwt.decode(token, key='secreto', algorithms='HS256')
    return data