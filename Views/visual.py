import tkinter as tk
from tkinter import filedialog, Listbox, Label, Button, Scale, Frame, HORIZONTAL, END, messagebox
from Tooltip import Tooltip
from Controllers.funciones import FuncionesReproductor
import os

class Reproductor:
    def __init__(self):
        self.funciones = FuncionesReproductor()
        self.ventana = tk.Tk()
        self.ventana.title("spotify_chibiado")
        self.ventana.geometry("800x600")
        self.ventana.resizable(0, 0)
        self.ventana.iconbitmap("icons\icons8-spotify-188.png")

        self.lienzo = tk.Canvas(self.ventana, bg="gray", width=800, height=600)
        self.lienzo.pack()

        # miniventana1
        self.miniventana1 = tk.Frame(self.lienzo, bg="#cc9900", bd=10, relief="groove", width=250, height=580)
        self.miniventana1.pack(side="left", fill="y", padx=5, pady=5)

        # miniventana2
        self.miniventana2 = tk.Frame(self.lienzo, bg="#ffb300", bd=10, relief="groove", width=530, height=580)
        self.miniventana2.pack(side="right", fill="both", expand=True, padx=5, pady=5)

        # Iconos
        self.iconoPlay = tk.PhotoImage(file=r"icons/control_play_blue.png")
        self.iconoPausa = tk.PhotoImage(file=r"icons/control_pause_blue.png")
        self.iconoStop = tk.PhotoImage(file=r"icons/control_stop_blue.png")
        self.iconoResumen = tk.PhotoImage(file=r"icons/control_end_blue.png")
        self.iconoSiguiente = tk.PhotoImage(file=r"icons/control_fastforward_blue.png")
        self.iconoAnterior = tk.PhotoImage(file=r"icons/control_rewind_blue.png")
        self.iconoAdelantar10s = tk.PhotoImage(file=r"icons/arrow_right.png")
        self.iconoRetroceder10s = tk.PhotoImage(file=r"icons/arrow_left.png")
        self.iconoAyuda = tk.PhotoImage(file=r"icons\ayuda-16.png")
        self.iconoBuscarCarpeta = tk.PhotoImage(file=r"icons\buscarcarpeta.png")

        # Elementos en miniventana1 (izquierda)
        self.etiquetaEstado = Label(self.miniventana1, text="canciones", bg="blue", fg="yellow", 
                                  font=("Old English Text MT", 10, "bold"))
        self.etiquetaEstado.pack(pady=(10, 5))

        self.listaCanciones = Listbox(self.miniventana1, bg="white")
        self.listaCanciones.pack(fill="both", expand=True, padx=10, pady=5)
        self.listaCanciones.bind("<<ListboxSelect>>", self.escojerCancion)

        self.btnAyuda = Button(self.miniventana1, image=self.iconoAyuda, bg="pink", command=self.mostrarAyuda)
        self.btnAyuda.pack(pady=10, padx=20, fill="x")

        self.btnCargar = Button(self.miniventana1, image=self.iconoBuscarCarpeta, 
                               command=self.seleccionCarpetaForanea, bg="pink")
        self.btnCargar.pack(pady=10, padx=20, fill="x")

        # Elementos en miniventana2 (derecha)
        self.labelEstadoCancion = Label(self.miniventana2, text="Cargando...", bg="blue", fg="yellow",
                                      font=("Old English Text MT", 14, "bold"))
        self.labelEstadoCancion.pack(pady=(50, 50))

        self.barraProgreso = Scale(self.miniventana2, from_=0, to=100, orient=HORIZONTAL, length=300, showvalue=0)
        self.barraProgreso.pack(fill="x", padx=20, pady=30)

        self.labelCancionActual = Label(self.miniventana2, text="Cancion: Nada aun ", bg="blue", fg="yellow",
                                      font=("Old English Text MT", 14, "bold"))
        self.labelCancionActual.pack(pady=5)

        self.labelDuracion = Label(self.miniventana2, text="Duracion: 00:00", bg="blue", fg="yellow",
                                 font=("Old English Text MT", 14, "bold"))
        self.labelDuracion.pack(pady=20)

        self.frameBarras = Frame(self.miniventana2, bg="#ffb300")
        self.frameBarras.pack(pady=10)

        # Controles de ecualización
        self.Bajos = Scale(self.frameBarras, from_=200, to=0, orient="vertical", label='Bajos', command=self.bajos)
        self.Bajos.set(100)
        self.Bajos.pack(side="left", padx=5, pady=20, fill="y", expand=True)

        self.Tono = Scale(self.frameBarras, from_=200, to=0, orient="vertical", label='tonos', command=self.tono)
        self.Tono.set(100)
        self.Tono.pack(side="left", padx=5, pady=20, fill="y", expand=True)

        self.Agudos = Scale(self.frameBarras, from_=200, to=0, orient="vertical", label='Agudos', command=self.agudos)
        self.Agudos.set(100)
        self.Agudos.pack(side="left", padx=5, pady=20, fill="y", expand=True)

        self.Volumen = Scale(self.frameBarras, from_=100, to=0, orient="vertical", label='Volumen', command=self.volumen)
        self.Volumen.set(50)
        self.Volumen.pack(side="left", padx=5, pady=20, fill="y", expand=True)

        # Frame para botones de control
        self.frameBotones = Frame(self.miniventana2, bg="#ffb300")
        self.frameBotones.pack(pady=10)

        # Botones de reproducción
        self.btnAnterior = Button(self.frameBotones, image=self.iconoAnterior, command=self.anteriorCancion, 
                                 width=48, height=48, padx=10, pady=10)
        self.btnAnterior.grid(row=0, column=1, padx=5)

        self.btnDevolver = Button(self.frameBotones, image=self.iconoRetroceder10s, command=self.retroceder10Segundos, 
                                width=48, height=48, padx=10, pady=10)
        self.btnDevolver.grid(row=0, column=0, padx=5)

        self.btnStop = Button(self.frameBotones, image=self.iconoStop, state="disabled", command=self.stop, 
                             width=48, height=48, padx=10, pady=10)
        self.btnStop.grid(row=0, column=2, padx=5)

        self.btnPausa = Button(self.frameBotones, image=self.iconoPausa, state="disabled", command=self.pausa, 
                              width=48, height=48, padx=10, pady=10)
        self.btnPausa.grid(row=0, column=3, padx=5)

        self.btnPlay = Button(self.frameBotones, image=self.iconoPlay, command=self.play, 
                             width=48, height=48, padx=10, pady=10)
        self.btnPlay.grid(row=0, column=4, padx=5)

        self.btnResumen = Button(self.frameBotones, image=self.iconoResumen, state="disabled", command=self.resumen, 
                                width=48, height=48, padx=10, pady=10)
        self.btnResumen.grid(row=0, column=5, padx=5)

        self.btnSiguiente = Button(self.frameBotones, image=self.iconoSiguiente, command=self.siguienteCancion, 
                                  width=48, height=48, padx=10, pady=10)
        self.btnSiguiente.grid(row=0, column=6, padx=5)

        self.btnAvanzar = Button(self.frameBotones, image=self.iconoAdelantar10s, command=self.adelantar10Segundos, 
                                width=48, height=48, padx=10, pady=10)
        self.btnAvanzar.grid(row=0, column=7, padx=5)

        # Tooltips
        Tooltip(self.btnPlay, "Presione para reproducir la canción")
        Tooltip(self.btnPausa, "Presione para pausar")
        Tooltip(self.btnStop, "Presione para detener")
        Tooltip(self.btnResumen, "Presione para reanudar")
        Tooltip(self.btnSiguiente, "Siguiente canción")
        Tooltip(self.btnAnterior, "Canción anterior")
        Tooltip(self.btnAvanzar, "Adelantar 10 segundos")
        Tooltip(self.btnDevolver, "Retroceder 10 segundos")
        Tooltip(self.btnAyuda, "Ayuda")
        Tooltip(self.btnCargar, "Cargar Carpeta desde tu almacenamiento")

        # Carga inicial si existe carpeta "canciones"
        if os.path.exists("canciones"):
            self.cargarCarpetaForanea("canciones")

        # hotkeys
        self.ventana.bind_all('<Control-space>', lambda e: self.pausa())     
        self.ventana.bind_all('<Control-r>', lambda e: self.resumen())   
        self.ventana.bind_all('<Control-s>', lambda e: self.stop())      
        self.ventana.bind_all('<Control-Right>', lambda e: self.siguienteCancion())  
        self.ventana.bind_all('<Control-Left>', lambda e: self.anteriorCancion())  
        self.ventana.bind_all('<Control-f>', lambda e: self.adelantar10Segundos())    
        self.ventana.bind_all('<Control-d>', lambda e: self.retroceder10Segundos()) 
        self.ventana.bind_all('<Control-Return>', lambda e: self.play())   

        self.ventana.mainloop()

    def play(self):
        #if not self.funciones.Canciones:
         #   self.labelEstadoCancion.config(text="No hay canciones cargadas")
          #  return
        
        self.labelEstadoCancion.config(text="Reproduciendo...")
        self.btnPlay.config(state="disabled")
        self.btnPausa.config(state="normal")
        self.btnStop.config(state="normal")
        self.btnResumen.config(state="disabled")
        
        canActual = self.funciones.Canciones[self.funciones.cancionActual]
        #comprobar, 
        notificar = self.funciones.play(canActual)
        #if not comprobar:
         #   self.labelEstadoCancion.config(text=notificar)
          #  return

        self.labelCancionActual.config(text=f"Cancion: {os.path.basename(canActual)}")
        self.funciones.guardarDuracionCancion(canActual)
        self.labelDuracion.config(text=f"00:00 / {self.funciones.convertirTiempo(self.funciones.totalDuracion)}")
        self.barraProgreso.config(to=int(self.funciones.totalDuracion))
        self.actualizarProgreso()

    def stop(self):
        menajeConexion = self.funciones.stop()
        self.labelEstadoCancion.config(text=menajeConexion)
        self.btnPlay.config(state="normal")
        self.btnPausa.config(state="disabled")
        self.btnStop.config(state="disabled")
        self.btnResumen.config(state="disabled")
        self.labelCancionActual.config(text="Cancion: Aun no hay...")
        self.barraProgreso.set(0)
        self.labelDuracion.config(text=" 00:00")

    def pausa(self):
        mensajeComunicacion = self.funciones.pausa()
        self.labelEstadoCancion.config(text=mensajeComunicacion)
        self.btnPlay.config(state="normal")
        self.btnPausa.config(state="disabled")
        self.btnStop.config(state="disabled")
        self.btnResumen.config(state="normal")
        self.actualizarProgreso()

    def resumen(self):
        mensajeComunicacion = self.funciones.resumen()
        self.labelEstadoCancion.config(text=mensajeComunicacion)
        self.btnPlay.config(state="disabled")
        self.btnPausa.config(state="normal")
        self.btnStop.config(state="normal")
        self.btnResumen.config(state="disabled")
        self.actualizarProgreso()

    def siguienteCancion(self):
        self.funciones.cancionActual = self.funciones.siguienteCancion(self.funciones.Canciones)
        self.listaCanciones.selection_clear(0, END)
        self.listaCanciones.selection_set(self.funciones.cancionActual)
        self.btnPlay.config(state="disabled")
        self.btnPausa.config(state="normal")
        self.btnStop.config(state="normal")
        self.btnResumen.config(state="disabled")
        self.play()

    def anteriorCancion(self):
        self.funciones.cancionActual = self.funciones.anteriorCancion(self.funciones.Canciones)
        self.listaCanciones.selection_clear(0, END)
        self.listaCanciones.selection_set(self.funciones.cancionActual)
        self.btnPlay.config(state="disabled")
        self.btnPausa.config(state="normal")
        self.btnStop.config(state="normal")
        self.btnResumen.config(state="disabled")
        self.play()

    def adelantar10Segundos(self):
        comprobar = self.funciones.adelantar10Segundos()
        if not comprobar:
            
            self.btnPlay.config(state="disabled")
            self.btnPausa.config(state="normal")
            self.btnStop.config(state="normal")
            self.btnResumen.config(state="disabled")
    def retroceder10Segundos(self):
        comprobar = self.funciones.retroceder10Segundos()

        if not comprobar:
        
            self.btnPlay.config(state="disabled")
            self.btnPausa.config(state="normal")
            self.btnStop.config(state="normal")
            self.btnResumen.config(state="disabled")
    def volumen(self, valor):
        self.funciones.volumen(valor)

    def bajos(self, valor):
        self.funciones.bajos(valor)

    def tono(self, valor):
        self.funciones.tono(valor)

    def agudos(self, valor):
        self.funciones.agudos(valor)

    def mostrarAyuda(self):
        messagebox.showinfo("Ayuda", 
            "Bienvenido/a \n* Usa los botones para reproducir, pausar, detener, avanzar, devolver, adelantar o retroceder 10 segundos las canciones.\n* Puedes cargar canciones desde carpetas de tu almacenamiento.\n* Puedes usar atajos de teclado como:\n"
            "*Ctrl + Espacio = Pausar\n"
            "*Ctrl + Enter = Reproducir\n"
            "*Ctrl + S = Detener.\n"
            "*Ctrl + Flecha Izquierda/ Derecha = siguiente/anterior cancion. \n"
            "*Ctrl + R = Reanudar\n"
            "*Ctrl + F/D = Adelantar/Retroceder 10 segundos la cancion. \n")

    def escojerCancion(self, event):
        seleccionCAncion = self.listaCanciones.curselection()
        if seleccionCAncion:
            self.funciones.cancionActual = seleccionCAncion[0]

    def seleccionCarpetaForanea(self):
        carpeta = filedialog.askdirectory(title="Escoja la carpeta de canciones")
        if carpeta:
            self.cargarCarpetaForanea(carpeta)

    def cargarCarpetaForanea(self, ubicacionCarpeta):
        comprobar, cancionNombres, textoLabel = self.funciones.cargarCarpetaForanea(ubicacionCarpeta)
        if comprobar:
            self.listaCanciones.delete(0, END)
            for nombre in cancionNombres:
                self.listaCanciones.insert(END, nombre)
            self.etiquetaEstado.config(text=textoLabel)
            self.funciones.cancionActual = 0
            self.listaCanciones.selection_clear(0, END)
            self.listaCanciones.selection_set(0)
        else:
            self.etiquetaEstado.config(text=textoLabel)

    def actualizarProgreso(self):
        convertirSegundos = self.funciones.obtProcesoActualizado()

       
        self.barraProgreso.set(convertirSegundos)
        self.labelDuracion.config(text=f"Duracion: {self.funciones.convertirTiempo(convertirSegundos)} | "
                                     f"{self.funciones.convertirTiempo(self.funciones.totalDuracion)}")

        if self.funciones.verificarReproduccion():
            self.ventana.after(500, self.actualizarProgreso)
        else:
            self.barraProgreso.set(0)

if __name__ == "__main__":
    Reproductor()