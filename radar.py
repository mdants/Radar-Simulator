import numpy as np

# Parâmetros do pulso
frequencia_pulso = 1000  # Frequência do pulso (Hz)
duracao_pulso = 0.01  # Duração do pulso (segundos)
taxa_amostragem = 10000  # Taxa de amostragem (amostras por segundo)
amplitude_pulso = 1.0  # Amplitude do pulso

# Vetor de tempo para o pulso
t_pulso = np.linspace(0, duracao_pulso, int(taxa_amostragem * duracao_pulso), endpoint=False)

# Gerar o pulso (uma senoide, por exemplo)
pulso = amplitude_pulso * np.sin(2 * np.pi * frequencia_pulso * t_pulso)

# Salvar o pulso em um arquivo TXT
np.savetxt('pulso_emitido.txt', pulso)

print("Pulso emitido salvo em 'pulso_emitido.txt'.")