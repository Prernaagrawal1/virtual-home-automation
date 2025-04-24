const toggleButton = (appliance) => {
    axios.post(`/api/toggle/${appliance}`)
        .then(response => {
            getStatus();
        })
        .catch(error => {
            console.error("There was an error toggling the appliance!", error);
        });
};

const getStatus = () => {
    axios.get('/api/status')
        .then(response => {
            const appliances = response.data;
            let statusText = "Appliance Status:<br>";
            for (const appliance in appliances) {
                statusText += `${appliance.charAt(0).toUpperCase() + appliance.slice(1)}: ${appliances[appliance] ? 'On' : 'Off'}<br>`;
            }
            document.getElementById("status").innerHTML = statusText;
        })
        .catch(error => {
            console.error("There was an error getting the status!", error);
        });
};

document.getElementById("toggle-light").addEventListener("click", () => toggleButton("light"));
document.getElementById("toggle-fan").addEventListener("click", () => toggleButton("fan"));
document.getElementById("toggle-ac").addEventListener("click", () => toggleButton("ac"));

getStatus();
