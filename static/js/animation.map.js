// Initialize the map
// [50, -0.1] are the latitude and longitude
// 4 is the zoom
// mapid is the id of the div where the map will appear
var mymap = L
  .map('mapid')
  .setView([50, -0.1], 4);

// Add a tile to the map = a background. Comes from OpenStreetmap
L.tileLayer(
    'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a>',
    maxZoom: 6,
    }).addTo(mymap);
