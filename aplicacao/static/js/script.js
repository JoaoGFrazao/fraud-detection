function testTransaction() {

    var step = document.querySelector('input[name="step"]').value;
    var amount = document.querySelector('input[name="amount"]').value;
    var oldbalanceOrg =  document.querySelector('input[name="oldbalanceOrg"]').value;
    var newbalanceOrg = document.querySelector('input[name="newbalanceOrg"]').value;
    var oldbalanceDest = document.querySelector('input[name="oldbalanceDest"]').value;
    var newbalanceDest = document.querySelector('input[name="newbalanceDest"]').value;
    var type = document.querySelector('select[name="type"]').value;

    if(step < 0){
      return alert("Segundos para a conclusão da transação inválido")
    }
    if(amount <= 1){
      return alert("O valor da transação não pode ser menor ou igual a 0")
    }

    if (
      step == '' ||
      amount == '' ||
      oldbalanceOrg == '' ||
      newbalanceOrg == '' ||
      oldbalanceDest == '' ||
      newbalanceDest == '' ||
      type == ''
      ) {
        return alert("Preencha todos os campos corretamente")
  }


    console.log[step]
      
      fetch('/predict', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: `step=${step}&amount=${amount}&oldbalanceOrg=${oldbalanceOrg}&newbalanceOrg=${newbalanceOrg}&oldbalanceDest=${oldbalanceDest}&newbalanceDest=${newbalanceDest}&type=${type}`,
      })
        .then(response => response.json())
        .then(data => {
          console.log('Resposta do servidor:', data);
        })        
        .catch(error => {
          console.error('Erro ao enviar a solicitação:', error);
        })
        .finally(() => {
          window.location.reload();
      });
}    


fetch('/list_all')
    .then(response => response.json())
    .then(data => {
        const table = document.getElementById('transactions-table');


        data.forEach(transaction => {
            let button = document.createElement('button');
            button.className = 'delete_button';
            button.onclick = function () { deleteTrans(transaction.ID) };
            const row = table.insertRow();
            row.insertCell().textContent = transaction.ID;
            row.insertCell().textContent = transaction['Segundos para a Conclusão da Transação'] + " segundos";
            row.insertCell().textContent = "R$ " + transaction['Valor da Transação'];
            row.insertCell().textContent = "R$ " + transaction['Saldo do Remetente'];
            row.insertCell().textContent = "R$ " + transaction['Novo Saldo do Remetente'];
            row.insertCell().textContent = "R$ " + transaction['Saldo do Destinatário'];
            row.insertCell().textContent = "R$ " + transaction['Novo Saldo do Destinatário'];
            row.insertCell().textContent = transaction['Tipo de Transação'];
            row.insertCell().textContent = transaction['Verificação de Fraude'];
            row.insertCell(-1).appendChild(button);

            
            // Adiciona uma linha de divisão após cada linha da tabela
            const dividerRow = table.insertRow();
            const dividerCell = dividerRow.insertCell();
            dividerCell.colSpan = row.cells.length;
            dividerCell.style.borderTop = '2px solid black';
        });
    })

    function deleteTrans(transId) {
      var isConfirmed = confirm("Tem certeza que deseja excluir a transação de ID" + transId + "?" );
      if (isConfirmed) {
          fetch(`/trans_delete/${transId}`, {
              method: 'DELETE'
          })
              .then(response => response.json())
              .then(data => {
                  alert(data.message);
                  window.location.reload();
              })
              .catch(error => {
                  console.error('Erro ao excluir jogo:', error);
              });
      } else {
          exit;
      }
  }