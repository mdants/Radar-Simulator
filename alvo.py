import numpy as np
import matplotlib.pyplot as plt
from sinal import ruido, chirp_pulsado
import calculos
import pre_proc
from scipy.signal import hilbert

def sinal_recebido(alvos, fs, f, prt, n, k, B, t, pulso_emitido):
    c=300000000
    f = 0.75e9
    lambda_ = c/f

    pulso_recebido = pulso_emitido

    distancia = alvos[k][0] - n*alvos[k][1]*prt
    amplitude_atenuada = np.sqrt(calculos.pot_recebida(1000, 600, lambda_, alvos[k][0], 1)) * np.exp(1j*4*np.pi*distancia/lambda_)
    
    pulso_atrasado = np.zeros(len(pulso_recebido), dtype=complex)
    
    ko = int(2*distancia*fs/c)
    
    for i in range(ko, len(pulso_recebido)):
        pulso_atrasado[i]=pulso_recebido[i-ko]
    
    pulso_atenuado = pulso_atrasado * amplitude_atenuada + ruido(B, t)
    
    return pulso_atenuado

def burst(n_pulsos, t, tau, frp, fc, B, fs, alvos):
    matriz_pulsos_recebidos = []
    matriz_pulsos_emitidos = []

    for n in range(n_pulsos):
        # Sinal emitido
        pulso_emitido = chirp_pulsado(t, tau, fc, B)
        matriz_pulsos_emitidos.append(pulso_emitido)
        
        # Sinal recebido
        pulso_recebido = np.zeros(len(pulso_emitido), dtype=complex)

        for k in range(len(alvos)):
            pulso_recebido += sinal_recebido(alvos, fs, B/2, 1/frp, n, k, B, t, pulso_emitido)
            
        matriz_pulsos_recebidos.append(pulso_recebido)
    
    return matriz_pulsos_emitidos, matriz_pulsos_recebidos

def ler_cenario(nome_arquivo):
   
    # Carrega todas as linhas não vazias em um array NumPy
    dados = np.loadtxt(nome_arquivo, comments=None, dtype=float)  # comments=None evita que linhas vazias sejam ignoradas como comentários
    
    # Verifica se há um número par de valores (distância + velocidade)
    if len(dados) % 2 != 0:
        print("Aviso: Número ímpar de linhas. Último valor será ignorado.")
        dados = dados[:-1]  # Remove o último elemento se for ímpar
    
    # Redimensiona o array para N linhas x 2 colunas (distância, velocidade)
    dados = dados.reshape(-1, 2)
    
    return dados # Ou retorne `dados` diretamente se preferir um array NumPy
