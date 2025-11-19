import customtkinter as ctk
from tkinter import messagebox
import math

# ============================================================
#                   FUNCIONES RSA
# ============================================================

def modinv(a, m):
    def egcd(a, b):
        if a == 0:
            return b, 0, 1
        g, y, x = egcd(b % a, a)
        return g, x - (b // a) * y, y

    g, x, y = egcd(a, m)
    if g != 1:
        return None
    return x % m

def factorize(n):
    i = 2
    factors = []
    while i * i <= n:
        while n % i == 0:
            factors.append(i)
            n //= i
        i += 1
    if n > 1:
        factors.append(n)
    return factors


# ============================================================
#          CONFIGURAR CUSTOMTKINTER
# ============================================================

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

root = ctk.CTk()
root.title("RSA Calculator - Modern UI")
root.geometry("700x900")

font_title = ctk.CTkFont(size=18, weight="bold")


# ============================================================
#     CREAR CANVAS + SCROLLBAR (scroll para toda la app)
# ============================================================

main_canvas = ctk.CTkCanvas(root, highlightthickness=0, bg="#1a1a1a")
main_canvas.pack(side="left", fill="both", expand=True)

scrollbar = ctk.CTkScrollbar(root, orientation="vertical", command=main_canvas.yview)
scrollbar.pack(side="right", fill="y")

main_canvas.configure(yscrollcommand=scrollbar.set)

# Frame interno scrolleable
scroll_frame = ctk.CTkFrame(main_canvas)
scroll_window = main_canvas.create_window((0, 0), window=scroll_frame, anchor="nw")

def update_scroll(event=None):
    main_canvas.configure(scrollregion=main_canvas.bbox("all"))

scroll_frame.bind("<Configure>", update_scroll)

# Permitir scroll con la rueda del mouse
def mouse_scroll(event):
    main_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

root.bind_all("<MouseWheel>", mouse_scroll)



# ============================================================
#                   STEP 1
# ============================================================

frame1 = ctk.CTkFrame(scroll_frame, corner_radius=12)
frame1.pack(padx=20, pady=10, fill="x")

ctk.CTkLabel(frame1, text="Step 1: Compute N = p*q", font=font_title).pack(pady=5)

container1 = ctk.CTkFrame(frame1)
container1.pack()

ctk.CTkLabel(container1, text="p: ").grid(row=0, column=0, padx=5, pady=5)
entry_p = ctk.CTkEntry(container1, width=80)
entry_p.grid(row=0, column=1, padx=5)

ctk.CTkLabel(container1, text="q: ").grid(row=1, column=0, padx=5, pady=5)
entry_q = ctk.CTkEntry(container1, width=80)
entry_q.grid(row=1, column=1, padx=5)

label_N = ctk.CTkLabel(frame1, text="N = ")
label_N.pack(pady=5)

label_r = ctk.CTkLabel(frame1, text="r = ")
label_r.pack(pady=5)

ctk.CTkLabel(frame1, text="Candidates (1 mod r):").pack()
cand_list = ctk.CTkTextbox(frame1, height=90)
cand_list.pack(pady=5, padx=10)

def step1_compute():
    global p, q, N, r
    try:
        p = int(entry_p.get())
        q = int(entry_q.get())
    except:
        messagebox.showerror("Error", "p y q deben ser enteros.")
        return

    N = p * q
    r = (p - 1) * (q - 1)

    label_N.configure(text=f"N = {N}")
    label_r.configure(text=f"r = {r}")

    cand_list.delete("0.0", "end")
    for i in range(1, 31):
        cand_list.insert("end", f"{i*r + 1} ")

ctk.CTkButton(frame1, text="Compute N and r", command=step1_compute).pack(pady=10)


# ============================================================
#                   STEP 2
# ============================================================

frame2 = ctk.CTkFrame(scroll_frame, corner_radius=12)
frame2.pack(padx=20, pady=10, fill="x")

ctk.CTkLabel(frame2, text="Step 2: Factor a candidate K", font=font_title).pack(pady=5)

container2 = ctk.CTkFrame(frame2)
container2.pack()

ctk.CTkLabel(container2, text="K: ").grid(row=0, column=0, padx=5)
entry_K = ctk.CTkEntry(container2, width=100)
entry_K.grid(row=0, column=1, padx=5)

label_Kfactors = ctk.CTkLabel(frame2, text="factors of K: ")
label_Kfactors.pack(pady=5)

def step2_factor():
    try:
        K = int(entry_K.get())
    except:
        messagebox.showerror("Error", "K debe ser entero.")
        return

    factors = factorize(K)
    label_Kfactors.configure(text=f"factors of K: {' * '.join(map(str, factors))}")

ctk.CTkButton(frame2, text="Factorize K", command=step2_factor).pack(pady=10)



# ============================================================
#                   STEP 3
# ============================================================

frame3 = ctk.CTkFrame(scroll_frame, corner_radius=12)
frame3.pack(padx=20, pady=10, fill="x")

ctk.CTkLabel(frame3, text="Step 3: Choose e and d", font=font_title).pack(pady=5)

container3 = ctk.CTkFrame(frame3)
container3.pack()

ctk.CTkLabel(container3, text="e: ").grid(row=0, column=0, padx=5)
entry_e = ctk.CTkEntry(container3, width=100)
entry_e.grid(row=0, column=1, padx=5)

ctk.CTkLabel(container3, text="d: ").grid(row=1, column=0, padx=5)
entry_d = ctk.CTkEntry(container3, width=100)
entry_d.grid(row=1, column=1, padx=5)

label_check = ctk.CTkLabel(frame3, text="Consistency check:")
label_check.pack(pady=8)

def step3_check():
    try:
        e = int(entry_e.get())
        d = int(entry_d.get())
    except:
        messagebox.showerror("Error", "e y d deben ser enteros.")
        return

    message = (
        f"e = {e}\n"
        f"d = {d}\n"
        f"N = {N}\n"
        f"r = {r}\n"
        f"e*d = {e*d}\n"
        f"e*d mod r = {(e*d) % r}\n"
    )

    import math
    if math.gcd(e, r) == 1 and math.gcd(d, r) == 1 and (e * d) % r == 1:
        message += "\n✔ e*d mod r = 1\n✔ e and r are relatively prime\n✔ d and r are relatively prime"
    else:
        message += "\n❌ ERROR: e o d no cumplen los requisitos."

    label_check.configure(text=message)

ctk.CTkButton(frame3, text="Check e and d", command=step3_check).pack(pady=10)



# ============================================================
#                   STEP 4
# ============================================================

frame4 = ctk.CTkFrame(scroll_frame, corner_radius=12)
frame4.pack(padx=20, pady=10, fill="x")

ctk.CTkLabel(frame4, text="Step 4: Encode / Decode", font=font_title).pack(pady=5)

container4 = ctk.CTkFrame(frame4)
container4.pack()

ctk.CTkLabel(container4, text="Message (number): ").grid(row=0, column=0, padx=5)
entry_msg = ctk.CTkEntry(container4, width=120)
entry_msg.grid(row=0, column=1, padx=5)

label_cipher = ctk.CTkLabel(frame4, text="Encrypted = ")
label_cipher.pack(pady=5)

label_decrypted = ctk.CTkLabel(frame4, text="Decrypted = ")
label_decrypted.pack(pady=5)

def step4_process():
    try:
        e = int(entry_e.get())
        d = int(entry_d.get())
        message = int(entry_msg.get())
    except:
        messagebox.showerror("Error", "Valores incorrectos.")
        return

    if message >= N:
        messagebox.showerror("Error", "El mensaje debe ser menor que N.")
        return

    cipher = pow(message, e, N)
    decrypted = pow(cipher, d, N)

    label_cipher.configure(text=f"Encrypted = {cipher}")
    label_decrypted.configure(text=f"Decrypted = {decrypted}")

ctk.CTkButton(frame4, text="Encrypt / Decrypt", command=step4_process).pack(pady=10)


root.mainloop()
