from estrategia import create,start,finish,compra,venda

def update(capital,posicao,precoHoje,mediaLonga,mediaCurta,primeiroUltimoDia):
    if primeiroUltimoDia is False and mediaLonga != None:
        if mediaLonga >= mediaCurta and posicao == 1:
            capital, posicao = venda(capital, posicao, precoHoje, 2)
        elif mediaLonga <= mediaCurta and posicao == -1:
            capital, posicao = compra(capital, posicao, precoHoje, 2)
    elif primeiroUltimoDia is True and mediaLonga != None:
        if posicao == 1:
            capital, posicao = venda(capital, posicao, precoHoje, 1)
        elif posicao == -1:
            capital, posicao = compra(capital, posicao, precoHoje, 1)
        elif posicao == 0:
            if mediaLonga >= mediaCurta:
                capital, posicao = venda(capital, posicao, precoHoje, 1)
            elif mediaLonga <= mediaCurta:
                capital, posicao = compra(capital, posicao, precoHoje, 1)

    return capital, posicao

def media(data, periodo):
    media_movel = data['Close'].rolling(window=periodo).mean()
    return media_movel

def mediaMovel(base):
    capital = 0
    posicao = 0
    fechamentos = []
    riqueza = []

    base = create(base)
    base['MediaMovelLonga'] = media(base, 20)
    base['MediaMovelCurta'] = media(base, 7)
    
    for indice, hoje in base.iterrows():
        #start(hoje['Date'])
        capital, posicao = update(capital, posicao, hoje['Close'],hoje['MediaMovelLonga'],hoje['MediaMovelCurta'],base.index[-1] == indice or base.index[20] == indice)
        riquezaAtual = capital + posicao * hoje["Close"]
        fechamentos.append(hoje["Close"])
        riqueza.append(float(riquezaAtual))
        #finish(hoje['Date'])
        print(f'Capital: {capital}\tAções em posse: {posicao}\tRiqueza: {riquezaAtual}')

    return fechamentos,riqueza

mediaMovel('dados/BBDC4.csv')