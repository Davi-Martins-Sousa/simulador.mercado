from estrategia import create,start,finish,compra,venda

def aprendizadoSupervisionado(base):
    capital = 0
    posicao = 0
    fechamentos = []
    riqueza = []

    base = create(base)
    
    #base.drop('Date', axis=1, inplace= True)
    base['Retorno'] =  base['Close'].shift(-1) - base['Close']
    base['alvo'] = base['Retorno'].apply(lambda retorno: 1 if retorno > 0 else 0)
    base['SMA-8'] = base['Close'].rolling(window=8).mean()
    base['SMA-32'] = base['Close'].rolling(window=32).mean()
    base['EMA-8'] = base['Close'].ewm(span=8, adjust=False).mean()
    base['EMA-32'] = base['Close'].ewm(span=32, adjust=False).mean()
    
    
    print(base)

aprendizadoSupervisionado('./dados/BBDC4.csv')