import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import numpy as np
import UV

def criar_interface(fig1, fig2, fig3, fig4, alvos_real):
    janela = tk.Tk()
    janela.title("Simulador Radar")
    #janela.geometry("1800x900")
    janela.state('zoomed')
    janela.protocol("WM_DELETE_WINDOW", janela.quit)
    janela.iconbitmap('radar.ico')

    # Criar notesook (as abas)
    notebook = ttk.Notebook(janela)
    notebook.pack(fill=tk.BOTH, expand=True)

    # Criar as abas
    aba1 = ttk.Frame(notebook)
    aba2 = ttk.Frame(notebook)
    aba3 = ttk.Frame(notebook)

    notebook.add(aba1, text="Mapas Range-Doppler")
    notebook.add(aba2, text="Mapas Detecção")
    notebook.add(aba3, text="U.V.")

    # ============== Aba 1 ==============
    aba1.columnconfigure(0, weight=1)
    aba1.columnconfigure(1, weight=1)
    aba1.rowconfigure(0, weight=1)

    frame1 = ttk.Frame(aba1)
    frame1.grid(row=0, column=0, sticky="nsew")

    frame2 = ttk.Frame(aba1)
    frame2.grid(row=0, column=1, sticky="nsew")

    canvas1 = FigureCanvasTkAgg(fig1, master=frame1)
    canvas1.draw()
    canvas1.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    canvas2 = FigureCanvasTkAgg(fig2, master=frame2)
    canvas2.draw()
    canvas2.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    # ============== Aba 2 ==============
    aba2.columnconfigure(0, weight=1)
    aba2.columnconfigure(1, weight=1)
    aba2.rowconfigure(0, weight=1)

    frame3 = ttk.Frame(aba2)
    frame3.grid(row=0, column=0, sticky="nsew")

    frame4 = ttk.Frame(aba2)
    frame4.grid(row=0, column=1, sticky="nsew")

    canvas3 = FigureCanvasTkAgg(fig3, master=frame3)
    canvas3.draw()
    canvas3.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    canvas4 = FigureCanvasTkAgg(fig4, master=frame4)
    canvas4.draw()
    canvas4.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    # ============== Aba 3 ==============
    radar = UV.RadarPPI(alcance_max=80)
    radar.carregar_alvos(alvos_real)
    radar.configurar_display()
    radar.plotar_alvos()

    def atualizar_radar():
        radar.atualizar_varredura()
        canvas5.draw()
        aba3.after(10, atualizar_radar)  # atualiza a cada 100 ms

    canvas5 = FigureCanvasTkAgg(radar.fig, master=aba3)
    canvas5.draw()
    canvas5.get_tk_widget().pack(fill='both', expand=True)

    atualizar_radar()

    janela.mainloop()
