async function fetchBalanceOnly() {
    const balanceSpan = document.getElementById('balance-amount');
    const card = document.getElementById('card');

    try {
      const res = await fetch('/api/v1/information_users', {
        method: 'GET',
        credentials: 'include'
      });
  
      const json = await res.json();

      if (res.ok) {
        const balance = json.user_data.balance;

        balanceSpan.textContent = parseFloat(balance).toFixed(2);
      } else {
        balanceSpan.textContent = "Error";
      }
    } catch (err) {
      balanceSpan.textContent = "Failed";
    }
  }
  
  window.onload = fetchBalanceOnly;