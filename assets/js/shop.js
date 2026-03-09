/* =========================================================================
   SCENTS BY SARA - SHOP PAGE LOGIC
   Handles:
   - Variant Selection (Swatches & Size)
   - Filter Toggle & Logic
   - Sort Logic
   ========================================================================= */

document.addEventListener('DOMContentLoaded', () => {
    if (window.Choices) {
        document.querySelectorAll('.size-select').forEach((select) => {
            new window.Choices(select, {
                searchEnabled: false,
                itemSelectText: '',
                shouldSort: false,
                allowHTML: false,
                position: 'bottom'
            });
        });

        const sortSelectControl = document.getElementById('sort-select');
        if (sortSelectControl) {
            new window.Choices(sortSelectControl, {
                searchEnabled: false,
                itemSelectText: '',
                shouldSort: false,
                allowHTML: false,
                position: 'bottom'
            });
        }
    }

    /* --- Variant Selection: Color Swatches --- */
    const swatches = document.querySelectorAll('.swatch');
    swatches.forEach(swatch => {
        swatch.addEventListener('click', (e) => {
            const parent = swatch.closest('.color-swatches');
            parent.querySelectorAll('.swatch').forEach(s => s.classList.remove('active'));
            swatch.classList.add('active');

            // In a real app, this would swap the product image
            // console.log(`Selected color: ${swatch.classList[1]}`);
        });
    });

    /* --- Filter Button Logic --- */
    const filterBtn = document.querySelector('.filter-btn');
    const filterOverlay = document.createElement('div');
    filterOverlay.className = 'filter-overlay';
    filterOverlay.id = 'shop-filter-panel';
    filterOverlay.setAttribute('aria-hidden', 'true');
    filterOverlay.innerHTML = `
        <div class="filter-content container">
            <div class="filter-header flex-between mb-8">
                <h3 class="font-serif">FILTERS</h3>
                <button class="close-filters icon-btn">&times;</button>
            </div>
            <div class="filter-grid grid-cols-2">
                <div class="filter-group">
                    <h4>BODY SHAPE</h4>
                    <label><input type="checkbox" value="slim"> SLIM</label>
                    <label><input type="checkbox" value="curvy"> CURVY</label>
                    <label><input type="checkbox" value="plus-size"> PLUS SIZE</label>
                </div>
                <div class="filter-group">
                    <h4>BODY COLOUR</h4>
                    <label><input type="checkbox" value="ivory"> IVORY</label>
                    <label><input type="checkbox" value="caramel"> CARAMEL</label>
                    <label><input type="checkbox" value="mocha"> MOCHA</label>
                </div>
            </div>
            <div class="filter-footer mt-12 flex-between">
                <button class="btn-outline clear-filters">CLEAR ALL</button>
                <button class="btn-solid apply-filters">APPLY FILTERS</button>
            </div>
        </div>
    `;
    document.body.appendChild(filterOverlay);

    if (filterBtn) {
        filterBtn.addEventListener('click', () => {
            filterOverlay.classList.toggle('active');
            const isOpen = filterOverlay.classList.contains('active');
            filterBtn.setAttribute('aria-expanded', String(isOpen));
            filterOverlay.setAttribute('aria-hidden', isOpen ? 'false' : 'true');
            document.body.style.overflow = filterOverlay.classList.contains('active') ? 'hidden' : '';
        });
    }

    const closeFilters = filterOverlay.querySelector('.close-filters');
    if (closeFilters) {
        closeFilters.addEventListener('click', () => {
            filterOverlay.classList.remove('active');
            if (filterBtn) filterBtn.setAttribute('aria-expanded', 'false');
            filterOverlay.setAttribute('aria-hidden', 'true');
            document.body.style.overflow = '';
        });
    }

    const applyFiltersBtn = filterOverlay.querySelector('.apply-filters');
    if (applyFiltersBtn) {
        applyFiltersBtn.addEventListener('click', () => {
            const selectedShapes = Array.from(filterOverlay.querySelectorAll('.filter-group:first-child input:checked')).map(i => i.value);
            const selectedColors = Array.from(filterOverlay.querySelectorAll('.filter-group:nth-child(2) input:checked')).map(i => i.value);
            filterProducts(selectedShapes, selectedColors);
            filterOverlay.classList.remove('active');
            if (filterBtn) filterBtn.setAttribute('aria-expanded', 'false');
            filterOverlay.setAttribute('aria-hidden', 'true');
            document.body.style.overflow = '';
        });
    }

    const clearFiltersBtn = filterOverlay.querySelector('.clear-filters');
    if (clearFiltersBtn) {
        clearFiltersBtn.addEventListener('click', () => {
            filterOverlay.querySelectorAll('input').forEach(i => i.checked = false);
            filterProducts([], []);
        });
    }

    function getCardColors(card) {
        const definedColors = card.dataset.colors;
        if (definedColors) {
            return definedColors.split(/\s+/).filter(Boolean);
        }

        const swatches = Array.from(card.querySelectorAll('.color-swatches .swatch'));
        return swatches.map((swatch) => {
            if (swatch.classList.contains('swatch-tan')) return 'caramel';
            if (swatch.classList.contains('swatch-brown')) return 'mocha';
            return 'ivory';
        });
    }

    function filterProducts(shapes, colors) {
        const cards = document.querySelectorAll('.shop-card');
        cards.forEach(card => {
            const cardShape = card.dataset.category;
            const cardColors = getCardColors(card);
            const matchesShape = shapes.length === 0 || shapes.includes(cardShape);
            const matchesColor = colors.length === 0 || colors.some((color) => cardColors.includes(color));

            if (matchesShape && matchesColor) {
                card.style.display = '';
            } else {
                card.style.display = 'none';
            }
        });
    }

    /* --- Sort Dropdown Logic --- */
    const sortSelect = document.getElementById('sort-select');
    if (sortSelect) {
        sortSelect.addEventListener('change', () => {
            sortProducts(sortSelect.value);
        });
    }

    function sortProducts(order) {
        const grid = document.querySelector('.grid-cols-4');
        const cards = Array.from(grid.querySelectorAll('.shop-card'));

        cards.sort((a, b) => {
            const priceA = parseFloat(a.querySelector('.price-current').getAttribute('data-price-gbp'));
            const priceB = parseFloat(b.querySelector('.price-current').getAttribute('data-price-gbp'));
            return order === 'asc' ? priceA - priceB : priceB - priceA;
        });

        // Re-append in order
        cards.forEach(card => grid.appendChild(card));
    }

    /* --- Add to Cart Logic --- */
    const buyBtns = document.querySelectorAll('.btn-shop-now');
    buyBtns.forEach(btn => {
        btn.addEventListener('click', (e) => {
            const card = btn.closest('.shop-card');
            const name = card.querySelector('.product-name')?.textContent?.trim() || 'SHE IS TIMELESS';
            const priceEl = card.querySelector('.price-current');
            const price = parseFloat(priceEl?.getAttribute('data-price-gbp')) || 0;
            const size = (card.querySelector('.size-dropdown span')?.textContent || 'SIZE: SLIM')
                .replace('SIZE:', '')
                .trim();
            const image = card.querySelector('.product-image-wrap img')?.getAttribute('src') || 'assets/images/product-1.png';
            const activeSwatch = card.querySelector('.color-swatches .swatch.active');
            const color = activeSwatch?.classList.contains('swatch-tan') ? 'CARAMEL'
                : activeSwatch?.classList.contains('swatch-brown') ? 'EBONY'
                    : 'IVORY';

            if (window.CartState) {
                window.CartState.addItem({
                    id: `${name.toLowerCase().replace(/\s+/g, '-')}-${size.toLowerCase().replace(/\s+/g, '-')}`,
                    name,
                    price,
                    quantity: 1,
                    color,
                    size,
                    scent: 'VANILLA',
                    image,
                    url: 'product.html'
                });
            }

            // Simple visual feedback
            const originalText = btn.textContent;
            btn.textContent = 'ADDED TO BAG';
            btn.style.backgroundColor = 'var(--color-mocha)';
            btn.style.color = 'var(--color-sand)';

            setTimeout(() => {
                btn.textContent = originalText;
                btn.style.backgroundColor = '';
                btn.style.color = '';
            }, 2000);
        });
    });
});
