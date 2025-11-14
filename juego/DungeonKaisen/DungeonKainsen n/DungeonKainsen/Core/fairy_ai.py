# core/fairy_ai.py
import requests
import json
import os

class FairyAI:
    def __init__(self, api_key=None):
        self.api_key = api_key or os.environ.get("FAIRY_API_KEY") or self._read_api_key_file()
        self.api_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"

    def _read_api_key_file(self):
        try:
            path = os.path.join(os.getcwd(), "api_key.txt")
            if os.path.exists(path):
                with open(path, "r", encoding="utf-8") as f:
                    return f.read().strip()
        except Exception:
            return None
        return None

    def available(self):
        return bool(self.api_key)

    def preguntar(self, pregunta, contexto=None):
        if not self.api_key:
            raise RuntimeError("No API key provided to FairyAI")
        headers = {
            "Content-Type": "application/json",
            "X-goog-api-key": self.api_key
        }
        prompt_text = (
            "Eres un shikigami que ayuda a su hechicero con consejos de estadísticas y dotes. "
            "Responde de forma concisa y práctica, menciona probabilidades y mecánicas cuando sea relevante. "
            "Usuario: " + pregunta
        )
        payload = {
            "contents": [
                {
                    "parts": [
                        {"text": prompt_text}
                    ]
                }
            ]
        }
        resp = requests.post(self.api_url, headers=headers, json=payload, timeout=15)
        if resp.status_code != 200:
            raise RuntimeError(f"API responded {resp.status_code}: {resp.text}")
        data = resp.json()
        try:
            return data["candidates"][0]["content"]["parts"][0]["text"]
        except Exception:
            return json.dumps(data)