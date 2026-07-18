// MoneyLens 3D Mouse Tracking Head Rotation Script
(() => {
  document.addEventListener("DOMContentLoaded", () => {
    const heroImage = document.querySelector(".alpaca-hero-img");
    if (!heroImage) return;

    // Apply baseline CSS transitions directly for organic easing
    heroImage.style.transition = "transform 0.15s cubic-bezier(0.25, 1, 0.5, 1)";
    heroImage.style.transformStyle = "preserve-3d";

    let lastMouseX = window.innerWidth / 2;
    let lastMouseY = window.innerHeight / 2;
    let requestPending = false;

    function updateRotation() {
      const cx = window.innerWidth / 2;
      const cy = window.innerHeight / 2;

      const dx = lastMouseX - cx;
      const dy = lastMouseY - cy;

      // Map deltas to subtle tilt degrees
      // Max Y tilt: 15deg (looks left/right)
      // Max X tilt: -10deg (looks up/down)
      const rotateY = (dx / cx) * 18;
      const rotateX = (dy / cy) * -12;

      // Apply 3D perspective transform
      heroImage.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) scale(1.12)`;
      
      requestPending = false;
    }

    // Mouse move event tracker
    window.addEventListener("mousemove", (e) => {
      lastMouseX = e.clientX;
      lastMouseY = e.clientY;

      if (!requestPending) {
        requestAnimationFrame(updateRotation);
        requestPending = true;
      }
    });

    // Reset to center when mouse leaves window bounds
    document.addEventListener("mouseleave", () => {
      heroImage.style.transform = "perspective(1000px) rotateX(0deg) rotateY(0deg) scale(1.12)";
    });
  });
})();
