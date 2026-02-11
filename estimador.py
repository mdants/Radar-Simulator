import matplotlib.pyplot as plt
import numpy as np

def mapa_range_doppler(conv_fft, frp, fs):
    # Preparando os dados para o plot 3D
    n_ffts = conv_fft.shape[0]  # Número de FFTs (igual ao número de elementos em cada vetor)
    n_frequencias = conv_fft.shape[1]  # Número de frequências (igual ao número de vetores)

    c=300000000
    f = 0.75e9
    lambda_ = c/f
    # Criando arrays para os eixos X, Y e Z
    x = -np.arange(-n_frequencias/2, n_frequencias/2) * (lambda_*frp/64)  # Eixo X: frequências
    y = np.arange(n_ffts) * 1/(int(fs/frp)) * (c/(frp*2*1000))   # Eixo Y: índice da FFT (n-ésimo elemento)
    Z = 10*np.log10(conv_fft) # Eixo Z: magnitude das FFTs
    Z = Z.T
    # Criando uma malha para o plot 3D
    
    fig = plt.figure(figsize=(8,6))
    plt.imshow(Z, aspect='auto', extent=[y[0], y[-1], x[0], x[-1]])

    plt.xlabel('Distância (km)')
    plt.ylabel('Velocidade Radial (m/s)')
    plt.title('Mapa Range-Doppler')
    plt.colorbar(label='Intensidade (dB)')

    return fig

def detection_map(map, frp, legenda):
    # Preparando os dados para o plot 3D
    n_ffts = map.shape[0]  # Número de FFTs (igual ao número de elementos em cada vetor)
    n_frequencias = map.shape[1]  # Número de frequências (igual ao número de vetores)

    c=300000000
    f = 0.75e9
    lambda_ = c/f
    # Criando arrays para os eixos X, Y e Z
    x = -np.arange(-n_frequencias/2, n_frequencias/2) * (lambda_*frp/64)  # Eixo X: frequências
    y = np.arange(n_ffts) * 1/5000 * (c/(frp*2*1000))   # Eixo Y: índice da FFT (n-ésimo elemento)
    
    # Criando uma malha para o plot 3D
    
    fig = plt.figure(figsize=(8,6))
    plt.imshow(map.T, aspect='auto', extent=[y[0], y[-1], x[0], x[-1]])

    plt.xlabel('Distância (km)')
    plt.ylabel('Velocidade Radial (m/s)')
    plt.title(legenda)
    return fig

def plot_threshold_3d(threshold_map, frp, title='Mapa do Threshold (CFAR)', db_scale=False):

    n_ffts = threshold_map.shape[0]  # Número de FFTs (igual ao número de elementos em cada vetor)
    n_frequencias = threshold_map.shape[1]  # Número de frequências (igual ao número de vetores)

    c=300000000
    f = 0.75e9
    lambda_ = c/f
    # Criando arrays para os eixos X, Y e Z
    X, Y = np.meshgrid(-np.arange(-n_frequencias/2, n_frequencias/2) * (lambda_*frp/64), np.arange(n_ffts) * 1/5000 * (c/(frp*2*1000)))

    Z = threshold_map
    if db_scale:
        Z = 10 * np.log10(Z + 1e-12)  # Evita log(0)

    fig = plt.figure(figsize=(10, 7))
    ax = fig.add_subplot(111, projection='3d')

    surf = ax.plot_surface(X, Y, Z, cmap='viridis')

    ax.set_title(title)
    ax.set_xlabel('Range Bins')
    ax.set_ylabel('Velocidade (Doppler) Bins')
    ax.set_zlabel('Threshold (dB)' if db_scale else 'Threshold (linear)')

    fig.colorbar(surf, shrink=0.5, aspect=10, label='Threshold')

    plt.show()

def agrupa_alvo(dados, distancia_tolerancia_km=1, velocidade_tolerancia=50):
    grupos = []
    usado = np.zeros(len(dados), dtype=bool)

    # Converte para numpy array e distância para km
    dados = np.array(dados)
    dados[:, 0] /= 1000  # Converte distância para km
    
    for i, (dist, vel) in enumerate(dados):
            if not usado[i]:
                # Encontra todos os alvos próximos a este
                mask = (np.abs(dados[:, 0] - dist)) < distancia_tolerancia_km
                mask &= (np.abs(dados[:, 1] - vel)) < velocidade_tolerancia
                mask &= ~usado
                
                # Calcula a média do grupo
                if np.any(mask):
                    grupo = dados[mask]
                    media_dist = np.mean(grupo[:, 0]) * 1000  # Converte de volta para metros
                    media_vel = np.mean(grupo[:, 1])
                    if media_vel > 0:
                        media_vel = -(media_vel-velocidade_tolerancia)
                    else:
                        media_vel = -media_vel+velocidade_tolerancia
                    grupos.append([float(media_dist), float(media_vel)])
                    usado[mask] = True
    return grupos

def velocidade_real(alvos1, alvos2, prf1, prf2):

    c=300000000
    f = 0.75e9
    lambda_radar = c/f

    # Calcula os limites de velocidade não ambígua para cada PRF
    vna1 = (lambda_radar * prf1) / 4
    vna2 = (lambda_radar * prf2) / 4

    modulo1 = 2 * vna1
    modulo2 = 2 * vna2

    # Intervalo de busca de n (ajustável conforme o cenário)
    n_range = range(-5, 4)

    alvos = alvos1
    tol = 20

    for i in range(len(alvos)):
        for n in n_range:
            # Calcula o candidato de velocidade real baseado na PRF1
            v_real1 = alvos1[i][1] - n * modulo1
            v_real2 = alvos2[i][1] - n * modulo2
            # Verifica se este candidato é consistente com a PRF2
            
            if abs(v_real1-v_real2) < tol:
                alvos[i][1] = (v_real1+v_real2)/2

    return alvos

import numpy as np