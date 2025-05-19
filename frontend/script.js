let accessToken = sessionStorage.getItem('accessToken');

document.addEventListener("DOMContentLoaded", () => {
  const loginForm = document.getElementById("login-form");
  const registerForm = document.getElementById("register-form");
  const emailInput = document.getElementById("email");
  const passwordInput = document.getElementById("password");
  const createForm = document.getElementById("create-field-form");

  // Login
  loginForm.onsubmit = async (e) => {
    e.preventDefault();

    const email = emailInput.value;
    const password = passwordInput.value;

    const response = await fetch("/api/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, password })
    });

    if (response.ok) {
      const tokens = await response.json();
      accessToken = tokens.access_token;
      refreshToken = tokens.refresh_token;
      sessionStorage.setItem("accessToken", accessToken);
      sessionStorage.setItem("refreshToken", refreshToken);

      window.location.href = "/dashboard";
      loginForm.style.display = "none";
      createForm.style.display = "block";
      loadFields();
    } else {
      alert("Login failed!");
    }
  };
  if (registerForm) {
    registerForm.onsubmit = async (e) => {
        e.preventDefault();
        const full_name = registerForm.full_name.value;
        const email = registerForm.email.value;
        const password = registerForm.password.value;

        const response = await fetch("/api/register", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ full_name, email, password })
        });

        if (response.ok) {
            alert("Registration successful! Please login.");
            window.location.href = "/";
        } else {
            alert("Registration failed.");
        }
    };
}

  // Create field
  createForm.onsubmit = async (e) => {
    e.preventDefault();
    const label = document.getElementById("label").value;
    const value = document.getElementById("value").value;

    const response = await fetch("/api/dashboard/create", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${accessToken}`
      },
      body: JSON.stringify({ label, value })
    });

    if (response.ok) {
      alert("Field created!");
      document.getElementById("label").value = "";
      document.getElementById("value").value = "";
      loadFields();
    } else {
      alert("Failed to create field.");
    }
  };

  // Load fields on page load if logged in
  if (accessToken) {
    loginForm.style.display = "none";
    createForm.style.display = "block";
    loadFields();
  }
});

async function loadFields() {
  const container = document.getElementById("fields-container");
  container.innerHTML = "";

  const response = await fetch("/api/dashboard/read", {
    headers: { Authorization: `Bearer ${accessToken}` }
  });

  const fields = await response.json();

  fields.forEach(field => {
    const div = document.createElement("div");
    div.innerHTML = `
      <b>${field.label}</b>: ${field.value}
      <button onclick="editField(${field.id}, '${field.label}', '${field.value}')">Edit</button>
      <button onclick="deleteField(${field.id})">Delete</button>
    `;
    container.appendChild(div);
  });
}

async function editField(id, oldLabel, oldValue) {
  const label = prompt("New label:", oldLabel);
  const value = prompt("New value:", oldValue);

  if (!label || !value) return;

  const response = await fetch(`/api/dashboard/update/${id}`, {
    method: "PATCH",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${accessToken}`
    },
    body: JSON.stringify({ label, value })
  });

  if (response.ok) {
    alert("Field updated!");
    loadFields();
  } else {
    alert("Failed to update field.");
  }
}

async function deleteField(id) {
  if (!confirm("Are you sure you want to delete this field?")) return;

  const response = await fetch(`/api/dashboard/delete/${id}`, {
    method: "DELETE",
    headers: { Authorization: `Bearer ${accessToken}` }
  });

  if (response.ok) {
    alert("Field deleted!");
    loadFields();
  } else {
    alert("Failed to delete field.");
  }
}
