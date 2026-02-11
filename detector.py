import numpy as np
from scipy.fftpack import fft, fftfreq, ifft, fftshift
from estimador import detection_map, plot_threshold_3d
from sinal import hamming
from calculos import energia

def compressao_em_range(n_pulsos, fs, matriz_pulsos_tx, matriz_pulsos_rx):
    conv = []

    for n in range(n_pulsos):
        sinal_normalizado_tx = matriz_pulsos_tx[n]/np.sqrt(energia(matriz_pulsos_tx[n]))
        # Janelamento Hamming
        sinal_janelado_tx = hamming(sinal_normalizado_tx)
        
        # s(t) -> s*(-t) = h(t)
        sinal_complexo_tx = np.conj(sinal_janelado_tx[::-1])

        sinal_complexo_recebido = matriz_pulsos_rx[n]
        # Correlação 
        sinal_complexo_tx = fft(sinal_complexo_tx)
        sinal_complexo_recebido = fft(sinal_complexo_recebido)

        conv_ = sinal_complexo_tx * sinal_complexo_recebido
        conv_ = ifft(conv_)
        conv.append(conv_)
        
    conv = np.array(conv) 

    return conv

def integra_pulsos(conv):

    conv_transp = conv.T
    conv_fft = np.fft.fft(conv_transp, axis=1)
    conv_fft = np.concatenate((conv_fft.T[len(conv_fft.T) // 2:], conv_fft.T[:len(conv_fft.T) // 2]))
    conv_fft = conv_fft[::-1]
    conv_fft = abs(conv_fft.T)

    return conv_fft

def detections(detections, frp):
   
    c=300000000
    f = 0.75e9
    lambda_ = c/f
    fs = 10e6
    
    # Encontra os índices dos alvos detectados
    target_indices = np.argwhere(detections)
    
    n_ffts = detections.shape[0]  # Número de FFTs (igual ao número de elementos em cada vetor)
    n_frequencias = detections.shape[1]  # Número de frequências (igual ao número de vetores)

    range_bins = np.arange(n_ffts) * 1/(int(fs/frp)) * (c/(frp*2)) 
    velocity_bins = -np.arange(-n_frequencias/2, n_frequencias/2) * (lambda_*frp/64)

    # Cria a lista de alvos no formato solicitado
    targets = []
    for idx in target_indices:
        range_idx, velocity_idx = idx
        target_range = range_bins[range_idx]
        target_velocity = velocity_bins[velocity_idx]
        
        targets.append([float(target_range), float(target_velocity)])
    
    return targets

def np_threshold(rd_map, Pfa, noise_power):
    # Threshold fixo baseado na distribuição exponencial
    threshold = -noise_power * np.log(Pfa) * 1e8
    print(threshold)

    # Geração do mapa de detecção
    detection_map = np.zeros_like(rd_map)
    detection_map[rd_map > threshold] = rd_map[rd_map > threshold]

    mapa_filtrado, picos = filtrar_meia_potencia_picos(detection_map)
    
    return threshold, mapa_filtrado

def ca_cfar(rd_map, N=8, G=2, Pfa=1e-6):
    n_rows, n_cols = rd_map.shape
    threshold_map = np.zeros_like(rd_map)
    detection_map = np.zeros_like(rd_map)

    total_training = 2 * N
    alpha = total_training * (Pfa ** (-1 / total_training) - 1)

    for row in range(n_rows):
        signal = rd_map[row, :]
        threshold = np.zeros(n_cols)
        detections = np.zeros(n_cols)

        for i in range(n_cols):
            # Índices das células de treinamento
            guard_range = np.arange(i - G, i + G + 1) % n_cols
            training_range = np.arange(i - (N + G), i + (N + G) + 1) % n_cols

            # Remover células de guarda e a própria célula de teste
            training_cells = np.setdiff1d(training_range, guard_range)

            noise_level = np.mean(signal[training_cells])
            threshold[i] = alpha * noise_level

            if signal[i] > threshold[i]:
                detections[i] = signal[i]

        threshold_map[row, :] = threshold
        detection_map[row, :] = detections

    mapa_filtrado, picos = filtrar_meia_potencia_picos(detection_map)
    
    return threshold_map, mapa_filtrado

def cfar_np(k, conv_fft, frp):
    Pfa = 1e-6

    B = 3e6
    T = 290
    F = 20
    k_boltzman = 1.38e-23

    Pn = k_boltzman * T * B * F

    if k == 1:
        threshold, detections_map = np_threshold(conv_fft, Pfa, Pn)
        fig = detection_map(detections_map, frp, 'Neyman-Pearson')
    if k == 2:
        threshold_map, detections_map = ca_cfar(conv_fft, 10, 2, Pfa)
        fig = detection_map(detections_map, frp, 'CA-CFAR')
        #plot_threshold_3d(threshold_map, frp)
    
    return detections_map, fig

def filtrar_meia_potencia(detection_map):
   
    # Identificar as detecções (valores > 0)
    valores_detectados = detection_map[detection_map > 0]

    # Valor máximo dentre as detecções
    pico = np.max(valores_detectados)
    limiar_meia_potencia = 0.5 * pico
    
    # Criar novo mapa aplicando o critério
    mapa_filtrado = np.where(detection_map >= limiar_meia_potencia, detection_map, 0)

    return mapa_filtrado

from scipy.ndimage import maximum_filter

def filtrar_meia_potencia_picos(detection_map, tamanho_janela=7, debug=False):

    assert tamanho_janela % 2 == 1, "A janela deve ter tamanho ímpar."

    half = tamanho_janela // 2
    mapa_filtrado = np.zeros_like(detection_map)
    picos = []

    # Encontra picos locais (máximos na vizinhança)
    max_local = maximum_filter(detection_map, size=tamanho_janela, mode='constant')
    mascara_picos = (detection_map == max_local) & (detection_map > 0)

    indices_picos = np.argwhere(mascara_picos)

    for i, j in indices_picos:
        pico = detection_map[i, j]
        limiar = 0.5 * pico
        picos.append((i, j, pico))

        if debug:
            print(f"Pico detectado em ({i}, {j}) com potência {pico:.2f}, limiar = {limiar:.2f}")

        # Define limites da janela ao redor do pico
        i_min = max(i - half, 0)
        i_max = min(i + half + 1, detection_map.shape[0])
        j_min = max(j - half, 0)
        j_max = min(j + half + 1, detection_map.shape[1])

        # Aplica meia potência na janela
        bloco = detection_map[i_min:i_max, j_min:j_max]
        bloco_filtrado = np.where(bloco >= limiar, bloco, 0)

        # Atualiza mapa filtrado
        mapa_filtrado[i_min:i_max, j_min:j_max] = np.maximum(
            mapa_filtrado[i_min:i_max, j_min:j_max],
            bloco_filtrado
        )

    return mapa_filtrado, picos