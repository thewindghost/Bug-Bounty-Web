document.addEventListener("DOMContentLoaded", fetchProfileData);

async function fetchProfileData() {
    const resultBox = document.getElementById('result');
    const card = document.getElementById('card');

    try {
      const res = await fetch('/api/v1/information_admin', {
        method: 'GET',
        credentials: 'include'
      });

      const json = await res.json();
      resultBox.style.display = 'block';

      if (res.ok) {
        const u = json.admin_data;

        resultBox.innerHTML = `
        <strong><span style="color: #4a90e2;">Personal Information</strong></span><br>
        <strong>ID:</strong> <span style="color:#28a745;">${u.id}</span><br>
        <strong>First Name:</strong> <span style="color:#007BFF;">${u.first_name}</span><br>
        <strong>Last Name:</strong> <span style="color:#007BFF;">${u.last_name}</span><br>
        <strong>Email:</strong> <span style="color:#17a2b8;">${u.email}</span><br>
        <strong>Phone:</strong> <span style="color:rgb(255, 166, 0);">${u.number_phone}</span><br>
        <strong>Website:</strong> <span style="color:rgb(255, 166, 0);">${u.website_company}</span><br>
        <strong>Birth Date:</strong> <span style="color:rgb(255, 166, 0);">${u.birth_date}</span><br>
        <strong>Created At:</strong> <span style="color:rgb(255, 166, 0);">${u.created_at}</span><br>
        <br>

        <strong><span style="color: #4a90e2;">Account And Permissions</strong></span><br>
        <strong>Username:</strong> <span style="color:#007BFF; font-weight:bold;">${u.username}</span><br>
        <strong>Admin:</strong> <span style="color:${u.is_admin ? '#28a745' : '#dc3545'};">${u.is_admin}</span><br>
        <strong>Account Balance:</strong> <span style="color:rgb(255, 166, 0);">$${u.balance}</span><br>
        <br>

        <strong><span style="color: #4a90e2;">Password (hashed)</strong></span> <span style="color:rgb(255, 166, 0);">$${u.password}</span>
        `;
      } else {
        resultBox.innerHTML = `<span class="error">${json.error}</span>`;
      }
    } catch (err) {
      resultBox.innerHTML = `<span class="error">Internal server error.</span>`;
    } finally {
      card.style.visibility = 'visible';
    }
  }

  window.onload = fetchProfileData;