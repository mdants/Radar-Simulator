import numpy as np
import matplotlib.pyplot as plt
import detector
import alvo
import estimador
import interface

# Parâmetros
fs = 10e6
tau = 30e-6
frp = [2e3, 2.5e3]
prt = [1/ x for x in frp]
B = 3e6
fc = 0
n_pulsos = 32
Pfa = 1e-6

c=300000000
f = 0.75e9
lambda_ = c/f

# Cenário
alvos = np.array(alvo.ler_cenario("cenario.txt"))

t = np.linspace(0, prt[0], int(fs*prt[0]))
t2 = np.linspace(0, prt[1], int(fs*prt[1])) 

# Burst
matriz_pulsos_emitidos, matriz_pulsos_recebidos = alvo.burst(n_pulsos, t, tau, frp[0], fc, B, fs, alvos)
matriz_pulsos_emitidos2, matriz_pulsos_recebidos2 = alvo.burst(n_pulsos, t2, tau, frp[1], fc, B, fs, alvos)

# Filtro Casado
compressao_range = detector.compressao_em_range(n_pulsos, fs, matriz_pulsos_emitidos, matriz_pulsos_recebidos)
compressao_range2 = detector.compressao_em_range(n_pulsos, fs, matriz_pulsos_emitidos2, matriz_pulsos_recebidos2)

# g_fc = calculos.ganho_ponto_a_ponto(matriz_pulsos_recebidos, compressao_range)

# Integração de pulsos
pulsos_integrados = detector.integra_pulsos(compressao_range)
pulsos_integrados2 = detector.integra_pulsos(compressao_range2)

# Mapa Range Doppler
fig1 = estimador.mapa_range_doppler(pulsos_integrados, frp[0], fs)
fig2 = estimador.mapa_range_doppler(pulsos_integrados2, frp[1], fs)

# Subplot módulo
plt.figure()

plt.subplot(3,1,1)
plt.plot(t*1000, np.imag(matriz_pulsos_emitidos[0]))
plt.title('Pulso Transmitido')

plt.subplot(3,1,2)
plt.plot(t*1000, np.imag(matriz_pulsos_recebidos[0]))
plt.title('Pulso Recebido')

plt.subplot(3,1,3)
plt.plot(t*1000, 20*np.log10(abs(compressao_range[0])/max(abs(compressao_range[0]))))
plt.title('Compressão em range')

plt.show()

# Neyman-Pearson (1) / CA-CFAR (2)
detections_map, fig3 = detector.cfar_np(2, pulsos_integrados, frp[0])
detections_map2, fig4 = detector.cfar_np(2, pulsos_integrados2, frp[1])

# Identificação de alvos
alvos_real = detector.detections(detections_map, frp[0])
alvos_real2 = detector.detections(detections_map2, frp[1])

# Tratamento de ambiguidade
alvos_real = estimador.agrupa_alvo(alvos_real, 1.5, lambda_*frp[0]/(2*n_pulsos))
alvos_real2 = estimador.agrupa_alvo(alvos_real, 1.5, lambda_*frp[0]/(2*n_pulsos))

print(alvos_real)
print(alvos_real2)

alvos_definitivo = estimador.velocidade_real(alvos_real, alvos_real2, frp[0], frp[1])

# Interface
interface.criar_interface(fig1, fig2, fig3, fig4, alvos_definitivo)