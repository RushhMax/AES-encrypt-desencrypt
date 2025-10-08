
# AES-128 Cifrador/Descifrador con Tkinter

## Descripción
Este proyecto implementa **AES-128 desde cero** en Python, incluyendo cifrado y descifrado de bloques de 16 bytes. Además, cuenta con una **interfaz gráfica amigable** usando Tkinter, lo que permite cifrar y descifrar texto de manera interactiva.

El algoritmo implementa:

- Cifrado y descifrado de bloques de 16 bytes.
- Modo **ECB** (Electronic Codebook) para múltiples bloques.
- **Padding PKCS7** para manejar textos de longitud variable.
- Transformaciones AES completas: `SubBytes`, `ShiftRows`, `MixColumns`, `AddRoundKey`.
- Expansión de clave (**Key Schedule**) para generar las 11 claves de ronda.

---

## Funcionalidades

- **Cifrar texto**: ingresa un texto y una clave de 16 caracteres; el resultado se muestra en hexadecimal.
- **Descifrar texto**: ingresa el texto cifrado en hexadecimal y la clave para recuperar el texto original.
- **Limpiar campos**: limpia la entrada y el área de resultados.
- **Ejemplo de prueba**: carga un texto y clave de ejemplo para probar rápidamente.

---

## Requisitos

- Python 3.7 o superior
- Librerías estándar de Python:
  - `tkinter`
  - `ttk`
  - `scrolledtext`
  - `messagebox`

No se requieren librerías externas.

---

## Uso

1. Clonar o descargar el repositorio.
2. Ejecutar el archivo principal
3. Interactuar con la interfaz:

* Ingresar texto y clave para cifrar o descifrar.
* Hacer clic en los botones correspondientes: **Cifrar**, **Descifrar**, **Limpiar**, o **Probar Ejemplo**.
* Ver resultados en el área de texto inferior.

---

## Ejemplo de flujo

### Cifrar

* **Texto:** Hola desde la EPCC - Seguridad Informática
* **Clave:** clave-secreta-16
* **Resultado (hex):** ...

### Descifrar

* **Texto cifrado:** ... (hexadecimal)
* **Clave:** clave-secreta-16
* **Resultado:** Hola desde la EPCC - Seguridad Informática

---

## Estructura del código

* **aes_gui.py**: archivo principal con la implementación de AES-128 y la interfaz Tkinter.

**Funciones principales AES:**

* `encriptar_bloque()`, `desencriptar_bloque()`
* `pad_text()`, `unpad_text()`
* `expansion_clave()`
* Transformaciones: `sub_bytes()`, `shift_rows()`, `mezclar_columnas()`, `add_round_key()`

**Clase AESApp:**

* Define la interfaz y los botones interactivos.
* Métodos: `cifrar()`, `descifrar()`, `limpiar()`, `probar_ejemplo()`

---

## Notas importantes

* La clave debe tener **exactamente 16 caracteres**.
* El texto cifrado se muestra en **formato hexadecimal**.
* Actualmente el proyecto implementa **modo ECB**, no recomendado para grandes cantidades de datos sensibles. Para aplicaciones reales, se recomienda **AES con CBC o GCM**.

---

## Licencia

Este proyecto es de **código abierto** y puede ser utilizado con fines educativos y de aprendizaje.

```

Si quieres, puedo hacer otra versión con **capturas de pantalla simuladas y tablas de ejemplo de cifrado/descifrado**, que queda muy profesional para GitHub.  

¿Quieres que haga esa versión también?
```
