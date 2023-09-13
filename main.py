import pandas as pd
import matplotlib.pyplot as plt
from estrategiaBase import base
from estrategiaMediaMovel import mediaMovel

def main():
    fechamentos,riqueza = mediaMovel('dados/BBDC4.csv')
    #fechamentos,riqueza = mediaMovel('dados/PETR3.SA.csv')
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