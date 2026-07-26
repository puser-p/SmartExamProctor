import tkinter as tk
from tkinter import messagebox
import sqlite3


class RegisterStudent:

    def __init__(self):

        self.root = tk.Toplevel()

        self.root.title("Student Registration")

        self.root.geometry("700x600")

        self.root.configure(bg="#EAF2F8")

        self.create_widgets()

    def create_widgets(self):

        title = tk.Label(

            self.root,

            text="STUDENT REGISTRATION",

            font=("Arial",20,"bold"),

            bg="#1F618D",

            fg="white",

            pady=10

        )

        title.pack(fill="x")

        form = tk.Frame(self.root,bg="#EAF2F8")

        form.pack(pady=20)

        labels = [

            "Student Name",

            "Roll Number",

            "Department",

            "Semester",

            "Email",

            "Phone Number"

        ]

        self.entries=[]

        for label in labels:

            tk.Label(

                form,

                text=label,

                font=("Arial",12),

                bg="#EAF2F8"

            ).pack(anchor="w")

            entry=tk.Entry(form,width=40)

            entry.pack(pady=5)

            self.entries.append(entry)

        tk.Label(

            form,

            text="Gender",

            font=("Arial",12),

            bg="#EAF2F8"

        ).pack(anchor="w")

        self.gender=tk.StringVar()

        tk.Radiobutton(

            form,

            text="Male",

            variable=self.gender,

            value="Male",

            bg="#EAF2F8"

        ).pack(anchor="w")

        tk.Radiobutton(

            form,

            text="Female",

            variable=self.gender,

            value="Female",

            bg="#EAF2F8"

        ).pack(anchor="w")

        tk.Button(

            self.root,

            text="Save Student",

            bg="green",

            fg="white",

            width=20,

            command=self.save_student

        ).pack(pady=15)

    def save_student(self):

        name=self.entries[0].get()

        roll=self.entries[1].get()

        dept=self.entries[2].get()

        sem=self.entries[3].get()

        email=self.entries[4].get()

        phone=self.entries[5].get()

        gender=self.gender.get()

        if name=="" or roll=="":

            messagebox.showerror(

                "Error",

                "Name and Roll Number are required."

            )

            return

        conn=sqlite3.connect("database/exam.db")

        cursor=conn.cursor()

        try:

            cursor.execute("""

            INSERT INTO students(

            name,

            roll,

            department,

            semester,

            email,

            phone,

            gender

            )

            VALUES(?,?,?,?,?,?,?)

            """,

            (

                name,

                roll,

                dept,

                sem,

                email,

                phone,

                gender

            ))

            conn.commit()

            messagebox.showinfo(

                "Success",

                "Student Registered Successfully!"

            )

        except sqlite3.IntegrityError:

            messagebox.showerror(

                "Error",

                "Roll Number already exists."

            )

        conn.close()


if __name__=="__main__":

    RegisterStudent()

    tk.mainloop()