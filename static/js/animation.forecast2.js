// async function getapi(url1, url2) {
//   const response1 = await fetch(url1);
//   var data1 = await response1.json();
//   const response2 = await fetch(url2);
//   var data2 = await response2.json();
//   show(data1, data2);
// }

async function getapi(url) {
  const response1 = await fetch(url);
  var data = await response1.json();
  show(data);
}

function show(data) {
  // console.log(data);
  var city = data["timezone"];
  var temp = data["current"]["temp"];
  var list = data["daily"];
  var description = data["current"]["weather"][0]["description"];
  var iconcode = data["current"]["weather"][0]["icon"];
  var iconurl = "http://openweathermap.org/img/w/" + iconcode + ".png";
  $("#demo1").append(`
  <!-- Indicators -->
  <ul class="carousel-indicators mb-0">
    <li data-target="#demo1" data-slide-to="0" class="active"></li>
    <li data-target="#demo1" data-slide-to="1"></li>
    <li data-target="#demo1" data-slide-to="2"></li>
  </ul>
  <!-- Carousel inner -->
  <div class="carousel-inner">
    <div class="carousel-item active">
      <div class="d-flex justify-content-between mb-4 pb-2">
        <div>
          <h2 class="display-2"><strong>${temp}°C</strong></h2>
          <p class="text-muted mb-0">${city}</p>
          <p class="text-muted mb-0">${description.toUpperCase()}</p>
        </div>
        <div>
          <img src="${iconurl}"
            width="80px">
        </div>
      </div>
    </div>
  </div>
  `);

  for (let i = 0; i < list.length; i++) {
    var unixTime = list[i]["dt"];
    var date = new Date(unixTime*1000);
    var icd = list[i]["weather"][0]["icon"];
    var temp_day = list[i]["temp"]["day"];
    var des_day = list[i]["weather"][0]["description"];
    ic = "http://openweathermap.org/img/w/" + icd + ".png";
    addRow("demo");
  }
  function addRow(tableID){
    let tableRef = document.getElementById(tableID);
    let newRow = tableRef.insertRow(-1);
    let newCell0 = newRow.insertCell(0);
    let newCell1 = newRow.insertCell(1);
    let newCell2 = newRow.insertCell(2);
    let newCell3 = newRow.insertCell(3);
    let newText0 = document.createTextNode(date.toLocaleDateString("es", { "weekday": "long" }).toUpperCase() + " " + date.toLocaleDateString("es", { "day": "numeric" }));
    let newText1 = document.createTextNode(temp_day+" °C");
    let newText2 = document.createTextNode(des_day.toUpperCase());
    let img = document.createElement("div");
    img.innerHTML = `<img src="${ic}" width=50px"></img>`;
    newCell0.appendChild(newText0);
    newCell1.appendChild(newText1);
    newCell2.appendChild(newText2);
    newCell3.appendChild(img);
  }
  // for (let i = 0; i < list.length; i++) {
  //   var unixTime = list[i]["dt"];
  //   var date = new Date(unixTime*1000);
  //   var icd = list[i]["weather"][0]["icon"];
  //   var temp_day = list[i]["temp"]["day"];
  //   var des_day = list[i]["weather"][0]["description"];
  //   ic = "http://openweathermap.org/img/w/" + icd + ".png";
  //   $(".demo").append(`
  //   <div class="card mb-4" style="border-radius: 25px;">
  //     <div class="card-body p-4">
  //       <div class="carousel slide" data-ride="carousel">
  //         <div class="d-flex justify-content-around text-center mb-4 pb-3 pt-2">
  //           <div class="flex-column">${date.toLocaleDateString("es", { "weekday": "long" }).toUpperCase()}
  //             <p class="small"><strong>${temp_day}°C</strong></p>
  //             <i class="fas fa-sun fa-2x mb-3" style="color: #ddd;"></i>
  //             <p class="mb-0"><strong>${des_day.toUpperCase()}</strong></p>
  //             <img src="${ic}"width="100px">
  //           </div>
  //         </div>
  //       </div>
  //     </div>
  //   </div>
  //    `);
  // }
}

uri1 = "http://localhost/api/v1";
uri2 = "http://localhost/api/v2";
// getapi(uri1, uri2);
getapi(uri2);
