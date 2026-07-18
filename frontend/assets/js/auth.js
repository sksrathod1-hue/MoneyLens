/**
 * Handles login and registration form inputs, posting to auth endpoints.
 */
document.addEventListener("DOMContentLoaded", () => {
    const api = new MoneyLensAPI();
    
    // 1. Handle login form
    const loginForm = document.getElementById("loginForm");
    if (loginForm) {
        const errorDiv = document.getElementById("errorMessage");
        
        loginForm.addEventListener("submit", async (e) => {
            e.preventDefault();
            errorDiv.style.display = "none";
            
            const username = document.getElementById("username").value.trim();
            const password = document.getElementById("password").value;
            
            try {
                const response = await api.request("/auth/login", "POST", { username, password });
                
                // Cache token and user details
                api.setToken(response.access_token);
                api.setCurrentUser(response.user);
                
                // Redirect
                window.location.href = "dashboard.html";
            } catch (error) {
                errorDiv.textContent = error.message || "Failed to log in. Please check credentials.";
                errorDiv.style.display = "block";
            }
        });
    }
    
    // 2. Handle registration form
    const registerForm = document.getElementById("registerForm");
    if (registerForm) {
        const errorDiv = document.getElementById("errorMessage");
        const successDiv = document.getElementById("successMessage");
        
        registerForm.addEventListener("submit", async (e) => {
            e.preventDefault();
            errorDiv.style.display = "none";
            successDiv.style.display = "none";
            
            const username = document.getElementById("username").value.trim();
            const email = document.getElementById("email").value.trim();
            const password = document.getElementById("password").value;
            
            try {
                await api.request("/auth/register", "POST", { username, email, password });
                
                successDiv.textContent = "Registration successful! Redirecting to login page...";
                successDiv.style.display = "block";
                
                // Redirect to login after 1.5 seconds
                setTimeout(() => {
                    window.location.href = "login.html";
                }, 1500);
            } catch (error) {
                errorDiv.textContent = error.message || "Failed to register. Please check input parameters.";
                errorDiv.style.display = "block";
            }
        });
    }
});
