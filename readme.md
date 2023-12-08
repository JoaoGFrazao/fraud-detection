# API de Verificação de Transações Fraudulentas

Este é um exemplo de uma API construída em Flask para verificar transações financeiras e identificar possíveis fraudes. A API inclui endpoints para adicionar transações, listar todas as transações e excluir transações específicas.

A API utiliza um modelo de Árvore de Decisão para prever se uma transação é fraudulenta.

## Configuração do Ambiente Virtual

Para garantir uma instalação e execução da API isolada do sistema, é recomendável criar um ambiente virtual. Siga os passos abaixo para configurar o ambiente virtual e instalar as dependências:

### 1. Instalar o Virtualenv (caso ainda não tenha)

```
pip install virtualenv
```

### 2. Criar um Ambiente Virtual

```
virtualenv venv
```

### 3. Ativar o Ambiente Virtual (Windows)

```
venv\Scripts\activate
```

### 3. Ativar o Ambiente Virtual (Linux/macOS)

```
source venv/bin/activate
```

### 4. Instalar as Dependências

```
pip install -r requirements.txt
```

### 5. Executar a Aplicação

```
python app.py
```

Lembre-se de que, ao ativar o ambiente virtual, você isolará as dependências deste projeto do sistema, garantindo que não haja conflitos com outras aplicações Python em seu ambiente.

Para desativar o ambiente virtual, basta executar:

```
deactivate
```

Certifique-se de que o ambiente virtual esteja ativado sempre que estiver trabalhando com este projeto.

Com essas etapas, você estará pronto para executar a API em um ambiente virtual isolado.

## Endpoints

### 1. Página Inicial

- **Endpoint:** `/`
- **Método:** `GET`
- **Descrição:** Retorna a página inicial.

### 2. Verificar e Adicionar Transação

- **Endpoint:** `/predict`
- **Método:** `POST`
- **Descrição:** Verifica se uma operação é fraudulenta e a adiciona ao banco de dados.
- Parâmetros:
  - `step` (integer, obrigatório): O tempo em segundos que durou a transação.
  - `amount` (number, obrigatório): O valor da transação.
  - `oldbalanceOrg` (number, obrigatório): O saldo anterior da conta de origem.
  - `newbalanceOrg` (number, obrigatório): O saldo posterior da conta de origem.
  - `oldbalanceDest` (number, obrigatório): O saldo anterior da conta de destino.
  - `newbalanceDest` (number, obrigatório): O saldo posterior da conta de destino.
  - `type` (string, obrigatório): O tipo de transação, podendo ser cash_in, cash_out, transfer, debit, payment.
- Respostas:
  - **200 OK:** Transação adicionada com sucesso.
  - **400 Bad Request:** Dados mal inseridos.

### 3. Listar Todas as Transações

- **Endpoint:** `/list_all`
- **Método:** `GET`
- **Descrição:** Lista todas as transações.
- Respostas:
  - **200 OK:** Lista de todas as transações.
  - **204 No Content:** Nenhuma transação encontrada.

### 4. Deletar Transação por ID

- **Endpoint:** `/trans_delete/<int:id>`
- **Método:** `DELETE`
- **Descrição:** Deleta uma transação por ID.
- Parâmetros:
  - `id` (integer, obrigatório): ID da transação a ser deletada.
- Respostas:
  - **200 OK:** Transação deletada com sucesso.

## Sobre o Modelo

### 1. Árvore de Decisão

O modelo utilizado foi o de Árvore de Decisão Original por contar a maior acurácia e F1 Score

<h3>2. Métricas</h3>

Acurácia: 0.968
Precisão: 0.984
Recall: 0.951
F1: 0.967



## Teste Automatizado

O repositória conta também com um arquivo de teste para verificar se o modelo cumpre o requisito de acurácia ao ser testado em um Golden Dataset não visto anteriormente pelo modelo

- **Para rodar o teste execute:**

  ```
  pytest
  ```

  



## Observações

- Certifique-se de ter o arquivo `modelo.pkl` na mesma pasta do script para carregar o modelo de previsão.
- A aplicação usa SQLite como banco de dados e cria as tabelas automaticamente ao iniciar.