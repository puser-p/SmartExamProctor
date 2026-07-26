import tkinter as tk
import sys
from tkinter import ttk
from tkinter import messagebox
from utils.report_generator import ReportGenerator
from database.db_manager import DatabaseManager

class ExamSummary:

    def __init__(
        self,
        student_name,
        roll_no,
        duration,
        violations,
        score, 
        total_questions,
        dashboard=None
    ):
        self.student_name = student_name
        self.roll_no = str(roll_no)
        self.duration = duration
        self.violations = violations
        self.dashboard = dashboard
        self.score = score
        self.total_questions = total_questions

        self.root = tk.Toplevel()

     
        self.root.protocol("WM_DELETE_WINDOW", self.exit_program)

        self.root.title("Exam Summary")

        self.root.geometry("650x550")

        self.root.configure(bg="white")

        title = tk.Label(
            self.root,
            text="SMART EXAM PROCTORING SYSTEM",
            font=("Arial",20,"bold"),
            bg="#2C3E50",
            fg="white",
            pady=15
        )

        title.pack(fill="x")

        tk.Label(
            self.root,
            text="EXAM COMPLETED ✓",
            font=("Arial",18,"bold"),
            fg="green",
            bg="white"
        ).pack(pady=20)

        info = tk.Frame(self.root,bg="white")

        info.pack()

        tk.Label(
            info,
            text=f"Student Name : {self.student_name}",
            font=("Arial",14),
            bg="white"
        ).pack(anchor="w")

        tk.Label(
            info,
            text=f"Roll Number : {self.roll_no}",
            font=("Arial",14),
            bg="white"
        ).pack(anchor="w")

        tk.Label(
            info,
            text=f"Duration : {duration}",
            font=("Arial",14),
            bg="white"
        ).pack(anchor="w")
        tk.Label(
            info,
            text=f"Score : {self.score}/{self.total_questions}",
            font=("Arial",14,"bold"),
            fg="blue",
            bg="white"
        ).pack(anchor="w")
        tk.Label(
            info,
            text=f"Violations : {len(violations)}",
            font=("Arial",14),
            bg="white"
        ).pack(anchor="w")

        tk.Label(
            self.root,
            text="Violation Log",
            font=("Arial",16,"bold"),
            bg="white"
        ).pack(pady=15)

        self.listbox = tk.Listbox(
            self.root,
            width=70,
            height=10,
            font=("Arial",11)
        )

        self.listbox.pack()

        for item in violations:

            self.listbox.insert(tk.END,item)

        button_frame = tk.Frame(
            self.root,
            bg="white"
        )

        button_frame.pack(pady=20)

        tk.Button(
            button_frame,
            text="Generate Report",
            width=18,
            bg="blue",
            fg="white",
            font=("Arial",11,"bold"),
            command=self.generate_report
        ).grid(row=0,column=0,padx=10)

        tk.Button(
            button_frame,
            text="Exit",
            width=18,
            bg="red",
            fg="white",
            font=("Arial",11,"bold"),
            command=self.exit_program
        ).grid(row=0,column=1,padx=10)
   
    def generate_report(self):

        generator = ReportGenerator()

        report_path = generator.generate(

            self.student_name,

            self.roll_no,

            self.duration,

            self.violations

        )

        db = DatabaseManager()

        status = "PASS"

        if len(self.violations) > 10:

            status = "FAIL"

        db.save_exam_result(

            self.roll_no,

            self.student_name,

            self.duration,

            len(self.violations),

            status,

            report_path

        )

        db.close()

        messagebox.showinfo(

            "Success",

            f"Report Generated Successfully!\n\nSaved at:\n{report_path}"

        )
    
    def exit_program(self):
        self.root.destroy()
        if self.dashboard is not None:
            self.dashboard.deiconify()
        