from estrategia import create,start,finish,compra,venda



def aprendizadoSupervisionado(base):
    capital = 0
    posicao = 0
    fechamentos = []
    riqueza = []

    base = create(base)
    
    base['Close_Amanha'] = base['Close'].shift(-1)
    base['Retorno'] = base['Close_Amanha'] - base['Close']
    base.drop('Close_Amanha', axis=1, inplace=True)
    base.drop('Date', axis=1)
    base['alvo'] = base['Retorno'].apply(lambda retorno: 1 if retorno > 0 else 0)


    print(base)

aprendizadoSupervisionado('./dados/BBDC4.csv')