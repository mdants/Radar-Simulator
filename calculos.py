import numpy as np

def pot_sinal_1D(sinal):
    n = len(sinal)
    pot = 0

    for i in range(n):
        pot += abs(sinal[i]**2)
    
    pot = pot/n

    return pot

def energia(sinal):
    n = len(sinal)
    pot = 0

    for i in range(n):
        pot += abs(sinal[i]**2)

    return pot

def pot_recebida(Pt, G, lambda_, R, sigma):
    # Equação do radar para SNR
    pr = (Pt * G * G * lambda_**2 * sigma) / ((4 * np.pi)**3 * R**4)
    
    return float(pr)

def SNR(Pt, G, lambda_, R, sigma, B, F, k = 1.38e-23, T = 290):
    # Equação do radar para SNR
    snr = (Pt * G * G * lambda_**2 * sigma) / ((4 * np.pi)**3 * R**4 * k * T * B * F)
    
    return float(snr)

def ganho_ponto_a_ponto(x1, x2):
    matriz_ganhos = []
    n = len(x1)
    # Previne divisão por zero
    for i in range(n):
        eps = 1e-12
        x1[i] = np.abs(x1[i])
        x2[i] = np.abs(x2[i])

        ganho = x2[i]/(x1[i]+eps)

        matriz_ganhos.append(ganho)

    return matriz_ganhos