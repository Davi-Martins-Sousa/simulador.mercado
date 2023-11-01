import pandas as pd
import numpy as np
#import talib
import os
import math
from sklearn.neural_network import MLPRegressor
from sklearn.metrics import mean_absolute_error,mean_squared_error
from sklearn.preprocessing import MinMaxScaler
from estrategia import create,start,finish,compra,venda

def update(capital,posicao,precoHoje,decisao,ultimoDia):
    if ultimoDia == False :
        if decisao > 0:
            capital, posicao = compra(capital, posicao, precoHoje, 1)
        else:
            capital, posicao = venda(capital, posicao, precoHoje, 1)
    else:
        if posicao < 0:
            capital, posicao = compra(capital, posicao, precoHoje, -posicao)
        elif posicao > 0:
            capital, posicao = venda(capital, posicao, precoHoje, posicao)
    return capital, posicao

def regressao(base_path, ano_inicio = '1/3/2022', janela = False, tamanho_janela = 22, tipo = 'regressão'):

    if os.path.exists('./dados/{}-indicadores.csv'.format(base_path)):
        base = pd.read_csv('./dados/{}-indicadores.csv'.format(base_path))
    '''else:
        base = pd.read_csv('./dados/{}.csv'.format(base_path))

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

        colunas_para_normalizar = [
        'ADX-8', 'ADX-32',
        'AROON-down-8', 'AROON-up-8', 'AROON-down-32', 'AROON-up-32',
        'ATR-8', 'ATR-32',
        'BBANDS-supper-8', 'BBANDS-middle-8', 'BBANDS-lower-8',
        'BBANDS-supper-32', 'BBANDS-middle-32', 'BBANDS-lower-32',
        'CCI-8', 'CCI-32',
        'CMO-8', 'CMO-32',
        'DX-8', 'DX-32',
        'EMA-8', 'EMA-32',
        'MACD-8-16-4', 'MACD-signal-8-16-4', 'MACD-hist-8-16-4',
        'MACD-32-64-16', 'MACD-signal-32-64-16', 'MACD-hist-32-64-16',
        'MIDPOINT-8', 'MIDPOINT-32',
        'MINUS-DI-8', 'MINUS-DI-32',
        'MINUS-DM-8', 'MINUS-DM-32',
        'PLUS-DI-8', 'PLUS-DI-32',
        'PLUS-DM-8', 'PLUS-DM-32',
        'ROC-8', 'ROC-32',
        'RSI-8', 'RSI-32',
        'TEMA-8', 'TEMA-32',
        'TRIX-8', 'TRIX-32',
        'SMA-8', 'SMA-32',
        'WMA-8', 'WMA-32'
        ]

        # Crie um objeto StandardScaler
        scaler = MinMaxScaler()

        # Normalize as colunas especificadas
        base[colunas_para_normalizar] = scaler.fit_transform(base[colunas_para_normalizar])

        base.to_csv('./dados/{}-indicadores.csv'.format(base_path), index = False, header=True)
        base = pd.read_csv('./dados/{}-indicadores.csv'.format(base_path))'''

    # Remover linhas com valores NaN
    base = base.dropna()

    # Preparar os retorno e o alvo
    base['Retorno'] = base['Close'].shift(-1) - base['Close']
    base['Alvo'] = base['Retorno'].apply(lambda retorno: 1 if retorno > 0 else 0)

    # Define o inicio de teste
    base['Date'] = pd.to_datetime(base['Date'])
    data_inicio_teste_str = ano_inicio #'1/3/2022'
    data_inicio_teste = pd.to_datetime(data_inicio_teste_str).date() 
    indice_data_inicio = base[base['Date'].dt.date == data_inicio_teste].index[0]

    # Dividir os dados em treinamento e test
    X = base.drop(columns=['Date','Open','High','Low','Close','Volume','Alvo','Retorno'])
    y = base['Retorno']
    y = y.copy()
    y.iloc[-1] = 0
    
    previsao = []

    if(janela == False):
        X_train, X_test = X[base['Date'].dt.date < data_inicio_teste], X[base['Date'].dt.date >= data_inicio_teste]
        y_train, y_test = y[base['Date'].dt.date < data_inicio_teste], y[base['Date'].dt.date >= data_inicio_teste]

        if tipo == 'baseline':
            previsao = np.insert(y_test, 0, 0)[:-1]
        else:
            model = MLPRegressor(hidden_layer_sizes=(256, 64), activation='relu', solver='adam', max_iter=1024)
            model.fit(X_train, y_train)

            previsao = model.predict(X_test)

        mae = mean_absolute_error(y_test, previsao)
        mse = mean_squared_error(y_test, previsao)
        rmse = math.sqrt(mse)
        print("MAE: {:.4f}\tRMSE: {:.4f}".format(mae, rmse))

    else: 
        # Defina o tamanho da janela de treinamento
        janela_treinamento = tamanho_janela
        indice_data_inicio_temp = int(indice_data_inicio)
        base = base.reset_index(drop=True)
        previsao = []
        y_teste = []

        while indice_data_inicio_temp < len(base):

            # Dividir os dados em treinamento e teste com base nas datas da janela
            X_train = X[base.index < indice_data_inicio_temp]
            y_train = y[base.index < indice_data_inicio_temp]

            if indice_data_inicio_temp + janela_treinamento < len(base):
                X_test = X[(base.index >= indice_data_inicio_temp) & (base.index < indice_data_inicio_temp + janela_treinamento)]
                y_test = y[(base.index >= indice_data_inicio_temp) & (base.index < indice_data_inicio_temp + janela_treinamento)]
                y_teste.extend(y_test)
            else: 
                X_test = X[(base.index >= indice_data_inicio_temp)]
                y_test = y[(base.index >= indice_data_inicio_temp)]
                y_teste.extend(y_test)

            # Treinar um modelo de classificação (Random Forest)
            model = MLPRegressor(hidden_layer_sizes=(256, 64), activation='relu', solver='adam', max_iter=1024) 
            model.fit(X_train, y_train)

            # Fazer previsões para o dia atual
            previsao_janela = model.predict(X_test)

            # Adicionar as previsões ao vetor de previsões por dia
            previsao.extend(previsao_janela)

            # Atualize a data atual para a próxima janela
            indice_data_inicio_temp += janela_treinamento

        mae = mean_absolute_error(y_teste, previsao)
        mse = mean_squared_error(y_teste, previsao)
        rmse = math.sqrt(mse)
        print("MAE: {:.4f}\tRMSE: {:.4f}".format(mae, rmse))

    capital = 0
    posicao = 0
    fechamentos = []
    riqueza = []
    #print(len(previsao))

    for indice, hoje in base[base.index >= indice_data_inicio].iterrows():
            
        capital, posicao = update(capital, posicao, hoje['Close'], previsao[indice-indice_data_inicio],indice == base.index[-1])
        riquezaAtual = capital + posicao * hoje['Close']
        fechamentos.append(hoje['Close'])
        riqueza.append(float(riquezaAtual))
        preco = hoje['Close']

    print(f'Capital: {round(capital, 2)}\tAções em posse: {posicao}\tPreço: {round(preco, 2)}\tRiqueza: {round(riquezaAtual, 2)}')
        
    return fechamentos, riqueza