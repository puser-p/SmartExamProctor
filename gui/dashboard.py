import tkinter as tk
from tkinter import messagebox
from datetime import datetime
from gui.student_management import StudentManagement
from gui.exam_window import ExamWindow
from gui.analytics import AnalyticsDashboard
import os

class Dashboard:

    def __init__(self,master):

        
       
        self.master = master
        self.root = tk.Toplevel(master)

        self.root.title("AI Smart Exam Proctoring System")

        self.root.geometry("1000x650")

        self.root.configure(bg="#ECF0F1")

        self.root.resizable(False, False)

        self.create_widgets()

        self.update_time()

       

    def create_widgets(self):

        title = tk.Label(
            self.root,
            text="SMART EXAM PROCTORING SYSTEM",
      
            font=("Arial", 24, "bold"),
            bg="#1F618D",
            fg="white",
            pady=15
        )

        title.pack(fill="x")

        welcome = tk.Label(
            self.root,
            text="Welcome, Admin",
            font=("Arial", 18),
            bg="#EAF2F8"
        )

        welcome.pack(pady=20)

        self.date_label = tk.Label(
            self.root,
            font=("Arial", 13),
            bg="#EAF2F8"
        )

        self.date_label.pack()

        self.time_label = tk.Label(
            self.root,
            font=("Arial", 13),
            bg="#EAF2F8"
        )

        self.time_label.pack(pady=10)

        button_frame = tk.Frame(
            self.root,
            bg="#EAF2F8"
        )

        button_frame.pack(pady=20)

     
        buttons = [

            ("👨‍🎓 Student Management", self.open_student_management),

            ("📝 Start Examination", self.open_exam),

            ("📊 Analytics Dashboard", self.open_analytics),

            ("📂 Open Reports Folder", self.open_reports),

            ("🚪 Exit", self.exit_dashboard)

        ]
        for text, command in buttons:

            btn = tk.Button(

                button_frame,

                text=text,

                width=25,

                height=2,

                bg="#2874A6",

                fg="white",

                font=("Arial", 12),

                command=command

            )

            btn.pack(pady=8)

        self.status = tk.Label(

            self.root,

            text="Status : Ready",

            bg="lightgreen",

            font=("Arial", 11),

            anchor="w"

        )

        self.status.pack(side="bottom", fill="x")
        footer = tk.Label(
            self.root,
            text="Version 1.0   |   Developed by Pragati Singhal",
            bg="#ECF0F1",
            fg="gray",
            font=("Arial",10)
        )

        footer.pack(side="bottom", pady=5)
    def update_time(self):

        now = datetime.now()

        date = now.strftime("%d %B %Y")

        time = now.strftime("%I:%M:%S %p")

        self.date_label.config(text=f"Date : {date}")

        self.time_label.config(text=f"Time : {time}")

        self.root.after(1000, self.update_time)

    def not_ready(self):

        messagebox.showinfo(
            "Module",
            "This module will be developed in upcoming lessons."
        )

    def open_student_management(self):

        StudentManagement()


    def open_exam(self):
        self.root.withdraw()

        ExamWindow(dashboard=self.root)


    def open_analytics(self):

        AnalyticsDashboard()

    def exit_dashboard(self):

        self.root.destroy()      # close dashboard
        self.master.destroy()    # close hidden login window
    def open_reports(self):

        folder = "reports"

        if os.path.exists(folder):

            os.startfile(folder)

        else:

            messagebox.showinfo(

                "Reports",

                "No reports folder found."

            )
if __name__ == "__main__":
    Dashboard()