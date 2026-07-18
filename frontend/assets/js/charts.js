/**
 * MoneyLens Chart configurations.
 * Exports builder methods for Chart.js integrations with premium, customized dark themes.
 */
class MoneyLensCharts {
    /**
     * Builds category spending donut chart config.
     */
    static buildCategoryConfig(labels, data, colors) {
        return {
            type: 'doughnut',
            data: {
                labels: labels,
                datasets: [{
                    data: data,
                    backgroundColor: colors,
                    borderWidth: 2,
                    borderColor: '#162032',
                    hoverOffset: 4
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'right',
                        labels: {
                            color: '#9ca3af',
                            font: { family: 'Inter', size: 12 }
                        }
                    },
                    tooltip: {
                        backgroundColor: '#101622',
                        titleColor: '#fff',
                        bodyColor: '#d1d5db',
                        borderColor: '#243048',
                        borderWidth: 1
                    }
                },
                cutout: '65%'
            }
        };
    }

    /**
     * Builds income vs expense side-by-side bar chart config.
     */
    static buildComparisonConfig(income, expense) {
        return {
            type: 'bar',
            data: {
                labels: ['Monthly Aggregate'],
                datasets: [
                    {
                        label: 'Income',
                        data: [income],
                        backgroundColor: '#10b981',
                        borderRadius: 8
                    },
                    {
                        label: 'Expenses',
                        data: [expense],
                        backgroundColor: '#ef4444',
                        borderRadius: 8
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        labels: { color: '#9ca3af' }
                    }
                },
                scales: {
                    y: {
                        grid: { color: '#243048' },
                        ticks: { color: '#9ca3af' }
                    },
                    x: {
                        grid: { display: false },
                        ticks: { color: '#9ca3af' }
                    }
                }
            }
        };
    }

    /**
     * Builds line graph config for monthly income/expense trends.
     */
    static buildTrendConfig(labels, incomeData, expenseData) {
        return {
            type: 'line',
            data: {
                labels: labels,
                datasets: [
                    {
                        label: 'Income',
                        data: incomeData,
                        borderColor: '#10b981',
                        backgroundColor: 'rgba(16, 185, 129, 0.1)',
                        fill: true,
                        tension: 0.4,
                        borderWidth: 3
                    },
                    {
                        label: 'Expenses',
                        data: expenseData,
                        borderColor: '#ef4444',
                        backgroundColor: 'rgba(239, 68, 68, 0.1)',
                        fill: true,
                        tension: 0.4,
                        borderWidth: 3
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        labels: { color: '#9ca3af' }
                    }
                },
                scales: {
                    y: {
                        grid: { color: '#243048' },
                        ticks: { color: '#9ca3af' }
                    },
                    x: {
                        grid: { display: false },
                        ticks: { color: '#9ca3af' }
                    }
                }
            }
        };
    }
}
