import { showNotificationError } from './implementation.js';
import config from "./config.js";


(() => {
    function drawMap(latitude, longitude) {
        const map = L.map('map').setView([latitude, longitude], 13);
        L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
            maxZoom: 19,
            attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
        }).addTo(map);

        return map;
    }

    const host = config.host;

    axios.get(`${host}/geo/position`)
        .then(response => {
            console.log(response);

            const { latitude, longitude } = response?.data?.geo;
            const ip = response?.data?.ip;

            if (latitude === null || longitude === null) {
                throw Error("Either latitude or longitude not present in server response");
            }
            if (ip === null) {
                throw Error("IP not present in server response");
            }

            // drawing map
            const map = drawMap(latitude, longitude);
            // drawing marker
            const marker = L.marker([latitude, longitude]).addTo(map);
            marker.bindPopup(`<b>${ip}</b>`).openPopup();
        })
        .catch(err => {
            console.error(err);
            showNotificationError(err?.response?.data?.detail);
            // drawing plain map centered on New York because I love New York
            const NewYorkLatitude = 40.73;
            const NewYorkLongitude = -73.93;
            drawMap(NewYorkLatitude, NewYorkLongitude);
        });
})();
