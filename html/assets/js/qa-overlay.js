/* =========================================================================
   SCENTS BY SARA - QA OVERLAY SCRIPT
   Injects the design screenshot as a 50% opacity fixed layer for precise visual auditing.
   ========================================================================= */

(function initQAOverlay() {
    // Determine which image to load based on current page path
    const path = window.location.pathname;
    let screenshotName = '';

    if (path.includes('index.html') || path.endsWith('/v2/')) {
        screenshotName = 'home-page.png';
    } else if (path.includes('shop.html')) {
        screenshotName = 'shop-page.png';
    } else if (path.includes('product.html')) {
        screenshotName = 'product-page.png';
    } else if (path.includes('checkout.html')) {
        screenshotName = 'checkout-page.png';
    } else if (path.includes('your-story.html')) {
        screenshotName = 'your-story.jpeg';
    }

    if (!screenshotName) return;

    // Create container
    const overlay = document.createElement('div');
    overlay.id = 'qa-overlay-container';
    Object.assign(overlay.style, {
        position: 'absolute',
        top: '0',
        left: '50%',
        transform: 'translateX(-50%)',
        width: '100%',
        maxWidth: '1920px', // Assuming max screen capture width
        pointerEvents: 'none',
        zIndex: '9999',
        opacity: '0.4',
        display: 'none' // Default hidden
    });

    const img = document.createElement('img');
    img.src = `screenshots/${screenshotName}`;
    Object.assign(img.style, {
        width: '100%',
        display: 'block'
    });

    overlay.appendChild(img);
    document.body.appendChild(overlay);

    // Create Toggle Button
    const btn = document.createElement('button');
    btn.innerHTML = 'Toggle QA Overlay';
    Object.assign(btn.style, {
        position: 'fixed',
        bottom: '20px',
        right: '20px',
        zIndex: '10000',
        padding: '10px 15px',
        background: 'red',
        color: 'white',
        border: 'none',
        cursor: 'pointer',
        fontFamily: 'monospace',
        fontSize: '12px'
    });

    btn.addEventListener('click', () => {
        overlay.style.display = overlay.style.display === 'none' ? 'block' : 'none';
        btn.style.background = overlay.style.display === 'block' ? 'green' : 'red';
    });

    document.body.appendChild(btn);
})();
