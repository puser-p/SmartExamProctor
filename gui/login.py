import tkinter as tk
from tkinter import messagebox
from dashboard import Dashboard

# Create Window
root = tk.Tk()

# Window Title
root.title("AI Smart Exam Proctoring System")

# Window Size
root.geometry("700x500")

# Prevent Resize
root.resizable(False, False)

# Background Color
root.configure(bg="#EAF2F8")

# Heading
heading = tk.Label(
    root,
    text="AI SMART EXAM PROCTORING SYSTEM",
    font=("Arial", 22, "bold"),
    bg="#EAF2F8",
    fg="navy"
)
heading.pack(pady=30)

# Login Label
login_label = tk.Label(
    root,
    text="Admin Login",
    font=("Arial", 16),
    bg="#EAF2F8"
)
login_label.pack()

# Username
tk.Label(
    root,
    text="Username",
    font=("Arial", 12),
    bg="#EAF2F8"
).pack(pady=5)

username = tk.Entry(root, width=30)
username.pack()

# Password
tk.Label(
    root,
    text="Password",
    font=("Arial", 12),
    bg="#EAF2F8"
).pack(pady=5)

password = tk.Entry(root, show="*", width=30)
password.pack()

# Login Function
def login():
    user = username.get()
    pwd = password.get()

    if user == "admin" and pwd == "admin123":
        root.destroy()
        Dashboard()
    else:
        messagebox.showerror("Error", "Invalid Username or Password")

# Login Button
login_btn = tk.Button(
    root,
    text="Login",
    command=login,
    bg="green",
    fg="white",
    width=15
)
login_btn.pack(pady=20)

# Exit Button
exit_btn = tk.Button(
    root,
    text="Exit",
    command=root.destroy,
    bg="red",
    fg="white",
    width=15
)
exit_btn.pack()

root.mainloop()