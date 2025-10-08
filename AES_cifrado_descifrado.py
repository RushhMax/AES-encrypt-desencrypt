import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext

# AES-128 implementado desde cero (cifrado y descifrado de un bloque de 16 bytes)

SBOX = [
0x63,0x7c,0x77,0x7b,0xf2,0x6b,0x6f,0xc5,0x30,0x01,0x67,0x2b,0xfe,0xd7,0xab,0x76,
0xca,0x82,0xc9,0x7d,0xfa,0x59,0x47,0xf0,0xad,0xd4,0xa2,0xaf,0x9c,0xa4,0x72,0xc0,
0xb7,0xfd,0x93,0x26,0x36,0x3f,0xf7,0xcc,0x34,0xa5,0xe5,0xf1,0x71,0xd8,0x31,0x15,
0x04,0xc7,0x23,0xc3,0x18,0x96,0x05,0x9a,0x07,0x12,0x80,0xe2,0xeb,0x27,0xb2,0x75,
0x09,0x83,0x2c,0x1a,0x1b,0x6e,0x5a,0xa0,0x52,0x3b,0xd6,0xb3,0x29,0xe3,0x2f,0x84,
0x53,0xd1,0x00,0xed,0x20,0xfc,0xb1,0x5b,0x6a,0xcb,0xbe,0x39,0x4a,0x4c,0x58,0xcf,
0xd0,0xef,0xaa,0xfb,0x43,0x4d,0x33,0x85,0x45,0xf9,0x02,0x7f,0x50,0x3c,0x9f,0xa8,
0x51,0xa3,0x40,0x8f,0x92,0x9d,0x38,0xf5,0xbc,0xb6,0xda,0x21,0x10,0xff,0xf3,0xd2,
0xcd,0x0c,0x13,0xec,0x5f,0x97,0x44,0x17,0xc4,0xa7,0x7e,0x3d,0x64,0x5d,0x19,0x73,
0x60,0x81,0x4f,0xdc,0x22,0x2a,0x90,0x88,0x46,0xee,0xb8,0x14,0xde,0x5e,0x0b,0xdb,
0xe0,0x32,0x3a,0x0a,0x49,0x06,0x24,0x5c,0xc2,0xd3,0xac,0x62,0x91,0x95,0xe4,0x79,
0xe7,0xc8,0x37,0x6d,0x8d,0xd5,0x4e,0xa9,0x6c,0x56,0xf4,0xea,0x65,0x7a,0xae,0x08,
0xba,0x78,0x25,0x2e,0x1c,0xa6,0xb4,0xc6,0xe8,0xdd,0x74,0x1f,0x4b,0xbd,0x8b,0x8a,
0x70,0x3e,0xb5,0x66,0x48,0x03,0xf6,0x0e,0x61,0x35,0x57,0xb9,0x86,0xc1,0x1d,0x9e,
0xe1,0xf8,0x98,0x11,0x69,0xd9,0x8e,0x94,0x9b,0x1e,0x87,0xe9,0xce,0x55,0x28,0xdf,
0x8c,0xa1,0x89,0x0d,0xbf,0xe6,0x42,0x68,0x41,0x99,0x2d,0x0f,0xb0,0x54,0xbb,0x16
]

INV_SBOX = [0]*256
for i, v in enumerate(SBOX):
    INV_SBOX[v] = i

# CONSTANTES_RONDA para la expansión de clave
CONSTANTES_RONDA = [
    0x00,0x01,0x02,0x04,0x08,0x10,0x20,0x40,0x80,0x1B,0x36
]

def duplica_especial(a: int) -> int:
    """Multiplica por x (02) en GF(2^8) con polinomio 0x11B."""
    return ((a << 1) ^ 0x1B) & 0xFF if (a & 0x80) else (a << 1) & 0xFF

def multiplica_especial(a: int, b: int) -> int:
    """Multiplicación en GF(2^8) (algoritmo 'Russian peasant')."""
    res = 0
    for _ in range(8):
        if b & 1:
            res ^= a
        hi = a & 0x80
        a = (a << 1) & 0xFF
        if hi:
            a ^= 0x1B
        b >>= 1
    return res

def convertir_a_matriz(b: bytes) -> list:
    """Convierte 16 bytes en una matriz 4x4 (estado) siguiendo orden columna por columna."""
    return [[b[col*4 + row] for col in range(4)] for row in range(4)]

def convertir_a_bytes(matrix: list) -> bytes:
    """Convierte estado 4x4 de vuelta a 16 bytes (columna por columna)."""
    return bytes([matrix[row][col] for col in range(4) for row in range(4)])

# ---- Transformaciones básicas ----

def add_round_key(estado: list, llave_extra: bytes):
    """XOR del estado con la llave_extra (16 bytes)."""
    rk = convertir_a_matriz(llave_extra)
    for r in range(4):
        for c in range(4):
            estado[r][c] ^= rk[r][c]

def sub_bytes(estado: list):
    """Aplica S-box a cada byte del estado."""
    for r in range(4):
        for c in range(4):
            estado[r][c] = SBOX[estado[r][c]]

def inv_sub_bytes(estado: list):
    for r in range(4):
        for c in range(4):
            estado[r][c] = INV_SBOX[estado[r][c]]

def shift_rows(estado: list):
    """Rota las filas: row r rota r posiciones a la izquierda."""
    for r in range(1, 4):
        estado[r] = estado[r][r:] + estado[r][:r]

def inv_shift_rows(estado: list):
    for r in range(1, 4):
        estado[r] = estado[r][-r:] + estado[r][:-r]

def mezclar_una_columna(col: list):
    """MixColumns para una columna (4 bytes)."""
    a = col[:]  # original
    col[0] = multiplica_especial(a[0],2) ^ multiplica_especial(a[1],3) ^ a[2] ^ a[3]
    col[1] = a[0] ^ multiplica_especial(a[1],2) ^ multiplica_especial(a[2],3) ^ a[3]
    col[2] = a[0] ^ a[1] ^ multiplica_especial(a[2],2) ^ multiplica_especial(a[3],3)
    col[3] = multiplica_especial(a[0],3) ^ a[1] ^ a[2] ^ multiplica_especial(a[3],2)

def mezclar_columnas(estado: list):
    for c in range(4):
        col = [estado[r][c] for r in range(4)]
        mezclar_una_columna(col)
        for r in range(4):
            estado[r][c] = col[r]

def inv_mezclar_una_columna(col: list):
    a = col[:]
    col[0] = multiplica_especial(a[0],0x0e) ^ multiplica_especial(a[1],0x0b) ^ multiplica_especial(a[2],0x0d) ^ multiplica_especial(a[3],0x09)
    col[1] = multiplica_especial(a[0],0x09) ^ multiplica_especial(a[1],0x0e) ^ multiplica_especial(a[2],0x0b) ^ multiplica_especial(a[3],0x0d)
    col[2] = multiplica_especial(a[0],0x0d) ^ multiplica_especial(a[1],0x09) ^ multiplica_especial(a[2],0x0e) ^ multiplica_especial(a[3],0x0b)
    col[3] = multiplica_especial(a[0],0x0b) ^ multiplica_especial(a[1],0x0d) ^ multiplica_especial(a[2],0x09) ^ multiplica_especial(a[3],0x0e)

def inv_mezclar_columnas(estado: list):
    for c in range(4):
        col = [estado[r][c] for r in range(4)]
        inv_mezclar_una_columna(col)
        for r in range(4):
            estado[r][c] = col[r]

# ---- Key schedule (expansión de clave) ----
def expansion_clave(llave: bytes) -> list:
    """Genera 11 round keys (11 * 16 bytes) a partir de la clave de 16 bytes."""
    assert len(llave) == 16
    
    # Convertir clave a palabras de 4 bytes
    w = [list(llave[i:i+4]) for i in range(0, 16, 4)]

    # Expandir a 44 palabras
    for i in range(4, 44):
        temp = w[i-1][:]
        
        if i % 4 == 0:
            # RotWord + SubWord + CONSTANTES_RONDA
            temp = temp[1:] + temp[:1]  # RotWord
            temp = [SBOX[b] for b in temp]  # SubWord
            temp[0] ^= CONSTANTES_RONDA[i//4]  # CONSTANTES_RONDA
        else:
            # Solo XOR normal
            pass
            
        # Nueva palabra = palabra[i-4] XOR temp
        palabra_nueva = [w[i-4][j] ^ temp[j] for j in range(4)]
        w.append(palabra_nueva)
    
    # Convertir a round keys
    llaves_extra = []
    for i in range(0, 44, 4):
        llave_extra = []
        for j in range(4):
            llave_extra.extend(w[i+j])
        llaves_extra.append(bytes(llave_extra))
    
    return llaves_extra

def encriptar_bloque(texto: bytes, llave: bytes) -> bytes:
    """Cifra un bloque de 16 bytes con AES-128."""
    assert len(texto) == 16 and len(llave) == 16 
    llaves_extra = expansion_clave(llave)
    estado = convertir_a_matriz(texto)

    # AddRoundKey inicial
    add_round_key(estado, llaves_extra[0])

    # 9 rondas
    for ronda in range(1, 10):
        sub_bytes(estado)
        shift_rows(estado)
        mezclar_columnas(estado)
        add_round_key(estado, llaves_extra[ronda])

    # ronda final (sin mixcolumns)
    sub_bytes(estado)
    shift_rows(estado)
    add_round_key(estado, llaves_extra[10])

    return convertir_a_bytes(estado)

def desencriptar_bloque(ciphertext: bytes, llave: bytes) -> bytes:
    """Descifra un bloque de 16 bytes con AES-128."""
    assert len(ciphertext) == 16 and len(llave) == 16
    llaves_extra = expansion_clave(llave)
    estado = convertir_a_matriz(ciphertext)

    # add round key final
    add_round_key(estado, llaves_extra[10])
    inv_shift_rows(estado)
    inv_sub_bytes(estado)

    # 9 rondas inversas
    for ronda in range(9, 0, -1):
        add_round_key(estado, llaves_extra[ronda])
        inv_mezclar_columnas(estado)
        inv_shift_rows(estado)
        inv_sub_bytes(estado)

    # addRoundKey inicial
    add_round_key(estado, llaves_extra[0])

    return convertir_a_bytes(estado)

def pad_text(text: bytes, block_size: int = 16) -> bytes:
    """Aplica padding PKCS7 al texto."""
    padding_len = block_size - (len(text) % block_size)
    return text + bytes([padding_len] * padding_len)

def unpad_text(data: bytes) -> bytes:
    """Remueve padding PKCS7."""
    padding_len = data[-1]
    return data[:-padding_len]

# Funciones para manejar múltiples bloques
def encriptar(texto: bytes, llave: bytes) -> bytes:
    """Cifra texto de cualquier longitud con AES-128 en modo ECB."""
    texto_padded = pad_text(texto)
    resultado = b''
    
    # Procesar cada bloque de 16 bytes
    for i in range(0, len(texto_padded), 16):
        bloque = texto_padded[i:i+16]
        bloque_cifrado = encriptar_bloque(bloque, llave)
        resultado += bloque_cifrado
    
    return resultado

def desencriptar(ciphertext: bytes, llave: bytes) -> bytes:
    """Descifra texto cifrado con AES-128 en modo ECB."""
    resultado = b''
    
    # Procesar cada bloque de 16 bytes
    for i in range(0, len(ciphertext), 16):
        bloque = ciphertext[i:i+16]
        bloque_descifrado = desencriptar_bloque(bloque, llave)
        resultado += bloque_descifrado
    
    return unpad_text(resultado)

# Interfaz Gráfica
class AESApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AES-128 Cifrador/Descifrador")
        self.root.geometry("600x500")
        
        self.setup_ui()
    
    def setup_ui(self):
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Título
        title_label = ttk.Label(main_frame, text="AES-128 - Cifrado y Descifrado", 
                               font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Entrada de texto
        ttk.Label(main_frame, text="Texto:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.text_entry = scrolledtext.ScrolledText(main_frame, height=4, width=50)
        self.text_entry.grid(row=1, column=1, pady=5, sticky=(tk.W, tk.E))
        
        # Entrada de clave
        ttk.Label(main_frame, text="Clave (16 caracteres):").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.key_entry = ttk.Entry(main_frame, width=50)
        self.key_entry.grid(row=2, column=1, pady=5, sticky=(tk.W, tk.E))
        
        # Botones
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=3, column=0, columnspan=2, pady=20)
        
        ttk.Button(button_frame, text="Cifrar", command=self.cifrar).pack(side=tk.LEFT, padx=10)
        ttk.Button(button_frame, text="Descifrar", command=self.descifrar).pack(side=tk.LEFT, padx=10)
        ttk.Button(button_frame, text="Limpiar", command=self.limpiar).pack(side=tk.LEFT, padx=10)
        ttk.Button(button_frame, text="Probar Ejemplo", command=self.probar_ejemplo).pack(side=tk.LEFT, padx=10)
        
        # Resultados
        ttk.Label(main_frame, text="Resultado:").grid(row=4, column=0, sticky=tk.W, pady=(20, 5))
        self.result_text = scrolledtext.ScrolledText(main_frame, height=6, width=50, state=tk.DISABLED)
        self.result_text.grid(row=4, column=1, pady=5, sticky=(tk.W, tk.E))
        
        # Información
        info_label = ttk.Label(main_frame, 
                              text="Nota: La clave debe tener exactamente 16 caracteres. El texto se ajustará automáticamente.",
                              font=("Arial", 8), foreground="blue")
        info_label.grid(row=5, column=0, columnspan=2, pady=(10, 0))
        
        # Configurar expansión
        main_frame.columnconfigure(1, weight=1)
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
    
    def cifrar(self):
        try:
            texto = self.text_entry.get("1.0", tk.END).strip()
            clave = self.key_entry.get().strip()
            
            if not texto or not clave:
                messagebox.showwarning("Advertencia", "Por favor ingrese texto y clave.")
                return
            
            if len(clave) != 16:
                messagebox.showwarning("Advertencia", "La clave debe tener exactamente 16 caracteres.")
                return
            
            # Convertir a bytes
            texto_bytes = texto.encode('utf-8')
            
            # Cifrar
            clave_bytes = clave.encode('utf-8')
            texto_cifrado = encriptar(texto_bytes, clave_bytes)
            
            # Mostrar resultado
            self.mostrar_resultado(f"TEXTO CIFRADO EXITOSAMENTE\n\n"
                                  f"Texto original: {texto}\n"
                                  f"Longitud original: {len(texto_bytes)} bytes\n\n"
                                  f"Texto cifrado (hex): {texto_cifrado.hex()}\n"
                                  f"Longitud cifrada: {len(texto_cifrado)} bytes")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al cifrar: {str(e)}")
    
    def descifrar(self):
        try:
            texto = self.text_entry.get("1.0", tk.END).strip()
            clave = self.key_entry.get().strip()
            
            if not texto or not clave:
                messagebox.showwarning("Advertencia", "Por favor ingrese texto cifrado y clave.")
                return
            
            if len(clave) != 16:
                messagebox.showwarning("Advertencia", "La clave debe tener exactamente 16 caracteres.")
                return
            
            # Convertir hexadecimal a bytes
            try:
                texto_bytes = bytes.fromhex(texto)
            except:
                messagebox.showwarning("Advertencia", "El texto cifrado debe estar en formato hexadecimal válido.")
                return
            
            # Descifrar
            clave_bytes = clave.encode('utf-8')
            texto_descifrado_bytes = desencriptar(texto_bytes, clave_bytes)
            texto_descifrado = texto_descifrado_bytes.decode('utf-8')
            
            # Mostrar resultado
            self.mostrar_resultado(f"TEXTO DESCIFRADO EXITOSAMENTE\n\n"
                                  f"Texto cifrado (hex): {texto}\n"
                                  f"Longitud cifrada: {len(texto_bytes)} bytes\n\n"
                                  f"Texto descifrado: {texto_descifrado}\n"
                                  f"Longitud descifrada: {len(texto_descifrado)} caracteres")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al descifrar: {str(e)}")
    
    def mostrar_resultado(self, texto):
        self.result_text.config(state=tk.NORMAL)
        self.result_text.delete("1.0", tk.END)
        self.result_text.insert("1.0", texto)
        self.result_text.config(state=tk.DISABLED)
    
    def limpiar(self):
        self.text_entry.delete("1.0", tk.END)
        self.key_entry.delete(0, tk.END)
        self.mostrar_resultado("")
    
    def probar_ejemplo(self):
        # Ejemplo de prueba
        self.text_entry.delete("1.0", tk.END)
        self.text_entry.insert("1.0", "Hola desde la EPCC - Seguridad Informática")
        self.key_entry.delete(0, tk.END)
        self.key_entry.insert(0, "clave-secreta-16")
        messagebox.showinfo("Ejemplo", "Se ha cargado un ejemplo. Haga clic en 'Cifrar' para probar.")

def main():
    root = tk.Tk()
    app = AESApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()