var map = L.map('map', {
    minZoom: 6,
    maxBounds: [
        //south-west
        [40, -6],
        //north-east
        [52, 10]
    ],
}).setView([46.86584459507945, 2.4942937666232954], 6);

let marker;

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors',
    maxZoom: 18
}).addTo(map);

function onMapClick(e) {
    if (!modelReady) return
    let lat = e.latlng.lat.toFixed(6);
    let long = e.latlng.lng.toFixed(6);


    if (marker) {
        map.removeLayer(marker); // Remove previous marker
    }
    marker = L.marker([lat, long]).addTo(map); // Add new marker

    document.getElementById('info').innerHTML = 'Chargement...';

    fetch('/get_geo_info', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({lat: lat, long: long})
    }).then((r) => {
        return r.json()
    }).then((o) => {

        let names = o.names

        let innerUl = names.map((value) => `<li>${value}</li>`).join('')
        document.getElementById('info').innerHTML = `<ul>${innerUl}</ul>`
    })
}

map.on('click', onMapClick);