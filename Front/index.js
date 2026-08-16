console.log('Front-end script loaded');

const refreshButton = document.getElementById("refreshButton");
const weekStepsChart = document.getElementById('stepsChart').getContext('2d');

let stepsChartInstance;

const savedData = localStorage.getItem('weekStepsData');

if (savedData) {
    updateChart(JSON.parse(savedData));
}

fetchStepsData();

refreshButton.addEventListener("click", () => {
    fetchStepsData();
});

function fetchStepsData() {
    fetch('http://127.0.0.1:8000/steps/week')
        .then(response => response.json())
        .then(data => {
            localStorage.setItem('weekStepsData', JSON.stringify(data));
            updateChart(data);
        })
        .catch(error => console.error('Error fetching steps data:', error));
}
function updateChart(newData) { // Update the chart with new data
    if (stepsChartInstance) {
        stepsChartInstance.data.labels = Object.keys(newData);
        stepsChartInstance.data.datasets[0].data = Object.values(newData).map(day => day.steps);
        stepsChartInstance.update();
    } else {
        stepsChartInstance = new Chart(weekStepsChart, {
            type: 'bar',
            data: {
                labels: Object.keys(newData),
                datasets: [{
                    label: 'Steps',
                    data: Object.values(newData).map(day => day.steps),
                    backgroundColor: 'rgba(75, 192, 192, 0.2)',
                    borderColor: 'rgba(75, 192, 192, 1)',
                    borderWidth: 1
                }]
            },
            options: {
                animation: {
                    duration: 1000, // Animation duration in milliseconds
                    easing: 'easeInOutQuad' // Easing function for the animation
                },
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });
    }
}

