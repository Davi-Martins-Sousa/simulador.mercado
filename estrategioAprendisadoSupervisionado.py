import pandas as pd
import talib
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from estrategia import create,start,finish,compra,venda


def update(capital,posicao,precoHoje,decisao,ultimoDia):
    if ultimoDia == False :
        if decisao == 1:
            capital, posicao = venda(capital, posicao, precoHoje, 1)
        else:
            capital, posicao = compra(capital, posicao, precoHoje, 1)
    else:
        if posicao < 0:
            
            capital, posicao = venda(capital, posicao, precoHoje, posicao)
        elif posicao > 0:
            capital, posicao = compra(capital, posicao, precoHoje, posicao)
            

    return capital, posicao

def aprendizadoSupervisionado(base_path):
    # Carregar o arquivo CSV
    base = pd.read_csv(base_path)

    # Preparar os recursos e o alvo
    base['Retorno'] = base['Close'].shift(-1) - base['Close']
    base['alvo'] = base['Retorno'].apply(lambda retorno: 1 if retorno > 0 else 0)
    #base['ADX-4'] talib.ADX(base['High'], base['Low'], base['Close'], timeperiod=4)
    #base['ADX-16'] talib.ADX(base['High'], base['Low'], base['Close'], timeperiod=16)
    base['SMA-8'] = base['Close'].rolling(window=8).mean()
    base['SMA-32'] = base['Close'].rolling(window=32).mean()
    base['EMA-8'] = base['Close'].ewm(span=8, adjust=False).mean()
    base['EMA-32'] = base['Close'].ewm(span=32, adjust=False).mean()

    # Remover linhas com valores NaN
    base = base.dropna()

    # Define o inicio de teste
    base['Date'] = pd.to_datetime(base['Date'])
    data_inicio_teste_str = '1/3/2022'
    data_inicio_teste = pd.to_datetime(data_inicio_teste_str).date() 
    indice_data_inicio = base[base['Date'].dt.date == data_inicio_teste].index[0]

   # Dividir os dados em treinamento e teste
    X = base[['SMA-8', 'SMA-32', 'EMA-8', 'EMA-32']]
    y = base['alvo']
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
        riquezaAtual = capital + posicao * hoje["Close"]
        fechamentos.append(hoje["Close"])
        riqueza.append(float(riquezaAtual))

        print(f'Capital: {capital}\tAções em posse: {posicao}\tRiqueza: {riquezaAtual}')
        
    return fechamentos, riqueza

# Chamar a função com o seu arquivo de dados sequenciais
aprendizadoSupervisionado('./dados/BBDC4.csv')
