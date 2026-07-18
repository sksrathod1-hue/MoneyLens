/**
 * Budgets allocation page controller.
 */
document.addEventListener("DOMContentLoaded", () => {
    const api = new MoneyLensAPI();
    if (!api.getToken()) return;

    // Elements
    const budgetsGrid = document.getElementById("budgetsGrid");
    const budgetForm = document.getElementById("budgetForm");
    const budgetCategory = document.getElementById("budgetCategory");
    
    const startInput = document.getElementById("budgetStartDate");
    const endInput = document.getElementById("budgetEndDate");
    const formError = document.getElementById("budgetFormError");

    // Set default dates (start: first day of month, end: last day of month)
    const today = new Date();
    const firstDay = new Date(today.getFullYear(), today.getMonth(), 1);
    const lastDay = new Date(today.getFullYear(), today.getMonth() + 1, 0);
    
    startInput.value = firstDay.toISOString().split('T')[0];
    endInput.value = lastDay.toISOString().split('T')[0];

    // 1. Load categories for selector
    async function loadCategories() {
        try {
            const categories = await api.request("/settings/categories");
            budgetCategory.innerHTML = '<option value="">Select Category</option>';
            
            categories.forEach(cat => {
                if (cat.type === "expense") {
                    const opt = document.createElement("option");
                    opt.value = cat.id;
                    opt.textContent = cat.name;
                    budgetCategory.appendChild(opt);
                }
            });
        } catch (e) {
            console.error("Failed to load categories for budget:", e);
        }
    }

    // 2. Fetch and list budgets
    async function loadBudgets() {
        budgetsGrid.innerHTML = '<div class="card text-center text-muted p-40">Loading budgets...</div>';
        
        try {
            const budgets = await api.request("/budgets");
            budgetsGrid.innerHTML = "";
            
            if (budgets && budgets.length > 0) {
                budgets.forEach(budget => {
                    const spent = budget.spent;
                    const limit = budget.amount;
                    const remaining = limit - spent;
                    const pct = Math.min((spent / limit) * 100, 100);
                    
                    let barClass = "";
                    if (pct >= 100) {
                        barClass = "danger";
                    } else if (pct >= 80) {
                        barClass = "warning";
                    }
                    
                    const card = document.createElement("div");
                    card.className = "budget-card-item";
                    card.innerHTML = `
                        <div class="budget-card-header">
                            <div class="budget-card-title">
                                <span class="budget-card-color-dot" style="background-color: ${budget.category_color}"></span>
                                ${budget.category_name}
                            </div>
                            <button class="budget-delete-btn" data-id="${budget.id}">🗑️</button>
                        </div>
                        <div class="budget-amount-row">
                            ₹${spent.toFixed(2)} <span>/ ₹${limit.toFixed(2)} limit</span>
                        </div>
                        
                        <div class="budget-progress-container">
                            <div class="budget-progress-bar-outer">
                                <div class="budget-progress-bar-inner ${barClass}" style="width: ${pct}%;"></div>
                            </div>
                            <div class="budget-limits-row">
                                <span>${pct.toFixed(0)}% spent</span>
                                <span style="color: ${remaining < 0 ? 'var(--danger)' : 'var(--success)'}">
                                    ${remaining < 0 ? 'Exceeded by' : 'Remaining:'} ₹${Math.abs(remaining).toFixed(2)}
                                </span>
                            </div>
                        </div>
                        
                        <div class="budget-date-range">
                            Period: ${budget.start_date} to ${budget.end_date}
                        </div>
                    `;
                    budgetsGrid.appendChild(card);
                });
                
                // Wire delete actions
                document.querySelectorAll(".budget-delete-btn").forEach(btn => {
                    btn.addEventListener("click", async (e) => {
                        const bId = e.currentTarget.getAttribute("data-id");
                        if (confirm("Remove this budget constraint?")) {
                            try {
                                await api.request(`/budgets/${bId}`, "DELETE");
                                loadBudgets();
                            } catch (err) {
                                alert(err.message);
                            }
                        }
                    });
                });
            } else {
                budgetsGrid.innerHTML = `
                    <div class="card text-center text-muted p-40" style="grid-column: 1 / -1;">
                        No budgets are defined. Set a category target in the form to begin tracking limits.
                    </div>
                `;
            }
        } catch (e) {
            budgetsGrid.innerHTML = '<div class="card text-center text-danger p-40" style="grid-column: 1 / -1;">Error loading budgets.</div>';
        }
    }

    // 3. Form Submit handler
    budgetForm.addEventListener("submit", async (e) => {
        e.preventDefault();
        formError.style.display = "none";
        
        const category_id = parseInt(budgetCategory.value);
        const amount = parseFloat(document.getElementById("budgetAmount").value);
        const period = document.getElementById("budgetPeriod").value;
        const start_date = startInput.value;
        const end_date = endInput.value;
        
        try {
            await api.request("/budgets", "POST", {
                category_id, amount, period, start_date, end_date
            });
            
            // Reload and reset form
            loadBudgets();
            budgetForm.reset();
            
            // Reapply defaults
            startInput.value = firstDay.toISOString().split('T')[0];
            endInput.value = lastDay.toISOString().split('T')[0];
        } catch (err) {
            formError.textContent = err.message || "Failed to create budget.";
            formError.style.display = "block";
        }
    });

    loadCategories();
    loadBudgets();
});
