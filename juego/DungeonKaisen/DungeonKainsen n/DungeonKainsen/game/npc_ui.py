# game/npc_ui.py
# Simple dialogue box renderer and input handler.
# Usage: ui = DialogueUI(screen_width, screen_height, font); ui.show(line); ui.handle_event(e)

import pygame

class DialogueUI:
    def __init__(self, screen_w, screen_h, font=None, padding=12, box_h=140):
        self.screen_w = screen_w
        self.screen_h = screen_h
        self.font = font or pygame.font.SysFont("arial", 20)
        self.padding = padding
        self.box_h = box_h
        self.visible = False
        self.current_speaker = ""
        self.current_text = ""
        self.waiting_for_advance = False

    def show(self, speaker, text):
        self.current_speaker = speaker or ""
        self.current_text = text or ""
        self.visible = True
        self.waiting_for_advance = True

    def hide(self):
        self.visible = False
        self.current_speaker = ""
        self.current_text = ""
        self.waiting_for_advance = False

    def handle_event(self, event):
        """
        Returns True if the UI consumed the event (advance), False otherwise.
        """
        if not self.visible:
            return False
        if event.type == pygame.KEYDOWN and event.key in (pygame.K_RETURN, pygame.K_SPACE, pygame.K_e, pygame.K_f):
            self.waiting_for_advance = False
            return True
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.waiting_for_advance = False
            return True
        return False

    def draw(self, surface):
        if not self.visible:
            return
        w = self.screen_w
        h = self.box_h
        x = 20
        y = self.screen_h - h - 20
        # background
        pygame.draw.rect(surface, (20,20,30), (x-4, y-4, w - 40 + 8, h + 8))
        pygame.draw.rect(surface, (10,10,14), (x, y, w - 40, h))
        pygame.draw.rect(surface, (200,200,200), (x, y, w - 40, h), 2)
        # speaker
        if self.current_speaker:
            sp = self.font.render(self.current_speaker, True, (230,230,120))
            surface.blit(sp, (x + self.padding, y + self.padding))
            ty = y + self.padding + sp.get_height() + 6
        else:
            ty = y + self.padding
        # text (wrap)
        self._draw_text_wrapped(surface, self.current_text, x + self.padding, ty, w - 40 - 2*self.padding)

    def _draw_text_wrapped(self, surface, text, x, y, max_width):
        words = text.split(" ")
        line = ""
        line_h = self.font.get_height()
        for w in words:
            test = (line + " " + w).strip()
            surf = self.font.render(test, True, (220,220,220))
            if surf.get_width() > max_width and line != "":
                surface.blit(self.font.render(line, True, (220,220,220)), (x, y))
                y += line_h + 2
                line = w
            else:
                line = test
        if line:
            surface.blit(self.font.render(line, True, (220,220,220)), (x, y))