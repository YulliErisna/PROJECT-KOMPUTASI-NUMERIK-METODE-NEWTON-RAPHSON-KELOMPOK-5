import sympy as sp
import matplotlib.pyplot as plt
from termcolor import colored
from tabulate import tabulate

def newton_raphson(func_expr, dfunc_expr, x0, tol, max_iter):
    x = sp.symbols('x')
    f = sp.lambdify(x, func_expr)
    df = sp.lambdify(x, dfunc_expr)
    
    iter_count = 0
    error = tol + 1
    history = [(iter_count, x0, '-', '-')]
    
    while error > tol and iter_count < max_iter:
        f_x0 = f(x0)
        df_x0 = df(x0)
        
        if df_x0 == 0:
            print(colored("Turunan sama dengan nol. Iterasi dihentikan.", "red"))
            return None, history
        
        x1 = x0 - f_x0 / df_x0
        error = abs(x1 - x0)
        iter_count += 1
        x0 = x1
        history.append((iter_count, x0, f_x0, error))
    
    return x0, history

def tampilkan_tabel(history):
    headers = ["Iterasi", "x", "f(x)", "Error"]
    table = [[i[0], f"{i[1]:.6f}", f"{i[2]:.6f}" if i[2] != '-' else '-', f"{i[3]:.6f}" if i[3] != '-' else '-'] for i in history]
    print(tabulate(table, headers, tablefmt="pretty"))

def plot_function(func_expr, history):
    x_vals = [i/10 for i in range(-50, 51)]
    y_vals = [sp.lambdify(sp.symbols('x'), func_expr)(x) for x in x_vals]
    
    plt.plot(x_vals, y_vals, label="f(x)", color="blue")
    plt.scatter([h[1] for h in history], [0]*len(history), color="red", label="Iterasi", zorder=5)
    plt.axhline(0, color='black', linewidth=0.5)
    plt.axvline(0, color='black', linewidth=0.5)
    plt.title("Iterasi Newton-Raphson")
    plt.legend()
    plt.grid(True)
    plt.show()

# Bagian Input
func_input = input(colored("Masukkan fungsi f(x): ", "yellow")).replace("^", "**")
dfunc_input = input(colored("Masukkan turunan f'(x): ", "yellow")).replace("^", "**")
x0 = float(input(colored("Masukkan tebakan awal (x0): ", "yellow")))
tol = float(input(colored("Masukkan toleransi: ", "yellow")))
max_iter = int(input(colored("Masukkan jumlah iterasi maksimum: ", "yellow")))

# Menampilkan input yang diterima
print(colored("\nDiketahui: ", "cyan"))
print(f"Fungsi f(x)       : {func_input}")
print(f"Turunan f'(x)     : {dfunc_input}")
print(f"Tebakan awal (x0) : {x0}")
print(f"Toleransi         : {tol}")
print(f"Iterasi maksimum  : {max_iter}")

# Mengonversi string input menjadi ekspresi sympy
x = sp.symbols('x')
func_expr = sp.sympify(func_input)
dfunc_expr = sp.sympify(dfunc_input)

# Menjalankan Metode Newton-Raphson
root, history = newton_raphson(func_expr, dfunc_expr, x0, tol, max_iter)

# Menampilkan hasil iterasi dalam bentuk tabel
print(colored("\nHasil Iterasi: ", "cyan"))
tampilkan_tabel(history)

# Menampilkan grafik iterasi
if root is not None:
    print(colored(f"\nAkar ditemukan: {root:.6f}", "green"))
    plot_function(func_expr, history)
else:
    print(colored("Akar tidak ditemukan dalam iterasi yang diberikan.", "red"))
