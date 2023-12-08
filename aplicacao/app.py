from flask import Flask, render_template, request, url_for, redirect, jsonify
from modelo import Model
from transactions import Transactions, db
import numpy as np
from flasgger import Swagger

app = Flask(__name__)
swagger = Swagger(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///transactions.sqlite3'
db.init_app(app)

@app.route('/')
def home():
    """
    Endpoint que retorna a página inicial.
    ---
    responses:
      200:
        description: Página inicial.
    """
    return render_template("home.html"), 200

@app.route('/predict', methods=['POST'])
def predict():
    """
    Endpoint para verificar se uma operação é fraudulenta e adiciona-la no banco de dados.

    ---
    parameters:
      - name: step
        in: formData
        type: integer
        required: true
        description: O tempo em segundos que durou a transação.
      - name: amount
        in: formData
        type: number
        required: true
        description: O valor da transação.
      - name: oldbalanceOrg
        in: formData
        type: number
        required: true
        description: O saldo anterior da conta de origem.
      - name: newbalanceOrg
        in: formData
        type: number
        required: true
        description: O saldo posterior da conta de origem.
      - name: oldbalanceDest
        in: formData
        type: number
        required: true
        description: O saldo anterior da conta de destino.
      - name: newbalanceDest
        in: formData
        type: number
        required: true
        description: O saldo posterior da conta de destino.
      - name: type
        in: formData
        type: string
        required: true
        description: O tipo de transação podendo ser cash_in, cash_out, transfer, debit, payment.

    responses:
      200:
        description: Sucesso, a transação foi adicionada com sucesso ao banco de dados.
      400:
        description: Bad Request. Algum dado foi mal inserido.
    """
    ml_path = 'modelo.pkl'
    modelo = Model.carrega_modelo(ml_path)

    step = request.form.get('step')
    amount = request.form.get('amount')
    oldbalanceOrg = request.form.get('oldbalanceOrg')
    newbalanceOrg = request.form.get('newbalanceOrg')
    oldbalanceDest = request.form.get('oldbalanceDest')
    newbalanceDest = request.form.get('newbalanceDest')
    type = request.form.get('type')

    type_TRANSFER = type_PAYMENT = type_DEBIT = type_CASH_IN = type_CASH_OUT = 0

    if type == "cash_out":
        type_TRANSFER = type_PAYMENT = type_DEBIT = type_CASH_IN = 0
        type_CASH_OUT = 1
    elif type == "cash_in":
        type_TRANSFER = type_PAYMENT = type_DEBIT = type_CASH_OUT = 0
        type_CASH_IN = 1
    elif type == "transfer":
        type_CASH_IN = type_PAYMENT = type_DEBIT = type_CASH_OUT = 0
        type_TRANSFER = 1
    elif type == "debit":
        type_CASH_IN = type_PAYMENT = type_TRANSFER = type_CASH_OUT = 0
        type_DEBIT = 1
    elif type == "payment":
        type_CASH_IN = type_TRANSFER = type_DEBIT = type_CASH_OUT = 0
        type_PAYMENT = 1
    else:
        return("Tipo de transação não identificada")
    
    data_to_predict = [step, amount, oldbalanceOrg, newbalanceOrg, oldbalanceDest, newbalanceDest, type_CASH_IN, type_CASH_OUT, type_DEBIT, type_PAYMENT, type_TRANSFER]
    data_to_predict_reshape = np.array(data_to_predict).reshape(1, -1)
    isFraud = modelo.predict(data_to_predict_reshape)[0]


    transaction = Transactions(step, amount, oldbalanceOrg, newbalanceOrg, oldbalanceDest, newbalanceDest,type_CASH_IN, type_CASH_OUT, type_DEBIT, type_PAYMENT, type_TRANSFER,  isFraud)
    
    db.session.add(transaction)
    db.session.commit()

    return ("Transação adicionada com sucesso")


@app.route('/list_all', methods=['GET'])
def list_transactions():
    """
    Endpoint para listar todas as transações.
    ---
    responses:
      200:
        description: Lista de todas as transações.
      204:
        description: Nenhuma transação encontrada.
    """
    transactions = Transactions.query.all()
    transactions_list = []
    
    for transaction in transactions:

        tipo = 0
        if transaction.type_CASH_IN == 1:
            tipo = "Cash-In"
        elif transaction.type_CASH_OUT == 1:
            tipo = "Cash-Out"
        elif transaction.type_DEBIT == 1:
            tipo = "Débito"
        elif transaction.type_PAYMENT == 1:
            tipo = "Pagamento"
        elif transaction.type_TRANSFER == 1:
            tipo = "Transferência"
        else:
            return("Tipo de transação não identificada")
        
        fraud = 0
        if transaction.isFraud == 1:
            fraud = "FRAUDE"
        elif transaction.isFraud == 0:
            fraud = "OK"

        trans_data = {
            'ID': transaction.id,
            'Segundos para a Conclusão da Transação': transaction.step,
            'Valor da Transação': transaction.amount,
            'Saldo do Remetente': transaction.oldbalanceOrg,
            'Novo Saldo do Remetente': transaction.newbalanceOrg,
            'Saldo do Destinatário': transaction.oldbalanceDest,
            'Novo Saldo do Destinatário': transaction.newbalanceDest,
            'Tipo de Transação': tipo,
            'Verificação de Fraude': fraud
        }
        transactions_list.append(trans_data)
    if len(transactions_list) == 0:
      return "Não existem transações cadastradas", 200 

    return jsonify(transactions_list)

@app.route('/trans_delete/<int:id>', methods=['DELETE'])
def delete(id):
    """
    Endpoint para deletar uma transação por ID.
    ---
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: ID da transação a ser deletada.
    responses:
      200:
        description: Transação deletada com sucesso.
    """
    trans_to_delete = Transactions.query.get_or_404(id)
    db.session.delete(trans_to_delete)
    db.session.commit()
    return jsonify({'message': 'Transação deletada com sucesso'})


with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)