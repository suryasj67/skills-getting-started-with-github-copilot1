document.addEventListener("DOMContentLoaded", () => {
  const activitiesList = document.getElementById("activities-list");
  const activitySelect = document.getElementById("activity");
  const signupForm = document.getElementById("signup-form");
  const messageDiv = document.getElementById("message");

  // Function to fetch activities from API
  async function fetchActivities() {
    try {
      const response = await fetch("/activities");
      const activities = await response.json();

      // Clear loading message
      activitiesList.innerHTML = "";

      // Populate activities list
      renderActivities(activities);
    } catch (error) {
      activitiesList.innerHTML = "<p>Failed to load activities. Please try again later.</p>";
      console.error("Error fetching activities:", error);
    }
  }

  // Render activities to the page
  function renderActivities(activities) {
    activitiesList.innerHTML = "";
    activitySelect.innerHTML = '<option value="">-- Select an activity --</option>';
    Object.entries(activities).forEach(([name, info]) => {
      const card = document.createElement("div");
      card.className = "activity-card";
      card.innerHTML = `
        <h4>${name}</h4>
        <p><strong>Description:</strong> ${info.description}</p>
        <p><strong>Schedule:</strong> ${info.schedule}</p>
        <p><strong>Max Participants:</strong> ${info.max_participants}</p>
        <div class="participants-section">
          <strong>Participants:</strong>
          <ul class="participants-list" style="list-style-type: none; padding-left: 0;">
            ${info.participants.length > 0
              ? info.participants.map(email => `
                <li style="display: flex; align-items: center; margin-bottom: 3px;">
                  <span>${email}</span>
                  <button class="delete-btn" data-activity="${name}" data-email="${email}" title="Remove" style="background: none; border: none; color: #c00; margin-left: 8px; cursor: pointer; font-size: 1.2em;">&#128465;</button>
                </li>
              `).join("")
              : '<li><em>No participants yet</em></li>'}
          </ul>
        </div>
      `;
      activitiesList.appendChild(card);

      // Add option to select dropdown
      const option = document.createElement("option");
      option.value = name;
      option.textContent = name;
      activitySelect.appendChild(option);
    });

    // Attach delete event listeners
    document.querySelectorAll('.delete-btn').forEach(btn => {
      btn.addEventListener('click', async (e) => {
        e.preventDefault();
        const activity = btn.getAttribute('data-activity');
        const email = btn.getAttribute('data-email');
        if (confirm(`Remove ${email} from ${activity}?`)) {
          const res = await fetch(`/activities/${encodeURIComponent(activity)}/unregister`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email })
          });
          const data = await res.json();
          if (data.success) {
            fetchActivities();
          } else {
            alert(data.error || 'Failed to remove participant.');
          }
        }
      });
    });
  }

  // Handle form submission
  signupForm.addEventListener("submit", async (event) => {
    event.preventDefault();

    const email = document.getElementById("email").value;
    const activity = document.getElementById("activity").value;

    try {
      const response = await fetch(
        `/activities/${encodeURIComponent(activity)}/signup?email=${encodeURIComponent(email)}`,
        {
          method: "POST",
        }
      );

      const result = await response.json();

      if (response.ok) {
        messageDiv.textContent = result.message;
        messageDiv.className = "success";
        signupForm.reset();
        fetchActivities(); // Refresh activities list immediately
      } else {
        messageDiv.textContent = result.detail || "An error occurred";
        messageDiv.className = "error";
      }

      messageDiv.classList.remove("hidden");

      // Hide message after 5 seconds
      setTimeout(() => {
        messageDiv.classList.add("hidden");
      }, 5000);
    } catch (error) {
      messageDiv.textContent = "Failed to sign up. Please try again.";
      messageDiv.className = "error";
      messageDiv.classList.remove("hidden");
      console.error("Error signing up:", error);
    }
  });

  // Initialize app
  fetchActivities();
});
