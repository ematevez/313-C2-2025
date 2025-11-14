# game/camera.py
# Simple Camera helper: stores offsets and provides centering and optional smoothing.

class Camera:
    def __init__(self, tile_size, screen_size=(1000, 1000)):
        self.tile_size = tile_size
        self.screen_w, self.screen_h = screen_size
        self.offset_x = 0.0
        self.offset_y = 0.0
        # smoothing factor used only if center_immediately is False
        self.smooth = 0.12
        self.center_immediately = True

    def center_on(self, px, py):
        desired_x = px - (self.screen_w // 2)
        desired_y = py - (self.screen_h // 2)
        if desired_x < 0:
            desired_x = 0.0
        if desired_y < 0:
            desired_y = 0.0
        if self.center_immediately:
            self.offset_x = float(desired_x)
            self.offset_y = float(desired_y)
        else:
            self.offset_x += (desired_x - self.offset_x) * self.smooth
            self.offset_y += (desired_y - self.offset_y) * self.smooth
            if self.offset_x < 0:
                self.offset_x = 0.0
            if self.offset_y < 0:
                self.offset_y = 0.0