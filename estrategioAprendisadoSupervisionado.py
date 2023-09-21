import pandas as pd
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
    base = pd.read_csv(base_path)

    # Preparar os recursos e o alvo
    base['Retorno'] = base['Close'].shift(-1) - base['Close']
    base['alvo'] = base['Retorno'].apply(lambda retorno: 1 if retorno > 0 else 0)
    base['SMA-8'] = base['Close'].rolling(window=8).mean()
    base['SMA-32'] = base['Close'].rolling(window=32).mean()
    base['EMA-8'] = base['Close'].ewm(span=8, adjust=False).mean()
    base['EMA-32'] = base['Close'].ewm(span=32, adjust=False).mean()

    # Remover linhas com valores NaN
    base = base.dropna()

    # Definir o tamanho da janela para a validação cruzada deslizante
    janela_treino = int(0.8 * len(base))  # 80% para treinamento

    # Dividir os dados em treinamento e teste
    X = base[['SMA-8', 'SMA-32', 'EMA-8', 'EMA-32']]
    y = base['alvo']
    X_train, X_test = X[:janela_treino], X[janela_treino:]
    y_train, y_test = y[:janela_treino], y[janela_treino:]

    # Treinar um modelo de classificação (Random Forest)
    model = RandomForestClassifier(random_state=42)
    model.fit(X_train, y_train)

    previsao = model.predict(X_test)

    capital = 0
    posicao = 0
    fechamentos = []
    riqueza = []

    for indice, hoje in base.iloc[int(0.8 * len(base))+31:].iterrows():
        #print(previsao[indice-int(0.8 * len(base))-31])
        print(hoje['Close'])
        capital, posicao = update(capital, posicao, hoje['Close'], previsao[indice-int(0.8 * len(base))-32],base.index[-1] == indice)

        riquezaAtual = capital + posicao * hoje["Close"]
        fechamentos.append(hoje["Close"])
        riqueza.append(float(riquezaAtual))

        print(f'Capital: {capital}\tAções em posse: {posicao}\tRiqueza: {riquezaAtual}')
        
    return fechamentos, riqueza

# Chamar a função com o seu arquivo de dados sequenciais
aprendizadoSupervisionado('./dados/BBDC4.csv')
