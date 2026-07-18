/**
 * MoneyLens client API Service class.
 * Handles fetching, request headers, error interceptions, and auth session tokens.
 */
class MoneyLensAPI {
    constructor() {
        this.baseUrl = "http://localhost:5000/api";
    }

    /**
     * Get saved JWT access token from localStorage.
     */
    getToken() {
        return localStorage.getItem("moneylens_token");
    }

    /**
     * Saves JWT access token to localStorage.
     */
    setToken(token) {
        localStorage.setItem("moneylens_token", token);
    }

    /**
     * Clear auth tokens and user profile session.
     */
    clearSession() {
        localStorage.removeItem("moneylens_token");
        localStorage.removeItem("moneylens_user");
    }

    /**
     * Get cached user profile info.
     */
    getCurrentUser() {
        const user = localStorage.getItem("moneylens_user");
        return user ? JSON.parse(user) : null;
    }

    /**
     * Saves user profile metadata to localStorage.
     */
    setCurrentUser(user) {
        localStorage.setItem("moneylens_user", JSON.stringify(user));
    }

    /**
     * General fetch utility with authentication headers.
     * 
     * @param {string} endpoint - API path (e.g. '/transactions')
     * @param {string} method - HTTP method
     * @param {object} body - Payload object (for POST, PUT)
     * @param {boolean} isMultipart - True if uploading files
     */
    async request(endpoint, method = "GET", body = null, isMultipart = false) {
        const url = `${this.baseUrl}${endpoint}`;
        
        const headers = {};
        const token = this.getToken();
        if (token) {
            headers["Authorization"] = `Bearer ${token}`;
        }

        let options = { method, headers };

        if (body) {
            if (isMultipart) {
                // Let browser set the proper boundary headers automatically
                options.body = body;
            } else {
                headers["Content-Type"] = "application/json";
                options.body = JSON.stringify(body);
            }
        }

        try {
            const response = await fetch(url, options);
            const data = await response.json();

            if (!response.ok) {
                if (response.status === 401 && endpoint !== "/auth/login") {
                    this.clearSession();
                    window.location.href = "login.html";
                }
                const error = new Error(data.message || "Something went wrong");
                error.status = response.status;
                error.response = data;
                throw error;
            }

            return data;
        } catch (error) {
            console.error(`API Request error on ${endpoint}:`, error);
            throw error;
        }
    }
}
