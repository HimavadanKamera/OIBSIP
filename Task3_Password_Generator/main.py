import tkinter as tk
from tkinter import messagebox
import string
import secrets
import pyperclip

root = tk.Tk()
root.title("Advanced Random Password Generator")
root.geometry("550x700")
root.resizable(False, False)

history = []

# -------------------- Functions --------------------

def check_strength(password):
    score = 0

    if len(password) >= 8:
        score += 1
    if len(password) >= 12:
        score += 1
    if any(c.isupper() for c in password):
        score += 1
    if any(c.islower() for c in password):
        score += 1
    if any(c.isdigit() for c in password):
        score += 1
    if any(c in string.punctuation for c in password):
        score += 1

    if score <= 2:
        return "Weak"
    elif score <= 4:
        return "Medium"
    else:
        return "Strong"


def copy_password():
    password = password_entry.get()

    if password:
        pyperclip.copy(password)
        messagebox.showinfo("Copied", "Password copied to clipboard!")
    else:
        messagebox.showwarning("Warning", "Generate a password first.")


def update_history(password):
    history.insert(0, password)

    if len(history) > 5:
        history.pop()

    history_box.delete(0, tk.END)

    for item in history:
        history_box.insert(tk.END, item)


def generate_password():
    try:
        length = int(length_entry.get())

        if length < 8:
            messagebox.showerror("Error", "Password length must be at least 8.")
            return

        pools = []

        upper = string.ascii_uppercase
        lower = string.ascii_lowercase
        digits = string.digits
        symbols = string.punctuation

        if exclude_var.get():
            remove = "0O1l"
            upper = ''.join(c for c in upper if c not in remove)
            lower = ''.join(c for c in lower if c not in remove)
            digits = ''.join(c for c in digits if c not in remove)

        if upper_var.get():
            pools.append(upper)

        if lower_var.get():
            pools.append(lower)

        if number_var.get():
            pools.append(digits)

        if symbol_var.get():
            pools.append(symbols)

        if len(pools) < 2:
            messagebox.showerror(
                "Error",
                "Select at least TWO character types."
            )
            return

        password = []

        # Ensure one character from each selected category
        for pool in pools:
            password.append(secrets.choice(pool))

        all_characters = "".join(pools)

        while len(password) < length:
            password.append(secrets.choice(all_characters))

        secrets.SystemRandom().shuffle(password)

        password = "".join(password)

        password_entry.delete(0, tk.END)
        password_entry.insert(0, password)

        strength_label.config(
            text="Strength : " + check_strength(password)
        )

        update_history(password)

    except ValueError:
        messagebox.showerror(
            "Error",
            "Please enter a valid number."
        )

# -------------------- GUI --------------------

title = tk.Label(
    root,
    text="Advanced Random Password Generator",
    font=("Arial", 18, "bold")
)
title.pack(pady=15)

tk.Label(root, text="Password Length").pack()

length_entry = tk.Entry(root, width=10)
length_entry.pack(pady=5)

upper_var = tk.BooleanVar()
lower_var = tk.BooleanVar()
number_var = tk.BooleanVar()
symbol_var = tk.BooleanVar()
exclude_var = tk.BooleanVar()

tk.Checkbutton(
    root,
    text="Uppercase (A-Z)",
    variable=upper_var
).pack(anchor="w", padx=120)

tk.Checkbutton(
    root,
    text="Lowercase (a-z)",
    variable=lower_var
).pack(anchor="w", padx=120)

tk.Checkbutton(
    root,
    text="Numbers (0-9)",
    variable=number_var
).pack(anchor="w", padx=120)

tk.Checkbutton(
    root,
    text="Symbols (!@#$)",
    variable=symbol_var
).pack(anchor="w", padx=120)

tk.Checkbutton(
    root,
    text="Exclude Ambiguous Characters (0 O l 1)",
    variable=exclude_var
).pack(anchor="w", padx=120, pady=10)

generate_btn = tk.Button(
    root,
    text="Generate Password",
    width=20,
    command=generate_password
)
generate_btn.pack(pady=10)

tk.Label(root, text="Generated Password").pack()

password_entry = tk.Entry(root, width=45)
password_entry.pack()

copy_btn = tk.Button(
    root,
    text="Copy to Clipboard",
    command=copy_password
)
copy_btn.pack(pady=10)

strength_label = tk.Label(
    root,
    text="Strength : "
)
strength_label.pack()

tk.Label(
    root,
    text="Last 5 Generated Passwords"
).pack(pady=(20, 5))

history_box = tk.Listbox(root, width=45, height=5)
history_box.pack()

root.mainloop()