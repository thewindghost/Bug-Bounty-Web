function clearLogs() {
    if (!confirm("Are you sure you want to delete the entire log ?")) return;

    fetch('/api/v1/clear_logs', {
      method: 'POST',
      credentials: 'include',
      headers: {
        'Content-Type': 'application/json'
      }
    })
    .then(res => res.json())
    .then(data => {
      if (data.status === "success") {
        alert("Logs deleted successfully!");
        location.reload();
      } else {
        alert("Error when deleting logs: " + data.message);
      }
    })
    .catch(err => {
      alert("Server connection error: " + err);
    });
  }