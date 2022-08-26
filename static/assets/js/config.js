// Most of the params can also be set in the query string
// ex: http://{yourdomain}/index.html?apikey=00000000000000000000000000000000&latitude=45.4973&longitude=-73.5707&lang=en&theme=black

var apiKey = "9a33c608af643fd3bf10cb2a2eedaa38"; // OpenWeatherMap api key
var latitude = "-25.4973"; // Showing Montreal.  search your city on google map and look at the url to get your latitude and longitude
var longitude = "-57.6359";
var lang = "sp"; // too many options.  check here https://openweathermap.org/api/one-call-api#multi
var units = "metric"; // metric (Celsius), imperial (Fahrenheit), standard (Kelvin)
var degreeSymbol = "C"; // C or F
var rainPrecUnit = "mm";
var snowPrecUnit = "cm";
var windUnit = "km/h";
var forecastNbOfDays = 5; // 0 to 8
var hourlyNbOfHours = 12; // 0-49
var theme = "Blue"; // "blue", "black", "white"

var showScrollingAlerts = true;
var showCurrentWeather = true;
var showCurrentIcon = true;
var showCurrentSummary = true;
var showCurrentWind = true;
var showCurrentWindBearing = true;
var showCurrentHumidity = true;
var showCurrentDate = true;
var showCurrentTime = true;

var showHourlyIcon = true;
var showHourlyWind = true;
var showHourlyWindBearing = false;
var showHourlyAccumulation = true;
var showHourlyHumidity = true;
var showHourlyProbability = true;

var showForecastIcon = true;
var showForecastSummary = true;
var showForecastMinTemp = true;
var showForecastWind = true;
var showForecastWindBearing = false;
var showForecastHumidity = true;
var showForecastAccumulation = true;
var showForecastProbability = true;

var debugging = false; // will allow showing forecast for past days.  Usefull when playing with sample data

// Add your language if missing
var labelsDict =
{
    "default": {
        todayLabel: "Hoy",
        windLabel: "Viento",
        apparentTempLabel: "Sensacion",
        week: ['Domingo', 'Lunes', 'Martes', 'Miercoles', 'Jueves', 'Viernes', 'Sábado'],
        month: ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
    },
    "fr": {
        todayLabel: "Aujourd'hui",
        windLabel: "vent",
        apparentTempLabel: "ressentie",
        week: ['Dimanche', 'Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi'],
        month: ['Janvier', 'Février', 'Mars', 'Avril', 'Mai', 'Juin', 'Juillet', 'Août', 'Septembre', 'Octobre', 'Novembre', 'Décembre']
    }
};

var labels;
var url;
