from PyQt6.QtCore import QTimer

class CineController:
    def __init__(self, frame_update_callback, interval_ms = 100):
        """
        Parameters:
            frame_update_callback: function to call for updating frames
            interval_ms: default playback interval
        """
        self.timer = QTimer()
        self.timer.timeout.connect(frame_update_callback)

        self.interval = interval_ms
        self.timer.setInterval(self.interval)
        self.is_playing = False

    def start(self):
        if not self.is_playing:
            self.timer.start()
            self.is_playing = True

    def stop(self):
        if self.is_playing:
            self.timer.stop()
            self.is_playing = False

    def toggle(self):
        if self.is_playing:
            self.stop()
        else:
            self.start()

    def set_speed(self, interval_ms):
        """Sets new interval and restarts if already playing."""
        self.interval = interval_ms
        self.timer.setInterval(self.interval)
        if self.is_playing:
            self.timer.start()

    def increase_speed(self, step=30, min_interval=10):
        self.set_speed(max(min_interval, self.interval - step))

    def decrease_speed(self, step=30, max_interval=250):
        self.set_speed(min(max_interval, self.interval + step))

    def get_speed(self):
        return self.interval