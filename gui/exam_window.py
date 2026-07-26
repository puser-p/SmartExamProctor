import tkinter as tk
import cv2
import time
from utils.logger import ViolationLogger
from PIL import Image
from PIL import ImageTk
from tkinter import messagebox
from detection.camera import Camera
from detection.face_detector import FaceDetector
from tkinter import ttk
from gui.exam_summary import ExamSummary
from datetime import datetime
from detection.phone_detector import PhoneDetector
from detection.recognizer import FaceRecognizer
from database.db_manager import DatabaseManager
class ExamWindow:

    
    def __init__(
        self,
        
        student_name="Student",
        roll_no="000",
        
        dashboard=None
    ):
        self.student_name = student_name
        self.roll_no = str(roll_no)
        self.student_roll = self.roll_no
        self.dashboard = dashboard
       
        self.root = tk.Toplevel()

        self.root.title("Smart Exam Proctoring System")
        self.root.state("zoomed")
        self.root.protocol("WM_DELETE_WINDOW", self.close_window)

        

        self.root.configure(bg="white")
        self.camera = Camera()
        self.recognizer = FaceRecognizer()

        self.detector = FaceDetector()
        self.logger = ViolationLogger()
        self.camera_status = tk.StringVar(value="🟢 Camera Connected")
        self.face_status = tk.StringVar(value="🟢 Face Detected")
        self.student_status = tk.StringVar(value="🟢 Student Verified")
        self.person_status = tk.StringVar(value="🟢 One Person")
        self.phone_status = tk.StringVar(value="🟢 No Phone Detected")
        self.exam_status = tk.StringVar(value="🔴 Exam Not Started")
        # Face monitoring
        self.face_present = False
        self.face_missing_time = None
        self.face_missing_logged = False
        self.face_present = True
        self.face_missing_since = None
        self.violation_count = 0
        self.multiple_person_logged = False
        self.phone_detector = PhoneDetector()
        self.phone_logged = False
        self.last_unknown = False
        self.camera_job = None
        self.timer_job = None
        self.questions = self.recognizer.db.get_questions()

        self.current_question = 0

        self.answers = {}

        self.score = 0

        self.create_widgets()

        self.load_question()
        self.remaining_seconds = 60 * 60    # 1 hour
        self.exam_running = False

        


        self.update_camera()
       

    def create_widgets(self):

        title = tk.Label(

            self.root,

            text="SMART EXAM PROCTORING SYSTEM",

            font=("Arial",22,"bold"),

            bg="#2C3E50",

            fg="white",

            pady=15

        )

        title.pack(fill="x")

        info = tk.Frame(self.root,bg="white")

        info.pack(fill="x",pady=10)

        tk.Label(

            info,

            text="Student :",

            font=("Arial",14,"bold"),

            bg="white"

        ).grid(row=0,column=0,padx=10)

        self.student_name_label = tk.Label(
            info,
            text=self.student_name,
            font=("Arial",14),
            bg="white"
        )

        self.student_name_label.grid(row=0,column=1)

        tk.Label(

            info,

            text="Roll No :",

            font=("Arial",14,"bold"),

            bg="white"

        ).grid(row=0,column=2,padx=20)

        self.roll_label = tk.Label(
            info,
            text=self.roll_no,
            font=("Arial",14),
            bg="white"
        )

        self.roll_label.grid(row=0,column=3)

        camera = tk.LabelFrame(

            self.root,

            text="Live Camera",

            font=("Arial",14,"bold"),

            padx=10,

            pady=10

        )

        camera.pack(side="left",padx=20,pady=20)
        question_frame = tk.LabelFrame(
            self.root,
            text="Online Examination",
            font=("Arial", 14, "bold"),
            padx=10,
            pady=10
        )

        question_frame.pack(side="left", fill="both", expand=True, padx=10)

        self.question_label = tk.Label(
            question_frame,
            text="",
            font=("Arial", 14),
            justify="left",
            wraplength=500
        )

        self.question_label.pack(anchor="w", pady=10)

        self.answer_var = tk.StringVar()

        self.option_buttons = []

        for i in range(4):

            rb = tk.Radiobutton(
                question_frame,
                text="",
                variable=self.answer_var,
                value="",
                font=("Arial", 12),
                anchor="w",
                justify="left"
            )

            rb.pack(anchor="w", pady=5)

            self.option_buttons.append(rb)
        navigation = tk.Frame(question_frame)

        navigation.pack(pady=20)

        tk.Button(
            navigation,
            text="Previous",
            width=12,
            command=self.previous_question
        ).grid(row=0,column=0,padx=10)

        tk.Button(
            navigation,
            text="Next",
            width=12,
            command=self.next_question
        ).grid(row=0,column=1,padx=10)
        self.camera_label = tk.Label(

            camera,

            width=700,

            height=500,

            bg="black"

        )

        self.camera_label.pack()

        right = tk.Frame(self.root,bg="white")

        right.pack(side="right",fill="y",padx=20)

        tk.Label(

            right,

            text="Time Remaining",

            font=("Arial",16,"bold"),

            bg="white"

        ).pack()
  
        self.timer = tk.Label(

            right,

            text="01:00:00",

            font=("Arial",24,"bold"),

            fg="red",

            bg="white"

        )

        self.timer.pack(pady=20)
        status_frame = tk.LabelFrame(
            right,
            text="AI STATUS",
            font=("Arial", 13, "bold"),
            padx=10,
            pady=10
        )

        status_frame.pack(fill="x", pady=15)

        tk.Label(
            status_frame,
            textvariable=self.camera_status,
            anchor="w",
            font=("Arial",11)
        ).pack(fill="x")

        tk.Label(
            status_frame,
            textvariable=self.face_status,
            anchor="w",
            font=("Arial",11)
        ).pack(fill="x")

        tk.Label(
            status_frame,
            textvariable=self.student_status,
            anchor="w",
            font=("Arial",11)
        ).pack(fill="x")

        tk.Label(
            status_frame,
            textvariable=self.person_status,
            anchor="w",
            font=("Arial",11)
        ).pack(fill="x")

        tk.Label(
            status_frame,
            textvariable=self.phone_status,
            anchor="w",
            font=("Arial",11)
        ).pack(fill="x")

        tk.Label(
            status_frame,
            textvariable=self.exam_status,
            anchor="w",
            font=("Arial",11)
        ).pack(fill="x")
        button_frame = tk.Frame(right, bg="white")
        button_frame.pack(fill="x", pady=10)

        self.start_btn = tk.Button(
            button_frame,
            text="Start Exam",
            bg="green",
            fg="white",
            font=("Arial", 12, "bold"),
            command=self.start_exam
        )
        self.start_btn.pack(fill="x", pady=5)

        self.submit_btn = tk.Button(
            button_frame,
            text="Submit Exam",
            bg="red",
            fg="white",
            font=("Arial", 12, "bold"),
            command=self.submit_exam
        )
        self.submit_btn.pack(fill="x", pady=5)
        self.violation_label = tk.Label(
            right,
            text="Violations : 0",
            font=("Arial",13,"bold"),
            fg="red",
            bg="white"
        )

        self.violation_label.pack(pady=5)
        tk.Label(

            right,

            text="Violations",

            font=("Arial",16,"bold"),

            bg="white"

        ).pack()
        log_frame = tk.Frame(right)
        log_frame.pack(fill="both", expand=True, pady=10)

        scrollbar = tk.Scrollbar(log_frame)

        scrollbar.pack(side="right", fill="y")

        self.listbox = tk.Listbox(
            log_frame,
            height=8,
            yscrollcommand=scrollbar.set
        )

        self.listbox.pack(side="left", fill="both", expand=True)

        scrollbar.config(command=self.listbox.yview)
      

    

    def start_exam(self):

        if not self.exam_running:

            self.exam_running = True
            self.exam_status.set("🟢 Exam Running")
            self.add_violation("Exam Started")


            self.update_timer()


    def submit_exam(self):
        qid = self.questions[self.current_question][0]
        self.answers[qid] = self.answer_var.get()

        self.exam_running = False

        self.add_violation("Exam Submitted")
        if self.camera_job is not None:
            self.root.after_cancel(self.camera_job)

        if self.timer_job is not None:
            self.root.after_cancel(self.timer_job)
        self.camera.release()
        cv2.destroyAllWindows()

        violations = self.logger.get_logs()
        duration = self.timer.cget("text")
        student_name = self.student_name
        student_roll = self.student_roll
        if self.camera_job:
            self.root.after_cancel(self.camera_job)

        if self.timer_job:
            self.root.after_cancel(self.timer_job)
        db = DatabaseManager()

        score = 0

        for question in self.questions:

            qid = question[0]

            correct_answer = question[6]

            selected_answer = self.answers.get(qid, "")

            is_correct = int(selected_answer == correct_answer)

            if is_correct:
                score += 1

            db.save_student_answer(

                self.student_roll,

                qid,

                selected_answer,

                correct_answer,

                is_correct

            )

        db.close()
        self.root.destroy()
        ExamSummary(
            student_name=student_name,
            roll_no=student_roll,
            duration=duration,
            violations=violations,
            score=score,

            total_questions=len(self.questions),
            dashboard=self.dashboard
        )
        
        
        self.exam_status.set("🔴 Exam Finished")


    def update_camera(self):

        frame = self.camera.read()

        if frame is None:
            self.root.after(20, self.update_camera)
            return

        # Face recognition (draws name on frame)
        frame, recognized_name, recognized_roll, faces = self.recognizer.recognize(frame)
      
        print("ExamWindow recognized_roll =", recognized_roll)

        # Face detection (for counting faces)
        
        if recognized_roll is not None:

            self.student_name = recognized_name
            self.student_roll = recognized_roll
            self.roll_no = recognized_roll

            self.student_name_label.config(text=recognized_name)
            self.roll_label.config(text=recognized_roll)
        # ---------------- Student Verification ---------------- #
   
        if recognized_roll is None:

            self.camera_status.set("No Face")
            self.last_unknown = False

        elif str(recognized_roll) == str(self.student_roll):

            self.camera_status.set("Student Verified")
            self.last_unknown = False

        else:

            self.camera_status.set("Unknown Person")

            if not self.last_unknown:

                self.add_violation("Unknown Person Detected")
                self.last_unknown = True

        # ---------------- Face Detection ---------------- #

        if faces is None or len(faces) == 0:

            self.face_status.set("🔴 Face Not Detected")

            if self.face_present:
                self.face_present = False
                self.face_missing_time = time.time()

            elif (
                self.face_missing_time is not None
                and not self.face_missing_logged
                and time.time() - self.face_missing_time >= 3
            ):
                self.add_violation("Face Missing")
                self.face_missing_logged = True

        else:

            self.face_status.set("🟢 Face Detected")

            if not self.face_present:

                self.face_present = True

                if self.face_missing_logged:
                    self.add_violation("Face Detected Again")

                self.face_missing_logged = False

            # Multiple persons

            if len(faces) > 1:

                self.person_status.set("🔴 Multiple Persons")

                if not self.multiple_person_logged:

                    self.add_violation("Multiple Persons Detected")
                    self.multiple_person_logged = True

            else:

                self.person_status.set("🟢 One Person")
                self.multiple_person_logged = False

        # ---------------- Phone Detection ---------------- #

        frame, phone_found = self.phone_detector.detect(frame)

        if phone_found:

            self.phone_status.set("🔴 Phone Detected")

            if not self.phone_logged:

                self.add_violation("Mobile Phone Detected")
                self.phone_logged = True

        else:

            self.phone_status.set("🟢 No Phone Detected")
            self.phone_logged = False

        # ---------------- Display ---------------- #

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        image = Image.fromarray(frame)
        image = image.resize((900, 600))

        photo = ImageTk.PhotoImage(image)

        self.camera_label.configure(image=photo)
        self.camera_label.image = photo
        if self.exam_running or self.root.winfo_exists():
            self.camera_job = self.root.after(20, self.update_camera)
            
    
    def update_timer(self):

        if self.exam_running:

            if self.remaining_seconds > 0:

                self.remaining_seconds -= 1

                hrs = self.remaining_seconds // 3600
                mins = (self.remaining_seconds % 3600) // 60
                secs = self.remaining_seconds % 60

                self.timer.config(
                    text=f"{hrs:02d}:{mins:02d}:{secs:02d}"
                )
                

             

            else:

                self.listbox.insert("end", "Time Over!")

                self.submit_exam()
        if self.root.winfo_exists():
            self.timer_job = self.root.after(1000, self.update_timer)
    def add_violation(self, message):

        current_time = datetime.now().strftime("%H:%M:%S")

        log = f"[{current_time}] {message}"

        self.logger.add(log)

        self.listbox.insert("end", log)

        self.listbox.yview_moveto(1)

        if message not in ("Exam Started", "Exam Submitted"):

            self.violation_count += 1

            self.violation_label.config(
                text=f"Violations : {self.violation_count}"
            )
    def load_question(self):

        if len(self.questions) == 0:
            return

        question = self.questions[self.current_question]

        self.question_label.config(

            text=f"Q{self.current_question+1}. {question[1]}"

        )

        options = question[2:6]

        for rb, option in zip(self.option_buttons, options):

            rb.config(

                text=option,

                value=option

            )

        qid = question[0]

        if qid in self.answers:

            self.answer_var.set(self.answers[qid])

        else:

            self.answer_var.set("")
    def next_question(self):

        qid = self.questions[self.current_question][0]

        self.answers[qid] = self.answer_var.get()

        if self.current_question < len(self.questions)-1:

            self.current_question += 1

            self.load_question()
    def previous_question(self):

        qid = self.questions[self.current_question][0]

        self.answers[qid] = self.answer_var.get()

        if self.current_question > 0:

            self.current_question -= 1

            self.load_question()
    def close_window(self):

        if self.camera_job is not None:
            self.root.after_cancel(self.camera_job)

        if self.timer_job is not None:
            self.root.after_cancel(self.timer_job)

        self.camera.release()
        cv2.destroyAllWindows()

        self.root.destroy()
        if self.dashboard is not None:
            self.dashboard.deiconify()
if __name__ == "__main__":

    ExamWindow(
        student_name="Pragati Singhal",
        roll_no="704"
    )