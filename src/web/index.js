var dropdown = document.getElementById("dropdownMenu");
var inputDiv = document.getElementById("inputDiv");
var displayDiv = document.getElementById("displayDiv");

const serverUrl = "http://localhost:8080/data";

function changeInputOptions() {
    var selectedOption = dropdown.value;

    inputDiv.innerHTML = "";

    switch (selectedOption) {
        case "0":
            inputDiv.innerHTML = `
                <label for="countryInput">Country:</label>
                <input type="text" id="countryInput" name="country">
            `;
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

function displayData(data)
{
	// displayDiv.innerHTML = "";
    var newString = "";
	for(let i = 0; i < data.length; ++i)
    {
        newString += `${data[i]["Name"]},`
    }
    displayDiv.innerHTML = newString;


}

function postData(data)
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
        // console.log(data);
		displayData(data)
	})
	.catch((error) => {
		console.error('Error:', error);
	});
}

function handleAirportsInCountry()
{
	var countryInput = document.getElementById("countryInput");
	postData({"function" : "Handle Airports In Country", "country" : countryInput.value});
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
function handleSubmit() {
    var selectedOption = dropdown.value;

    switch (selectedOption) {
        case "0":
            handleAirportsInCountry();
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

// Add an event listener to the dropdown
dropdown.addEventListener("change", changeInputOptions);
submitButton.addEventListener("click", handleSubmit);
changeInputOptions();