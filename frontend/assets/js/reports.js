/**
 * Reports controller to instantiate Chart.js configurations and update filters.
 */
document.addEventListener("DOMContentLoaded", () => {
    const api = new MoneyLensAPI();
    if (!api.getToken()) return;

    // Date variables defaults
    const today = new Date();
    const prior30Days = new Date(new Date().setDate(today.getDate() - 30));
    
    const startInput = document.getElementById("reportStartDate");
    const endInput = document.getElementById("reportEndDate");
    const updateBtn = document.getElementById("updateReportBtn");

    startInput.value = prior30Days.toISOString().split('T')[0];
    endInput.value = today.toISOString().split('T')[0];

    // Chart pointers
    let categoryChart = null;
    let comparisonChart = null;
    let trendChart = null;

    async function loadReports() {
        const startDate = startInput.value;
        const endDate = endInput.value;
        
        try {
            // 1. Fetch Category distribution
            const catData = await api.request(`/reports/category-breakdown?start_date=${startDate}&end_date=${endDate}`);
            const catCanvas = document.getElementById("categoryChart");
            const catPlaceholder = document.getElementById("categoryChartPlaceholder");

            if (catData && catData.length > 0) {
                catCanvas.style.display = "block";
                catPlaceholder.style.display = "none";

                const labels = catData.map(c => c.category);
                const values = catData.map(c => c.total);
                const colors = catData.map(c => c.color);

                if (categoryChart) categoryChart.destroy();
                categoryChart = new Chart(catCanvas.getContext('2d'), MoneyLensCharts.buildCategoryConfig(labels, values, colors));
            } else {
                catCanvas.style.display = "none";
                catPlaceholder.style.display = "block";
            }

            // 2. Fetch Income vs Expense totals
            const compData = await api.request(`/reports/income-vs-expense?start_date=${startDate}&end_date=${endDate}`);
            const compCanvas = document.getElementById("comparisonChart");

            if (comparisonChart) comparisonChart.destroy();
            comparisonChart = new Chart(compCanvas.getContext('2d'), MoneyLensCharts.buildComparisonConfig(compData.income, compData.expense));

            // 3. Fetch trends (always fetch past 6 months regardless of date filters)
            const trendData = await api.request("/reports/trends");
            const trendCanvas = document.getElementById("trendChart");

            if (trendData && trendData.length > 0) {
                const months = trendData.map(t => t.month);
                const incomes = trendData.map(t => t.income);
                const expenses = trendData.map(t => t.expense);

                if (trendChart) trendChart.destroy();
                trendChart = new Chart(trendCanvas.getContext('2d'), MoneyLensCharts.buildTrendConfig(months, incomes, expenses));
            }

        } catch (e) {
            console.error("Reports loading error:", e);
        }
    }

    updateBtn.addEventListener("click", loadReports);
    loadReports();
});
