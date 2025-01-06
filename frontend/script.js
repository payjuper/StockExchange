const buyForm = document.getElementById('buy-form');
    const buyResult = document.getElementById('buy-result');

    buyForm.addEventListener('submit', (event) => {
        event.preventDefault();

        const symbol = document.getElementById('symbol').value;
        const quantity = document.getElementById('quantity').value;
        const price = document.getElementById('price').value;

        fetch('http://127.0.0.1:5000/buy', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ symbol, quantity, price })
        })
            .then(response => response.json())
            .then(data => {
                buyResult.innerText = data.message;
            })
            .catch(error => {
                buyResult.innerText = "Error: " + error.message;
            });
    });

