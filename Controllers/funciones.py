import pygame.mixer as mx
import os
from mutagen.mp3 import MP3
from mutagen.oggvorbis import OggVorbis
from mutagen.wave import WAVE

class FuncionesReproductor:
    def __init__(self):
        mx.init(frequency=44100, size=-16, channels=2, buffer=4096)
        self.Canciones = []
        self.cancionActual = 0
        self.Bajos = 1.0
        self.Tono = 1.0
        self.Agudos = 1.0
        self.totalDuracion = 0

    def play(self, cancion_actual):
        try:
            mx.music.load(cancion_actual)
            mx.music.play()
            return True, "Reproduciendo..."
        except Exception as l:
            return False, f"Error al reproducir: {l}"

    def stop(self):
        mx.music.stop()
        return "Reproduccion detenida"

    def pausa(self):
        mx.music.pause()
        return "Reproduccion pausada"

    def resumen(self):
        mx.music.unpause()
        return "reproduccion reanudada "

    def siguienteCancion(self, lista_canciones):
        if lista_canciones:
            self.cancionActual = (self.cancionActual + 1) % len(lista_canciones)
            return self.cancionActual
        return 0

    def anteriorCancion(self, lista_canciones):
        if lista_canciones:
            self.cancionActual = (self.cancionActual - 1) % len(lista_canciones)
            return self.cancionActual
        return 0

    def adelantar10Segundos(self):
        try:
            mx.music.set_pos(mx.music.get_pos() / 1000 + 10)
            return True
        except:
            return False

    def retroceder10Segundos(self):
        try:
            mx.music.set_pos(mx.music.get_pos() / 1000 - 10)
            return True
        except:
            return False

    def volumen(self, valor):
        mx.music.set_volume(float(valor) / 100)

    def bajos(self, valor):
        self.Bajos = float(valor) / 100
        self.Ecualizacion()

    def tono(self, valor):
        self.Tono = float(valor) / 100
        self.Ecualizacion()

    def agudos(self, valor):
        self.Agudos = float(valor) / 100
        self.Ecualizacion()

    def Ecualizacion(self):
        balance = (self.Bajos * 0.4 + self.Tono * 0.3 + self.Agudos * 0.3)
        volumen = mx.music.get_volume()
        mx.music.set_volume(volumen * balance)

    def cargarCarpetaForanea(self, ubicacionCarpeta):
        try:
            carpetaArchivos = os.listdir(ubicacionCarpeta)
            cancionesValidas = (".mp3", ".wav", ".ogg")
            canciones = [os.path.join(ubicacionCarpeta, archivo) for archivo in carpetaArchivos if archivo.lower().endswith(cancionesValidas)]
            if canciones:
                self.Canciones = canciones
                cancionNombres = [os.path.basename(cancion) for cancion in canciones]
                return True, cancionNombres, f"Total de {len(canciones)} canciones"
            else:
                return False, [], "No hay canciones...."
        except Exception as h:
            return False, [], f"Error: {h}"

    def guardarDuracionCancion(self, archivo):
        try:
            if archivo.lower().endswith('.mp3'):
                audio = MP3(archivo)
            elif archivo.lower().endswith('.ogg'):
                audio = OggVorbis(archivo)
            elif archivo.lower().endswith('.wav'):
                audio = WAVE(archivo)
            else:
                return 0
            self.totalDuracion = audio.info.length
            return audio.info.length
        except:
            return 0

    def obtProcesoActualizado(self):
        segundosTranscurrido = mx.music.get_pos()
        return max(segundosTranscurrido / 1000,0) 
        #if segundosTranscurrido >= 0 else 0

        #return mx.music.get_pos() / 1000

    def verificarReproduccion(self):
        return mx.music.get_busy() and mx.music.get_pos() >= 0 

    def convertirTiempo(self, segundos):
        minutos = int(segundos // 60)
        segs = int(segundos % 60)
        return f"{minutos:02d}:{segs:02d}"