console.log('check');

fetch('/get-key')
  .then(res => { return res.json(); })
  .then(data => {
    const stripe = Stripe(data.public_key);
    let items = [];

    document.querySelectorAll('.item-id').forEach(item => {
      items.push(item.textContent);
    });

    document.getElementById('payment-form').addEventListener('submit', ev => {
      ev.preventDefault();
      fetch('/create-checkout-session', {
        method: 'post',
        body: JSON.stringify({'items': items}),
        headers: { 
          'Accept': 'application/json, text/plain, */*',
          'Content-Type': 'application/json'
        },
      })
        .then(res => { return res.json(); })
        .then(data => {
          return stripe.redirectToCheckout({sessionId: data.sessionId});
        })
        .then(res => { console.log(res); });
    });
  });