import tkinter as tk
from tkinter import messagebox
import sqlite3
import datetime
import matplotlib.pyplot as plt

# ---------------- DATABASE ---------------- #

try:
    conn = sqlite3.connect("bmi_records.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS bmi(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        weight REAL,
        height REAL,
        bmi REAL,
        category TEXT,
        date TEXT
    )
    """)

    conn.commit()

except Exception as e:
    messagebox.showerror("Database Error", str(e))


# ---------------- FUNCTIONS ---------------- #

def calculate_bmi():
    try:
        name = name_entry.get().strip()
        weight = float(weight_entry.get())
        height = float(height_entry.get())

        if name == "":
            messagebox.showerror("Error", "Enter Name")
            return

        if weight <= 0 or height <= 0:
            messagebox.showerror("Error", "Weight and Height must be positive.")
            return

        bmi = weight / (height * height)

        if bmi < 18.5:
            category = "Underweight"
            color = "blue"

        elif bmi < 25:
            category = "Normal"
            color = "green"

        elif bmi < 30:
            category = "Overweight"
            color = "orange"

        else:
            category = "Obese"
            color = "red"

        result_label.config(
            text=f"BMI : {bmi:.2f}\nCategory : {category}",
            fg=color
        )

        save_record(name, weight, height, bmi, category)

    except ValueError:
        messagebox.showerror("Error", "Enter valid numbers.")


def save_record(name, weight, height, bmi, category):

    try:
        cursor.execute(
            """
            INSERT INTO bmi(name,weight,height,bmi,category,date)
            VALUES(?,?,?,?,?,?)
            """,
            (
                name,
                weight,
                height,
                bmi,
                category,
                str(datetime.date.today())
            )
        )

        conn.commit()

    except Exception as e:
        messagebox.showerror("Database Error", str(e))


def show_history():

    history.delete(0, tk.END)

    cursor.execute(
        """
        SELECT name,bmi,category,date
        FROM bmi
        ORDER BY id DESC
        LIMIT 10
        """
    )

    rows = cursor.fetchall()

    for row in rows:
        history.insert(
            tk.END,
            f"{row[3]} | {row[0]} | {row[1]:.2f} | {row[2]}"
        )


def show_graph():

    name = name_entry.get().strip()

    if name == "":
        messagebox.showerror("Error", "Enter Name")
        return

    cursor.execute(
        """
        SELECT date,bmi
        FROM bmi
        WHERE name=?
        """,
        (name,)
    )

    rows = cursor.fetchall()

    if len(rows) == 0:
        messagebox.showinfo("Info", "No records found.")
        return

    dates = [r[0] for r in rows]
    values = [r[1] for r in rows]

    plt.figure(figsize=(6,4))
    plt.plot(dates, values, marker="o")
    plt.title(name + "'s BMI Trend")
    plt.xlabel("Date")
    plt.ylabel("BMI")
    plt.grid(True)
    plt.xticks(rotation=30)
    plt.tight_layout()
    plt.show()


# ---------------- GUI ---------------- #

root = tk.Tk()

root.title("Advanced BMI Calculator")
root.geometry("550x700")
root.resizable(False,False)

title = tk.Label(
    root,
    text="Advanced BMI Calculator",
    font=("Arial",20,"bold")
)
title.pack(pady=20)

tk.Label(root,text="Name").pack()

name_entry = tk.Entry(root,width=30)
name_entry.pack(pady=5)

tk.Label(root,text="Weight (kg)").pack()

weight_entry = tk.Entry(root,width=30)
weight_entry.pack(pady=5)

tk.Label(root,text="Height (m)").pack()

height_entry = tk.Entry(root,width=30)
height_entry.pack(pady=5)

tk.Button(
    root,
    text="Calculate BMI",
    width=20,
    command=calculate_bmi
).pack(pady=15)

result_label = tk.Label(
    root,
    text="",
    font=("Arial",15,"bold")
)

result_label.pack()

tk.Button(
    root,
    text="Show History",
    command=show_history
).pack(pady=10)

tk.Button(
    root,
    text="Show BMI Graph",
    command=show_graph
).pack(pady=5)

history = tk.Listbox(
    root,
    width=65,
    height=10
)

history.pack(pady=20)

root.mainloop()

conn.close()