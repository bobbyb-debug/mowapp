// Function to initialize the calendar
function initializeCalendar() {
    const calendarContainer = document.getElementById("calendar");

    // Check if the calendar container exists
    if (!calendarContainer) {
        console.error("Calendar container not found!");
        return;
    }

    // Create a simple calendar using a table
    const currentDate = new Date();
    const month = currentDate.getMonth();  // Current month (0 - 11)
    const year = currentDate.getFullYear();  // Current year

    // Set the month and year at the top of the calendar
    const monthNames = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];
    const monthYearHeader = document.createElement("h2");
    monthYearHeader.innerText = `${monthNames[month]} ${year}`;
    calendarContainer.appendChild(monthYearHeader);

    // Create the calendar grid (7 columns for days of the week)
    const table = document.createElement("table");
    const headerRow = document.createElement("tr");
    const daysOfWeek = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"];

    // Create header row for days of the week
    daysOfWeek.forEach(day => {
        const th = document.createElement("th");
        th.innerText = day;
        headerRow.appendChild(th);
    });
    table.appendChild(headerRow);

    // Get the first day of the month and the number of days in the month
    const firstDayOfMonth = new Date(year, month, 1).getDay();
    const daysInMonth = new Date(year, month + 1, 0).getDate();

    let dayCounter = 1;
    let currentRow = document.createElement("tr");

    // Add empty cells for the days before the 1st of the month
    for (let i = 0; i < firstDayOfMonth; i++) {
        const td = document.createElement("td");
        currentRow.appendChild(td);
    }

    // Loop through the days of the month
    for (let i = firstDayOfMonth; i < 7; i++) {
        const td = document.createElement("td");
        td.innerText = dayCounter;
        td.classList.add("calendar-day");
        td.addEventListener("click", () => handleDayClick(dayCounter));
        currentRow.appendChild(td);
        dayCounter++;
    }
    table.appendChild(currentRow);

    // Continue creating rows for the rest of the month
    while (dayCounter <= daysInMonth) {
        currentRow = document.createElement("tr");
        for (let i = 0; i < 7 && dayCounter <= daysInMonth; i++) {
            const td = document.createElement("td");
            td.innerText = dayCounter;
            td.classList.add("calendar-day");
            td.addEventListener("click", () => handleDayClick(dayCounter));
            currentRow.appendChild(td);
            dayCounter++;
        }
        table.appendChild(currentRow);
    }

    // Append the table to the calendar container
    calendarContainer.appendChild(table);
}

// Function to handle clicks on a specific day
function handleDayClick(day) {
    alert(`You clicked on ${day}`);
    // You can extend this functionality to add events, appointments, or tasks to specific days
}

// Initialize the calendar on page load
window.onload = function() {
    initializeCalendar();
};
