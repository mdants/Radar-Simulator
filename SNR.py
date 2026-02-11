import numpy as np

def calculate_snr(Pt, Gt, Gr, lambda_, R, sigma, k, T, B, F):
    # Equação do radar para SNR
    SNR = (Pt * Gt * Gr * lambda_**2 * sigma) / ((4 * np.pi)**3 * R**4 * k * T * B * F)
    
    return SNR

pt = 1e3  # Potência transmitida (1000 W)
gt = 10   # Ganho da antena transmissora (linear)
gr = 10   # Ganho da antena receptora (linear)
lambda_ = 0.03  # Comprimento de onda (30 mm para 10 GHz)
r = 10000  # Distância ao alvo (10 km)
sigma = 1  # Seção transversal do radar (1 m²)
k = 1.38e-23  # Constante de Boltzmann (J/K)
t = 290  # Temperatura (K)
b = 1e6  # Largura de banda (1 MHz)
f = 2  # Fator de ruído (linear)

SNR = calculate_snr(pt, gt, gr, lambda_, r, sigma, k, t, b, f)
print(f"SNR: {10 * np.log10(SNR):.2f} dB")
