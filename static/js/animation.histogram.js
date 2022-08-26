let listYear = [];
let listMonth = [];
let listCity = [];
let miny = 1947;
let maxy = new Date().getFullYear() + 1;

listYear.push("Año");
for (let i = miny; i < maxy; i++) {
  listYear.push(i);
}

listMonth.push("Mes");
for (let i = 1; i < 13; i++) {
  listMonth.push(i);
}

let selectCity = document.getElementById("combocity");
function setData(data) {
  listCity.push("Estacion");
  for (i = 0; i < data.length; i++) {
    listCity.push(data[i].station);
  }
  mapSelect(selectCity, listCity);
}

const getData = (url) =>
  new Promise((resolve, reject) => {
    fetch(url)
      .then((response) => response.json())
      .then((json) => resolve(json))
      .catch((error) => reject(error));
  });

const url = `http://localhost/api/v5`;
getData(url).then((data) => setData(data));

let selectMonth = document.getElementById("combomonth");
let selectYear = document.getElementById("comboyear");

window.addEventListener("load", (event) => {
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
      graphic(data);
    });
});

function graphic(data1) {
  var arrayLabel = [];
  var arrayData = [];
  for (var i = 0; i < data1.length; i++) {
    arrayLabel.push(data1[i].date);
    arrayData.push(data1[i].tmax);
  }
  const ctx = document.getElementById("histogram").getContext("2d");

  const chart = new Chart(ctx, {
    type: "bar",
    data: {
      labels: arrayLabel,
      datasets: [
        {
          label: "Temperatura Max Historicas",
          data: arrayData,
          backgroundColor: "#27AE60",
          borderColor: "#196F3D",
          borderWidth: 2,
          borderSkipped: false,
        },
      ],
    },
    options: {
      scales: {
        xAxes: [
          {
            display: false,
            barPercentage: 1.3,
            ticks: {
              max: 31,
            },
          },
          {
            display: true,
            ticks: {
              autoSkip: false,
              max: 31,
            },
          },
        ],
        yAxes: [
          {
            ticks: {
              beginAtZero: true,
            },
          },
        ],
      },
    },
  });
}
