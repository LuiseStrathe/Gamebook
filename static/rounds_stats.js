
/*  
    Contains all Chart JS functions for 
    the Rounds Stats page.
    
*/


Chart.defaults.font.size = 14;
Chart.defaults.font.family = "'Dotum', sans-serif";
Chart.defaults.color = 'white';





// WINNER BOARD

var ctx_w = document.getElementById('winnerBoard').getContext('2d');

var winner_board = new Chart(ctx_w, {
    type: 'bar',
    
    data: {
        labels: [],             // x-axis
        datasets: [{}, {}, {}, {}, {}, {}, {}, {}, {}, {}],
    },

    options: {
        responsive: true,
        indexAxis: 'y',
        borderWidth: 3,
        
        scales: {
            y: {
                stacked: true,
                beginAtZero: true,},
            x: {
                stacked: true,
                beginAtZero: true,
                ticks: {precision:0,}},
        },



        plugins: {
            legend: {
                display: true,
                position: 'top',},

            tooltip: {
                backgroundColor: '#5f5f5f',
                displayColors: true,
                callbacks: {
                    label: function(context) {
                        return context.dataset.label + ': ' + context.parsed.x;},},},
                    
            title: {
                display: true,
                text: 'Rounds games played & games won:',},},
    },},);
                


function updateWinners(players, colors, chart_data) {
    
    var n = 2;
    winner_board.data.labels = players;

    for (var i = 0; i < n; i++) {
        winner_board.data.datasets[i].label = ['won', 'not won'][i];
        winner_board.data.datasets[i].data = chart_data[i];
        winner_board.data.datasets[i].backgroundColor = colors[i];
        winner_board.data.datasets[i].borderColor = colors[0];
    }
    
    winner_board.data.datasets.splice(n, 10-n);

    winner_board.update();
}




