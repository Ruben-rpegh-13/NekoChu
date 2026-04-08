"""
NekoChu - Animated Pikachu desktop mascot using GTK.
"""

import math
import time
import random

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk, GLib, cairo, GdkPixbuf

from Xlib import display
from Xlib.ext import shape

from config import FRAME_WIDTH, FRAME_HEIGHT, SPEED, RAGE_DURATION, RAGE_MESSAGES


class NekoChu(Gtk.Window):
    def __init__(self):
        super().__init__()

        self.set_decorated(False)
        self.set_keep_above(True)
        self.set_app_paintable(True)

        screen = self.get_screen()
        visual = screen.get_rgba_visual()
        if visual:
            self.set_visual(visual)

        self.set_default_size(FRAME_WIDTH, FRAME_HEIGHT)

        self.sheet = GdkPixbuf.Pixbuf.new_from_file("sprites/pikachu64.png")

        self.animations = {
            "walk_right": self.get_row(0),
            "walk_left": self.get_row(1),
            "idle_right": self.get_row(2),
            "idle_left": self.get_row(3),
            "drag_right": self.get_row(2),
            "drag_left": self.get_row(3),
            "sleep_right": self.get_row(2),
            "sleep_left": self.get_row(3),
            "annoyed_right": self.get_row(0),
            "annoyed_left": self.get_row(1),
            "rage_right": self.get_row(0),
            "rage_left": self.get_row(1),
        }

        self.state = "idle"
        self.direction = "right"
        self.frame_index = 0
        self.last_frame_time = time.time()
        self.frame_delay = 0.15
        self.rage_delay = 0.08

        self.x = 300
        self.y = 300

        self.region_cache = {}
        self.last_frame_applied = -1

        self.dragging = False
        self.sleep_manager = SleepManagerGTK()
        self.click_tracker = ClickTrackerGTK()
        self.text_bubble = TextBubbleGTK()
        self.lightning_effect = LightningEffectGTK()

        self.connect("draw", self.on_draw)

        GLib.timeout_add(16, self.update)

    def get_row(self, row):
        frames = []
        cols = self.sheet.get_width() // FRAME_WIDTH

        for col in range(cols):
            frame = self.sheet.new_subpixbuf(
                col * FRAME_WIDTH,
                row * FRAME_HEIGHT,
                FRAME_WIDTH,
                FRAME_HEIGHT
            )
            frames.append(frame)

        return frames

    def get_mouse_position(self):
        display_ = Gdk.Display.get_default()
        seat = display_.get_default_seat()
        pointer = seat.get_pointer()
        screen, x, y = pointer.get_position()
        return x, y

    def set_input_region_from_sprite(self, frame):
        gdk_window = self.get_window()
        xid = gdk_window.get_xid()

        d = display.Display()
        win = d.create_resource_object('window', xid)

        frame_key = id(frame)

        if frame_key in self.region_cache:
            rectangles = self.region_cache[frame_key]
        else:
            width = frame.get_width()
            height = frame.get_height()
            pixels = frame.get_pixels()
            rowstride = frame.get_rowstride()
            n_channels = frame.get_n_channels()

            rectangles = []

            for y in range(height):
                start = None

                for x in range(width):
                    offset = y * rowstride + x * n_channels
                    alpha = pixels[offset + 3]

                    if alpha > 20:
                        if start is None:
                            start = x
                    else:
                        if start is not None:
                            rectangles.append((start, y, x - start, 1))
                            start = None

                if start is not None:
                    rectangles.append((start, y, width - start, 1))

            self.region_cache[frame_key] = rectangles

        win.shape_rectangles(
            shape.So.Set,
            shape.Sk.Input,
            0, 0,
            rectangles
        )

        d.flush()

    def set_state(self, new_state):
        if self.state != new_state:
            self.state = new_state
            self.frame_index = 0

    def contains_point(self, mx, my):
        return (self.x <= mx <= self.x + FRAME_WIDTH and
                self.y <= my <= self.y + FRAME_HEIGHT)

    def update(self):
        mx, my = self.get_mouse_position()
        self.sleep_manager.record_activity()

        if self.dragging:
            self.x = mx - FRAME_WIDTH // 2
            self.y = my - FRAME_HEIGHT // 2
            self.set_state("drag")
        elif self.state not in ("sleep", "annoyed", "rage"):
            dx = mx - self.x
            dy = my - self.y
            dist = math.sqrt(dx*dx + dy*dy)

            if dist > 10:
                self.set_state("walk")
                self.direction = "right" if dx > 0 else "left"
                self.x += dx * dist * 0.0008
                self.y += dy * dist * 0.0008
            else:
                self.set_state("idle")

        if self.state == "sleep":
            self.move(int(self.x), int(self.y))
            self.queue_draw()
            return True

        if self.state == "annoyed":
            if self.click_tracker.should_calm_down():
                self.set_state("idle")
                self.text_bubble.hide()
        elif self.state == "rage":
            if self.click_tracker.rage_should_end():
                self.set_state("idle")
                self.lightning_effect.deactivate()
                self.text_bubble.hide()
        elif self.sleep_manager.should_sleep():
            self.set_state("sleep")
        elif self.state == "sleep":
            self.sleep_manager.wake_up()
            self.set_state("idle")
            self.text_bubble.hide()

        now = time.time()
        delay = self.rage_delay if self.state == "rage" else self.frame_delay
        if now - self.last_frame_time > delay:
            self.frame_index += 1
            self.last_frame_time = now

        self.lightning_effect.update()

        self.move(int(self.x), int(self.y))
        self.queue_draw()
        return True

    def on_draw(self, widget, cr):
        cr.set_source_rgba(0, 0, 0, 0)
        cr.set_operator(cairo.OPERATOR_SOURCE)
        cr.paint()

        key = f"{self.state}_{self.direction}"
        frames = self.animations.get(key, self.animations["idle_right"])

        frame = frames[self.frame_index % len(frames)]

        if self.last_frame_applied != self.frame_index:
            self.set_input_region_from_sprite(frame)
            self.last_frame_applied = self.frame_index

        Gdk.cairo_set_source_pixbuf(cr, frame, 0, 0)
        cr.paint()

        if self.lightning_effect.is_active():
            self.lightning_effect.draw(cr, self.x + FRAME_WIDTH // 2, self.y + FRAME_HEIGHT // 2)
        else:
            self.text_bubble.draw(cr, self.x + FRAME_WIDTH // 2, self.y)

        return False

    def handle_click(self, mx, my):
        self.sleep_manager.record_activity()

        if self.contains_point(mx, my) and self.state != "rage":
            if self.click_tracker.record_click():
                should_rage, message = self.click_tracker.check_rage()
                
                if should_rage:
                    self.set_state("rage")
                    rage_msg = random.choice(RAGE_MESSAGES)
                    self.lightning_effect.activate(rage_msg)
                    self.text_bubble.show(rage_msg)
                elif message:
                    self.set_state("annoyed")
                    self.text_bubble.show(message)
                elif self.state == "annoyed":
                    remaining = len(self.click_tracker.messages) - self.click_tracker.message_index
                    if remaining > 0:
                        self.text_bubble.show(f"¡{remaining} avisos quedan!")
            elif self.state == "annoyed":
                self.text_bubble.show("¡Ya basta!")
        else:
            self.dragging = True

    def handle_release(self):
        self.dragging = False

    def handle_key(self, keyval):
        self.sleep_manager.record_activity()
        if self.state == "sleep":
            self.sleep_manager.wake_up()
            self.set_state("idle")
            self.text_bubble.hide()
        elif self.state == "annoyed":
            self.set_state("idle")
            self.text_bubble.hide()
        elif self.state == "rage":
            self.set_state("idle")
            self.lightning_effect.deactivate()
            self.text_bubble.hide()


class SleepManagerGTK:
    def __init__(self, timeout=10.0):
        self.timeout = timeout
        self.last_activity = time.time()

    def record_activity(self):
        self.last_activity = time.time()

    def should_sleep(self):
        return time.time() - self.last_activity > self.timeout

    def wake_up(self):
        pass


class ClickTrackerGTK:
    def __init__(self, threshold=5, reset_time=2.0):
        self.threshold = threshold
        self.reset_time = reset_time
        self.clicks = 0
        self.last_click_time = 0.0
        self.annoyed_time = 0.0
        self.rage_start_time = 0.0
        self.message_index = 0
        self.rage_cooldown = 15.0
        self.messages = [
            "¡Pii!",
            "¡Pika!",
            "¡Pi-ka!",
            "¡PIKA-CHU!",
            "¡Ya basta!",
            "¡No más!",
            "...",
            "¡Última advertencia!",
        ]

    def record_click(self):
        now = time.time()

        if now - self.last_click_time > self.reset_time:
            self.clicks = 0
            self.message_index = 0

        if now - self.rage_start_time < self.rage_cooldown and self.rage_start_time > 0:
            return False

        self.clicks += 1
        self.last_click_time = now

        if self.clicks >= self.threshold:
            self.clicks = 0
            return True
        return False

    def check_rage(self):
        if self.message_index >= len(self.messages):
            self.rage_start_time = time.time()
            return (True, None)
        
        message = self.messages[self.message_index]
        self.message_index += 1
        self.annoyed_time = time.time()
        return (False, message)

    def should_calm_down(self):
        return time.time() - self.annoyed_time > 3.0

    def rage_should_end(self):
        return time.time() - self.rage_start_time > RAGE_DURATION


class TextBubbleGTK:
    def __init__(self):
        self.text = ""
        self.lifetime = 3.0
        self.start_time = 0.0

    def show(self, text):
        self.text = text
        self.lifetime = 2.0
        self.start_time = time.time()

    def hide(self):
        self.text = ""

    def is_visible(self):
        if not self.text:
            return False
        return time.time() - self.start_time < self.lifetime

    def draw(self, cr, x, y):
        if not self.is_visible():
            return

        cr.save()
        cr.set_source_rgba(1, 1, 1, 0.9)
        cr.rectangle(x - 50, y - 40, 100, 30)
        cr.fill()
        cr.restore()


class LightningEffectGTK:
    def __init__(self):
        self.active = False
        self.text = ""
        self.start_time = 0.0
        self.bolts = []
        self._generate_bolts()

    def _generate_bolts(self):
        self.bolts = []
        for _ in range(5):
            angle = random.uniform(0, 2 * math.pi)
            distance = random.uniform(50, 100)
            self.bolts.append({
                "angle": angle,
                "distance": distance,
                "size": random.randint(20, 40),
                "speed": random.uniform(0.5, 1.5),
            })

    def activate(self, message=""):
        self.active = True
        self.text = message
        self.start_time = time.time()
        self._generate_bolts()

    def is_active(self):
        return self.active and time.time() - self.start_time < RAGE_DURATION

    def update(self):
        pass

    def deactivate(self):
        self.active = False

    def draw(self, cr, x, y):
        if not self.is_active():
            return

        elapsed = time.time() - self.start_time
        pulse = abs(math.sin(elapsed * 10))

        for bolt in self.bolts:
            bx = x + math.cos(bolt["angle"]) * bolt["distance"]
            by = y + math.sin(bolt["angle"]) * bolt["distance"]
            
            size = int(bolt["size"] * (0.8 + 0.2 * pulse))
            alpha = int(200 * (0.5 + 0.5 * pulse))
            
            cr.save()
            cr.set_source_rgba(1, 1, 0, alpha / 255.0)
            cr.set_line_width(3)
            cr.move_to(bx, by)
            cr.line_to(bx + size * 0.3, by + size)
            cr.stroke()
            cr.restore()


class EventController(Gtk.EventBox):
    def __init__(self, nekochu):
        super().__init__()
        self.nekochu = nekochu
        self.set_above_child(False)
        self.connect("button-press-event", self.on_press)
        self.connect("button-release-event", self.on_release)
        self.connect("motion-notify-event", self.on_motion)

    def on_press(self, widget, event):
        mx, my = self.nekochu.get_mouse_position()
        self.nekochu.handle_click(mx, my)

    def on_release(self, widget, event):
        self.nekochu.handle_release()

    def on_motion(self, widget, event):
        pass


def main():
    win = NekoChu()
    win.connect("destroy", Gtk.main_quit)

    controller = EventController(win)
    controller.add(win)

    def handle_keypress(widget, event):
        if event.keyval == Gdk.KEY_Escape:
            Gtk.main_quit()
        elif event.keyval == Gdk.KEY_space:
            win.handle_key(event.keyval)

    win.connect("key-press-event", handle_keypress)

    controller.show_all()
    win.show_all()

    Gtk.main()


if __name__ == "__main__":
    main()
