
/*  
    Contains all Chart JS functions for 
    the Rounds Stats page.
    
*/


Chart.defaults.font.size = 14;
Chart.defaults.font.family = "'Dotum', sans-serif";
Chart.defaults.color = 'white';



// Puzzles Logged


function logs_chart(
    categories, players, colors, chart_data) {

    var ctx = document.getElementById('logsChart').getContext('2d');

    var chart_object = new Chart(ctx, {
        type: 'bar',
        
        data: {
            labels: [],            
            datasets: [{}],},

        options: {
            responsive: true,
            borderWidth: 3,
            barShowStroke : false,
            barPercentage: 0.8,
            categoryPercentage: 0.8,
            interaction: {intersect: false,},
            skipNull: true,
            
            scales: {
                y: {
                    beginAtZero: true,
                    border: {color: 'white',},
                    title: {
                        display: true,
                        text: 'Number of finished puzzles (logs)',},
                    ticks: {color: 'white',},},
                x: {
                    beginAtZero: true,
                    border: {color: 'white',},
                    title: {
                        display: true,
                        text: 'Pieces per puzzle',},
                    ticks: {color: 'white',},},
            },

            plugins: {
                legend: { display: false,},

                tooltip: {
                    backgroundColor: '#5f5f5f',
                    displayColors: true,
                    callbacks: {
                        label: function(context) {
                            return context.dataset.label + ': ' + context.parsed.x;},},},
                        
                title: {
                    display: true,
                    text: 'Puzzles finished per player and number of pieces:',},},
    },},);
    

    var n = players.length;
    chart_object.data.labels = categories;
    

    for (var i = 0; i < n; i++) {
        
        chart_object.data.datasets[i].label = players[i];
        chart_object.data.datasets[i].data = chart_data[i];
        chart_object.data.datasets[i].backgroundColor = colors[i][0];
        chart_object.data.datasets[i].borderColor = colors[i][0];
        
        if (i < n - 1) {
            chart_object.data.datasets.push({});}
    }

    chart_object.update();
}






// Speed by Player


function player_speed_chart(
    categories, players, colors, chart_data) {

    var ctx = document.getElementById('playerSpeedChart').getContext('2d');

    var chart_object = new Chart(ctx, {
        type: 'bar',
        
        data: {
            labels: categories,            
            datasets: [{}],},
                

        options: {
            responsive: true,
            borderWidth: 3,
            barShowStroke : false,
            barPercentage: 1.6,
            categoryPercentage: 0.7,
            interaction: {intersect: false,},
            skipNull: true,
            
            scales: {
                y: {
                    stacked: false,
                    beginAtZero: true,
                    border: {color: 'white',},
                    
                    title: {
                        display: true,
                        text: 'Pieces per Minute',},
                    ticks: {color: 'white',},},
                x: {
                    stacked: false,
                    beginAtZero: true,
                    border: {color: 'white',},
                    title: {
                        display: true,
                        text: 'Pieces per puzzle',},
                    ticks: {color: 'white',},},},

            plugins: {
                legend: { display: false,},

                tooltip: {
                    backgroundColor: '#5f5f5f',
                    displayColors: true,},
                        
                title: {
                    display: true,
                    text: 'Player speed - in average & fastest:',},},
    },},);
    

    var n_players = players.length;
    var stacks = ['avg', 'fastest'];
    var n_stacks = stacks.length;
    var n_sets = n_players * n_stacks;

    for (var p = 0; p < n_players; p++) {
        for (var s = 0; s < n_stacks; s++) {

            stack = stacks[s];
            set_id = p * n_stacks + s;
            
            chart_object.data.datasets[set_id].label = players[p] + ' ' + stacks[s];
            chart_object.data.datasets[set_id].stack = 'stack_' + players[p];
            chart_object.data.datasets[set_id].data = chart_data[p][s];
            chart_object.data.datasets[set_id].backgroundColor = colors[p][s];
            chart_object.data.datasets[set_id].borderColor = colors[p][0];

            if (set_id < n_sets - 1) {
                chart_object.data.datasets.push({});}}
    }

    chart_object.update();
}





// Speed by Puzzle

function puzzle_speed_chart(
    categories, puzzles, colors, chart_data) {

    var ctx = document.getElementById('puzzleSpeedChart').getContext('2d');

    var chart_object = new Chart(ctx, {
        type: 'bar',
        
        data: {
            labels: categories,            
            datasets: [{}],},
                

        options: {
            responsive: true,
            borderWidth: 3,
            barPercentage: 1.6,
            categoryPercentage: 0.7,
            
            scales: {
                y: {
                    stacked: false,
                    beginAtZero: true,
                    border: {color: 'white',},
                    
                    title: {
                        display: true,
                        text: 'Pieces per Minute',},
                    ticks: {color: 'white',},},
                x: {
                    stacked: false,
                    beginAtZero: true,
                    border: {color: 'white',},
                    title: {
                        display: true,
                        text: 'Pieces per puzzle',},
                    ticks: {color: 'white',},},},

            plugins: {
                
                legend: { display: false,},

                tooltip: {
                    backgroundColor: '#5f5f5f',
                    displayColors: true,},
                        
                title: {
                    display: true,
                    text: 'Puzzle speed - on average & fastest:',},},
    },},);
    

    var n_puzzles = puzzles.length;
    var stacks = ['avg', 'fastest'];
    var n_stacks = stacks.length;
    var n_sets = n_puzzles * n_stacks;

    for (var p = 0; p < n_puzzles; p++) {
        for (var s = 0; s < n_stacks; s++) {

            stack = stacks[s];
            set_id = p * n_stacks + s;
            
            if (chart_data[p][s] == null) {
                continue;}
            chart_object.data.datasets[set_id].label = puzzles[p] + ' ' + stacks[s];
            chart_object.data.datasets[set_id].stack = 'stack_' + puzzles[p];
            chart_object.data.datasets[set_id].data = chart_data[p][s];
            chart_object.data.datasets[set_id].backgroundColor = colors[p][s];
            chart_object.data.datasets[set_id].borderColor = colors[p][0];

            if (set_id < n_sets - 1) {
                chart_object.data.datasets.push({});}}
    }

    chart_object.update();
}
