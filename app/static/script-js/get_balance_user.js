async function fetchBalanceOnly() {
    const balanceSpan = document.getElementById('balance-amount');

    try {
      const res = await fetch('/api/v1/information_user', {
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
  
  document.addEventListener("DOMContentLoaded", () => {
    fetchBalanceOnly();
  });