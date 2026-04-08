import time
from config import ANNOYANCE_CLICKS, CLICK_THRESHOLD, ANNOYANCE_RESET_TIME


class ClickTracker:
    def __init__(self):
        self.clicks = []
        self.message_index = 0
        self.last_click_time = 0

    def record_click(self):
        now = time.time()
        self.clicks.append(now)
        self.last_click_time = now

        self.clicks = [c for c in self.clicks if now - c < ANNOYANCE_RESET_TIME]

        if len(self.clicks) >= ANNOYANCE_CLICKS:
            self.clicks = []
            self.message_index = 0
            return True, None

        if len(self.clicks) > 0:
            self.message_index = min(len(self.clicks) - 1, 3)
            from config import ANNOYANCE_MESSAGES

            if self.message_index < len(ANNOYANCE_MESSAGES):
                return False, ANNOYANCE_MESSAGES[self.message_index]

        return False, None

    def reset(self):
        self.clicks = []
        self.message_index = 0
