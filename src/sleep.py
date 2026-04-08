"""
Sleep state management for the entity.
"""

import time

from config import SLEEP_TIMEOUT


class SleepManager:
    def __init__(self, timeout: float = SLEEP_TIMEOUT):
        self.timeout = timeout
        self.last_activity = time.time()
    
    def record_activity(self) -> None:
        """Record user activity, resetting the sleep timer."""
        self.last_activity = time.time()
    
    def should_sleep(self) -> bool:
        """Check if enough time has passed to enter sleep mode."""
        return time.time() - self.last_activity > self.timeout
    
    def wake_up(self, entity) -> None:
        """Wake up the entity if it's sleeping."""
        if entity.state == "sleep":
            entity.set_state("idle")
