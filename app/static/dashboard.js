const pumpSwitch = document.getElementById("pumpSwitch");
const pumpStatus = document.getElementById("pumpStatus");
const waterFlow = document.getElementById("waterFlow");
const waterFlowSum = document.getElementById("waterFlowSum");
const waterFlowSince = document.getElementById("waterflowSince");

const temperatureAir = document.getElementById("temperatureAir");
const humidityAir = document.getElementById("humidityAir");

const voltageBattery = document.getElementById("voltageBattery");
const voltageSolar = document.getElementById("voltageSolar");

const moistureGround = document.getElementById("moistureGround");
const temperatureGround = document.getElementById("temperatureGround");

const info = document.getElementById("info");


const REFRESH_SECONDS = 5;

info.innerText = `${info.innerText} ${REFRESH_SECONDS} seconds`;

const updateStatusIcon = (isSuccessful) => {
    const statusIcon = document.getElementById('statusIcon');
    statusIcon.innerHTML = isSuccessful
        ? '<h5><i class="bi bi-check-circle text-success"></i> Connected</h5>'
        : '<h5><i class="bi bi-x-circle text-danger"></i> Disconnected</h5>';
};

pumpSwitch.addEventListener('change', async () => {
    const switchStatus = pumpSwitch.checked;
    console.log("Switch is now", switchStatus);

    // Send a POST request to the server to update the switch status
    await fetch(`/switch/${switchStatus}`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json'
        }
    });
});

async function updateSensorStatus() {
    try {
        const response = await fetch('/status');

        updateStatusIcon(response.ok);

        const sensorStatus = await response.json();
        console.log("Status:", sensorStatus);

        if (sensorStatus.relay_on) {
            pumpSwitch.checked = true;
            pumpStatus.innerHTML = "ON";
        } else {
            pumpSwitch.checked = false;
            pumpStatus.innerHTML = "OFF";
        }

        if (waterFlow) {
            waterFlow.innerHTML = sensorStatus.waterflow;
        }
        if (waterFlowSum) {
            waterFlowSum.innerHTML = sensorStatus.waterflow_sum;
        }
        if (waterFlowSince) {
            waterFlowSince.innerHTML = sensorStatus.waterflow_since;
        }
        if (temperatureAir) {
            temperatureAir.innerHTML = sensorStatus.temperature_air;
            // addData(new Date(), sensorStatus.temperature_air);
        }
        if (humidityAir) {
            humidityAir.innerHTML = sensorStatus.humidity_air;
        }

        if (voltageBattery) {
            voltageBattery.innerHTML = sensorStatus.voltage_battery;
        }

        if (voltageSolar) {
            voltageSolar.innerHTML = sensorStatus.voltage_solar;
        }

        if (moistureGround) {
            moistureGround.innerHTML = sensorStatus.moisture_ground;
        }

        if (temperatureGround) {
            temperatureGround.innerHTML = sensorStatus.temperature_ground;
        }

    } catch (e) {
        console.log("Failed to connect to API: ", e);
        updateStatusIcon(false);
    }

}

setInterval(updateSensorStatus, REFRESH_SECONDS * 1000);

// function formatDateTime(date) {
//     const year = date.getFullYear();
//     const month = (date.getMonth() + 1).toString().padStart(2, '0'); // January is 0!
//     const day = date.getDate().toString().padStart(2, '0');
//     const hours = date.getHours().toString().padStart(2, '0');
//     const minutes = date.getMinutes().toString().padStart(2, '0');
//     const seconds = date.getSeconds().toString().padStart(2, '0');

//     return `${hours}:${minutes}:${seconds} ${year}-${month}-${day}`;
// }

// function setupGraph() {
//     return new Chart("xy-plot", {
//         type: "line",
//         data: {
//             labels: [],
//             datasets: [{
//                 fill: false,
//                 lineTension: 0,
//                 backgroundColor: "rgba(0,0,255,1.0)",
//                 borderColor: "rgba(0,0,255)",
//                 data: []
//             }]
//         },
//         options: {
//             legend: { display: false },
//             // scales: {
//             //     yAxes: [{ ticks: { min: 6, max: 16 } }],
//             // }
//         }
//     });
// }

// const xyChart = setupGraph();

// function addData(x, y) {
//     console.log("Adding", y);

//     xyChart.data.labels.push(formatDateTime(x));
//     xyChart.data.datasets[0].data.push(y);

//     // Check if the data array exceeds 20 data points
//     if (xyChart.data.datasets[0].data.length > 5) {
//         // Remove the oldest data point
//         xyChart.data.datasets.forEach((dataset) => {
//             dataset.data.shift();
//         });
//         xyChart.data.labels.shift();
//     }
//     xyChart.update(); // Refresh the chart to display the new data
// }
