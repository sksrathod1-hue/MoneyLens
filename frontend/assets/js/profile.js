/**
 * Profile detail page controller.
 */
document.addEventListener("DOMContentLoaded", () => {
    const api = new MoneyLensAPI();
    if (!api.getToken()) return;

    // Elements
    const usernameText = document.getElementById("profileUsername");
    const emailText = document.getElementById("profileEmailText");
    const txCountText = document.getElementById("profileTxCount");
    const budgetCountText = document.getElementById("profileBudgetCount");
    
    const profileForm = document.getElementById("profileForm");
    const emailInput = document.getElementById("updateEmail");
    
    const profileError = document.getElementById("profileError");
    const profileSuccess = document.getElementById("profileSuccess");

    async function loadProfile() {
        try {
            const data = await api.request("/profile");
            
            // Set displays
            usernameText.textContent = data.username;
            emailText.textContent = data.email;
            txCountText.textContent = data.stats.total_transactions;
            budgetCountText.textContent = data.stats.total_budgets;
            
            // Set input default
            emailInput.value = data.email;
            
            // Update session cache
            api.setCurrentUser(data);
        } catch (e) {
            console.error("Failed to load profile details:", e);
        }
    }

    profileForm.addEventListener("submit", async (e) => {
        e.preventDefault();
        profileError.style.display = "none";
        profileSuccess.style.display = "none";
        
        const email = emailInput.value.trim();
        
        try {
            const resp = await api.request("/profile", "PUT", { email });
            profileSuccess.textContent = "Profile updated successfully!";
            profileSuccess.style.display = "block";
            
            // Reload updated values
            loadProfile();
        } catch (err) {
            profileError.textContent = err.message || "Failed to update profile email.";
            profileError.style.display = "block";
        }
    });

    loadProfile();
});
