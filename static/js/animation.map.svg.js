// select the canvas element created in the html.
var canvas = document.getElementById("my_dataviz");

// Actual width and height. No idea if clienWidth would be a better option..?
var width = canvas.offsetWidth;
var height = canvas.offsetHeight;

// Set a projection for the map. Projection = transform a lat/long on a position on the 2d map.
var projection = d3
  .geoNaturalEarth1()
  .scale(width / 1.3 / Math.PI)
  .translate([width / 2, height / 2]);

// Get the 'context'
var ctx = canvas.getContext("2d");

// geographic path generator for given projection and canvas context
const pathGenerator = d3.geoPath(projection, ctx);

// Draw a background
// ctx.fillStyle = '#ddd';
// ctx.fillRect(0, 0, width, height);

// Load external data and boot
d3.json(
  "https://raw.githubusercontent.com/holtzy/D3-graph-gallery/master/DATA/world.geojson",
  function (data) {
    // initialize the path
    ctx.beginPath();

    // Got the positions of the path
    pathGenerator(data);

    // Fill the paths
    ctx.fillStyle = "#999";
    ctx.fill();

    // Add stroke
    ctx.strokeStyle = "#69b3a2";
    ctx.stroke();
  }
);
