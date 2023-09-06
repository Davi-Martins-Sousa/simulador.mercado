import pandas as pd
import matplotlib.pyplot as plt

def create(base):
    base = pd.read_csv(base)
    return base

def start(data):
    print(f'Início do dia: {data}')

def update(capital, posicao, precoOntem, precoHoje, primeiroUltimoDia):
    if precoOntem is not None and primeiroUltimoDia is False:
        if precoHoje > precoOntem and posicao > -1:
            capital, posicao, precoHoje = venda(capital, posicao, precoHoje, 2)
        elif precoHoje < precoOntem and posicao < 1:
            capital, posicao, precoHoje = compra(capital, posicao, precoHoje, 2)
    elif precoOntem is not None and primeiroUltimoDia is True:
        if posicao > 0:
            capital, posicao, precoHoje = venda(capital, posicao, precoHoje, 1)
        elif posicao < 0:
            capital, posicao, precoHoje = compra(capital, posicao, precoHoje, 1)
        elif posicao == 0:
            if precoHoje > precoOntem and posicao > -1:
                capital, posicao, precoHoje = venda(capital, posicao, precoHoje, 1)
            elif precoHoje < precoOntem and posicao < 1:
                capital, posicao, precoHoje = compra(capital, posicao, precoHoje, 1)

    return capital, posicao, precoHoje

def compra(capital, posicao, precoHoje, volume):
    posicao += volume
    capital += volume * precoHoje - 0.00  # preço de hoje - slippage
    return capital, posicao, precoHoje

def venda(capital, posicao, precoHoje, volume):
    posicao -= volume
    capital -= volume * precoHoje + 0.00  # preço de hoje + slippage
    return capital, posicao, precoHoje

def finish(data):
    print(f'Fim do dia: {data}')

def main():
    capital = 0
    posicao = 0
    precoOntem = None
    fechamentos = []
    riqueza = []
    base = create('dados/BBDC4.csv')

    
    for indice, hoje in base.iterrows():
        #start(hoje['Date'])
        capital, posicao, precoOntem = update(capital, posicao, precoOntem, hoje['Close'],base.index[-1] == indice or base.index[1] == indice)
        riqueza_atual = capital - posicao * hoje["Close"]
        fechamentos.append(hoje["Close"])
        riqueza.append(float(riqueza_atual))
        #finish(hoje['Date'])
        print(f'Capital: {capital}\tAções em posse: {posicao}\tRiqueza: {riqueza_atual}')

    # Agora, vamos criar um gráfico com os valores de fechamento e a riqueza
    plt.figure(figsize=(12, 6))
    plt.plot(fechamentos, label='Fechamento', marker='')
    plt.plot(riqueza, label='Riqueza', marker='')
    plt.xlabel('Dia')
    plt.ylabel('Valor')
    plt.title('Evolução do Fechamento e Riqueza ao longo do tempo')
    plt.legend()
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()
