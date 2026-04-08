"""
Click tracking for interaction mechanics.
"""

import time

from config import ANNOYANCE_CLICKS, ANNOYANCE_RESET_TIME, ANNOYANCE_MESSAGES, RAGE_COOLDOWN


class ClickTracker:
    """Track clicks to determine player annoyance level."""
    
    def __init__(self):
        self.clicks = 0
        self.last_click_time = 0.0
        self.message_index = 0
        self.last_rage_time = 0.0
    
    def record_click(self) -> tuple[bool, str | None]:
        """
        Record a click. Returns (should_show_rage, message).
        message is None for normal annoyance, str for the message to show.
        """
        now = time.time()
        
        if now - self.last_click_time > ANNOYANCE_RESET_TIME:
            self.clicks = 0
            self.message_index = 0
        
        if now - self.last_rage_time < RAGE_COOLDOWN:
            return (False, None)
        
        self.clicks += 1
        self.last_click_time = now
        
        if self.clicks >= ANNOYANCE_CLICKS:
            self.clicks = 0
            
            if self.message_index >= len(ANNOYANCE_MESSAGES):
                self.last_rage_time = now
                return (True, None)
            
            message = ANNOYANCE_MESSAGES[self.message_index]
            self.message_index += 1
            return (False, message)
        
        return (False, None)
    
    def should_show_rage(self) -> bool:
        """Check if rage animation should play."""
        return time.time() - self.last_rage_time < RAGE_COOLDOWN
    
    def reset(self) -> None:
        """Reset annoyance state."""
        self.clicks = 0
        self.message_index = 0
    
    def get_click_count(self) -> int:
        """Get current click count within threshold."""
        now = time.time()
        if now - self.last_click_time > ANNOYANCE_RESET_TIME:
            return 0
        return self.clicks
