import tkinter as tk
from tkinter import ttk, messagebox
import random
import math


class DiffieHellmanApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Алгоритм Диффи-Хеллмана — Обмен ключами")
        self.root.geometry("750x600")
        self.root.configure(bg="#f0f0f0")

        # Стили
        style = ttk.Style()
        style.configure("TLabel", background="#f0f0f0", font=("Arial", 10))
        style.configure("TButton", font=("Arial", 10))

        # Заголовок
        tk.Label(root, text="Протокол Диффи-Хеллмана", font=("Arial", 16, "bold"), bg="#f0f0f0", fg="#2c3e50").pack(
            pady=10)

        # Основной фрейм
        main_frame = tk.Frame(root, bg="#f0f0f0")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        # Левая часть — параметры протокола
        left_frame = tk.LabelFrame(main_frame, text="Публичные параметры", font=("Arial", 12, "bold"), bg="#f0f0f0",
                                   padx=10, pady=10)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)

        tk.Label(left_frame, text="p (большое простое число):", bg="#f0f0f0").grid(row=0, column=0, sticky="w", pady=5)
        self.p_entry = tk.Entry(left_frame, width=20, font=("Arial", 10))
        self.p_entry.grid(row=0, column=1, pady=5)
        self.p_entry.insert(0, "23")

        # Поле для g с кнопкой проверки
        tk.Label(left_frame, text="g (первообразный корень):", bg="#f0f0f0").grid(row=1, column=0, sticky="w", pady=5)
        g_frame = tk.Frame(left_frame, bg="#f0f0f0")
        g_frame.grid(row=1, column=1, pady=5, sticky="w")

        self.g_entry = tk.Entry(g_frame, width=15, font=("Arial", 10))
        self.g_entry.pack(side=tk.LEFT)
        self.g_entry.insert(0, "5")

        # Кнопка проверки g
        tk.Button(g_frame, text="Проверить g", command=self.show_primitive_roots,
                  bg="#9b59b6", fg="white", font=("Arial", 8, "bold"), width=10).pack(side=tk.LEFT, padx=5)

        # Кнопка генерации простого числа
        tk.Button(left_frame, text="Сгенерировать простое p", command=self.generate_prime, bg="#3498db", fg="white",
                  font=("Arial", 9)).grid(row=2, column=0, columnspan=2, pady=10)

        # Правая часть — Алиса
        alice_frame = tk.LabelFrame(main_frame, text="Алиса (Сторона A)", font=("Arial", 12, "bold"), bg="#e8f8f5",
                                    padx=10, pady=10)
        alice_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)

        tk.Label(alice_frame, text="Секретный ключ a:", bg="#e8f8f5").grid(row=0, column=0, sticky="w", pady=5)
        self.a_entry = tk.Entry(alice_frame, width=20, font=("Arial", 10))
        self.a_entry.grid(row=0, column=1, pady=5)
        self.a_entry.insert(0, "6")

        tk.Button(alice_frame, text="Случайный a", command=lambda: self.random_key(self.a_entry), bg="#2ecc71",
                  fg="white", font=("Arial", 9)).grid(row=0, column=2, padx=5)

        self.A_value = tk.StringVar(value="—")
        tk.Label(alice_frame, text="Публичный ключ A = g^a mod p:", bg="#e8f8f5").grid(row=1, column=0, columnspan=2,
                                                                                       sticky="w", pady=5)
        tk.Label(alice_frame, textvariable=self.A_value, font=("Arial", 10, "bold"), fg="#e74c3c", bg="#e8f8f5").grid(
            row=1, column=2)

        # Серверная часть — Боб
        bob_frame = tk.LabelFrame(main_frame, text="Боб (Сторона B)", font=("Arial", 12, "bold"), bg="#ebf5fb", padx=10,
                                  pady=10)
        bob_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)

        tk.Label(bob_frame, text="Секретный ключ b:", bg="#ebf5fb").grid(row=0, column=0, sticky="w", pady=5)
        self.b_entry = tk.Entry(bob_frame, width=20, font=("Arial", 10))
        self.b_entry.grid(row=0, column=1, pady=5)
        self.b_entry.insert(0, "9")

        tk.Button(bob_frame, text="Случайный b", command=lambda: self.random_key(self.b_entry), bg="#2ecc71",
                  fg="white", font=("Arial", 9)).grid(row=0, column=2, padx=5)

        self.B_value = tk.StringVar(value="—")
        tk.Label(bob_frame, text="Публичный ключ B = g^b mod p:", bg="#ebf5fb").grid(row=1, column=0, columnspan=2,
                                                                                     sticky="w", pady=5)
        tk.Label(bob_frame, textvariable=self.B_value, font=("Arial", 10, "bold"), fg="#e74c3c", bg="#ebf5fb").grid(
            row=1, column=2)

        # Общий секретный ключ
        common_frame = tk.LabelFrame(root, text="Результат", font=("Arial", 12, "bold"), bg="#f9e79f", padx=10, pady=10)
        common_frame.pack(fill=tk.X, padx=20, pady=10)

        self.s_value = tk.StringVar(value="—")
        tk.Label(common_frame, textvariable=self.s_value, font=("Arial", 14, "bold"), fg="#e74c3c", bg="#f9e79f").pack(
            pady=10)

        # Нижняя панель с кнопками
        button_frame = tk.Frame(root, bg="#f0f0f0")
        button_frame.pack(pady=10)

        tk.Button(button_frame, text="Рассчитать ключи", command=self.calculate_keys, bg="#3498db", fg="white",
                  font=("Arial", 11, "bold"), width=20).pack(side=tk.LEFT, padx=10)
        tk.Button(button_frame, text="Сбросить всё", command=self.reset, bg="#e74c3c", fg="white",
                  font=("Arial", 11, "bold"), width=15).pack(side=tk.LEFT, padx=10)

        # Информационное поле
        self.info_text = tk.Text(root, height=8, font=("Courier", 9), bg="#fef9e7", fg="#2c3e50")
        self.info_text.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

    # ========== ФУНКЦИИ ПРОВЕРКИ ==========

    def is_prime(self, n):
        """Проверка на простоту"""
        if n < 2: return False
        if n == 2: return True
        if n % 2 == 0: return False
        for i in range(3, int(math.sqrt(n)) + 1, 2):
            if n % i == 0:
                return False
        return True

    def is_primitive_root(self, g, p):
        """Проверка, является ли g первообразным корнем по модулю p"""
        if not self.is_prime(p):
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

        # Проверка условия: g^((p-1)/q) mod p != 1 для всех q
        for q in factors:
            if pow(g, phi // q, p) == 1:
                return False
        return True

    def get_primitive_roots(self, p):
        """Возвращает список всех первообразных корней по модулю p"""
        if not self.is_prime(p):
            return []
        roots = []
        for g in range(2, p):
            if self.is_primitive_root(g, p):
                roots.append(g)
        return roots

    # ========== НОВАЯ ФУНКЦИЯ: ОКНО С ПЕРВООБРАЗНЫМИ КОРНЯМИ ==========

    def show_primitive_roots(self):
        """Открывает окно со всеми первообразными корнями для текущего p"""
        try:
            p = int(self.p_entry.get().strip())
        except ValueError:
            messagebox.showerror("Ошибка", "Введите корректное число для p!")
            return

        if not self.is_prime(p):
            messagebox.showerror("Ошибка", f"Число p = {p} не является простым!")
            return

        roots = self.get_primitive_roots(p)
        if not roots:
            messagebox.showinfo("Результат", f"Для p = {p} нет первообразных корней (невозможно).")
            return

        # Создаём новое окно
        win = tk.Toplevel(self.root)
        win.title(f"Первообразные корни для p = {p}")
        win.geometry("400x300")
        win.configure(bg="#f0f0f0")

        tk.Label(win, text=f"Первообразные корни по модулю {p}:",
                 font=("Arial", 12, "bold"), bg="#f0f0f0").pack(pady=10)

        # Фрейм с квадратиками
        frame = tk.Frame(win, bg="#f0f0f0")
        frame.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)

        # Создаём квадратики
        row = 0
        col = 0
        for g in roots:
            btn = tk.Button(frame, text=str(g), width=5, height=2,
                            font=("Arial", 10, "bold"),
                            bg="#2ecc71", fg="white",
                            command=lambda val=g: self.select_g(val, win))
            btn.grid(row=row, column=col, padx=5, pady=5)
            col += 1
            if col >= 6:  # 6 квадратиков в строке
                col = 0
                row += 1

        tk.Label(win, text="Нажмите на число, чтобы выбрать его",
                 font=("Arial", 9), fg="gray", bg="#f0f0f0").pack(pady=10)

        # Кнопка закрытия
        tk.Button(win, text="Закрыть", command=win.destroy,
                  bg="#e74c3c", fg="white", font=("Arial", 10, "bold")).pack(pady=10)

    def select_g(self, g, window):
        """Выбирает g и закрывает окно"""
        self.g_entry.delete(0, tk.END)
        self.g_entry.insert(0, str(g))
        self.log(f"Выбран g = {g} (первообразный корень по модулю p = {self.p_entry.get()})")
        window.destroy()

    # ========== ОСТАЛЬНЫЕ ФУНКЦИИ (БЕЗ ИЗМЕНЕНИЙ) ==========

    def random_key(self, entry):
        """Генерирует случайный секретный ключ от 2 до 20"""
        entry.delete(0, tk.END)
        entry.insert(0, str(random.randint(2, 20)))

    def generate_prime(self):
        """Генерирует небольшое простое число (для демонстрации)"""
        for candidate in range(random.randint(10, 100), 1000):
            if self.is_prime(candidate):
                self.p_entry.delete(0, tk.END)
                self.p_entry.insert(0, str(candidate))
                self.log(f"Сгенерировано простое число p = {candidate}")
                return
        self.log("Не удалось сгенерировать простое число.")

    def log(self, message):
        """Добавляет сообщение в лог"""
        self.info_text.insert(tk.END, f"{message}\n")
        self.info_text.see(tk.END)

    def mod_pow(self, base, exp, mod):
        """Быстрое возведение в степень по модулю"""
        return pow(base, exp, mod)

    def calculate_keys(self):
        """Основной расчёт протокола Диффи-Хеллмана"""
        try:
            # Чтение параметров
            p = int(self.p_entry.get())
            g = int(self.g_entry.get())
            a = int(self.a_entry.get())
            b = int(self.b_entry.get())

            # Проверка p
            if not self.is_prime(p):
                messagebox.showerror("Ошибка", f"p = {p} не является простым числом!")
                return

            # Проверка g
            if not (1 < g < p):
                messagebox.showerror("Ошибка", f"g должно быть 1 < g < {p}")
                return

            # Проверка, что g — первообразный корень
            if not self.is_primitive_root(g, p):
                roots = self.get_primitive_roots(p)
                messagebox.showerror(
                    "Ошибка",
                    f"Число g = {g} не является первообразным корнем по модулю {p}.\n\n"
                    f"Подходящие значения: {roots}\n"
                    f"Используйте кнопку 'Проверить g' для выбора правильного значения."
                )
                return

            # Защита от дурака для a и b (добавлено по твоей просьбе)
            if a <= 0 or b <= 0:
                messagebox.showerror("Ошибка", "Секреты a и b должны быть положительными числами!")
                return

            if a >= p or b >= p:
                messagebox.showerror("Ошибка", "Секреты a и b должны быть меньше p!")
                return

            # Очистка лога
            self.info_text.delete(1.0, tk.END)
            self.log("=" * 50)
            self.log("Протокол Диффи-Хеллмана")
            self.log("=" * 50)
            self.log(f"Публичные параметры: p = {p}, g = {g}")
            self.log(f"Секретный ключ Алисы a = {a}")
            self.log(f"Секретный ключ Боба b = {b}")

            # Вычисление публичных ключей
            A = self.mod_pow(g, a, p)
            B = self.mod_pow(g, b, p)

            self.A_value.set(str(A))
            self.B_value.set(str(B))

            self.log(f"\nАлиса вычисляет A = g^a mod p = {g}^{a} mod {p} = {A}")
            self.log(f"Боб вычисляет B = g^b mod p = {g}^{b} mod {p} = {B}")
            self.log(f"Алиса отправляет A = {A} Бобу")
            self.log(f"Боб отправляет B = {B} Алисе")

            # Вычисление общего секрета
            s_alice = self.mod_pow(B, a, p)
            s_bob = self.mod_pow(A, b, p)

            self.log(f"\nАлиса вычисляет s = B^a mod p = {B}^{a} mod {p} = {s_alice}")
            self.log(f"Боб вычисляет s = A^b mod p = {A}^{b} mod {p} = {s_bob}")

            if s_alice == s_bob:
                self.s_value.set(f"Общий секретный ключ: {s_alice}")
                self.log(f"\n✅ Успех! Общий секрет: {s_alice}")
                self.log("Теперь Алиса и Боб могут использовать этот ключ для симметричного шифрования.")
            else:
                self.s_value.set("Ошибка: ключи не совпадают!")
                self.log("\n❌ Ошибка: ключи не совпадают!")

        except ValueError:
            messagebox.showerror("Ошибка", "Введите корректные числа во все поля!")

    def reset(self):
        """Сбрасывает все поля"""
        self.p_entry.delete(0, tk.END)
        self.p_entry.insert(0, "23")
        self.g_entry.delete(0, tk.END)
        self.g_entry.insert(0, "5")
        self.a_entry.delete(0, tk.END)
        self.a_entry.insert(0, "6")
        self.b_entry.delete(0, tk.END)
        self.b_entry.insert(0, "9")
        self.A_value.set("—")
        self.B_value.set("—")
        self.s_value.set("—")
        self.info_text.delete(1.0, tk.END)
        self.log("Сброс выполнен.")


if __name__ == "__main__":
    root = tk.Tk()
    app = DiffieHellmanApp(root)
    root.mainloop()