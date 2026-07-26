import os
import sqlite3
import subprocess
from datetime import datetime
import sys
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

import matplotlib
matplotlib.use("TkAgg")

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


DATABASE = "database/exam.db"


class AnalyticsDashboard:

    def __init__(self):

    
        self.root = tk.Toplevel()

        self.root.title("Smart Exam Analytics")

        self.root.state("zoomed")

        self.root.configure(bg="#F4F6F8")

        self.connection = sqlite3.connect(DATABASE)
        self.cursor = self.connection.cursor()

        self.load_statistics()

        # ================= MAIN CONTAINER ================= #

        self.main = tk.Frame(
            self.root,
            bg="#F4F6F8"
        )

        self.main.pack(
            fill="both",
            expand=True
        )

        # Row 0
        self.create_header()

        # Row 1
        self.create_cards()

        # Row 2
        self.create_history_table()

        # Row 3
        self.create_buttons()

        # Row 4
        self.create_chart_frame()

        self.load_exam_history()

        self.draw_charts()

        self.root.mainloop()
    def create_header(self):

        header = tk.Frame(
            self.main,
            bg="#2C3E50",
            height=70
        )

        header.pack(
            fill="x"
        )

        header.pack_propagate(False)

        tk.Label(
            header,
            text="SMART EXAM ANALYTICS DASHBOARD",
            bg="#2C3E50",
            fg="white",
            font=("Arial",24,"bold")
        ).pack(
            pady=15
        )


    def load_statistics(self):

        self.cursor.execute("SELECT COUNT(*) FROM students")

        self.total_students = self.cursor.fetchone()[0]

        self.cursor.execute("SELECT COUNT(*) FROM exam_results")

        self.total_exams = self.cursor.fetchone()[0]

        self.cursor.execute("SELECT AVG(violations) FROM exam_results")

        avg = self.cursor.fetchone()[0]

        if avg is None:

            avg = 0

        self.average_violations = round(avg,2)

        self.cursor.execute("SELECT MAX(violations) FROM exam_results")

        highest = self.cursor.fetchone()[0]

        if highest is None:

            highest = 0

        self.highest = highest
    def create_cards(self):

        self.card_frame = tk.Frame(
            self.main,
            bg="#F4F6F8"
        )

        self.card_frame.pack(
            fill="x",
            pady=15
        )

        cards = [

            ("Total Students", self.total_students),

            ("Total Exams", self.total_exams),

            ("Average Violations", self.average_violations),

            ("Highest Violations", self.highest)

        ]

        for title, value in cards:

            card = tk.Frame(

                self.card_frame,

                bg="#3498DB",

                width=230,

                height=110,

                relief="raised",

                bd=2

            )

            card.pack(
                side="left",
                padx=18,
                expand=True
            )

            card.pack_propagate(False)

            tk.Label(

                card,

                text=title,

                bg="#3498DB",

                fg="white",

                font=("Arial",14,"bold")

            ).pack(pady=(18,5))

            tk.Label(

                card,

                text=str(value),

                bg="#3498DB",

                fg="white",

                font=("Arial",26,"bold")

            ).pack()
    def create_history_table(self):

        history_frame = tk.Frame(
            self.main,
            bg="white",
            bd=1,
            relief="solid"
        )

        history_frame.pack(
            fill="x",
            padx=20,
            pady=10
        )

        tk.Label(
            history_frame,
            text="Exam History",
            font=("Arial",18,"bold"),
            bg="white"
        ).pack(
            anchor="w",
            padx=15,
            pady=10
        )

        table_frame = tk.Frame(
            history_frame,
            bg="white"
        )

        table_frame.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        columns = (
            "Roll",
            "Name",
            "Date",
            "Duration",
            "Violations",
            "Status",
            "Report"
        )

        self.tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            height=8
        )

        headings = {
            "Roll":"Roll",
            "Name":"Student Name",
            "Date":"Exam Date",
            "Duration":"Duration",
            "Violations":"Violations",
            "Status":"Status",
            "Report":"PDF Report"
        }

        for col in columns:

            self.tree.heading(col,text=headings[col])

            self.tree.column(
                col,
                anchor="center",
                width=140
            )

        scrollbar = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=self.tree.yview
        )

        self.tree.configure(
            yscrollcommand=scrollbar.set
        )

        self.tree.pack(
            side="left",
            fill="both",
            expand=True
        )

        scrollbar.pack(
            side="right",
            fill="y"
        )
    def create_buttons(self):

        button_frame = tk.Frame(
            self.main,
            bg="#F4F6F8"
        )

        button_frame.pack(
            pady=15
        )

        tk.Button(
            button_frame,
            text="Open Selected Report",
            width=22,
            bg="#27AE60",
            fg="white",
            font=("Arial",12,"bold"),
            command=self.open_report
        ).pack(
            side="left",
            padx=15
        )

        tk.Button(
            button_frame,
            text="Refresh Dashboard",
            width=22,
            bg="#2980B9",
            fg="white",
            font=("Arial",12,"bold"),
            command=self.refresh_dashboard
        ).pack(
            side="left",
            padx=15
        )

    def load_exam_history(self):

        for row in self.tree.get_children():

            self.tree.delete(row)

        self.cursor.execute("""

        SELECT

        roll,

        name,

        exam_date,

        duration,

        violations,

        status,

        report_path

        FROM exam_results

        ORDER BY id DESC

        """)

        rows=self.cursor.fetchall()

        for row in rows:

            self.tree.insert("",tk.END,values=row)
  
    def refresh_dashboard(self):

        self.load_statistics()

        self.load_exam_history()

        self.draw_charts()
    def open_report(self):

        selected = self.tree.focus()

        if not selected:

            messagebox.showwarning(
                "No Selection",
                "Please select a report first."
            )
            return

        values = self.tree.item(selected)["values"]

        report_path = values[6]
        if not os.path.exists(report_path):

            messagebox.showerror(
                "Error",
                "Report not found."
            )
            return
        try:

            if sys.platform.startswith("win"):

                os.startfile(report_path)

            elif sys.platform.startswith("darwin"):

                subprocess.call(["open", report_path])

            else:

                subprocess.call(["xdg-open", report_path])

        except Exception as e:

            messagebox.showerror(
                "Error",
                str(e)
            )
        print(values)
        print(report_path)
        print(os.path.abspath(report_path))
        print(os.path.exists(report_path))
    def create_chart_frame(self):

        self.chart_frame = tk.Frame(
            self.main,
            bg="#F4F6F8"
        )

        self.chart_frame.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=(10,20)
        )

        self.left_chart = tk.Frame(
            self.chart_frame,
            bg="white",
            relief="solid",
            bd=1
        )

        self.left_chart.pack(
            side="left",
            fill="both",
            expand=True,
            padx=(0,10)
        )

        self.right_chart = tk.Frame(
            self.chart_frame,
            bg="white",
            relief="solid",
            bd=1
        )

        self.right_chart.pack(
            side="left",
            fill="both",
            expand=True,
            padx=(10,0)
        )

    def draw_charts(self):
        for widget in self.left_chart.winfo_children():
            widget.destroy()

        for widget in self.right_chart.winfo_children():
            widget.destroy()
        print("draw_charts called")

        self.cursor.execute("""
            SELECT name, violations
            FROM exam_results
        """)

        rows = self.cursor.fetchall()
        print(rows)

        if len(rows) == 0:
            return

        names = [r[0] for r in rows]

        violations = [r[1] for r in rows]

        fig = Figure(figsize=(5,3.5), dpi=100)

        ax = fig.add_subplot(111)
        ax.bar(
            names,
            violations,
            width=0.4
        )

       
        fig.tight_layout(pad=2)

        tk.Label(
            self.left_chart,
            text="Violations Per Student",
            font=("Arial",14,"bold"),
            bg="white"
        ).pack(pady=5)

        canvas = FigureCanvasTkAgg(
            fig,
            self.left_chart
        )

        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)



        fig2 = Figure(figsize=(5,4), dpi=100)

        ax2 = fig2.add_subplot(111)

        low = 0
        medium = 0
        high = 0

        for v in violations:

            if v < 5:
                low += 1
            elif v < 15:
                medium += 1
            else:
                high += 1

        data = []
        labels = []

        if low:
            data.append(low)
            labels.append("Low")

        if medium:
            data.append(medium)
            labels.append("Medium")

        if high:
            data.append(high)
            labels.append("High")
        ax2.pie(
            data,
            labels=labels,
            autopct="%1.1f%%",
            startangle=90,
            pctdistance=0.75,
            radius=0.8,
            labeldistance=1.15
        )

        ax2.axis("equal")
    
        fig2.tight_layout(pad=2)
    

        tk.Label(
            self.right_chart,
        
            text="Risk Distribution",
            font=("Arial",14,"bold"),
            bg="white"
        ).pack(pady=5)

        canvas2 = FigureCanvasTkAgg(
            fig2,
            master=self.right_chart
        )

        canvas2.draw()

        canvas2.get_tk_widget().pack(
            fill="both",
            expand=True
        )

    

