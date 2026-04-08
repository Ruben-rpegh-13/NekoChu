import time
from config import SLEEP_TIMEOUT


class SleepManager:
    def __init__(self):
        self.last_activity = time.time()
        self.sleep_delay = SLEEP_TIMEOUT

    def record_activity(self):
        self.last_activity = time.time()

    def should_sleep(self):
        return time.time() - self.last_activity > self.sleep_delay

    def wake_up(self, entity):
        entity.is_sleeping = False
        entity.set_state("idle")
        self.record_activity()
