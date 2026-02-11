import numpy as np

def calcular_ganho_ponto_a_ponto(x1, x2, modo_db=False):
    """
    Calcula o ganho ponto a ponto entre dois sinais.

    Parâmetros:
    x1 : ndarray
        Sinal de entrada (referência)
    x2 : ndarray
        Sinal de saída (ou processado)
    modo_db : bool
        Se True, retorna o ganho em dB

    Retorna:
    ganho : ndarray
        Vetor de ganho ponto a ponto (linear ou dB)
    """

    # Previne divisão por zero
    eps = 1e-12
    x1_abs = np.abs(x1)
    x2_abs = np.abs(x2)

    ganho = x2_abs / (x1_abs + eps)

    if modo_db:
        ganho = 20 * np.log10(ganho + eps)

    return ganho

# Exemplo de uso
if __name__ == "__main__":
    # Sinais de exemplo
    x1 = np.array([1, 2, 3, 4, 5], dtype=float)
    x2 = np.array([2, 4, 3, 2, 1], dtype=float)

    ganho_linear = calcular_ganho_ponto_a_ponto(x1, x2, modo_db=False)
    ganho_db = calcular_ganho_ponto_a_ponto(x1, x2, modo_db=True)

    print("Ganho linear:", ganho_linear)
    print("Ganho em dB:", ganho_db)
