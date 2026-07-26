import tkinter as tk
from tkinter import messagebox
from gui.dashboard import Dashboard


# ---------------- LOGIN FUNCTION ---------------- #

def login():

    user = username.get().strip()

    pwd = password.get().strip()

    if user == "admin" and pwd == "admin123":

        root.withdraw()

        Dashboard(root)

    else:

        messagebox.showerror(

            "Login Failed",

            "Invalid Username or Password."

        )


# ---------------- CLEAR FUNCTION ---------------- #

def clear():

    username.delete(0, tk.END)

    password.delete(0, tk.END)

    username.focus()
def exit_dashboard(self):
    self.root.destroy()

# ---------------- WINDOW ---------------- #

root = tk.Tk()

root.title("Smart Exam Proctoring System")

root.geometry("850x550")

root.configure(bg="#ECF0F1")

root.resizable(False, False)

try:

    root.iconbitmap("icons/app.ico")

except:

    pass


# ---------------- HEADER ---------------- #

header = tk.Frame(

    root,

    bg="#2C3E50",

    height=90

)

header.pack(fill="x")

header.pack_propagate(False)

tk.Label(

    header,

    text="SMART EXAM PROCTORING SYSTEM",

    font=("Arial", 24, "bold"),

    bg="#2C3E50",

    fg="white"

).pack(pady=(15, 0))

tk.Label(

    header,

    text="AI Based Online Examination Monitoring",

    font=("Arial", 12),

    bg="#2C3E50",

    fg="white"

).pack()


# ---------------- LOGIN CARD ---------------- #

card = tk.Frame(

    root,

    bg="white",

    relief="raised",

    bd=2

)

card.pack(

    pady=40,

    ipadx=25,

    ipady=25

)

tk.Label(

    card,

    text="Administrator Login",

    font=("Arial", 18, "bold"),

    bg="white",

    fg="#2C3E50"

).grid(

    row=0,

    column=0,

    columnspan=2,

    pady=(10, 25)

)


tk.Label(

    card,

    text="Username",

    font=("Arial", 12),

    bg="white"

).grid(

    row=1,

    column=0,

    sticky="w",

    pady=10

)

username = tk.Entry(

    card,

    font=("Arial", 12),

    width=28

)

username.grid(

    row=1,

    column=1,

    padx=15

)


tk.Label(

    card,

    text="Password",

    font=("Arial", 12),

    bg="white"

).grid(

    row=2,

    column=0,

    sticky="w",

    pady=10

)

password = tk.Entry(

    card,

    show="*",

    font=("Arial", 12),

    width=28

)

password.grid(

    row=2,

    column=1,

    padx=15

)


# ---------------- BUTTONS ---------------- #

button_frame = tk.Frame(

    card,

    bg="white"

)

button_frame.grid(

    row=3,

    column=0,

    columnspan=2,

    pady=25

)


tk.Button(

    button_frame,

    text="Login",

    width=15,

    bg="#2ECC71",

    fg="white",

    font=("Arial", 11, "bold"),

    command=login

).grid(

    row=0,

    column=0,

    padx=8

)


tk.Button(

    button_frame,

    text="Clear",

    width=15,

    bg="#F39C12",

    fg="white",

    font=("Arial", 11, "bold"),

    command=clear

).grid(

    row=0,

    column=1,

    padx=8

)


tk.Button(

    button_frame,

    text="Exit",

    width=15,

    bg="#E74C3C",

    fg="white",

    font=("Arial", 11, "bold"),

    command=root.destroy

).grid(

    row=0,

    column=2,

    padx=8

)


# ---------------- FOOTER ---------------- #

footer = tk.Label(

    root,

    text="Version 1.0     |     Developed by Pragati Singhal",

    font=("Arial", 10),

    bg="#ECF0F1",

    fg="gray"

)

footer.pack(

    side="bottom",

    pady=12

)


username.focus()

root.mainloop()