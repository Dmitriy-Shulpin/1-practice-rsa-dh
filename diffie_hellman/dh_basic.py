import tkinter as tk
from tkinter import messagebox, scrolledtext
import math


# =============================================
# Проверка на простоту (с учетом 2)
# =============================================
def is_prime(n):
    if n < 2: return False
    if n == 2: return True
    if n % 2 == 0: return False
    for i in range(3, int(math.sqrt(n)) + 1, 2):
        if n % i == 0:
            return False
    return True


# =============================================
# Проверка на первообразный корень (ТОЧНЫЙ АЛГОРИТМ)
# =============================================
def is_primitive_root(g, p):
    if not is_prime(p):
        return False
    if g <= 1 or g >= p:
        return False

    # Разложение (p-1) на простые множители
    phi = p - 1
    factors = []
    temp = phi
    i = 2
    while i * i <= temp:
        if temp % i == 0:
            factors.append(i)
            while temp % i == 0:
                temp //= i
        i += 1
    if temp > 1:
        factors.append(temp)

    # Проверка условия
    for q in factors:
        if pow(g, phi // q, p) == 1:
            return False
    return True


# =============================================
# Основная функция
# =============================================
def run():
    out.delete("1.0", tk.END)

    try:
        p = int(entry_p.get().strip())
        g = int(entry_g.get().strip())
        a = int(entry_a.get().strip())
        b = int(entry_b.get().strip())
    except ValueError:
        messagebox.showerror("Ошибка", "Введите корректные целые числа!")
        return

    if not is_prime(p):
        messagebox.showerror("Ошибка", f"Число p = {p} не является простым!")
        return

    if not (1 < g < p):
        messagebox.showerror("Ошибка", f"g должно быть 1 < g < {p}")
        return

    if not is_primitive_root(g, p):
        # Теперь подсказка — просто совет, а не список
        messagebox.showerror("Ошибка",
                             f"Число g = {g} не является первообразным корнем по модулю {p}.\n\n"
                             "Подсказка: первообразные корни часто встречаются среди чисел 2, 3, 5, 6, 7, 8.\n"
                             "Попробуйте подобрать другое значение g.")
        return

    if a <= 0 or b <= 0:
        messagebox.showerror("Ошибка", "Секреты a и b должны быть положительными числами!")
        return

    # Вычисления
    A = pow(g, a, p)
    B = pow(g, b, p)
    K_alice = pow(B, a, p)
    K_bob = pow(A, b, p)

    # Вывод
    out.insert(tk.END, "=" * 60 + "\n")
    out.insert(tk.END, "ПРОТОКОЛ ДИФФИ-ХЕЛЛМАНА\n")
    out.insert(tk.END, "=" * 60 + "\n\n")

    out.insert(tk.END, "--- Исходные данные ---\n")
    out.insert(tk.END, f"p = {p}\n")
    out.insert(tk.END, f"g = {g}\n")
    out.insert(tk.END, f"a = {a}\n")
    out.insert(tk.END, f"b = {b}\n\n")

    out.insert(tk.END, "--- Шаг 1: Открытые ключи ---\n")
    out.insert(tk.END, f"A = {g}^{a} mod {p} = {A}\n")
    out.insert(tk.END, f"B = {g}^{b} mod {p} = {B}\n\n")

    out.insert(tk.END, "--- Шаг 2: Общий ключ ---\n")
    out.insert(tk.END, f"K = {B}^{a} mod {p} = {K_alice}\n")
    out.insert(tk.END, f"K = {A}^{b} mod {p} = {K_bob}\n\n")

    if K_alice == K_bob:
        out.insert(tk.END, f"✅ Общий секретный ключ: K = {K_alice}\n")
    else:
        out.insert(tk.END, "❌ Ошибка! Ключи не совпали.\n")

    out.see(tk.END)


# =============================================
# Очистка
# =============================================
def clear_all():
    entry_p.delete(0, tk.END)
    entry_g.delete(0, tk.END)
    entry_a.delete(0, tk.END)
    entry_b.delete(0, tk.END)
    out.delete("1.0", tk.END)


# =============================================
# Интерфейс
# =============================================
root = tk.Tk()
root.title("Diffie-Hellman — Протокол обмена ключами")
root.geometry("750x650")
root.minsize(700, 600)

tk.Label(root, text="Протокол Диффи-Хеллмана", font=("Arial", 16, "bold")).pack(pady=10)

frame_input = tk.Frame(root)
frame_input.pack(pady=10, padx=20, fill="x")

tk.Label(frame_input, text="p (простое число):", font=("Arial", 10)).grid(row=0, column=0, sticky="w", padx=5, pady=5)
entry_p = tk.Entry(frame_input, width=20)
entry_p.grid(row=0, column=1, padx=5, pady=5)

tk.Label(frame_input, text="g (первообразный корень):", font=("Arial", 10)).grid(row=1, column=0, sticky="w", padx=5,
                                                                                 pady=5)
entry_g = tk.Entry(frame_input, width=20)
entry_g.grid(row=1, column=1, padx=5, pady=5)

tk.Label(frame_input, text="a (секрет Алисы):", font=("Arial", 10)).grid(row=2, column=0, sticky="w", padx=5, pady=5)
entry_a = tk.Entry(frame_input, width=20)
entry_a.grid(row=2, column=1, padx=5, pady=5)

tk.Label(frame_input, text="b (секрет Боба):", font=("Arial", 10)).grid(row=3, column=0, sticky="w", padx=5, pady=5)
entry_b = tk.Entry(frame_input, width=20)
entry_b.grid(row=3, column=1, padx=5, pady=5)

tk.Label(frame_input, text="Пример: p=11, g=7 (первообразный корень), a=1, b=2", font=("Arial", 9), fg="gray").grid(
    row=4, column=0, columnspan=2, pady=5)

frame_buttons = tk.Frame(root)
frame_buttons.pack(pady=10)

btn_run = tk.Button(frame_buttons, text="Вычислить общий ключ", command=run, bg="#4CAF50", fg="white",
                    font=("Arial", 10, "bold"), width=20)
btn_run.pack(side="left", padx=10)

btn_clear = tk.Button(frame_buttons, text="Очистить", command=clear_all, bg="#f0f0f0", font=("Arial", 10, "bold"),
                      width=15)
btn_clear.pack(side="left", padx=10)

tk.Label(root, text="Результаты:", font=("Arial", 12, "bold")).pack(pady=5)

out = scrolledtext.ScrolledText(root, width=85, height=22, font=("Courier New", 10))
out.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)

root.mainloop()