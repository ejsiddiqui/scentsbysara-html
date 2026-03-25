/* =========================================================================
   Cart page rendering and behavior
   ========================================================================= */

document.addEventListener('DOMContentLoaded', () => {
    if (!window.CartState) return;

    const tableBody = document.getElementById('cart-items-table');
    const mobileList = document.getElementById('cart-mobile-list');
    const emptyState = document.getElementById('cart-empty');
    const subtotalEl = document.getElementById('cart-subtotal');
    const shippingEl = document.getElementById('cart-shipping');
    const taxEl = document.getElementById('cart-tax');
    const totalEl = document.getElementById('cart-total');

    if (!tableBody || !mobileList || !emptyState || !subtotalEl || !shippingEl || !taxEl || !totalEl) return;

    const formatCurrency = (gbpValue) => window.CurrencyConverter ? window.CurrencyConverter.formatPrice(gbpValue) : `£${gbpValue.toFixed(2)}`;

    const render = () => {
        const items = window.CartState.getItems();
        const totals = window.CartState.getTotals(items);
        const hasItems = items.length > 0;

        emptyState.classList.toggle('hidden', hasItems);
        tableBody.innerHTML = '';
        mobileList.innerHTML = '';

        subtotalEl.innerHTML = formatCurrency(totals.subtotal);
        shippingEl.innerHTML = formatCurrency(totals.shipping);
        taxEl.innerHTML = formatCurrency(totals.tax);
        totalEl.innerHTML = formatCurrency(totals.total);

        items.forEach((item) => {
            const lineTotal = item.price * item.quantity;

            const tableRow = document.createElement('tr');
            tableRow.innerHTML = `
                <td>
                    <div class="cart-product-info">
                        <div class="cart-img-wrap">
                            <img src="${item.image}" alt="${item.name}">
                        </div>
                        <div>
                            <h3 class="mb-2">${item.name}</h3>
                            <p class="text-micro text-muted mb-4">${item.color} · ${item.size} · ${item.scent}</p>
                            <button class="remove-btn" data-remove-line="${item.lineId}" type="button">REMOVE</button>
                        </div>
                    </div>
                </td>
                <td><span class="font-sans">${formatCurrency(item.price)}</span></td>
                <td>
                    <div class="qty-selector">
                        <button type="button" data-qty-change="${item.lineId}" data-delta="-1" aria-label="Decrease quantity">-</button>
                        <input type="text" value="${item.quantity}" readonly aria-label="Quantity">
                        <button type="button" data-qty-change="${item.lineId}" data-delta="1" aria-label="Increase quantity">+</button>
                    </div>
                </td>
                <td style="text-align: right;"><span class="line-total">${formatCurrency(lineTotal)}</span></td>
            `;
            tableBody.appendChild(tableRow);

            const mobileItem = document.createElement('article');
            mobileItem.className = 'cart-mobile-item';
            mobileItem.innerHTML = `
                <div class="cart-product-info">
                    <div class="cart-img-wrap">
                        <img src="${item.image}" alt="${item.name}">
                    </div>
                    <div>
                        <h3 class="font-sans text-md font-weight-normal mb-2">${item.name}</h3>
                        <p class="text-micro text-muted">${item.color} · ${item.size}</p>
                        <p class="text-micro text-muted">${item.scent}</p>
                    </div>
                </div>
                <div class="cart-mobile-meta">
                    <div class="cart-mobile-row">
                        <span class="text-sm text-muted">Price</span>
                        <span>${formatCurrency(item.price)}</span>
                    </div>
                    <div class="cart-mobile-row">
                        <span class="text-sm text-muted">Quantity</span>
                        <div class="qty-selector">
                            <button type="button" data-qty-change="${item.lineId}" data-delta="-1" aria-label="Decrease quantity">-</button>
                            <input type="text" value="${item.quantity}" readonly aria-label="Quantity">
                            <button type="button" data-qty-change="${item.lineId}" data-delta="1" aria-label="Increase quantity">+</button>
                        </div>
                    </div>
                    <div class="cart-mobile-row">
                        <span class="text-sm text-muted">Total</span>
                        <span class="line-total">${formatCurrency(lineTotal)}</span>
                    </div>
                    <button class="remove-btn" data-remove-line="${item.lineId}" type="button">REMOVE</button>
                </div>
            `;
            mobileList.appendChild(mobileItem);
        });
    };

    document.addEventListener('click', (event) => {
        const target = event.target;
        if (!(target instanceof HTMLElement)) return;

        const removeLine = target.getAttribute('data-remove-line');
        if (removeLine) {
            window.CartState.removeItem(removeLine);
            render();
            return;
        }

        const qtyLine = target.getAttribute('data-qty-change');
        if (qtyLine) {
            const delta = Number(target.getAttribute('data-delta') || 0);
            const current = window.CartState.getItems().find((item) => item.lineId === qtyLine);
            if (!current) return;
            const next = Math.max(1, current.quantity + delta);
            window.CartState.updateQuantity(qtyLine, next);
            render();
        }
    });

    render();

    if (window.CurrencyConverter) {
        window.CurrencyConverter.onChange(render);
    }
});
