
/*  
    Contains all Chart JS functions for 
    the Rounds Game page.
    
*/


Chart.defaults.font.size = 14;
Chart.defaults.font.family = "'Dotum', sans-serif";
Chart.defaults.color = 'white';





// ROUNDS historic play chart

function updateRoundsChart(
    rounds, players, colors, chart_data) {

    var ctx = document.getElementById('rounds_chart').getContext('2d');

    var rounds_chart = new Chart(ctx, {
        type: 'line',
        
        data: {
            labels: [],             // x-axis
            datasets: [{}],},

        options: {
            responsive: true,
            
            scales: {
                y: {
                    beginAtZero: true,
                    border:{ dash: [2, 8],},
                    grid: { color: '#d2d2d2c7',},},},

            plugins: {
                legend: {
                    display: true,
                    position: 'top',},

                tooltip: {
                    backgroundColor: '#5f5f5f',
                    displayColors: true,
                    callbacks: {
                        label: function(context) {
                            return context.dataset.label + ': ' + context.parsed.y;},},},
                        
                title: {
                    display: true,
                    text: 'Total Points by Round',},},

            elements: {
                point: {
                    radius: 5,},
                line: {
                    tension: 0.3,
                    borderWidth: 3,},}
        },},);

    
    var n = players.length;
    rounds_chart.data.labels = rounds;

    for (var i = 0; i < n; i++) {
        rounds_chart.data.datasets[i].label = players[i];
        rounds_chart.data.datasets[i].data = chart_data[i];
        rounds_chart.data.datasets[i].backgroundColor = colors[i];
        rounds_chart.data.datasets[i].borderColor = colors[i];

        if (i < n - 1) {
            rounds_chart.data.datasets.push({});}
    }

    rounds_chart.update();
}


// DICE historic play chart

function updateDiceChart(
    rounds, players, colors, chart_data) {

    var ctx = document.getElementById('dice_chart').getContext('2d');

    var dice_chart = new Chart(ctx, {
        type: 'line',
        
        data: {
            labels: [],             // x-axis
            datasets: [{}],},

        options: {
            responsive: true,
            
            scales: {
                y: {
                    beginAtZero: true,
                    border:{ dash: [2, 8],},
                    grid: { color: '#d2d2d2c7',},},},

            plugins: {
                legend: {
                    display: true,
                    position: 'top',},

                tooltip: {
                    backgroundColor: '#5f5f5f',
                    displayColors: true,
                    callbacks: {
                        label: function(context) {
                            return context.dataset.label + ': ' + context.parsed.y;},},},
                        
                title: {
                    display: true,
                    text: 'Total Points by Round',},

                annotation: {
                    annotations: [{
                        type: 'line',
                        mode: 'vertical',
                        scaleID: 'x',
                        value: 12,
                        borderColor: 'yellow',
                        borderWidth: 2,
                        label: {
                            enabled: true,
                            content: 'Vertical Line'}
                    }]}
                },

            elements: {
                point: {
                    radius: 5,},
                line: {
                    tension: 0.3,
                    borderWidth: 3,},}
        },},);

    
    var n = players.length;
    dice_chart.data.labels = rounds;

    for (var i = 0; i < n; i++) {
        dice_chart.data.datasets[i].label = players[i];
        dice_chart.data.datasets[i].data = chart_data[i];
        dice_chart.data.datasets[i].backgroundColor = colors[i];
        dice_chart.data.datasets[i].borderColor = colors[i];

        if (i < n - 1) {
            dice_chart.data.datasets.push({});}
    }

    dice_chart.update();
}