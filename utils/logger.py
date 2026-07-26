from datetime import datetime


class ViolationLogger:

    def __init__(self):
        self.logs = []

    def add(self, message):

        current_time = datetime.now().strftime("%H:%M:%S")

        entry = f"{current_time}  {message}"

        self.logs.append(entry)

        return entry

    def get_logs(self):
        return self.logs