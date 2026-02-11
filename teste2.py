def velocidade_real_duas_prfs(v1, v2, prf1, prf2, lambda_radar):
    """
    Calcula a velocidade real de um alvo a partir das velocidades aparentes medidas em duas PRFs.
    
    Parâmetros:
    - v1: velocidade aparente medida na PRF1 (em m/s)
    - v2: velocidade aparente medida na PRF2 (em m/s)
    - prf1: frequência de repetição de pulso 1 (em Hz)
    - prf2: frequência de repetição de pulso 2 (em Hz)
    - lambda_radar: comprimento de onda do radar (em metros)

    Retorna:
    - Lista com as velocidades reais possíveis (em m/s)
    """

    # Calcula os limites de velocidade não ambígua para cada PRF
    vna1 = (lambda_radar * prf1) / 4
    vna2 = (lambda_radar * prf2) / 4

    modulo1 = 2 * vna1
    modulo2 = 2 * vna2

    # Intervalo de busca de n (ajustável conforme o cenário)
    n_range = range(-10, 11)

    candidatos = []

    for n in n_range:
        # Calcula o candidato de velocidade real baseado na PRF1
        vcand = v1 + n * modulo1

        # Verifica se este candidato é consistente com a PRF2
        resto = (vcand - v2) % modulo2

        # Critério de aceitação (tolerância para erros numéricos)
        if resto < 1e-6 or abs(resto - modulo2) < 1e-6:
            candidatos.append(vcand)

    # Remove duplicatas e ordena
    candidatos = sorted(list(set(candidatos)))

    return candidatos

# Dados do radar e medidas
lambda_radar = 0.03  # metros (ex.: banda X)
prf1 = 1000          # Hz
prf2 = 1200          # Hz

v1 = 2               # m/s (velocidade medida na PRF1)
v2 = -7              # m/s (velocidade medida na PRF2)

# Chama a função
velocidades_reais = velocidade_real_duas_prfs(v1, v2, prf1, prf2, lambda_radar)

# Mostra o resultado
print("Velocidade real possível(s):", velocidades_reais)