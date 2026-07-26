import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

from detection.face_capture import FaceCapture
from database.db_manager import DatabaseManager

db = DatabaseManager()

db.create_table()

print("Students")
print(db.get_students())

print("\nExam Results")
print(db.get_exam_results())

db.close()
class StudentManagement:

    def __init__(self):

        
        self.root = tk.Toplevel()

        self.root.title("Student Management System")

        self.root.geometry("1200x700")

        self.root.configure(bg="#F4F6F7")

        self.root.resizable(False, False)
        self.db = DatabaseManager()
        self.db.create_table()
        self.face_capture = FaceCapture()

        self.create_widgets()
        self.fetch_students()

       
        
    
    def create_widgets(self):

        header = tk.Label(

            self.root,

            text="STUDENT MANAGEMENT SYSTEM",

            font=("Arial", 24, "bold"),

            bg="#154360",

            fg="white",

            pady=15

        )

        header.pack(fill="x")

        main_frame = tk.Frame(

            self.root,

            bg="#F4F6F7"

        )

        main_frame.pack(

            fill="both",

            expand=True,

            padx=20,

            pady=20

        )
        # Left Frame
        self.left_frame = tk.LabelFrame(
            main_frame,
            text="Student Details",
            font=("Arial", 12, "bold"),
            bg="#F4F6F7",
            padx=15,
            pady=15,
            width=400
        )

        self.left_frame.pack(
            side="left",
            fill="y",
            padx=(0, 10)
        )
        tk.Label(
            self.left_frame,
            text="Student Name",
            font=("Arial", 12),
            bg="#F4F6F7"
        ).pack(anchor="w", pady=10)
        # Prevent the left frame from shrinking
        self.left_frame.pack_propagate(False)


        # ==========================
        # Student Name
        # ==========================

        tk.Label(
            self.left_frame,
            text="Student Name",
            font=("Arial", 11),
            bg="#F4F6F7"
        ).grid(row=0, column=0, sticky="w", pady=8)

        self.name_var = tk.StringVar()

        tk.Entry(
            self.left_frame,
            textvariable=self.name_var,
            font=("Arial",11),
            width=28
        ).grid(row=0, column=1, pady=8)

        tk.Label(
            self.left_frame,
            text="Roll Number",
            font=("Arial",11),
            bg="#F4F6F7"
        ).grid(row=1,column=0,sticky="w",pady=8)

        self.roll_var = tk.StringVar()

        tk.Entry(
            self.left_frame,
            textvariable=self.roll_var,
            font=("Arial",11),
            width=28
        ).grid(row=1,column=1,pady=8)
        tk.Label(
            self.left_frame,
            text="Department",
            font=("Arial",11),
            bg="#F4F6F7"
        ).grid(row=2,column=0,sticky="w",pady=8)

        self.dept_var = tk.StringVar()

        tk.Entry(
            self.left_frame,
            textvariable=self.dept_var,
            font=("Arial",11),
            width=28
        ).grid(row=2,column=1,pady=8)
        tk.Label(
            self.left_frame,
            text="Semester",
            font=("Arial",11),
            bg="#F4F6F7"
        ).grid(row=3,column=0,sticky="w",pady=8)

        self.sem_var = tk.StringVar()

        semester = ttk.Combobox(
            self.left_frame,
            textvariable=self.sem_var,
            values=[
                "Semester 1",
                "Semester 2",
                "Semester 3",
                "Semester 4",
                "Semester 5",
                "Semester 6",
                "Semester 7",
                "Semester 8"
            ],
            state="readonly",
            width=26
        )

        semester.grid(row=3,column=1,pady=8)
        semester.current(0)
        tk.Label(
            self.left_frame,
            text="Email",
            font=("Arial",11),
            bg="#F4F6F7"
        ).grid(row=4,column=0,sticky="w",pady=8)

        self.email_var = tk.StringVar()

        tk.Entry(
            self.left_frame,
            textvariable=self.email_var,
            font=("Arial",11),
            width=28
        ).grid(row=4,column=1,pady=8)
        tk.Label(
            self.left_frame,
            text="Phone Number",
            font=("Arial",11),
            bg="#F4F6F7"
        ).grid(row=5,column=0,sticky="w",pady=8)

        self.phone_var = tk.StringVar()

        tk.Entry(
            self.left_frame,
            textvariable=self.phone_var,
            font=("Arial",11),
            width=28
        ).grid(row=5,column=1,pady=8)
        tk.Label(
            self.left_frame,
            text="Gender",
            font=("Arial",11),
            bg="#F4F6F7"
        ).grid(row=6,column=0,sticky="w",pady=8)

        self.gender_var = tk.StringVar(value="Male")

        tk.Radiobutton(
            self.left_frame,
            text="Male",
            variable=self.gender_var,
            value="Male",
            bg="#F4F6F7"
        ).grid(row=6,column=1,sticky="w")

        tk.Radiobutton(
            self.left_frame,
            text="Female",
            variable=self.gender_var,
            value="Female",
            bg="#F4F6F7"
        ).grid(row=6,column=1,padx=90,sticky="w")
        # ==========================
        # Buttons Frame
        # ==========================

        button_frame = tk.Frame(self.left_frame, bg="#F4F6F7")
        button_frame.grid(row=7, column=0, columnspan=2, pady=20)

        tk.Button(
            button_frame,
            text="Save",
            width=12,
            bg="#27AE60",
            fg="white",
            font=("Arial", 10, "bold"),
            command=self.save_student
        ).grid(row=0, column=0, padx=5, pady=5)

        tk.Button(
            button_frame,
            text="Update",
            width=12,
            bg="#2980B9",
            fg="white",
            font=("Arial", 10, "bold"),
            command=self.update_student
        ).grid(row=0, column=1, padx=5, pady=5)

        tk.Button(
            button_frame,
            text="Delete",
            width=12,
            bg="#C0392B",
            fg="white",
            font=("Arial", 10, "bold"),
            command=self.delete_student
        ).grid(row=1, column=0, padx=5, pady=5)

        tk.Button(
            button_frame,
            text="Clear",
            width=12,
            bg="#7F8C8D",
            fg="white",
            font=("Arial", 10, "bold"),
            command=self.clear_fields
        ).grid(row=1, column=1, padx=5, pady=5)


        tk.Button(
            button_frame,
            text="Capture Face",
            width=27,
            bg="#8E44AD",
            fg="white",
            font=("Arial",10,"bold"),
            command=self.capture_face
        ).grid(
            row=2,
            column=0,
            columnspan=2,
            pady=10
        )
        # Right Frame
        self.right_frame = tk.LabelFrame(
            main_frame,
            text="Student Records",
            font=("Arial", 12, "bold"),
            bg="#F4F6F7",
            padx=15,
            pady=15
        )

        self.right_frame.pack(
            side="right",
            fill="both",
            expand=True
        )
        # ==========================
        # Student Records Table
        # ==========================

        columns = (
            "ID",
            "Name",
            "Roll",
            "Department",
            "Semester",
            "Email",
            "Phone",
            "Gender"
        )
        # ==========================
        # Search Frame
        # ==========================

        search_frame = tk.Frame(self.right_frame, bg="#F4F6F7")
        search_frame.pack(fill="x", pady=10)

        tk.Label(
            search_frame,
            text="Search Roll No:",
            bg="#F4F6F7",
            font=("Arial", 11, "bold")
        ).pack(side="left", padx=5)

        self.search_var = tk.StringVar()

        tk.Entry(
            search_frame,
            textvariable=self.search_var,
            width=20,
            font=("Arial", 11)
        ).pack(side="left", padx=5)

        tk.Button(
            search_frame,
            text="Search",
            bg="#3498DB",
            fg="white",
            command=self.search_student
        ).pack(side="left", padx=5)

        tk.Button(
            search_frame,
            text="Show All",
            bg="#27AE60",
            fg="white",
            command=self.fetch_students
        ).pack(side="left", padx=5)
        self.student_table = ttk.Treeview(
            self.right_frame,
            columns=columns,
            show="headings"
        )

        for col in columns:
            self.student_table.heading(col, text=col)
            self.student_table.column(col, width=120, anchor="center")

        scroll_y = ttk.Scrollbar(
            self.right_frame,
            orient="vertical",
            command=self.student_table.yview
        )

        self.student_table.configure(
            yscrollcommand=scroll_y.set
        )

        scroll_y.pack(side="right", fill="y")
        self.student_table.pack(fill="both", expand=True)
        self.student_table.bind(
            "<<TreeviewSelect>>",
            self.get_cursor
        )
    def get_cursor(self, event):

        selected = self.student_table.focus()

        values = self.student_table.item(selected, "values")

        if not values:
            return

        self.name_var.set(values[1])
        self.roll_var.set(values[2])
        self.dept_var.set(values[3])
        self.sem_var.set(values[4])
        self.email_var.set(values[5])
        self.phone_var.set(values[6])
        self.gender_var.set(values[7])
    def save_student(self):

        name = self.name_var.get().strip()
        roll = self.roll_var.get().strip()
        department = self.dept_var.get().strip()
        semester = self.sem_var.get().strip()
        email = self.email_var.get().strip()
        phone = self.phone_var.get().strip()
        gender = self.gender_var.get().strip()

        # Required Fields Validation
        if (
            name == "" or
            roll == "" or
            department == "" or
            email == "" or
            phone == ""
        ):
            messagebox.showerror(
                "Validation Error",
                "Please fill all required fields."
            )
            return

        # Phone Number Validation
        if not phone.isdigit() or len(phone) != 10:
            messagebox.showerror(
                "Validation Error",
                "Phone number must contain exactly 10 digits."
            )
            return

        # Email Validation
        if "@" not in email or "." not in email:
            messagebox.showerror(
                "Validation Error",
                "Please enter a valid email address."
            )
            return

        try:
            self.db.insert_student(
                name,
                roll,
                department,
                semester,
                email,
                phone,
                gender
            )

            messagebox.showinfo(
                "Success",
                "Student Saved Successfully!"
            )
            self.fetch_students()
            self.clear_fields()

        except Exception as e:
            messagebox.showerror(
                "Database Error",
                str(e)
            )
    def clear_fields(self):

        self.name_var.set("")
        self.roll_var.set("")
        self.dept_var.set("")
        self.sem_var.set("Semester 1")
        self.email_var.set("")
        self.phone_var.set("")
        self.gender_var.set("Male")
    def fetch_students(self):

        self.student_table.delete(*self.student_table.get_children())

        rows = self.db.get_students()

        for row in rows:
            self.student_table.insert("", tk.END, values=row)
    def update_student(self):
        print("Roll:", repr(self.roll_var.get()))

        if self.roll_var.get().strip() == "":
            messagebox.showerror(
                "Error",
                "Select a student first."
            )
            return

        self.db.update_student(

            self.name_var.get(),

            self.roll_var.get(),

            self.dept_var.get(),

            self.sem_var.get(),

            self.email_var.get(),

            self.phone_var.get(),

            self.gender_var.get()

        )

        messagebox.showinfo(
            "Success",
            "Student Updated Successfully!"
        )

        self.fetch_students()

        self.clear_fields()
    def delete_student(self):

        if self.roll_var.get().strip() == "":
            messagebox.showerror(
                "Error",
                "Please select a student."
            )
            return

        answer = messagebox.askyesno(

            "Confirm",

            "Delete this student?"

        )

        if answer:

            self.db.delete_student(

                self.roll_var.get()

            )

            messagebox.showinfo(

                "Success",

                "Student Deleted Successfully."

            )

            self.fetch_students()

            self.clear_fields()
    def search_student(self):

        roll = self.search_var.get().strip()

        if roll == "":
            messagebox.showwarning(
                "Warning",
                "Enter a Roll Number to search."
            )
            return

        rows = self.db.search_student(roll)

        self.student_table.delete(*self.student_table.get_children())

        if not rows:
            messagebox.showinfo(
                "Search",
                "No student found."
            )
            return

        for row in rows:
            self.student_table.insert("", tk.END, values=row)
    def capture_face(self):
        print("Capture Face button clicked!")

        roll = self.roll_var.get().strip()

        if roll == "":

            messagebox.showerror(
                "Error",
                "Please select or enter a student first."
            )

            return

        images = self.face_capture.capture(roll)

        messagebox.showinfo(
            "Completed",
            f"{images} images captured successfully."
        )
if __name__ == "__main__":

    StudentManagement()
