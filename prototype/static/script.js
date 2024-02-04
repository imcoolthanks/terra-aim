// Initialize variables
const heartRateData = {
    labels: [],
    datasets: [{
        label: 'Heart Rate',
        borderColor: 'rgb(75, 192, 192)',
        borderWidth: 2,
        fill: false,
        data: [],
    }]
};

const ctxHeartRate = document.getElementById('heartRateGraph').getContext('2d');
const heartRateChart = new Chart(ctxHeartRate, {
    type: 'line',
    data: heartRateData,
    options: {
        scales: {
            x: {
                type: 'linear',
                position: 'bottom',
            },
            y: {
                min: 0,
                max: 200,
            }
        }
    }
});

// Function to fetch heart rate data from the API
function fetchHeartRateData() {
    // Make an API GET request to your Flask endpoint for heart rate
    $.get('/get_average_heartrate/', function (data) {
        // Update the chart data and labels for heart rate
        heartRateData.labels.push(heartRateData.labels.length);
        heartRateData.datasets[0].data.push(data.value);

        // Remove the oldest data point if there are too many points to keep the graph moving
        if (heartRateData.labels.length > 20) {
            heartRateData.labels.shift();
            heartRateData.datasets[0].data.shift();
        }

        // Update the heart rate chart
        heartRateChart.update();

        // Call the function recursively to keep polling the API for heart rate
        setTimeout(fetchHeartRateData, 1000); // Adjust the interval as needed
    });
}

// Start fetching data for both heart rate and shooting accuracy
fetchHeartRateData();
