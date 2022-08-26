let listCity = ["Select", "Luque", "Paraguarí"];
let listMonth = ["Select", "1", "2", "3", "4", "5"];
let listYear = ["Select", "1980", "1981", "1982", "1999"];

let selectCity = document.getElementById("combocity");
let selectMonth = document.getElementById("combomonth");
let selectYear = document.getElementById("comboyear");

window.addEventListener("load", (event) => {
  mapSelect(selectCity, listCity);
  mapSelect(selectMonth, listMonth);
  mapSelect(selectYear, listYear);
});

function mapSelect(combo, values) {
  combo.innerHTML = "";
  for (let item of values) {
    combo.innerHTML += `
        <option>${item}</option>
        `;
  }
}

const form = document.getElementById("search");
form.addEventListener("submit", (event) => {
  event.preventDefault();
  var city = document.getElementById("combocity").value;
  var year = document.getElementById("comboyear").value;
  var month = document.getElementById("combomonth").value;
  var data = { city: city, month: month, year: year };
  var url = new URL("http://localhost/api/v4");
  for (let k in data) {
    url.searchParams.append(k, data[k]);
  }
  fetch(url)
    .then((response) => response.json())
    .then((data) => {
      console.log(data);
      graphic(data);
    });
});

var margin = { top: 10, right: 30, bottom: 30, left: 60 },
  width = 460 - margin.left - margin.right,
  height = 400 - margin.top - margin.bottom;

// append the svg object to the body of the page
var svg = d3
  .select("#my_dataviz1")
  .append("svg")
  .attr("width", width + margin.left + margin.right)
  .attr("height", height + margin.top + margin.bottom)
  .append("g")
  .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

//Read the data

function graphic(data) {
  for (let i = 0; i < data.length; i++) {
    // Add X axis --> it is a date format
    var x = d3
      .scaleTime()
      .domain(
        d3.extent(data[i], function (d) {
          return d.date;
        })
      )
      .range([0, width]);
  }
  svg
    .append("g")
    .attr("transform", "translate(0," + height + ")")
    .call(d3.axisBottom(x));
  // Add Y axis
  var y = d3.scaleLinear().domain([0, 31]).range([height, 0]);
  svg.append("g").call(d3.axisLeft(y));
  // Add the line
  for (let i = 0; i < data.length; i++) {
    svg
      .append("path")
      .datum(data[i])
      .attr("fill", "none")
      .attr("stroke", "#69b3a2")
      .attr("stroke-width", 1.5)
      .attr(
        "d",
        d3
          .line()
          .x(function (d) {
            return x(d.date);
          })
          .y(function (d) {
            return y(d.value);
          })
      );
  }
  // Add the points
  for (let i = 0; i < data.length; i++) {
    svg
      .append("g")
      .selectAll("dot")
      .data(data[i])
      .enter()
      .append("circle")
      .attr("cx", function (d) {
        return x(d.date);
      })
      .attr("cy", function (d) {
        return y(d.value);
      })
      .attr("r", 5)
      .attr("fill", "#69b3a2");
  }
}
