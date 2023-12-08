import pickle

class Model:
    @staticmethod
    def carrega_modelo(caminho):
        with open(caminho, 'rb') as arquivo:
            modelo = pickle.load(arquivo)
        return modelo

