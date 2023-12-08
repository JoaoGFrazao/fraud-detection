import warnings
import pytest
from modelo import Model
import pandas as pd
import pytest
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score

ml_path = 'modelo.pkl'
modelo = Model.carrega_modelo(ml_path)

# Carregar o conjunto de dados de teste
dados_teste = pd.read_csv('golden.csv')
X_teste = dados_teste.drop('isFraud', axis=1)
y_teste = dados_teste['isFraud']


# Teste para avaliar a acurácia do modelo
def test_avaliar_acuracia():
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", category=UserWarning)
        previsoes = modelo.predict(X_teste)
        acuracia = accuracy_score(y_teste, previsoes)
        tolerancia_acuracia = 0.85

    # Verificar se a acurácia é maior que a tolerância
    assert acuracia > tolerancia_acuracia, f'A acurácia ({acuracia}) é menor que a tolerância ({tolerancia_acuracia})'

if __name__ == '__main__':
    pytest.main()