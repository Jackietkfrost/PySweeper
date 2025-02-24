import time

class Timer:
    def __init__(self):
        self.start_time = time.time()
        self.elapsed_time = 0

    def update(self):
        self.elapsed_time = time.time() - self.start_time

    def get_time(self):
        return self.elapsed_time