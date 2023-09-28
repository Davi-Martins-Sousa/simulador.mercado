import pandas as pd
import talib
import os
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from estrategia import create,start,finish,compra,venda

def update(capital,posicao,precoHoje,decisao,ultimoDia):
    if ultimoDia == False :
        if decisao == 1:
            capital, posicao = compra(capital, posicao, precoHoje, 1)
        else:
            capital, posicao = venda(capital, posicao, precoHoje, 1)
    else:
        if posicao < 0:
            capital, posicao = venda(capital, posicao, precoHoje, posicao)
        elif posicao > 0:
            capital, posicao = compra(capital, posicao, precoHoje, posicao)
    return capital, posicao

def aprendizadoSupervisionado(base_path):
    # Carregar o arquivo CSV
    

    if os.path.exists('./dados/{}-indicadores---------.csv'.format(base_path)):
        base = pd.read_csv('./dados/{}-indicadores.csv'.format(base_path))
    else:
        base = pd.read_csv('./dados/{}.csv'.format(base_path))

        # Preparar os retorno e o alvo
        base['Retorno'] = base['Close'].shift(-1) - base['Close']
        base['Alvo'] = base['Retorno'].apply(lambda retorno: 1 if retorno > 0 else 0)


        # Preparar os indicadores técnicos
        base['ADX-8'] = talib.ADX(base['High'], base['Low'], base['Close'], timeperiod=8)
        base['ADX-32'] = talib.ADX(base['High'], base['Low'], base['Close'], timeperiod=32)
        base['AROON-down-8'], base['AROON-up-8'] = talib.AROON(base['High'], base['Low'], timeperiod=8)
        base['AROON-down-32'], base['AROON-up-32'] =  talib.AROON(base['High'], base['Low'], timeperiod=32)
        base['ATR-8'] = talib.ATR(base['High'], base['Low'], base['Close'], timeperiod=8)
        base['ATR-32'] = talib.ATR(base['High'], base['Low'], base['Close'], timeperiod=32)
        base['BBANDS-supper-8'], base['BBANDS-middle-8'], base['BBANDS-lower-8'] = talib.BBANDS(base['Close'], timeperiod=8)
        base['BBANDS-supper-32'], base['BBANDS-middle-32'], base['BBANDS-lower-32'] = talib.BBANDS(base['Close'], timeperiod=32)
        base['CCI-8'] = talib.CCI(base['High'], base['Low'], base['Close'], timeperiod=8)
        base['CCI-32'] = talib.CCI(base['High'], base['Low'], base['Close'], timeperiod=32)
        base['CMO-8'] = talib.CMO(base['Close'], timeperiod=8)
        base['CMO-32'] = talib.CMO(base['Close'], timeperiod=32)
        base['DX-8'] = talib.DX(base['High'], base['Low'], base['Close'], timeperiod=8)
        base['DX-32'] = talib.DX(base['High'], base['Low'], base['Close'], timeperiod=32)
        base['EMA-8'] = base['Close'].ewm(span=8, adjust=False).mean()
        base['EMA-32'] = base['Close'].ewm(span=32, adjust=False).mean()
        base['MACD-8-16-4'], base['MACD-signal-8-16-4'], base['MACD-hist-8-16-4'] = talib.MACD(base['Close'], fastperiod=8, slowperiod=16, signalperiod=4)
        base['MACD-32-64-16'], base['MACD-signal-32-64-16'], base['MACD-hist-32-64-16'] = talib.MACD(base['Close'], fastperiod=32, slowperiod=64, signalperiod=16)
        base['MIDPOINT-8'] = talib.MIDPOINT(base['Close'], timeperiod=8)
        base['MIDPOINT-32'] = talib.MIDPOINT(base['Close'], timeperiod=32)
        base['MINUS-DI-8'] = talib.MINUS_DI(base['High'], base['Low'], base['Close'], timeperiod=8)
        base['MINUS-DI-32'] = talib.MINUS_DI(base['High'], base['Low'], base['Close'], timeperiod=32)
        base['MINUS-DM-8'] = talib.MINUS_DM(base['High'], base['Low'], timeperiod=8)
        base['MINUS-DM-32'] = talib.MINUS_DM(base['High'], base['Low'], timeperiod=32)
        base['PLUS-DI-8'] = talib.PLUS_DI(base['High'], base['Low'], base['Close'], timeperiod=8)
        base['PLUS-DI-32'] = talib.PLUS_DI(base['High'], base['Low'], base['Close'], timeperiod=32)
        base['PLUS-DM-8'] = talib.PLUS_DM(base['High'], base['Low'], timeperiod=8)
        base['PLUS-DM-32'] = talib.PLUS_DM(base['High'], base['Low'], timeperiod=32)
        base['ROC-8'] = talib.ROC(base['Close'], timeperiod=8)
        base['ROC-32'] = talib.ROC(base['Close'], timeperiod=32)
        base['RSI-8'] = talib.RSI(base['Close'], timeperiod=8)
        base['RSI-32'] = talib.RSI(base['Close'], timeperiod=32)
        base['TEMA-8'] = talib.TEMA(base['Close'], timeperiod=8)
        base['TEMA-32'] = talib.TEMA(base['Close'], timeperiod=32)
        base['TRIX-8'] = talib.TRIX(base['Close'], timeperiod=8)
        base['TRIX-32'] = talib.TRIX(base['Close'], timeperiod=32)
        base['SMA-8'] = base['Close'].rolling(window=8).mean()
        base['SMA-32'] = base['Close'].rolling(window=32).mean()
        base['WMA-8'] = talib.WMA(base['Close'], timeperiod=8)
        base['WMA-32'] = talib.WMA(base['Close'], timeperiod=32)

        base.to_csv('./dados/{}-indicadores.csv'.format(base_path), index = False, header=True)
        base = pd.read_csv('./dados/{}-indicadores.csv'.format(base_path))

    # Remover linhas com valores NaN
    base = base.dropna()

    # Define o inicio de teste
    base['Date'] = pd.to_datetime(base['Date'])
    data_inicio_teste_str = '1/3/2022'
    data_inicio_teste = pd.to_datetime(data_inicio_teste_str).date() 
    indice_data_inicio = base[base['Date'].dt.date == data_inicio_teste].index[0]

   # Dividir os dados em treinamento e teste
    X = base.drop(columns=['Date','Open','High','Low','Close','Volume','Alvo','Retorno'])
    #X = base[['SMA-4', 'SMA-16', 'EMA-4', 'EMA-15']]
    y = base['Alvo']
    X_train, X_test = X[base['Date'].dt.date < data_inicio_teste], X[base['Date'].dt.date >= data_inicio_teste]
    y_train, y_test = y[base['Date'].dt.date < data_inicio_teste], y[base['Date'].dt.date >= data_inicio_teste]


    # Treinar um modelo de classificação (Random Forest)
    model = RandomForestClassifier(random_state=42)
    model.fit(X_train, y_train)

    previsao = model.predict(X_test)

    capital = 0
    posicao = 0
    fechamentos = []
    riqueza = []

    for indice, hoje in base[base['Date'].dt.date >= data_inicio_teste].iterrows():
        capital, posicao = update(capital, posicao, hoje['Close'], previsao[indice-indice_data_inicio],indice == base.index[-1])
        riquezaAtual = capital + posicao * hoje['Close']
        fechamentos.append(hoje['Close'])
        riqueza.append(float(riquezaAtual))
        preco = hoje['Close']

        print(f'Capital: {capital}\tAções em posse: {posicao}\tPreço: {preco}\tRiqueza: {riquezaAtual}')
        
    return fechamentos, riqueza

# Chamar a função com o seu arquivo de dados sequenciais
aprendizadoSupervisionado('BBDC4')