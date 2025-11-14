# main.py
# Entrypoint — carga la clase Game desde game.core y la ejecuta.

from core import *

if __name__ == "__main__":
    game = Game()
    try:
        game.run()
    except SystemExit:
        pass
    except Exception as e:
        print("Unhandled exception:", e)
        try:
            game.quit_and_cleanup(save=False)
        except Exception:
            pass
        raise