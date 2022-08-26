// API call
uri = "http://localhost/api/v2";

fetch(uri)
  .then((response) => response.json())
  .then((data) => {
    //console.log(data);

    // Weather main data
    let current = data.current;
    let description = data.current.weather[0].description;
    let temp = Math.round(data.current.temp);
    let name = data.timezone;
    let unixTime = current.dt;
    let date = new Date(unixTime * 1000);
    let icd = current.weather[0].icon;
    let list = data.daily;
    ic = "http://openweathermap.org/img/w/" + icd + ".png";
    document.getElementById("description").innerHTML =
      description.toUpperCase();
    document.getElementById("temp").innerHTML = temp + "°C";
    document.getElementById("city").innerHTML = name;
    document.getElementById("month").innerHTML =
      date.toLocaleDateString("es", { month: "long" }).toUpperCase() +
      " " +
      date.toLocaleDateString("es", { day: "numeric" }) +
      " " +
      date.toLocaleDateString("es", { year: "numeric" }) +
      ", ";
    document.getElementById("day").innerHTML = date
      .toLocaleDateString("es", { weekday: "long" })
      .toUpperCase();
    document.getElementById(
      "icon"
    ).innerHTML = `<img src="${ic}" width=150px"></img>`;
    for (let i = 1; i < list.length; i++) {
      var unixTime1 = list[i]["dt"];
      var date1 = new Date(unixTime1 * 1000);
      var icon = list[i].weather[0].icon;
      var temp_day = list[i].temp.day;
      pathicon = "http://openweathermap.org/img/w/" + icon + ".png";
      addElement("item");
    }
    function addElement(Id) {
      let item = document.getElementById(Id);
      let div = document.createElement("div");
      div.classList.add("weakly-weather-item");
      div.innerHTML = `<p class="mb-1">${date1
        .toLocaleDateString("es", { weekday: "short" })
        .toUpperCase()}</p><img src="${pathicon}" width=50px"></img><p class="mb-0">${Math.round(
        temp_day
      )} °C</p>`;
      item.appendChild(div);
    }
  });
