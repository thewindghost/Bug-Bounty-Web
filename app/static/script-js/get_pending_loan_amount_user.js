async function fetchPendingLoanAmountOnly() {
    const pending_loan_amountSpan = document.getElementById('pending-loan-amount');

    try {
      const res = await fetch('/api/v1/information_user', {
        method: 'GET',
        credentials: 'include'
      });
  
      const json = await res.json();

      if (res.ok) {
        const pending_loan_amountdata = json.user_data.pending_loan_amount;

        pending_loan_amountSpan.textContent = parseFloat(pending_loan_amountdata).toFixed(2);
      } else {
        pending_loan_amountSpan.textContent = "Error";
      }
    } catch (err) {
        pending_loan_amountSpan.textContent = "Failed";
    }
  }
  
  document.addEventListener("DOMContentLoaded", () => {
    fetchPendingLoanAmountOnly();
  });