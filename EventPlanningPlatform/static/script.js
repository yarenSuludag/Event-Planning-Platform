document.addEventListener('DOMContentLoaded', function() {
    fetch('http://localhost:8000/api/events/')
    .then(response => response.json())
    .then(data => {
        const eventList = document.getElementById('event-list');
        data.forEach(event => {
            const eventItem = document.createElement('div');
            eventItem.className = 'event-item';
            eventItem.innerHTML = `<h3>${event.name}</h3><p>${event.description}</p><p>${event.date}</p>`;
            eventList.appendChild(eventItem);
        });
    })
    .catch(error => console.error('Hata oluştu:', error));
});
