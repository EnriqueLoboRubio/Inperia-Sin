import sqlite3
from utils.encriptar import encriptar_contrasena, verificar_contrasena

# Función para crear la base de datos y la tabla de usuarios
def crear_bd():
    conexion = sqlite3.connect('db/usuarios.db')
    cursor = conexion.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            contrasena TEXT NOT NULL,
            tipo_usuario TEXT NOT NULL CHECK(tipo_usuario IN ('profesional', 'usuario'))
        )
    ''')

    conexion.commit()
    conexion.close()

# Función para agregar un nuevo usuario a la base de datos
def agregar_usuario(nombre, email, contrasena, tipo_usuario):
    conexion = sqlite3.connect('db/usuarios.db')
    cursor = conexion.cursor()
    try: 
        contrasena_encriptada = encriptar_contrasena(contrasena)
        cursor.execute('''
            INSERT INTO usuarios (nombre, email, contrasena, tipo_usuario)
            VALUES (?, ?, ?, ?)
        ''', (nombre, email, contrasena_encriptada, tipo_usuario))
    except sqlite3.IntegrityError:
        print("Error: El email ya está en uso.")
        return False
    
    conexion.commit()
    conexion.close()

# Función para verificar el login de un usuario, devuelve el tipo de usuario si es correcto o None si no lo es
def verificar_login(email, contrasena):
    conexion = sqlite3.connect("db/usuarios.db")
    cursor = conexion.cursor()
    cursor.execute("SELECT contrasena, tipo_usuario FROM usuarios WHERE email=?", (email,))
    resultado = cursor.fetchone()
    
    conexion.close()
    
    if resultado:
        contrasena_encriptada, tipo_usuario = resultado
        if verificar_contrasena(contrasena, contrasena_encriptada):
            return tipo_usuario #login correcto
    return None #login incorrecto

def eliminar_usuario(email):
    conexion = sqlite3.connect('db/usuarios.db')
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM usuarios WHERE email=?", (email,))
    conexion.commit()
    conexion.close()

def encontrar_usuario(email):
    conexion = sqlite3.connect('db/usuarios.db')
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM usuarios WHERE email=?", (email,))
    usuario = cursor.fetchone()
    conexion.close()
    return usuario
