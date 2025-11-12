#!/usr/bin/env python3
"""
SentinelLab - Script único integrador para Tecnicatura Universitaria
Integra: concurrencia, algoritmos (A*), NN desde cero, NLP básico, mini-juego CLI,
visión por computador (OpenCV), FastAPI para UI, bot (Telegram stub / realable),
scraping/automatización (requests + BS4 stub), intérprete simple, y proyecto integrador.

Modo de uso:
    python sentinellab.py --help

Advertencia: este script es una base didáctica y contiene componentes que
requieren dependencias opcionales (opencv-python, numpy, fastapi, uvicorn, requests).
Donde hay servicios remotos (Telegram token, cámara), el script maneja stubs si no
están disponibles.


Dependencias recomendadas

Para usar todas las funcionalidades:

Python 3.9+

numpy (pip install numpy)

opencv (pip install opencv-python)

fastapi + uvicorn (pip install fastapi uvicorn)

requests + bs4 (pip install requests beautifulsoup4)

(opcional) python-telegram-bot o telegram para notificaciones reales

El script se ejecuta con flags:

python sentinellab.py --demo → demo integradora CLI (lo principal para clase).

python sentinellab.py --run-server → levanta la API (si fastapi y uvicorn instalados).

python sentinellab.py --motion-demo → demo de visión (si OpenCV instalado).

python sentinellab.py --mlp-xor → entrena la MLP XOR (requiere numpy).

"""

import threading
import multiprocessing
import asyncio
import time
import queue
import math
import random
import os
import sys
import json
from http import HTTPStatus
from dataclasses import dataclass, field
from typing import List, Tuple, Dict, Optional, Any

# Optional imports will be lazy-imported where needed:
# numpy, cv2, fastapi, uvicorn, requests, bs4, pygame (not required)

# -----------------------------
# UTILIDADES / CONFIG
# -----------------------------
APP_NAME = "SentinelLab"
VERSION = "1.0-edu"
WORKDIR = os.path.abspath(os.path.dirname(__file__))

def try_import(name):
    try:
        return __import__(name)
    except Exception:
        return None

np = try_import("numpy")
cv2 = try_import("cv2")
fastapi = try_import("fastapi")
uvicorn = try_import("uvicorn")
requests = try_import("requests")
bs4 = try_import("bs4")
# telegram bot will be a stub unless python-telegram-bot is available
telegram = try_import("telegram")

# -----------------------------
# 1) CONCURRENCIA: Threaded Downloader + Task Queue
# -----------------------------
class ConcurrentDownloader:
    """
    Threaded downloader with a worker pool, progress queue and retry logic.
    It's educational: uses threading, queue, and demonstrates synchronization.
    """
    def __init__(self, urls: List[str], n_workers: int = 4, dest_folder: str = "downloads"):
        self.urls = urls
        self.n_workers = max(1, n_workers)
        self.dest_folder = os.path.join(WORKDIR, dest_folder)
        os.makedirs(self.dest_folder, exist_ok=True)
        self.q = queue.Queue()
        self._lock = threading.Lock()
        self.results = []
        for u in urls:
            self.q.put(u)

    def _download_stub(self, url, path):
        # If requests available, try real download; otherwise create a stub file.
        if requests:
            try:
                resp = requests.get(url, timeout=6)
                with open(path, "wb") as f:
                    f.write(resp.content)
                return True, len(resp.content)
            except Exception as e:
                return False, str(e)
        else:
            # Create a small stub file to simulate a download
            with open(path, "wb") as f:
                f.write(f"STUB for {url}".encode("utf-8"))
            return True, 10

    def worker(self, wid):
        while True:
            try:
                url = self.q.get_nowait()
            except queue.Empty:
                break
            fname = f"file_worker{wid}_" + os.path.basename(url).replace("/", "_")[:40]
            path = os.path.join(self.dest_folder, fname)
            success, meta = self._download_stub(url, path)
            with self._lock:
                self.results.append({"url": url, "path": path, "success": success, "meta": meta})
            print(f"[Worker {wid}] finished {url} -> {path} ({'OK' if success else 'ERR'})")
            self.q.task_done()

    def run(self):
        threads = []
        for i in range(self.n_workers):
            t = threading.Thread(target=self.worker, args=(i+1,), daemon=True)
            threads.append(t)
            t.start()
        for t in threads:
            t.join()
        return self.results

# -----------------------------
# 2) ALGORITMOS: A* para laberintos
# -----------------------------
@dataclass(order=True)
class AStarNode:
    f: float
    pos: Tuple[int,int] = field(compare=False)
    g: float = field(compare=False, default=0.0)
    parent: Optional['AStarNode'] = field(compare=False, default=None)

def astar_grid(start: Tuple[int,int], goal: Tuple[int,int], grid: List[List[int]]):
    """
    grid: 0-free, 1-block
    Returns path list from start to goal or empty list.
    """
    rows, cols = len(grid), len(grid[0])
    def h(p): return abs(p[0]-goal[0]) + abs(p[1]-goal[1])
    open_set = {}
    import heapq
    pq = []
    start_node = AStarNode(f=h(start), pos=start, g=0)
    heapq.heappush(pq, start_node)
    open_set[start] = start_node
    closed = set()
    while pq:
        node = heapq.heappop(pq)
        if node.pos == goal:
            # reconstruct
            path = []
            cur = node
            while cur:
                path.append(cur.pos)
                cur = cur.parent
            return list(reversed(path))
        closed.add(node.pos)
        x,y = node.pos
        for dx,dy in [(1,0),(-1,0),(0,1),(0,-1)]:
            nx,ny = x+dx, y+dy
            if not (0<=nx<rows and 0<=ny<cols): continue
            if grid[nx][ny]==1: continue
            ng = node.g + 1
            if (nx,ny) in closed: continue
            if (nx,ny) not in open_set or ng < open_set[(nx,ny)].g:
                hn = h((nx,ny))
                newn = AStarNode(f=ng+hn, pos=(nx,ny), g=ng, parent=node)
                open_set[(nx,ny)] = newn
                heapq.heappush(pq, newn)
    return []

def generate_maze(rows, cols, density=0.25, seed=None):
    r = random.Random(seed)
    grid = [[0 if r.random() > density else 1 for _ in range(cols)] for _ in range(rows)]
    # ensure start/end free
    grid[0][0] = 0
    grid[rows-1][cols-1] = 0
    return grid

# -----------------------------
# 3) RED NEURONAL DESDE CERO: MLP sencillo
# -----------------------------
class SimpleMLP:
    """
    MLP con una capa oculta, implementado con numpy si está disponible.
    Entrenamiento por descenso de gradiente y backprop desde cero.
    """
    def __init__(self, n_in, n_hidden, n_out, lr=0.1, seed=0):
        if np is None:
            raise RuntimeError("SimpleMLP requires numpy. Instalar numpy para usar.")
        rnd = np.random.RandomState(seed)
        self.W1 = rnd.randn(n_in, n_hidden) * 0.1
        self.b1 = np.zeros((1, n_hidden))
        self.W2 = rnd.randn(n_hidden, n_out) * 0.1
        self.b2 = np.zeros((1, n_out))
        self.lr = lr

    @staticmethod
    def sigmoid(x): return 1 / (1 + np.exp(-x))
    @staticmethod
    def sigmoid_deriv(y): return y * (1 - y)

    def forward(self, X):
        z1 = X.dot(self.W1) + self.b1
        a1 = self.sigmoid(z1)
        z2 = a1.dot(self.W2) + self.b2
        a2 = self.sigmoid(z2)
        return a1, a2

    def train(self, X, y, epochs=1000, verbose=False):
        for ep in range(epochs):
            a1, a2 = self.forward(X)
            error = y - a2
            loss = np.mean(error**2)
            if verbose and ep % (epochs//5+1) == 0:
                print(f"[MLP] ep={ep} loss={loss:.6f}")
            d2 = error * self.sigmoid_deriv(a2)
            dW2 = a1.T.dot(d2)
            db2 = np.sum(d2, axis=0, keepdims=True)
            d1 = d2.dot(self.W2.T) * self.sigmoid_deriv(a1)
            dW1 = X.T.dot(d1)
            db1 = np.sum(d1, axis=0, keepdims=True)
            # update
            self.W2 += self.lr * dW2
            self.b2 += self.lr * db2
            self.W1 += self.lr * dW1
            self.b1 += self.lr * db1

    def predict(self, X):
        _, a2 = self.forward(X)
        return a2

# -----------------------------
# 4) NLP BÁSICO: tokenizer + simple TF-like scoring (sin sklearn)
# -----------------------------
import re
_WORD_RE = re.compile(r"[A-Za-zÀ-ÖØ-öø-ÿ]+", re.UNICODE)

class TinyNLP:
    def __init__(self):
        self.docs = []
        self.term_index = {}

    @staticmethod
    def tokenize(text:str):
        tokens = [t.lower() for t in _WORD_RE.findall(text)]
        return tokens

    def add_doc(self, doc:str):
        tokens = self.tokenize(doc)
        counts = {}
        for t in tokens:
            counts[t] = counts.get(t,0)+1
        doc_id = len(self.docs)
        self.docs.append({"text":doc, "tokens":tokens, "counts":counts})
        for t in counts:
            self.term_index.setdefault(t, []).append(doc_id)

    def tfidf_vector(self, doc_id):
        # naive tf * log(N/df)
        N = len(self.docs)
        counts = self.docs[doc_id]["counts"]
        vec = {}
        for t,tf in counts.items():
            df = len(self.term_index.get(t,[]))
            idf = math.log((1+N)/(1+df)) + 1
            vec[t] = tf * idf
        return vec

    def most_similar(self, doc_id, topk=3):
        v1 = self.tfidf_vector(doc_id)
        scores = []
        for i in range(len(self.docs)):
            if i==doc_id: continue
            v2 = self.tfidf_vector(i)
            # cosine similarity
            num = sum(v1.get(k,0)*v2.get(k,0) for k in v1)
            den1 = math.sqrt(sum(v*v for v in v1.values()))
            den2 = math.sqrt(sum(v*v for v in v2.values()))
            den = den1*den2
            sim = num/den if den>0 else 0
            scores.append((sim,i))
        scores.sort(reverse=True)
        return scores[:topk]

# -----------------------------
# 5) MINI-JUEGO CLI: "Maze Runner" + visualization ASCII
# -----------------------------
def ascii_maze_show(grid, path=None):
    rows, cols = len(grid), len(grid[0])
    out = []
    pathset = set(path or [])
    for i in range(rows):
        row = ""
        for j in range(cols):
            if (i,j) in pathset:
                row += "*"
            elif grid[i][j]==1:
                row += "#"
            else:
                row += "."
        out.append(row)
    print("\n".join(out))

# -----------------------------
# 6) VISIÓN POR COMPUTADORA: pequeña demo de detector de movimiento
# -----------------------------
class MotionDetector:
    """
    Si cv2 está disponible, hace captura de cámara (o de archivo) y detecta movimiento básico.
    """
    def __init__(self, src=0, min_area=500):
        if cv2 is None:
            raise RuntimeError("MotionDetector requires opencv (cv2).")
        self.src = src
        self.min_area = min_area
        self.running = False

    def run(self, on_motion=None, max_frames=200):
        cap = cv2.VideoCapture(self.src)
        time.sleep(0.5)
        ret, frame = cap.read()
        if not ret:
            cap.release()
            raise RuntimeError("No frame from source")
        prev = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        prev = cv2.GaussianBlur(prev, (21,21), 0)
        self.running = True
        frames = 0
        while self.running and frames < max_frames:
            ret, frame = cap.read()
            if not ret: break
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            gray = cv2.GaussianBlur(gray, (21,21), 0)
            diff = cv2.absdiff(prev, gray)
            thresh = cv2.threshold(diff, 25, 255, cv2.THRESH_BINARY)[1]
            thresh = cv2.dilate(thresh, None, iterations=2)
            cnts, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            motion = False
            for c in cnts:
                if cv2.contourArea(c) < self.min_area: continue
                motion = True
                (x,y,w,h) = cv2.boundingRect(c)
                cv2.rectangle(frame, (x,y), (x+w, y+h), (0,255,0), 2)
            if motion and on_motion:
                on_motion(frame)
            cv2.imshow("SentinelLab - Motion", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            prev = gray
            frames += 1
        cap.release()
        cv2.destroyAllWindows()
        self.running = False

# -----------------------------
# 7) WEB API: FastAPI + endpoints to trigger features
# -----------------------------
def build_fastapi(app_state):
    """
    Construye la app FastAPI si fastapi está disponible.
    app_state: dict compartido con otras partes para orquestación.
    """
    if fastapi is None:
        return None
    from fastapi import FastAPI, BackgroundTasks
    from fastapi.responses import JSONResponse, StreamingResponse
    import io
    app = FastAPI(title=APP_NAME)

    @app.get("/health")
    def health():
        return {"status": "ok", "version": VERSION}

    @app.get("/start_downloader")
    def start_downloader(q: int = 3):
        # create a sample list of URLs for demo (they can be changed)
        urls = [
            "https://example.com/index.html",
            "https://example.com/image.png",
            "https://example.com/file.bin",
        ]
        cd = ConcurrentDownloader(urls, n_workers=q)
        res = cd.run()
        return JSONResponse(content={"results": res})

    @app.get("/maze_solve")
    def maze_solve(rows: int=15, cols: int=30, density: float=0.25):
        g = generate_maze(rows, cols, density=density, seed=42)
        start = (0,0)
        goal = (rows-1, cols-1)
        path = astar_grid(start, goal, g)
        # return small summary
        return {"rows":rows,"cols":cols,"density":density,"path_len":len(path),
                "path_sample": path[:20]}

    @app.get("/nlp_add")
    def nlp_add(text: str):
        nlp = app_state.setdefault("nlp", TinyNLP())
        nlp.add_doc(text)
        return {"status":"added", "doc_id": len(nlp.docs)-1}

    @app.get("/nlp_sim")
    def nlp_sim(doc_id: int=0):
        nlp = app_state.get("nlp")
        if not nlp:
            return {"error":"no docs"}
        sims = nlp.most_similar(doc_id)
        return {"sims":sims}

    @app.get("/mlp_xor")
    def mlp_xor(epochs: int=3000):
        if np is None:
            return {"error":"numpy missing"}
        X = np.array([[0,0],[0,1],[1,0],[1,1]])
        y = np.array([[0],[1],[1],[0]])
        mlp = SimpleMLP(2,4,1,lr=0.1)
        mlp.train(X,y,epochs=epochs)
        preds = (mlp.predict(X) > 0.5).astype(int).tolist()
        return {"preds":preds}

    return app

# -----------------------------
# 8) AUTOMATIZACIÓN / BOT: Telegram notifier (stub if token missing)
# -----------------------------
class TelegramNotifier:
    """
    Muy simple: si existe python-telegram-bot o telegram, puede enviar;
    si no, actúa como stub que escribe en logs.
    Para usar real: export TELEGRAM_TOKEN and TELEGRAM_CHAT_ID
    """
    def __init__(self):
        self.token = os.environ.get("TELEGRAM_TOKEN")
        self.chat_id = os.environ.get("TELEGRAM_CHAT_ID")
        if telegram and self.token:
            try:
                from telegram import Bot
                self.bot = Bot(token=self.token)
            except Exception:
                self.bot = None
        else:
            self.bot = None

    def notify(self, text, image_path=None):
        if self.bot:
            try:
                if image_path:
                    with open(image_path, "rb") as f:
                        self.bot.send_photo(chat_id=self.chat_id, photo=f, caption=text)
                else:
                    self.bot.send_message(chat_id=self.chat_id, text=text)
                return True
            except Exception as e:
                print("[TelegramNotifier] error sending:", e)
                return False
        else:
            # Stub behavior: write to a local log file
            logf = os.path.join(WORKDIR, "sentinel_notifications.log")
            with open(logf, "a", encoding="utf-8") as f:
                f.write(f"{time.asctime()} - NOTIFY - {text}\n")
            print("[TelegramStub] wrote log:", text)
            return True

# -----------------------------
# 9) INTÉRPRETE SIMPLE: reglas y acciones
# -----------------------------
class MiniInterpreter:
    """
    Interprete de reglas muy sencillo:
    Sintaxis de ejemplo:
        NOTIFY "Alerta detectada" WHEN motion > 0
        RUN_FUNC start_downloader PARAMS 5
    Permite ejecutar acciones definidas por el host (callbacks).
    """
    def __init__(self):
        self.actions = {}

    def register_action(self, name, fn):
        self.actions[name.upper()] = fn

    def parse_and_execute(self, script: str, context: dict):
        lines = [l.strip() for l in script.splitlines() if l.strip() and not l.strip().startswith("#")]
        results = []
        for ln in lines:
            parts = ln.split()
            cmd = parts[0].upper()
            if cmd == "NOTIFY":
                # NOTIFY "text with spaces" WHEN <var> > <num>
                # naive parse
                try:
                    quote_open = ln.index('"')
                    quote_close = ln.index('"', quote_open+1)
                    msg = ln[quote_open+1:quote_close]
                except ValueError:
                    msg = "Notification"
                cond = ln[quote_close+1:].strip()
                ok = False
                if cond.upper().startswith("WHEN"):
                    cond_expr = cond[4:].strip()
                    # evaluate safely using context
                    try:
                        ok = eval(cond_expr, {}, context)
                    except Exception:
                        ok = False
                if ok:
                    # if notifier registered, call it
                    notif = self.actions.get("NOTIFY")
                    if notif:
                        notif(msg)
                    results.append(("NOTIFY", msg, True))
                else:
                    results.append(("NOTIFY", msg, False))
            elif cmd == "RUN_FUNC":
                # RUN_FUNC name [PARAMS ...]
                fname = parts[1]
                params = []
                # naive param parse
                if "PARAMS" in parts:
                    ix = parts.index("PARAMS")
                    params = [int(x) if x.isdigit() else x.strip('"') for x in parts[ix+1:]]
                fn = self.actions.get(fname.upper())
                if fn:
                    try:
                        out = fn(*params)
                        results.append(("RUN_FUNC", fname, True, out))
                    except Exception as e:
                        results.append(("RUN_FUNC", fname, False, str(e)))
                else:
                    results.append(("RUN_FUNC", fname, False, "not found"))
            else:
                results.append(("UNKNOWN", ln))
        return results

# -----------------------------
# ORQUESTADOR / DEMO INTEGRADORA
# -----------------------------
def demo_integration():
    print(f"=== {APP_NAME} DEMO INTEGRACIÓN ===")
    # 1) Descargar concurrente (stub) en hilos
    urls = [
        "https://example.com/alpha.txt",
        "https://example.com/beta.jpg",
        "https://example.com/gamma.bin",
        "https://example.com/delta.mp4"
    ]
    cd = ConcurrentDownloader(urls, n_workers=3)
    thr = threading.Thread(target=lambda: cd.run(), daemon=True)
    thr.start()

    # 2) Generar laberinto y resolver (A*)
    grid = generate_maze(16, 32, density=0.22, seed=1234)
    path = astar_grid((0,0),(15,31),grid)
    print("Maze path length:", len(path))
    ascii_maze_show(grid, path[:200])

    # 3) Entrenar una red simple XOR (si numpy)
    if np:
        X = np.array([[0,0],[0,1],[1,0],[1,1]])
        y = np.array([[0],[1],[1],[0]])
        mlp = SimpleMLP(2,6,1, lr=0.2)
        mlp.train(X,y,epochs=2000, verbose=True)
        preds = (mlp.predict(X) > 0.5).astype(int).flatten().tolist()
        print("XOR preds:", preds)
    else:
        print("NumPy no disponible: salto MLP")

    # 4) NLP: agregar docs y encontrar similaridades
    nlp = TinyNLP()
    nlp.add_doc("El barco llegó al puerto y descargó la carga.")
    nlp.add_doc("La alarma del sistema detectó movimiento en la cubierta.")
    nlp.add_doc("El equipo técnico realizó el mantenimiento de la antena.")
    sims = nlp.most_similar(1)
    print("Similar docs to doc1:", sims)

    # 5) Mini intérprete que orquesta: registra notificador (stub) y función
    interp = MiniInterpreter()
    notifier = TelegramNotifier()
    interp.register_action("NOTIFY", lambda msg: notifier.notify(msg))
    interp.register_action("start_downloader", lambda q=2: ConcurrentDownloader(urls, n_workers=int(q)).run())
    # Script de ejemplo: notificá si hubo movimiento (aquí la condición es simulada)
    script = '''
    # Notificar si flag motion > 0
    NOTIFY "Alerta: movimiento detectado en zona A" WHEN motion_count > 0
    RUN_FUNC start_downloader PARAMS 2
    '''
    # Simulamos contexto con motion_count
    context = {"motion_count": 1}
    res = interp.parse_and_execute(script, context)
    print("Interpreter results:", res)

    # 6) Mostrar resultados de descarga (esperar hilo)
    thr.join(timeout=2)
    print("Downloads done (sample):", cd.results[:3])

    # Fin demo
    print("=== DEMO FINALIZADA ===")

# -----------------------------
# UTIL CLI
# -----------------------------
def print_help():
    print(f"{APP_NAME} {VERSION}")
    print("Opciones:")
    print("  --demo                     Ejecuta la demo integradora (CLI)")
    print("  --run-server               Levanta FastAPI (si está instalado) en 127.0.0.1:8000")
    print("  --motion-demo              Ejecuta detector de movimiento (requiere opencv)")
    print("  --mlp-xor                 Entrena MLP XOR demo (requiere numpy)")
    print("  --make-pdf                Genera un resumen (no implementado aquí, ejemplo en la cátedra)")
    print("  --help                    Esta ayuda")

# -----------------------------
# ENTRADA PRINCIPAL
# -----------------------------
if __name__ == "__main__":
    args = sys.argv[1:]
    if not args or "--help" in args:
        print_help()
        sys.exit(0)
    if "--demo" in args:
        demo_integration()
        sys.exit(0)
    if "--mlp-xor" in args:
        if np is None:
            print("Instalar numpy para usar MLP.")
            sys.exit(1)
        X = np.array([[0,0],[0,1],[1,0],[1,1]])
        y = np.array([[0],[1],[1],[0]])
        mlp = SimpleMLP(2,6,1, lr=0.2)
        mlp.train(X,y,epochs=5000, verbose=True)
        print("Preds:", (mlp.predict(X)>0.5).astype(int).flatten().tolist())
        sys.exit(0)
    if "--run-server" in args:
        if fastapi is None or uvicorn is None:
            print("Instalar fastapi y uvicorn para levantar el servidor.")
            sys.exit(1)
        app_state = {}
        app = build_fastapi(app_state)
        if app is None:
            print("No se pudo construir FastAPI.")
            sys.exit(1)
        print("Iniciando FastAPI en http://127.0.0.1:8000")
        uvicorn.run(app, host="127.0.0.1", port=8000)
        sys.exit(0)
    if "--motion-demo" in args:
        if cv2 is None:
            print("Instalar opencv-python para demo de movimiento.")
            sys.exit(1)
        md = MotionDetector(src=0, min_area=800)
        def on_motion(frame):
            print("[MotionDetector] Evento: movimiento detectado (frame capturado).")
        md.run(on_motion=on_motion, max_frames=500)
        sys.exit(0)

    print("Opción no reconocida. Usa --help.")
