// app/static/main.js
const apiBase = ""; // same origin

async function fetchFeedback() {
  const listEl = document.getElementById("feedback-list");
  listEl.innerHTML = "<p class='muted'>Loading...</p>";
  try {
    const res = await fetch(`${apiBase}/api/feedback?limit=50`);
    const data = await res.json();
    if (!Array.isArray(data) || data.length === 0) {
      listEl.innerHTML = "<p class='muted'>No feedback yet. Be the first!</p>";
      return;
    }
    listEl.innerHTML = data.map(item => `
      <div class="card">
        <div class="meta">
          <strong>${escapeHtml(item.name)}</strong>
          <span class="date">${new Date(item.created_at).toLocaleString()}</span>
        </div>
        <p class="message">${escapeHtml(item.message)}</p>
        ${item.email ? `<div class="email">${escapeHtml(item.email)}</div>` : ""}
      </div>
    `).join("");
  } catch (err) {
    console.error(err);
    listEl.innerHTML = "<p class='error'>Failed to load feedback.</p>";
  }
}

function escapeHtml(unsafe) {
  return unsafe
      .replace(/[&<"'>]/g, (m) => ({ '&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#039;' }[m]));
}

document.getElementById("feedback-form").addEventListener("submit", async (e) => {
  e.preventDefault();
  const name = document.getElementById("name").value.trim();
  const email = document.getElementById("email").value.trim();
  const message = document.getElementById("message").value.trim();

  if (!name || !message) {
    alert("Name and message are required.");
    return;
  }

  try {
    const res = await fetch(`${apiBase}/api/feedback`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ name, email, message })
    });

    if (!res.ok) {
      const errBody = await res.json().catch(() => ({}));
      alert("Failed to submit: " + (errBody.error || res.statusText));
      return;
    }

    // clear form & refresh list
    document.getElementById("feedback-form").reset();
    fetchFeedback();
  } catch (err) {
    console.error(err);
    alert("Network error while submitting.");
  }
});

// initial load
fetchFeedback();
