import bcrypt

def encriptar_contrasena(contraseña):
    salt = bcrypt.gensalt()
    encriptada = bcrypt.hashpw(contraseña.encode('utf-8'), salt)
    return encriptada.decode('utf-8')

def verificar_contrasena(contraseña, encriptada):
    return bcrypt.checkpw(contraseña.encode('utf-8'), encriptada.encode('utf-8'))