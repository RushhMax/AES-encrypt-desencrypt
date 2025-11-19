
# **RSA Calculator – GUI (CustomTkinter)**

Aplicación educativa y visual para entender paso a paso el funcionamiento del algoritmo RSA.
Permite calcular (N), (\phi(N)), generar candidatos, factorizar valores, verificar parámetros (e) y (d), cifrar, y *descifrar de forma independiente*.

---

## 📌 **Características principales**

### ✔️ **Interfaz Moderna (CustomTkinter)**

Diseño oscuro, limpio y con scroll vertical para manejar una interfaz larga.

### ✔️ **Cálculo paso a paso del RSA**

1. **Step 1:**

   * Ingresar (p) y (q)
   * Calcular (N = pq)
   * Calcular (\phi(N) = (p-1)(q-1))
   * Mostrar candidatos del tipo (K = 1 \mod r)

2. **Step 2:**

   * Ingresar un valor K
   * Factorizarlo automáticamente

3. **Step 3:**

   * Ingresar valores personalizados de **e** y **d**
   * Verificar condiciones:

     * (gcd(e, r) = 1)
     * (gcd(d, r) = 1)
     * (e \cdot d \equiv 1 \mod r)

4. **Step 4:**

   * Cifrar un mensaje numérico con (e)
   * Descifrar con (d)
   * **Descifrado independiente:** permitir ingresar un ciphertext manualmente

---

## 📦 **Requisitos**

### Python 3.8+

Instalar dependencias:

```bash
pip install customtkinter
```

CustomTkinter funciona en Windows, Linux y macOS.

---

## ▶️ **Cómo ejecutar**

Ejecuta directamente el archivo:

```bash
python RSA_cifrado_descifrado.py
```

La ventana abrirá automáticamente la interfaz.

---

## 🧩 **Estructura del programa**

### 🔹 **Funciones RSA**

* `modinv(a, m)` — calcula inverso modular
* `factorize(n)` — factorización simple por prueba de divisores
* Cifrado/descifrado con `pow(m, e, N)`

### 🔹 **Interfaz**

* Construida con **CustomTkinter**
* Scroll vertical para toda la app
* Organizada en 4 módulos:

  * Step 1: Parámetros base
  * Step 2: Factorización
  * Step 3: Elección y verificación
  * Step 4: Cifrar / Descifrar


## 🧪 **Modo de uso**

### 1️⃣ **Calcular N y r**

1. Ingresa **p** y **q** (números primos)
2. Presiona **Compute N and r**

### 2️⃣ **Factorizar un K**

Opcional pero útil para ejercicios educativos.

### 3️⃣ **Evaluar e y d**

Escribe valores e/d y verifica:

→ Si todo está correcto, la interfaz muestra checks ✔️
→ Si hay error, muestra alertas ❌

### 4️⃣ **Cifrado y descifrado**

* Ingresa un mensaje numérico < N
* Presiona **Encrypt / Decrypt**

### 5️⃣ **Descifrado independiente**

Perfecto para pruebas externas.

* Ingresa un ciphertext manualmente
* Haz clic en **Decrypt Only**

---

## 📚 **Propósito del proyecto**

Esta herramienta está diseñada para:

* Estudiantes de criptografía
* Profesores que necesitan demostraciones visuales
* Cursos de seguridad informática
* Experimentación con RSA desde cero