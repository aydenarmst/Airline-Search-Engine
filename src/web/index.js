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
function changeInputOptions() {
    var selectedOption = dropdown.value;

    inputDiv.innerHTML = "";

    switch (selectedOption) {
        case "0":
            inputDiv.innerHTML = generateAirlineHTML(0);
            console.log(generateAirlineHTML(0));
            break;
        case "1":
            inputDiv.innerHTML = `
                <label for="stopsInput">Number of Stops:</label>
                <input type="number" id="stopsInput" name="stops" min="0">
            `;
            break;
        case "2":
            inputDiv.innerHTML = `
                <label for="codeShareInput">Code Share:</label>
                <input type="checkbox" id="codeShareInput" name="codeShare">
            `;
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
            handlefindAirline();
            break;
        case "1":
            handleAirlinesWithStops();
            break;
        case "2":
            handleAirlinesWithCodeShare();
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



function handlefindAirline()
{
	var inputInfo = getAirlineFormData(0);
    removeEmptyStringAttributes(inputInfo);
	postData({"function" : "findAirline", "conditions" : JSON.stringify(inputInfo)}, displayData);
}

function handleAirlinesWithStops()
{
	
	var stopInput = document.getElementById("stopsInput");
	if(isNaN(stopInput.value)) return 0;
	var stopCount = parseInt(stopInput.value);

}

function handleAirlinesWithCodeShare()
{
	var codeShare = document.getElementById('codeShareInput');
	if (codeShare.checked) {
		console.log("Checkbox is checked");
	} else {
		console.log("Checkbox is not checked");
	}
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