/**
 * Dashboard page analytics fetcher.
 */
document.addEventListener("DOMContentLoaded", () => {
    const api = new MoneyLensAPI();
    
    // Safety check - wait for token
    if (!api.getToken()) return;
    
    const user = api.getCurrentUser();
    if (user) {
        const usernameDisplay = document.getElementById("username-display");
        if (usernameDisplay) usernameDisplay.textContent = user.username;
    }
    
    // Set absolute URL of local webhook endpoint
    const urlDisplay = document.getElementById("webhook-url-display");
    if (urlDisplay) {
        urlDisplay.textContent = `${window.location.protocol}//${window.location.host}/api/sms/webhook`;
    }
    
    const incomeVal = document.getElementById("income-val");
    const expenseVal = document.getElementById("expense-val");
    const savingsVal = document.getElementById("savings-val");
    
    const recentTxList = document.getElementById("recent-transactions-list");
    const budgetProgressList = document.getElementById("budgets-progress-list");
    
    const insightTitle = document.getElementById("insight-title");
    const insightText = document.getElementById("insight-text");
    const insightTag = document.getElementById("insight-tag");
    
    async function loadDashboardSummary() {
        try {
            const data = await api.request("/dashboard/summary");
            
            // 1. Render Metrics
            incomeVal.textContent = `₹${data.metrics.monthly_income.toFixed(2)}`;
            expenseVal.textContent = `₹${data.metrics.monthly_expense.toFixed(2)}`;
            savingsVal.textContent = `₹${data.metrics.net_savings.toFixed(2)}`;
            
            if (data.metrics.net_savings < 0) {
                savingsVal.style.color = "var(--danger)";
            } else {
                savingsVal.style.color = "var(--success)";
            }
            
            // 2. Render Recent Transactions List
            recentTxList.innerHTML = "";
            if (data.recent_transactions && data.recent_transactions.length > 0) {
                data.recent_transactions.forEach(tx => {
                    // Map category icons
                    const iconMap = {
                        "briefcase": "💼", "laptop": "💻", "trending-up": "📈",
                        "coffee": "☕", "home": "🏠", "bolt": "⚡",
                        "car": "🚗", "film": "🎬", "shopping-cart": "🛒",
                        "shopping-bag": "🛍️", "heartbeat": "❤️", "tag": "🏷️"
                    };
                    const visualIcon = iconMap[tx.category_icon] || "🏷️";
                    const isIncome = tx.type === "income";
                    const sign = isIncome ? "+" : "-";
                    
                    const item = document.createElement("div");
                    item.className = "tx-mini-item";
                    item.innerHTML = `
                        <div class="tx-left-block">
                            <div class="tx-icon-bullet" style="background-color: ${tx.category_color};">${visualIcon}</div>
                            <div class="tx-info">
                                <span class="tx-desc">${tx.description || tx.category_name}</span>
                                <span class="tx-meta">${tx.date} ${tx.sms_sender ? '• via SMS' : ''}</span>
                            </div>
                        </div>
                        <span class="tx-amount-val ${tx.type}">${sign}₹${tx.amount.toFixed(2)}</span>
                    `;
                    recentTxList.appendChild(item);
                });
            } else {
                recentTxList.innerHTML = `<p class="text-center text-muted p-20">No recent transactions. Add one to start!</p>`;
            }
            
            // 3. Render Active Budgets progress
            budgetProgressList.innerHTML = "";
            if (data.budgets && data.budgets.length > 0) {
                data.budgets.forEach(budget => {
                    const spent = budget.spent;
                    const limit = budget.amount;
                    const pct = Math.min((spent / limit) * 100, 100);
                    
                    let warningClass = "";
                    if (pct >= 100) {
                        warningClass = "danger";
                    } else if (pct >= 80) {
                        warningClass = "warning";
                    }
                    
                    const item = document.createElement("div");
                    item.className = "budget-mini-item";
                    item.innerHTML = `
                        <div class="budget-meta-row">
                            <span>${budget.category_name}</span>
                            <span>₹${spent.toFixed(2)} / ₹${limit.toFixed(2)} (${pct.toFixed(0)}%)</span>
                        </div>
                        <div class="budget-bar-outer">
                            <div class="budget-bar-inner ${warningClass}" style="width: ${pct}%;"></div>
                        </div>
                    `;
                    budgetProgressList.appendChild(item);
                });
            } else {
                budgetProgressList.innerHTML = `<p class="text-center text-muted p-20">No active budgets. Set targets to limit spending.</p>`;
            }
            
            // 4. Render top AI Insight
            if (data.top_insight) {
                insightTitle.textContent = data.top_insight.title;
                insightText.textContent = data.top_insight.insight;
                insightTag.textContent = data.top_insight.category;
            }
            
        } catch (error) {
            console.error("Dashboard load failed:", error);
        }
    }
    
    loadDashboardSummary();
});
