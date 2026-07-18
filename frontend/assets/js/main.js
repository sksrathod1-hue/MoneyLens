/**
 * MoneyLens Main JS.
 * Handles page initialization, template inclusions (sidebar, navbar), and user sessions.
 */
document.addEventListener("DOMContentLoaded", () => {
    const api = new MoneyLensAPI();
    
    // 1. Redirect if not logged in and on an application page
    const publicPages = ["index.html", "login.html", "register.html", ""];
    const currentPage = window.location.pathname.split("/").pop();
    
    const isPublic = publicPages.includes(currentPage);
    const token = api.getToken();
    
    if (!token && !isPublic) {
        window.location.href = "login.html";
        return;
    }
    
    if (token && (currentPage === "login.html" || currentPage === "register.html")) {
        window.location.href = "dashboard.html";
        return;
    }
    
    // 2. Load reusable HTML layout components dynamically
    if (!isPublic && token) {
        loadComponent("sidebar-container", "components/sidebar.html", initSidebarCallbacks);
        loadComponent("navbar-container", "components/navbar.html", initNavbarCallbacks);
        loadComponent("footer-container", "components/footer.html");
    }
});

/**
 * Utility to fetch HTML fragment and render into container.
 */
async function loadComponent(containerId, filepath, callback = null) {
    const container = document.getElementById(containerId);
    if (!container) return;
    
    try {
        const response = await fetch(filepath);
        if (response.ok) {
            const html = await response.text();
            container.innerHTML = html;
            if (callback) callback();
        } else {
            console.error(`Failed to load component: ${filepath}`);
        }
    } catch (e) {
        console.error(`Error loading component ${filepath}:`, e);
    }
}

/**
 * Hook event listeners and highlights on loaded sidebar navigation.
 */
function initSidebarCallbacks() {
    const currentFile = window.location.pathname.split("/").pop() || "dashboard.html";
    
    // Set active link item class
    const menuLinks = document.querySelectorAll(".sidebar-menu a");
    menuLinks.forEach(link => {
        const linkFile = link.getAttribute("href");
        if (linkFile === currentFile) {
            link.classList.add("active");
        } else {
            link.classList.remove("active");
        }
    });
}

/**
 * Hook settings and logs on top navbar.
 */
function initNavbarCallbacks() {
    const api = new MoneyLensAPI();
    const user = api.getCurrentUser();
    
    // Set logged-in username
    const navbarUser = document.getElementById("navbar-username");
    if (navbarUser && user) {
        navbarUser.textContent = user.username;
    }
    
    // Wire up logout button
    const logoutBtn = document.getElementById("logout-btn");
    if (logoutBtn) {
        logoutBtn.addEventListener("click", (e) => {
            e.preventDefault();
            api.clearSession();
            window.location.href = "index.html";
        });
    }
}
