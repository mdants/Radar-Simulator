import numpy as np
from scipy.fftpack import fft, fftfreq, ifft, fftshift
from calculos import pot_sinal_1D
import matplotlib.pyplot as plt

def ddc(sinal, fator_decimacao):

    if fator_decimacao <= 0:
        raise ValueError("O fator de decimação deve ser maior que zero.")
    
    # Seleciona uma amostra a cada 'fator_decimacao' amostras
    sinal_decimado = sinal[::fator_decimacao]
    
    return sinal_decimado

def hilbert_(sinal_real, fs):
    fi = 2.5e6
    t = np.arange(len(sinal_real)) / fs
    
    # Deslocamento para frequencia intermediária
    sinal_fi = sinal_real * np.cos(2 * np.pi * fi * t)

    # Aplicar Transformada de Fourier
    y_fft = fft(sinal_fi)  # Transformada de Fourier do sinal complexo
    n = len(sinal_fi)
    freqs = fftfreq(n, 1/fs)

    # Selecionar metade da fft e fft inversa
    y_fft2 = y_fft.copy()
    y_fft2[freqs < 0] = 0
    y_fft2[freqs >= 0] = 2 * y_fft2[freqs >= 0]
    
    sinal_complexo_fi = ifft(y_fft2)
    
    sinal_complexo = sinal_complexo_fi * np.exp(-1j * 2 * np.pi * fi * t)

    return sinal_complexo

def hilbert_2(sinal_real, fs):

    # Aplicar Transformada de Fourier
    y_fft = fft(sinal_real)  # Transformada de Fourier do sinal complexo
    n = len(sinal_real)
    freqs = fftfreq(n, 1/fs)

    # Selecionar metade da fft e fft inversa
    y_fft2 = y_fft.copy()
    y_fft2[freqs < 0] = 0
    y_fft2[freqs >= 0] = 2 * y_fft2[freqs >= 0]
    
    sinal_complexo = ifft(y_fft2)

    return sinal_complexo