import numpy as np

def chirp(t, fc, B, phi0=0):

    k = B/t[-1] 
    f0 = fc - B/2

    phase = 2 * np.pi * (f0 * t + 0.5 * k * t**2) + np.deg2rad(phi0)
    
    chirp_signal = np.sqrt(1000)*np.exp(1j*phase)
    
    return chirp_signal

def chirp_pulsado(t, tau, fc, B, phi0=0):  
    # Inicializar o sinal periódico com zeros
    sinal_periodico = np.zeros_like(t, dtype=complex)

    # Índices correspondentes no vetor de tempo
    indices = (t >= 0) & (t < tau)

    # Gerar o chirp no intervalo atual
    sinal_periodico[indices] = chirp(t[indices], fc, B, phi0)

    return sinal_periodico

def ruido(B, t):
    k = 1.38e-23
    T = 290
    F = 20  # Fator de ruído (ideal)
    Pn = k * T * B * F
    sigma_n = np.sqrt(Pn/2)

    noise = np.random.normal(0, sigma_n, len(t)) + 1j*np.random.normal(0, sigma_n, len(t))
 
    return noise

def hamming(sinal):
    fs = 10e6 
    tau = 30e-6

    N = int(fs*tau)

    sinal = sinal.copy()

    # Gera janela de Hamming para a duração do pulso
    janela = np.hamming(N)

    # Aplica a janela ao trecho do pulso
    sinal[0:N] *= janela

    return sinal
