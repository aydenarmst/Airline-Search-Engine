var dropdown = document.getElementById("dropdownMenu");
var inputDiv = document.getElementById("inputDiv");
var displayDiv = document.getElementById("displayDiv");

const serverUrl = "http://localhost:8080/data";

function removeEmptyStringAttributes(obj) {
    for (const key in obj) {
      if (obj.hasOwnProperty(key) && obj[key] === "") {
        delete obj[key];
      }
    }
  }


function generateAirlineHTML(id)
{
  return `<div id="specificAirline"><label for="airlineId${id}">Airline ID:</label>
  <input type="text" id="airlineId${id}" name="airlineId" required>

  <label for="airlineName${id}">Name:</label>
  <input type="text" id="airlineName${id}" name="airlineName" required>

  <label for="airlineAlias${id}">Alias:</label>
  <input type="text" id="airlineAlias${id}" name="airlineAlias">

  <label for="iataCode${id}">IATA Code:</label>
  <input type="text" id="iataCode${id}" name="iataCode">

  <label for="icaoCode${id}">ICAO Code:</label>
  <input type="text" id="icaoCode${id}" name="icaoCode">

  <label for="callsign${id}">Callsign:</label>
  <input type="text" id="callsign${id}" name="callsign">

  <label for="country${id}">Country:</label>
  <input type="text" id="country${id}" name="country" required>

  <label for="active${id}">Active (Y/N):</label>
  <input type="text" id="active${id}" name="active" maxlength="1" required pattern="[YNyn]"></div>`;
}

function generateAirportHTML(id) {
return `<div id="specificAirline">
    <label for="airportId${id}">Airport ID:</label>
    <input type="text" id="airportId${id}" name="airportId" required>

    <label for="airportName${id}">Name:</label>
    <input type="text" id="airportName${id}" name="airportName" required>

    <label for="city${id}">City:</label>
    <input type="text" id="city${id}" name="city" required>

    <label for="country${id}">Country:</label>
    <input type="text" id="country${id}" name="country" required>

    <label for="iataCode${id}">IATA Code:</label>
    <input type="text" id="iataCode${id}" name="iataCode">

    <label for="icaoCode${id}">ICAO Code:</label>
    <input type="text" id="icaoCode${id}" name="icaoCode">

    <label for="latitude${id}">Latitude:</label>
    <input type="text" id="latitude${id}" name="latitude" required>

    <label for="longitude${id}">Longitude:</label>
    <input type="text" id="longitude${id}" name="longitude" required>

    <label for="altitude${id}">Altitude:</label>
    <input type="text" id="altitude${id}" name="altitude" required>

    <label for="timezone${id}">Timezone:</label>
    <input type="text" id="timezone${id}" name="timezone" required>

    <label for="dst${id}">DST:</label>
    <input type="text" id="dst${id}" name="dst" maxlength="1" required pattern="[EASOZNUeasoznu]">

    <label for="tzDatabase${id}">Tz Database Timezone:</label>
    <input type="text" id="tzDatabase${id}" name="tzDatabase" required>

    <label for="type${id}">Type:</label>
    <input type="text" id="type${id}" name="type" required>

    <label for="source${id}">Source:</label>
    <input type="text" id="source${id}" name="source" required>
</div>`;
}

function generateAirportHTML(id) {
    return `<div id="specificAirline">
        <label for="airportId${id}">Airport ID:</label>
        <input type="text" id="airportId${id}" name="airportId" required>
    
        <label for="airportName${id}">Name:</label>
        <input type="text" id="airportName${id}" name="airportName" required>
    
        <label for="city${id}">City:</label>
        <input type="text" id="city${id}" name="city" required>
    
        <label for="country${id}">Country:</label>
        <input type="text" id="country${id}" name="country" required>
    
        <label for="iataCode${id}">IATA Code:</label>
        <input type="text" id="iataCode${id}" name="iataCode">
    
        <label for="icaoCode${id}">ICAO Code:</label>
        <input type="text" id="icaoCode${id}" name="icaoCode">
    
        <label for="latitude${id}">Latitude:</label>
        <input type="text" id="latitude${id}" name="latitude" required>
    
        <label for="longitude${id}">Longitude:</label>
        <input type="text" id="longitude${id}" name="longitude" required>
    
        <label for="altitude${id}">Altitude:</label>
        <input type="text" id="altitude${id}" name="altitude" required>
    
        <label for="timezone${id}">Timezone:</label>
        <input type="text" id="timezone${id}" name="timezone" required>
    
        <label for="dst${id}">DST:</label>
        <input type="text" id="dst${id}" name="dst" maxlength="1" required pattern="[EASOZNUeasoznu]">
    
        <label for="tzDatabase${id}">Tz Database Timezone:</label>
        <input type="text" id="tzDatabase${id}" name="tzDatabase" required>
    
        <label for="type${id}">Type:</label>
        <input type="text" id="type${id}" name="type" required>
    
        <label for="source${id}">Source:</label>
        <input type="text" id="source${id}" name="source" required>
    </div>`;
}


function findDHopsCitiesHTML(id)
{
    return `<div id="specificAirline">
        <label for="city${id}">City:</label>
        <input type="text" id="city${id}" name="city" required>

        <label for="hopCount${id}">Hop Count:</label>
        <input type="number" id="hopCount${id}" name="hopCount" required>
    </div>`;
}


function getAirportFormData(id) {
const airportId = document.getElementById(`airportId${id}`).value;
const airportName = document.getElementById(`airportName${id}`).value;
const city = document.getElementById(`city${id}`).value;
const country = document.getElementById(`country${id}`).value;
const iataCode = document.getElementById(`iataCode${id}`).value;
const icaoCode = document.getElementById(`icaoCode${id}`).value;
const latitude = document.getElementById(`latitude${id}`).value;
const longitude = document.getElementById(`longitude${id}`).value;
const altitude = document.getElementById(`altitude${id}`).value;
const timezone = document.getElementById(`timezone${id}`).value;
const dst = document.getElementById(`dst${id}`).value;
const tzDatabase = document.getElementById(`tzDatabase${id}`).value;
const type = document.getElementById(`type${id}`).value;
const source = document.getElementById(`source${id}`).value;

return {
    "Airport ID": airportId,
    "Name": airportName,
    "City": city,
    "Country": country,
    "IATA": iataCode,
    "ICAO": icaoCode,
    "Latitude": latitude,
    "Longitude": longitude,
    "Altitude": altitude,
    "Timezone": timezone,
    "DST": dst,
    "Tz Database Timezone": tzDatabase,
    "Type": type,
    "Source": source
};
}
  
  

function getAirlineFormData(id) {
    const airlineId = document.getElementById(`airlineId${id}`).value;
    const airlineName = document.getElementById(`airlineName${id}`).value;
    const airlineAlias = document.getElementById(`airlineAlias${id}`).value;
    const iataCode = document.getElementById(`iataCode${id}`).value;
    const icaoCode = document.getElementById(`icaoCode${id}`).value;
    const callsign = document.getElementById(`callsign${id}`).value;
    const country = document.getElementById(`country${id}`).value;
    const active = document.getElementById(`active${id}`).value;
    return {
      "Airline ID" : airlineId,
      "Name" : airlineName,
      "Alias" : airlineAlias,
      "IATA" : iataCode,
      "ICAO" : icaoCode,
      "Callsign" : callsign,
      "Country" : country,
      "Active" : active
    };
}

function findDHopsCitiesData(id) {
    const city = document.getElementById(`city${id}`).value;
    const hopCount = document.getElementById(`hopCount${id}`).value;
    return {
        "City": city,
        "Hop Count": hopCount
    };
}




// function generateRouteHTML(id) {
//     return `<div id="specificAirline">
//       <label for="airline${id}">Airline:</label>
//       <input type="text" id="airline${id}" name="airline" required>
  
//       <label for="airlineId${id}">Airline ID:</label>
//       <input type="text" id="airlineId${id}" name="airlineId" required>
  
//       <label for="sourceAirport${id}">Source Airport:</label>
//       <input type="text" id="sourceAirport${id}" name="sourceAirport" required>
  
//       <label for="sourceAirportId${id}">Source Airport ID:</label>
//       <input type="text" id="sourceAirportId${id}" name="sourceAirportId" required>
  
//       <label for="destinationAirport${id}">Destination Airport:</label>
//       <input type="text" id="destinationAirport${id}" name="destinationAirport" required>
  
//       <label for="destinationAirportId${id}">Destination Airport ID:</label>
//       <input type="text" id="destinationAirportId${id}" name="destinationAirportId" required>
  
//       <label for="codeshare${id}">Codeshare (Y/N):</label>
//       <input type="text" id="codeshare${id}" name="codeshare" maxlength="1" required pattern="[YNyn]">
  
//       <label for="stops${id}">Stops:</label>
//       <input type="text" id="stops${id}" name="stops" required>
  
//       <label for="equipment${id}">Equipment:</label>
//       <input type="text" id="equipment${id}" name="equipment" required>
//     </div>`;
// }

// function getRouteFormData(id) {
//     const airline = document.getElementById(`airline${id}`).value;
//     const airlineId = document.getElementById(`airlineId${id}`).value;
//     const sourceAirport = document.getElementById(`sourceAirport${id}`).value;
//     const sourceAirportId = document.getElementById(`sourceAirportId${id}`).value;
//     const destinationAirport = document.getElementById(`destinationAirport${id}`).value;
//     const destinationAirportId = document.getElementById(`destinationAirportId${id}`).value;
//     const codeshare = document.getElementById(`codeshare${id}`).value;
//     const stops = document.getElementById(`stops${id}`).value;
//     const equipment = document.getElementById(`equipment${id}`).value;
  
//     return {
//       "Airline": airline,
//       "Airline ID": airlineId,
//       "Source Airport": sourceAirport,
//       "Source Airport ID": sourceAirportId,
//       "Destination Airport": destinationAirport,
//       "Destination Airport ID": destinationAirportId,
//       "Codeshare": codeshare,
//       "Stops": stops,
//       "Equipment": equipment
//     };
//   }
  

  
function changeInputOptions() {
    var selectedOption = dropdown.value;

    inputDiv.innerHTML = "";

    switch (selectedOption) {
        case "0":
            inputDiv.innerHTML = generateAirlineHTML(0);
            console.log(generateAirlineHTML(0));
            break;
        case "1":
            inputDiv.innerHTML = generateAirportHTML(0);
            break;
        case "2":
            inputDiv.innerHTML = findDHopsCitiesHTML(0);
            break;
        case "3":
            inputDiv.innerHTML = `
                <label for="activeCountryInput">Country:</label>
                <input type="text" id="countryInput" name="activeCountry">
            `;
            break;
        default:
            break;
    }
}

function handleSubmit() {
    var selectedOption = dropdown.value;

    switch (selectedOption) {
        case "0":
            handleFindAirline();
            break;
        case "1":
            handleFindAirports();
            break;
        case "2":
            // handlefindRoutes();
            handleFindDHops();
            break;
        case "3":
            handleActiveAirlinesInCountry();
            break;
        default:
            break;
    }
}



function displayData(data)
{
	// displayDiv.innerHTML = "";
    var newString;
    if(data.length == 0)
    {
        newString = "<h1>No Results Found.</h1>";
    }
    var newString = "<div id = \"nameGrid\">";
	for(let i = 0; i < data.length; ++i)
    {
        newString += `<p>${data[i]["Name"]}</p>`
    }
    newString += "</div>";
    displayDiv.innerHTML = newString;
}

function displayDHops(data)
{
	// displayDiv.innerHTML = "";
    var newString;
    if(data.length == 0)
    {
        newString = "<h1>No Results Found.</h1>";
    }
    var newString = "<div id = \"nameGrid\">";
	for(let i = 0; i < data.length; ++i)
    {
        newString += `<p>${data[i]["City"]} : ${data[i]["Level"]}</p>`
    }
    newString += "</div>";
    displayDiv.innerHTML = newString;
}



function handleFindAirline()
{
	var inputInfo = getAirlineFormData(0);
    removeEmptyStringAttributes(inputInfo);
	postData({"function" : "findAirline", "conditions" : JSON.stringify(inputInfo)}, displayData);
}

function handleFindAirports()
{
	
    var inputInfo = getAirportFormData(0);
    removeEmptyStringAttributes(inputInfo);
	postData({"function" : "findAirports", "conditions" : JSON.stringify(inputInfo)}, displayData);

}
function handlefindRoutes()
{
	
    var inputInfo = getRouteFormData(0);
    removeEmptyStringAttributes(inputInfo);
	postData({"function" : "findRoutes", "conditions" : JSON.stringify(inputInfo)}, displayData);

}

function handleFindDHops()
{
    var inputInfo = findDHopsCitiesData(0);
    removeEmptyStringAttributes(inputInfo);
    postData({"function" : "findDHopsCities", "data" : JSON.stringify(inputInfo)}, displayDHops);
}

function handleActiveAirlinesInCountry()
{
	var countryName = document.getElementById("countryInput");
}


function postData(data, callback)
{
	fetch(serverUrl, {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json',
		},
		body: JSON.stringify(data),
	})
	.then(response => response.json())
	.then(data => {
        console.log(data);
		callback(data);
	})
	.catch((error) => {
		console.error('Error:', error);
	});
}

// Add an event listener to the dropdown
dropdown.addEventListener("change", changeInputOptions);
submitButton.addEventListener("click", handleSubmit);
changeInputOptions();