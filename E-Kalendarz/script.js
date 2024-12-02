document.addEventListener("DOMContentLoaded", () => {
    const dateElement = document.getElementById("date");
    const eventList = document.getElementById("event-list");
    const eventForm = document.getElementById("event-form");
    const deleteEventButton = document.getElementById("delete-event");

    // Show today's date
    const today = new Date().toISOString().split("T")[0];
    dateElement.textContent = today;

    // Load events from localStorage
    const loadEvents = () => {
        const events = JSON.parse(localStorage.getItem("events")) || [];
        eventList.innerHTML = events.map(
            event => `
            <div class="event">
                <p><strong>${event.date}</strong>: ${event.title} - ${event.desc}</p>
            </div>
            `
        ).join("");
    };

    // Add event
    eventForm.addEventListener("submit", (e) => {
        e.preventDefault();
        const date = document.getElementById("event-date").value;
        const title = document.getElementById("event-title").value;
        const desc = document.getElementById("event-desc").value;

        if (!date || !title || !desc) {
            alert("Wszystkie pola są wymagane!");
            return;
        }

        const events = JSON.parse(localStorage.getItem("events")) || [];
        events.push({ date, title, desc });
        localStorage.setItem("events", JSON.stringify(events));
        eventForm.reset();
        loadEvents();
    });

    // Delete event by title
    deleteEventButton.addEventListener("click", () => {
        const titleToDelete = document.getElementById("delete-title").value.trim();
        if (!titleToDelete) {
            alert("Proszę podać tytuł do usunięcia.");
            return;
        }

        let events = JSON.parse(localStorage.getItem("events")) || [];
        events = events.filter(event => event.title !== titleToDelete);
        localStorage.setItem("events", JSON.stringify(events));
        document.getElementById("delete-title").value = "";
        loadEvents();
    });

    // Initial load
    loadEvents();
});
