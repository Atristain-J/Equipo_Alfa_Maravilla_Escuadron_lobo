import re
import tkinter as tk
from tkinter import scrolledtext, messagebox

# Definimos las expresiones regulares para los diferentes tipos de tokens
TOKEN_PATTERNS = [
    ('PALABRA_CLAVE', r'\b(if|else|for|while|return|def|class)\b'),
    ('PALABRA_RESERVADA', r'\b[a-zA-Z_][a-zA-Z_0-9]*\b'),
    ('NÚMERO REAL', r'\b\d+(\.\d+)?\b'),
    ('OPERADOR', r'[+\-*/=<>]'),
    ('OPERADOR', r'[+\-*/=<>]'),
    ('CARACTER ESPECIAL', r'[.,:;()]'),
    ('CADENA', r'".*?"|\'[^\']*?\''),  
    ('COMENTARIO', r'#.*'),
    ('COMENTARIO_MULTILÍNEA', r'\'\'\'(.*?)\'\'\'|\"\"\"(.*?)\"\"\"', re.DOTALL),
    ('TABULACIÓN', r'\t'),
    ('ESPACIO_EN_BLANCO', r' '),
    ('SALTO_DE_LÍNEA', r'\n'),
    ('CARÁCTER_ESPECIAL', r'.'),
]

class Lexer:
    def __init__(self, code):
        self.code = code

    def tokenize(self):
        tokens = []
        pos = 0
        while pos < len(self.code):
            match = None
            for token_pattern in TOKEN_PATTERNS:
                token_type = token_pattern[0]
                pattern = token_pattern[1]
                flags = token_pattern[2] if len(token_pattern) > 2 else 0
                
                regex = re.compile(pattern, flags)
                match = regex.match(self.code, pos)
                if match:
                    text = match.group(0)
                    if token_type == 'ESPACIO_EN_BLANCO':
                        token_label = 'Espacio En Blanco'
                    elif token_type == 'TABULACIÓN':
                        token_label = 'Tabulación'
                    elif token_type == 'SALTO_DE_LÍNEA':
                        token_label = 'Salto de Línea'
                    else:
                        token_label = token_type.replace('_', ' ').capitalize()
                    tokens.append(f"<'{text}', {token_label}>")
                    pos = match.end(0)
                    break
            if not match:
                raise RuntimeError(f'Error de análisis en la posición {pos}')
        return tokens

# Función para analizar el código ingresado y mostrar los tokens
def analyze_code():
    code = input_text.get("1.0", tk.END)
    lexer = Lexer(code)
    tokens = lexer.tokenize()

    output_text.delete('1.0', tk.END)
    for token in tokens:
        output_text.insert(tk.END, token + '\n')

# Función para validar el inicio de sesión
def validar_login():
    usuario = entry_usuario.get()
    contraseña = entry_contraseña.get()

    try:
        with open('usuarios.txt', 'r') as file:
            for linea in file:
                credenciales = linea.strip().split(':')
                if credenciales[0] == usuario and credenciales[1] == contraseña:
                    messagebox.showinfo("Inicio de sesión exitoso", "Bienvenido!")
                    ventana_login.destroy()  # Cierra la ventana de inicio de sesión
                    mostrar_ventana_principal()  # Muestra la ventana principal
                    return
            messagebox.showerror("Error", "Usuario o contraseña incorrectos")
    except FileNotFoundError:
        messagebox.showerror("Error", "No se encontró el archivo de usuarios")

# Función para registrar un nuevo usuario
def registrar_usuario():
    nuevo_usuario = entry_nuevo_usuario.get()
    nueva_contraseña = entry_nueva_contraseña.get()

    if nuevo_usuario and nueva_contraseña:
        with open('usuarios.txt', 'a') as file:
            file.write(f"{nuevo_usuario}:{nueva_contraseña}\n")
        messagebox.showinfo("Registro exitoso", "El usuario ha sido registrado con éxito")
        ventana_registro.destroy()
        mostrar_ventana_login()  # Regresa a la ventana de inicio de sesión
    else:
        messagebox.showerror("Error", "Por favor, ingrese un usuario y una contraseña válidos")

# Función para regresar a la pantalla de inicio de sesión
def regresar_a_login():
    ventana_registro.destroy()
    mostrar_ventana_login()

# Ventana para el registro de un nuevo usuario
def mostrar_ventana_registro():
    global ventana_registro, entry_nuevo_usuario, entry_nueva_contraseña
    ventana_login.destroy()  # Cierra la ventana de login cuando abre la de registro
    ventana_registro = tk.Tk()
    ventana_registro.title("Registrar Nuevo Usuario")
    ventana_registro.geometry("300x200")  # Establecemos un tamaño fijo de ventana

    tk.Label(ventana_registro, text="Nuevo Usuario:").grid(row=0, column=0, sticky=tk.W)
    entry_nuevo_usuario = tk.Entry(ventana_registro)
    entry_nuevo_usuario.grid(row=0, column=1, sticky=tk.EW)

    tk.Label(ventana_registro, text="Nueva Contraseña:").grid(row=1, column=0, sticky=tk.W)
    entry_nueva_contraseña = tk.Entry(ventana_registro, show="*")
    entry_nueva_contraseña.grid(row=1, column=1, sticky=tk.EW)

    boton_registrar = tk.Button(ventana_registro, text="Registrar", command=registrar_usuario)
    boton_registrar.grid(row=2, column=0, columnspan=2)

    # Botón para regresar al login
    boton_regresar = tk.Button(ventana_registro, text="Regresar al Login", command=regresar_a_login)
    boton_regresar.grid(row=3, column=0, columnspan=2)

    # Permitir que la columna 1 se expanda
    ventana_registro.grid_columnconfigure(1, weight=1)

    ventana_registro.mainloop()

# Función para regresar al inicio desde el análisis léxico
def regresar_a_login_desde_analisis():
    root.destroy()
    mostrar_ventana_login()

# Ventana de inicio de sesión
def mostrar_ventana_login():
    global ventana_login, entry_usuario, entry_contraseña
    ventana_login = tk.Tk()
    ventana_login.title("Inicio de Sesión")
    ventana_login.geometry("300x200")  # Establecemos un tamaño fijo de ventana

    tk.Label(ventana_login, text="Usuario:").grid(row=0, column=0, sticky=tk.W)
    entry_usuario = tk.Entry(ventana_login)
    entry_usuario.grid(row=0, column=1, sticky=tk.EW)

    tk.Label(ventana_login, text="Contraseña:").grid(row=1, column=0, sticky=tk.W)
    entry_contraseña = tk.Entry(ventana_login, show="*")
    entry_contraseña.grid(row=1, column=1, sticky=tk.EW)

    boton_login = tk.Button(ventana_login, text="Iniciar sesión", command=validar_login)
    boton_login.grid(row=2, column=0, columnspan=2)

    boton_registrar = tk.Button(ventana_login, text="Registrar nuevo usuario", command=mostrar_ventana_registro)
    boton_registrar.grid(row=3, column=0, columnspan=2)

    # Permitir que la columna 1 se expanda
    ventana_login.grid_columnconfigure(1, weight=1)

    ventana_login.mainloop()

# Ventana principal para análisis léxico
def mostrar_ventana_principal():
    global root
    root = tk.Tk()
    root.title("Análisis Léxico")
    root.geometry("600x400")  # Establecemos un tamaño fijo de ventana

    label = tk.Label(root, text="Ingresa el código o texto para analizar:")
    label.pack()

    global input_text, output_text
    input_text = scrolledtext.ScrolledText(root, width=70, height=10)
    input_text.pack(fill=tk.BOTH, expand=True)

    analyze_button = tk.Button(root, text="Analizar", command=analyze_code)
    analyze_button.pack()

    output_text = scrolledtext.ScrolledText(root, width=70, height=10)
    output_text.pack(fill=tk.BOTH, expand=True)

    # Botón para regresar a la pantalla de login
    boton_regresar_login = tk.Button(root, text="Regresar al Login", command=regresar_a_login_desde_analisis)
    boton_regresar_login.pack()

    root.mainloop()

# Iniciar la ventana de login
mostrar_ventana_login()
