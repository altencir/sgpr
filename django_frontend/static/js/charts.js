function createStateChart(data) {
    const ctx = document.getElementById('stateChart').getContext('2d');
    
    new Chart(ctx, {
        type: 'pie',
        data: {
            labels: data.map(item => item.state),
            datasets: [{
                data: data.map(item => item.count),
                backgroundColor: [
                    '#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF',
                    '#FF9F40', '#FF6384', '#C9CBCF', '#4BC0C0', '#FF6384'
                ]
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'bottom'
                }
            }
        }
    });
}

function createCultureChart(data) {
    const ctx = document.getElementById('cultureChart').getContext('2d');
    
    new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: data.map(item => item.name),
            datasets: [{
                data: data.map(item => item.count),
                backgroundColor: [
                    '#28a745', '#ffc107', '#dc3545', '#007bff', '#6f42c1',
                    '#fd7e14', '#20c997', '#6c757d', '#e83e8c', '#17a2b8'
                ]
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'bottom'
                }
            }
        }
    });
}

function createLandUseChart(data) {
    const ctx = document.getElementById('landUseChart').getContext('2d');
    
    new Chart(ctx, {
        type: 'pie',
        data: {
            labels: data.map(item => item.name),
            datasets: [{
                data: data.map(item => item.value),
                backgroundColor: ['#28a745', '#198754']
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'bottom'
                }
            }
        }
    });
}