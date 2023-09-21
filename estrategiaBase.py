from estrategia import create,start,finish,compra,venda

def update(capital, posicao, precoOntem, precoHoje, primeiroUltimoDia):
    if precoOntem is not None and primeiroUltimoDia is False:
        if precoHoje > precoOntem and posicao == 1:
            capital, posicao = venda(capital, posicao, precoHoje, 2)
        elif precoHoje < precoOntem and posicao == -1:
            capital, posicao = compra(capital, posicao, precoHoje, 2)
    elif precoOntem is not None and primeiroUltimoDia is True:
        if posicao == 1:
            capital, posicao = venda(capital, posicao, precoHoje, 1)
        elif posicao == -1:
            capital, posicao = compra(capital, posicao, precoHoje, 1)
        elif posicao == 0:
            if precoHoje > precoOntem and posicao > -1:
                capital, posicao = venda(capital, posicao, precoHoje, 1)
            elif precoHoje < precoOntem and posicao < 1:
                capital, posicao = compra(capital, posicao, precoHoje, 1)

    return capital, posicao, precoHoje

def base(base):
    capital = 0
    posicao = 0
    precoOntem = None
    fechamentos = []
    riqueza = []

    base = create(base)
    
    for indice, hoje in base.iterrows():
        #start(hoje['Date'])
        capital, posicao, precoOntem = update(capital, posicao, precoOntem, hoje['Close'],base.index[-1] == indice or base.index[1] == indice)
        riquezaAtual = capital + posicao * hoje["Close"]
        fechamentos.append(hoje["Close"])
        riqueza.append(float(riquezaAtual))
        #finish(hoje['Date'])
        print(f'Capital: {capital}\tAções em posse: {posicao}\tRiqueza: {riquezaAtual}')

    return fechamentos,riqueza

base('./dados/BBDC4.csv')
