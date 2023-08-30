import pandas as pd

def create(base):
    base = pd.read_csv(base)
    return base

def start(data):
    print('Início do dia: {data}')

def update(capital,posicao,precoOntem,precoHoje,ultimoDia):
    if precoOntem is not None and ultimoDia is False:
        if precoHoje > precoOntem and posicao > -1:
            capital,posicao,precoHoje = venda(capital,posicao,precoHoje,2)
        elif precoHoje < precoOntem and posicao < 1:
           capital,posicao,precoHoje = compra(capital,posicao,precoHoje,2)
    elif precoOntem is not None and ultimoDia is True:
        if posicao > 0:
            capital,posicao,precoHoje = venda(capital,posicao,precoHoje,1)
        elif posicao < 0:
            capital,posicao,precoHoje = compra(capital,posicao,precoHoje,1)

    return capital,posicao,precoHoje

def compra(capital,posicao,precoHoje,volume):
    posicao += volume 
    capital += volume * precoHoje - 0.02 # preço de hoje - slippage
    return capital,posicao,precoHoje

def venda(capital,posicao,precoHoje, volume):
    posicao -= volume
    capital -= volume * precoHoje + 0.02 # preço de hoje + slippage
    return capital,posicao,precoHoje

def finish(data):
    print('Fim do dia: {data}')

def main():

    capital = 0
    #estado = 0 # long/short -1/1
    posicao = 0 # quantidade de ações compradas
    precoOntem = None # preço de ontem
    base = create('dados/PETR3.SA.csv')

    for indice, hoje in base.iterrows():
        #start(hoje['Date'])
        capital,posicao,precoOntem = update(capital,posicao,precoOntem,hoje['Close'],base.index[-1]==indice or base.index[0]==indice)
        #finish(hoje['Date'])
    
    print(f'Capital: {capital}\nAções em posse: {posicao}')

main()