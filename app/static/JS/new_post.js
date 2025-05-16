function updateValue(spanId, value) {
    document.getElementById(spanId).textContent = value;
}

document.addEventListener('DOMContentLoaded', () => {
    const locationInput  = document.getElementById('location');
    const suggestionsBox = document.getElementById('location-suggestions');
    const latInput       = document.getElementById('latitude');
    const lngInput       = document.getElementById('longitude');

    // Initialize map & draggable marker
    const map    = L.map('map').setView([0, 0], 2);
    const marker = L.marker([0, 0], { draggable: true }).addTo(map);

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; OpenStreetMap contributors'
    }).addTo(map);

    // Whenever marker is dragged, update hidden lat/lng
    marker.on('moveend', () => {
        const { lat, lng } = marker.getLatLng();
        latInput.value = lat;
        lngInput.value = lng;
    });

    let debounceTimeout;
    locationInput.addEventListener('input', () => {
        const query = locationInput.value.trim();
        if (!query) {
            suggestionsBox.style.display = 'none';
            return;
        }
        clearTimeout(debounceTimeout);
        debounceTimeout = setTimeout(() => {
            fetch(`https://nominatim.openstreetmap.org/search?format=json&addressdetails=1&q=${encodeURIComponent(query)}`)
              .then(res => res.json())
              .then(data => {
                suggestionsBox.innerHTML = '';
                if (data.length) {
                  data.forEach(loc => {
                    const name = loc.display_name;
                    const li = document.createElement('li');
                    li.textContent = name;
                    li.classList.add('list-group-item');
                    li.addEventListener('click', () => {
                      // 1) Fill the text input
                      locationInput.value = name;
                      // 2) Hide suggestions
                      suggestionsBox.style.display = 'none';
                      // 3) Move map & marker
                      const lat = parseFloat(loc.lat);
                      const lon = parseFloat(loc.lon);
                      map.setView([lat, lon], 15);
                      marker.setLatLng([lat, lon]);
                      // 4) Update hidden inputs
                      latInput.value = lat;
                      lngInput.value = lon;
                    });
                    suggestionsBox.appendChild(li);
                  });
                  suggestionsBox.style.display = 'block';
                } else {
                  suggestionsBox.style.display = 'none';
                }
              })
              .catch(err => console.error('Error fetching suggestions:', err));
        }, 300); // debounce
    });

    // Hide suggestions when clicking elsewhere
    document.addEventListener('click', e => {
      if (!locationInput.contains(e.target) && !suggestionsBox.contains(e.target)) {
        suggestionsBox.style.display = 'none';
      }
    });

    // Optional: allow clicking map to set marker & hidden fields
    map.on('click', e => {
      marker.setLatLng(e.latlng);
      latInput.value = e.latlng.lat;
      lngInput.value = e.latlng.lng;
    });
});