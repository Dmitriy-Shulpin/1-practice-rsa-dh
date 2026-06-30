import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import math


# =============================================
# Вспомогательные функции
# =============================================
def is_prime(n):
    if n < 2: return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0: return False
    return True


def gcd(a, b):
    while b:
        a, b = b, a % b
    return a


def find_d(e, phi):
    for d in range(2, phi):
        if (d * e) % phi == 1:
            return d
    return None


def get_possible_e(phi):
    return [x for x in range(2, phi) if gcd(x, phi) == 1]


# =============================================
# Шаг 1: Рассчитать допустимые e
# =============================================
def calculate_e():
    out.delete("1.0", tk.END)

    try:
        p = int(entry_p.get().strip())
        q = int(entry_q.get().strip())
    except ValueError:
        messagebox.showerror("Ошибка", "Введите корректные числа для p и q!")
        return

    if not is_prime(p):
        messagebox.showerror("Ошибка", f"p = {p} не является простым числом!")
        return
    if not is_prime(q):
        messagebox.showerror("Ошибка", f"q = {q} не является простым числом!")
        return
    if p == q:
        messagebox.showerror("Ошибка", "p и q должны быть разными!")
        return

    n = p * q
    phi = (p - 1) * (q - 1)
    possible_e = get_possible_e(phi)

    global current_n, current_phi, current_possible_e
    current_n = n
    current_phi = phi
    current_possible_e = possible_e

    out.insert(tk.END, "=" * 60 + "\n")
    out.insert(tk.END, "ШАГ 1. ПАРАМЕТРЫ RSA\n")
    out.insert(tk.END, "=" * 60 + "\n\n")
    out.insert(tk.END, f"p = {p}\n")
    out.insert(tk.END, f"q = {q}\n")
    out.insert(tk.END, f"n = p × q = {p} × {q} = {n}\n")
    out.insert(tk.END, f"φ(n) = (p-1) × (q-1) = {p - 1} × {q - 1} = {phi}\n\n")
    out.insert(tk.END, f"Допустимые значения e: {possible_e}\n")
    out.insert(tk.END, f"Максимальное количество e: {len(possible_e)}\n\n")
    out.insert(tk.END, "Теперь введите выбранное e в поле выше и нажмите 'Шифровать'.\n")

    # Автоматический скролл в начало
    out.see("1.0")


# =============================================
# Шаг 2: Шифрование с выбранным e
# =============================================
def run_encrypt():
    out.insert(tk.END, "\n" + "=" * 60 + "\n")
    out.insert(tk.END, "ШАГ 2. ШИФРОВАНИЕ И РАСШИФРОВАНИЕ\n")
    out.insert(tk.END, "=" * 60 + "\n\n")

    try:
        e = int(entry_e.get().strip())
        msg = entry_msg.get().strip()
    except ValueError:
        messagebox.showerror("Ошибка", "Введите корректное число для e!")
        return

    if current_n is None or current_phi is None or current_possible_e is None:
        messagebox.showerror("Ошибка", "Сначала нажмите 'Рассчитать e'!")
        return

    if e not in current_possible_e:
        messagebox.showerror(
            "Ошибка",
            f"e = {e} не подходит!\n\n"
            f"Допустимые значения: {current_possible_e}"
        )
        return

    d = find_d(e, current_phi)
    if d is None:
        messagebox.showerror("Ошибка", f"Не удалось найти d для e = {e}!")
        return

    out.insert(tk.END, f"e = {e}\n")
    out.insert(tk.END, f"d = {d}\n")
    out.insert(tk.END, f"Открытый ключ: (e, n) = ({e}, {current_n})\n")
    out.insert(tk.END, f"Закрытый ключ: (d, n) = ({d}, {current_n})\n\n")

    # Режим: число или текст
    if msg.isdigit() or (msg.startswith("-") and msg[1:].isdigit()):
        M = int(msg)
        if not (0 <= M < current_n):
            messagebox.showerror(
                "Ошибка",
                f"Число M = {M} должно быть в диапазоне: 0 ≤ M < {current_n}"
            )
            return
        C = pow(M, e, current_n)
        R = pow(C, d, current_n)
        out.insert(tk.END, f"Исходное число (M): {M}\n")
        out.insert(tk.END, f"Шифрование: C = {M}^{e} mod {current_n} = {C}\n")
        out.insert(tk.END, f"Расшифрование: M' = {C}^{d} mod {current_n} = {R}\n")
        if M == R:
            out.insert(tk.END, "\n✅ УСПЕХ! Числа совпадают.")
        else:
            out.insert(tk.END, "\n❌ ОШИБКА! Числа не совпадают.")
    else:
        out.insert(tk.END, f"Исходный текст: {msg}\n\n")
        encrypted = []
        decrypted_chars = []
        for ch in msg:
            code = ord(ch)
            if code >= current_n:
                messagebox.showerror(
                    "Ошибка",
                    f"Код символа '{ch}' ({code}) >= n = {current_n}\n"
                    "Используйте числа побольше (p и q) или введите число."
                )
                return
            enc_code = pow(code, e, current_n)
            dec_code = pow(enc_code, d, current_n)
            encrypted.append(enc_code)
            decrypted_chars.append(chr(dec_code))
        out.insert(tk.END, f"Зашифрованные коды: {encrypted}\n")
        out.insert(tk.END, f"Расшифрованный текст: {''.join(decrypted_chars)}\n")
        if msg == ''.join(decrypted_chars):
            out.insert(tk.END, "\n✅ УСПЕХ! Текст совпадает.")
        else:
            out.insert(tk.END, "\n❌ ОШИБКА! Текст не совпадает.")

    # Автоматический скролл в конец (чтобы видеть результаты)
    out.see(tk.END)


# =============================================
# Очистка
# =============================================
def clear_all():
    entry_p.delete(0, tk.END)
    entry_q.delete(0, tk.END)
    entry_e.delete(0, tk.END)
    entry_msg.delete(0, tk.END)
    out.delete("1.0", tk.END)
    global current_n, current_phi, current_possible_e
    current_n = None
    current_phi = None
    current_possible_e = None


# =============================================
# Интерфейс
# =============================================
root = tk.Tk()
root.title("RSA — Асимметричное шифрование")
root.geometry("900x750")
root.minsize(800, 700)  # Минимальный размер, чтобы не сжималось слишком сильно

current_n = None
current_phi = None
current_possible_e = None

# Заголовок
tk.Label(root, text="RSA — Шифрование и расшифрование", font=("Arial", 16, "bold")).pack(pady=10)

# Поля ввода
frame_input = tk.Frame(root)
frame_input.pack(pady=10, padx=20, fill="x")

tk.Label(frame_input, text="p (простое число):", font=("Arial", 10)).grid(row=0, column=0, sticky="w", padx=5, pady=5)
entry_p = tk.Entry(frame_input, width=15)
entry_p.grid(row=0, column=1, padx=5, pady=5)

tk.Label(frame_input, text="q (простое число):", font=("Arial", 10)).grid(row=1, column=0, sticky="w", padx=5, pady=5)
entry_q = tk.Entry(frame_input, width=15)
entry_q.grid(row=1, column=1, padx=5, pady=5)

tk.Label(frame_input, text="e (выберите из списка):", font=("Arial", 10)).grid(row=2, column=0, sticky="w", padx=5,
                                                                               pady=5)
entry_e = tk.Entry(frame_input, width=15)
entry_e.grid(row=2, column=1, padx=5, pady=5)

tk.Label(frame_input, text="Сообщение (число или текст):", font=("Arial", 10)).grid(row=3, column=0, sticky="w", padx=5,
                                                                                    pady=5)
entry_msg = tk.Entry(frame_input, width=30)
entry_msg.grid(row=3, column=1, padx=5, pady=5)

# Кнопки
frame_buttons = tk.Frame(root)
frame_buttons.pack(pady=10)

btn_calc = tk.Button(frame_buttons, text="1. Рассчитать e", command=calculate_e, bg="#2196F3", fg="white",
                     font=("Arial", 10, "bold"), width=18)
btn_calc.pack(side="left", padx=10)

btn_encrypt = tk.Button(frame_buttons, text="2. Шифровать", command=run_encrypt, bg="#4CAF50", fg="white",
                        font=("Arial", 10, "bold"), width=18)
btn_encrypt.pack(side="left", padx=10)

btn_clear = tk.Button(frame_buttons, text="Очистить всё", command=clear_all, bg="#f0f0f0", font=("Arial", 10, "bold"),
                      width=15)
btn_clear.pack(side="left", padx=10)

# Подсказки
tk.Label(root, text="Пример: p=3, q=11 → Допустимые e: [5, 7]", font=("Arial", 9), fg="gray").pack()
tk.Label(root, text="Пример: p=43, q=59 → Допустимые e: [2, 4, 6, 8, 10, 12, 14, 16, 18, 20, ...]", font=("Arial", 9),
         fg="gray").pack()

# Поле вывода
tk.Label(root, text="Результаты:", font=("Arial", 12, "bold")).pack(pady=5)

out = scrolledtext.ScrolledText(root, width=100, height=28, font=("Courier New", 10))
out.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)

root.mainloop()