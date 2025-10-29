import requests
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.clock import Clock


class SensorApp(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', padding=20, spacing=10, **kwargs)

        # Etiquetas de datos
        self.label_temp = Label(text="Temperatura: -- °C", font_size=24)
        self.label_hum = Label(text="Humedad: -- %", font_size=24)
        self.label_estado = Label(text="Estado: Esperando datos...", font_size=18, color=(0.7, 0.7, 0.7, 1))

        # Botón para actualizar
        self.btn_actualizar = Button(
            text="Actualizar Datos",
            size_hint=(1, 0.2),
            font_size=20,
            background_color=(0.2, 0.6, 0.9, 1)
        )
        self.btn_actualizar.bind(on_press=self.actualizar_datos)

        # Agregar widgets al layout
        self.add_widget(self.label_temp)
        self.add_widget(self.label_hum)
        self.add_widget(self.btn_actualizar)
        self.add_widget(self.label_estado)

        # Actualiza automáticamente cada 10 segundos
        Clock.schedule_interval(lambda dt: self.actualizar_datos(None), 10)

    def actualizar_datos(self, instance):
        try:
            url = "http://192.168.10.167:8000/nodemcu-app-last/"  # 🔹 Cambia a la IP de tu Django
            resp = requests.get(url, timeout=5)

            if resp.status_code == 200:
                data = resp.json()
                self.label_temp.text = f"Temperatura: {data['temperatura']} °C"
                self.label_hum.text = f"Humedad: {data['humedad']} %"
                self.label_estado.text = f"Última actualización: {data['fecha']}"
                self.label_estado.color = (0, 1, 0, 1)
            else:
                self.label_estado.text = f"Error HTTP {resp.status_code}"
                self.label_estado.color = (1, 0.3, 0.3, 1)

        except requests.exceptions.RequestException as e:
            self.label_estado.text = f"Sin conexión al servidor"
            self.label_estado.color = (1, 0.3, 0.3, 1)


class MainApp(App):
    def build(self):
        self.title = "Panel de Sensores - NodeMCU"
        return SensorApp()


if __name__ == "__main__":
    MainApp().run()
