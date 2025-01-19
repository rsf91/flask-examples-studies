import numpy as np

def sabr_volatility(f, k, t, alpha, beta, rho, volvol):
    """
    Calcula a volatilidade implícita usando o modelo SABR.

    Parâmetros:
    f      : float - Forward price (preço à vista ajustado para a entrega futura)
    k      : float - Strike price (preço de exercício)
    t      : float - Tempo até a expiração (em anos)
    alpha  : float - Volatilidade no tempo zero
    beta   : float - Parâmetro de elasticidade (0 <= beta <= 1)
    rho    : float - Correlação entre forward e volatilidade (-1 <= rho <= 1)
    volvol : float - Volatilidade da volatilidade (vol of vol)

    Retorno:
    float - Volatilidade implícita calculada para o strike especificado.
    """

    # Se o preço forward é igual ao strike, usar uma fórmula simplificada
    if f == k:
        fk = f ** (1 - beta)
        term1 = alpha / fk
        term2 = 1 + ((1 - beta) ** 2 * alpha ** 2 / (24 * fk ** 2) +
                     0.25 * rho * beta * alpha * volvol / fk +
                     (2 - 3 * rho ** 2) * volvol ** 2 / 24) * t
        return term1 * term2
    else:
        # Diferença entre forward e strike
        fk = (f * k) ** ((1 - beta) / 2)
        z = volvol / alpha * fk * np.log(f / k)
        chi_z = np.log((np.sqrt(1 - 2 * rho * z + z ** 2) + z - rho) / (1 - rho))
        
        # Fórmula geral da volatilidade do modelo SABR
        vol = (alpha / (fk * (1 + (1 - beta) ** 2 / 24 * np.log(f / k) ** 2 +
                              (1 - beta) ** 4 / 1920 * np.log(f / k) ** 4))) * (z / chi_z)

        return vol

def sabr_smile(f, t, alpha, beta, rho, volvol, strikes):
    """
    Calcula a curva de volatilidade implícita para uma gama de strikes.

    Parâmetros:
    f       : float - Forward price
    t       : float - Tempo até a expiração (em anos)
    alpha   : float - Volatilidade inicial
    beta    : float - Parâmetro de elasticidade
    rho     : float - Correlação
    volvol  : float - Volatilidade da volatilidade
    strikes : list or np.array - Lista de preços de exercício

    Retorno:
    np.array - Volatilidades implícitas correspondentes aos strikes fornecidos.
    """
    volatilities = np.array([sabr_volatility(f, k, t, alpha, beta, rho, volvol) for k in strikes])
    return volatilities

# Exemplo de uso
if __name__ == "__main__":
    # Parâmetros do modelo SABR
    f0 = 100       # Forward price
    t = 1.0        # Tempo até expiração (1 ano)
    alpha = 0.2    # Volatilidade inicial
    beta = 0.5     # Parâmetro de elasticidade
    rho = -0.3     # Correlação entre preço e volatilidade
    volvol = 0.4   # Volatilidade da volatilidade

    # Pontos de strike a serem avaliados
    strikes = np.linspace(80, 120, 10)

    # Cálculo das volatilidades implícitas
    vol_smile = sabr_smile(f0, t, alpha, beta, rho, volvol, strikes)

    # Exibir resultados
    print(strikes)
    print(vol_smile)
    #for strike, vol in zip(strikes, vol_smile):
    #    print(f"Strike: {strike:.2f}, Implied Volatility: {vol:.4f}")
