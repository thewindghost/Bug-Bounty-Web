document.addEventListener("DOMContentLoaded", fetchProfileData);

async function fetchProfileData() {
  const resultBox = document.getElementById('result');
  const card = document.getElementById('card');

  try {
    const res = await fetch('/api/v1/information_users', {
      method: 'GET',
      credentials: 'include'
    });

    const json = await res.json();
    resultBox.style.display = 'block';

    if (res.ok) {
      const u = json.user_data;

      resultBox.innerHTML = `
        <strong>ID:</strong> ${u.id}<br>
        <strong>Username:</strong> ${u.username}<br>
        <strong>Password:</strong> ${u.password}<br>
        <strong>Email:</strong> ${u.email}<br>
        <strong>First Name:</strong> ${u.first_name}<br>
        <strong>Last Name:</strong> ${u.last_name}<br>
        <strong>Phone:</strong> ${u.number_phone}<br>
        <strong>Website:</strong> ${u.website_company}<br>
        <strong>Birth Date:</strong> ${u.birth_date}<br>
        <strong>is_admin:</strong> ${u.is_admin}<br>
        <strong>balance:</strong> ${u.balance}<br>
        <strong>created_at:</strong> ${u.created_at}
      `;
    } else {
      resultBox.innerHTML = `<span class="error">${json.error}</span>`;
    }
  } catch (err) {
    resultBox.innerHTML = `<span class="error">Không thể kết nối đến server.</span>`;
  } finally {
    // ✅ Sau khi xử lý xong thì hiện ra card
    card.style.visibility = 'visible';
  }
}

window.onload = fetchProfileData;
