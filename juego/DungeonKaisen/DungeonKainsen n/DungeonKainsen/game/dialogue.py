# game/dialogue.py
# Simple DialogueManager: maneja diálogos por id (listas de líneas).
# API: start(dialog_id, npc_name), advance(), get_current(), is_active()

class DialogueManager:
    def __init__(self, dialogues=None):
        """
        dialogues: dict dialog_id -> list of dicts {"speaker":str, "text":str}
        """
        self.dialogues = dialogues or {}
        self.active_id = None
        self.active_lines = []
        self.index = 0
        self.npc_name = None

    def register(self, dialog_id, lines):
        self.dialogues[dialog_id] = lines

    def start(self, dialog_id, npc_name=None):
        if dialog_id not in self.dialogues:
            return False
        self.active_id = dialog_id
        self.active_lines = list(self.dialogues[dialog_id])
        self.index = 0
        self.npc_name = npc_name
        return True

    def current(self):
        if not self.is_active():
            return None
        return self.active_lines[self.index]

    def advance(self):
        if not self.is_active():
            return False
        self.index += 1
        if self.index >= len(self.active_lines):
            self.end()
            return False
        return True

    def is_active(self):
        return self.active_id is not None

    def end(self):
        self.active_id = None
        self.active_lines = []
        self.index = 0
        self.npc_name = None