/**
 * Transaction controller for listing, creation, uploads and deletions.
 */
document.addEventListener("DOMContentLoaded", () => {
    const api = new MoneyLensAPI();
    if (!api.getToken()) return;
    
    // Page Elements
    const openAddTxBtn = document.getElementById("openAddTxBtn");
    const closePanelBtn = document.getElementById("closePanelBtn");
    const addTxPanel = document.getElementById("addTxPanel");
    
    const filterType = document.getElementById("filterType");
    const filterCategory = document.getElementById("filterCategory");
    const transactionsTbody = document.getElementById("transactions-tbody");
    
    const txForm = document.getElementById("txForm");
    const txCategorySelect = document.getElementById("tx-category");
    const txDateInput = document.getElementById("tx-date");
    const txReceiptInput = document.getElementById("tx-receipt");
    const receiptUploadStatus = document.getElementById("receipt-upload-status");
    const receiptPathInput = document.getElementById("receipt-path");
    
    // Set default date to today
    txDateInput.value = new Date().toISOString().split('T')[0];
    
    // Toggle Slide Panel
    openAddTxBtn.addEventListener("click", () => {
        document.getElementById("panelTitle").textContent = "Log Transaction";
        txForm.reset();
        txDateInput.value = new Date().toISOString().split('T')[0];
        document.getElementById("tx-id").value = "";
        receiptUploadStatus.textContent = "";
        receiptPathInput.value = "";
        addTxPanel.classList.add("active");
    });
    
    closePanelBtn.addEventListener("click", () => {
        addTxPanel.classList.remove("active");
    });
    
    // 1. Fetch Categories for Filters and Forms
    async function loadCategories() {
        try {
            const categories = await api.request("/settings/categories");
            
            // Populating selectors
            filterCategory.innerHTML = '<option value="">All Categories</option>';
            txCategorySelect.innerHTML = '<option value="">Select Category</option>';
            
            categories.forEach(cat => {
                const opt = document.createElement("option");
                opt.value = cat.id;
                opt.textContent = `${cat.name} (${cat.type})`;
                
                // Clone option for form select
                const formOpt = opt.cloneNode(true);
                
                filterCategory.appendChild(opt);
                txCategorySelect.appendChild(formOpt);
            });
        } catch (e) {
            console.error("Failed to load categories:", e);
        }
    }
    
    // 2. Fetch and List Transactions
    async function loadTransactions() {
        transactionsTbody.innerHTML = '<tr><td colspan="6" class="text-center text-muted">Loading transactions...</td></tr>';
        
        let queryParams = [];
        if (filterType.value) queryParams.push(`type=${filterType.value}`);
        if (filterCategory.value) queryParams.push(`category_id=${filterCategory.value}`);
        
        const queryString = queryParams.length > 0 ? `?${queryParams.join("&")}` : "";
        
        try {
            const txs = await api.request(`/transactions${queryString}`);
            transactionsTbody.innerHTML = "";
            
            if (txs && txs.length > 0) {
                txs.forEach(tx => {
                    const isIncome = tx.type === "income";
                    const amtSign = isIncome ? "+" : "-";
                    const row = document.createElement("tr");
                    
                    // Receipt visual
                    const receiptIcon = tx.receipt_image_path 
                        ? `<a href="http://localhost:5000/${tx.receipt_image_path}" target="_blank" class="receipt-link" title="View receipt">📄</a>`
                        : '<span class="text-muted">-</span>';
                        
                    row.innerHTML = `
                        <td>${tx.date}</td>
                        <td>${tx.description || tx.category_name}</td>
                        <td>
                            <span class="badge-cat" style="background-color: ${tx.category_color}">
                                ${tx.category_name}
                            </span>
                        </td>
                        <td>
                            ${tx.sms_sender ? `<span class="sms-source">SMS: ${tx.sms_sender}</span>` : '<span class="text-muted">Manual</span>'}
                        </td>
                        <td class="tx-amount ${tx.type}">${amtSign}₹${tx.amount.toFixed(2)}</td>
                        <td>
                            <div class="action-btn-row">
                                ${receiptIcon}
                                <button class="delete-btn" data-id="${tx.id}">🗑️</button>
                            </div>
                        </td>
                    `;
                    transactionsTbody.appendChild(row);
                });
                
                // Wire up delete events
                document.querySelectorAll(".delete-btn").forEach(btn => {
                    btn.addEventListener("click", async (e) => {
                        const txId = e.currentTarget.getAttribute("data-id");
                        if (confirm("Are you sure you want to delete this transaction?")) {
                            try {
                                await api.request(`/transactions/${txId}`, "DELETE");
                                loadTransactions();
                            } catch (err) {
                                alert("Failed to delete transaction: " + err.message);
                            }
                        }
                    });
                });
            } else {
                transactionsTbody.innerHTML = '<tr><td colspan="6" class="text-center text-muted">No transactions found matching filter parameters.</td></tr>';
            }
        } catch (e) {
            transactionsTbody.innerHTML = '<tr><td colspan="6" class="text-center text-danger">Error loading transactions.</td></tr>';
        }
    }
    
    // 3. Receipt Upload Action
    txReceiptInput.addEventListener("change", async (e) => {
        const file = e.target.files[0];
        if (!file) return;
        
        receiptUploadStatus.className = "upload-status";
        receiptUploadStatus.textContent = "Uploading receipt file...";
        
        const formData = new FormData();
        formData.append("receipt", file);
        
        try {
            const resp = await api.request("/transactions/upload-receipt", "POST", formData, true);
            receiptUploadStatus.textContent = "Receipt uploaded successfully.";
            receiptUploadStatus.classList.add("success");
            receiptPathInput.value = resp.path;
        } catch (err) {
            receiptUploadStatus.textContent = err.message || "File upload failed.";
            receiptUploadStatus.classList.add("error");
        }
    });
    
    // 4. Form Submit
    txForm.addEventListener("submit", async (e) => {
        e.preventDefault();
        
        const type = document.querySelector('input[name="tx_type"]:checked').value;
        const amount = parseFloat(document.getElementById("tx-amount").value);
        const category_id = parseInt(document.getElementById("tx-category").value);
        const date = document.getElementById("tx-date").value;
        const description = document.getElementById("tx-desc").value.trim();
        const receipt_image_path = receiptPathInput.value;
        
        try {
            await api.request("/transactions", "POST", {
                type, amount, category_id, date, description, receipt_image_path
            });
            
            // Reload and collapse panel
            loadTransactions();
            addTxPanel.classList.remove("active");
            txForm.reset();
            receiptUploadStatus.textContent = "";
            receiptPathInput.value = "";
        } catch (err) {
            alert(err.message || "Failed to save transaction.");
        }
    });
    
    // Event listeners for filters
    filterType.addEventListener("change", loadTransactions);
    filterCategory.addEventListener("change", loadTransactions);
    
    // Initial loads
    loadCategories();
    loadTransactions();
    
    // Check if query string includes "add=true" to open panel instantly
    const urlParams = new URLSearchParams(window.location.search);
    if (urlParams.get("add") === "true") {
        setTimeout(() => openAddTxBtn.click(), 200);
    }
});
