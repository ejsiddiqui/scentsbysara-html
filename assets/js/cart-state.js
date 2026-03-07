/* =========================================================================
   Shared cart persistence and totals
   ========================================================================= */

(function initCartState() {
    const STORAGE_KEY = 'scentsbysara-cart-v1';
    const CART_CHANGE_EVENT = 'cart:updated';

    const toNumber = (value, fallback = 0) => {
        const parsed = Number(value);
        return Number.isFinite(parsed) ? parsed : fallback;
    };

    const sanitize = (item) => {
        const normalized = {
            id: item.id || item.name || `item-${Date.now()}`,
            name: item.name || 'Scents by Sara Candle',
            price: toNumber(item.price, 0),
            image: item.image || 'assets/images/product-1.png',
            quantity: Math.max(1, Math.floor(toNumber(item.quantity, 1))),
            color: item.color || 'IVORY',
            size: item.size || 'SLIM',
            scent: item.scent || 'VANILLA',
            url: item.url || 'product.html'
        };
        normalized.lineId = `${normalized.id}__${normalized.color}__${normalized.size}__${normalized.scent}`;
        return normalized;
    };

    const getItems = () => {
        try {
            const raw = localStorage.getItem(STORAGE_KEY);
            if (!raw) return [];
            const parsed = JSON.parse(raw);
            if (!Array.isArray(parsed)) return [];
            return parsed.map(sanitize);
        } catch {
            return [];
        }
    };

    const saveItems = (items) => {
        const nextItems = items.map(sanitize);
        localStorage.setItem(STORAGE_KEY, JSON.stringify(nextItems));
        window.dispatchEvent(new CustomEvent(CART_CHANGE_EVENT, {
            detail: {
                items: nextItems
            }
        }));
    };

    const addItem = (item) => {
        const cart = getItems();
        const next = sanitize(item);
        const existingIndex = cart.findIndex((row) => row.lineId === next.lineId);
        if (existingIndex >= 0) {
            cart[existingIndex].quantity += next.quantity;
        } else {
            cart.push(next);
        }
        saveItems(cart);
        return cart;
    };

    const updateQuantity = (lineId, quantity) => {
        const cart = getItems();
        const nextQuantity = Math.max(1, Math.floor(toNumber(quantity, 1)));
        const target = cart.find((row) => row.lineId === lineId);
        if (!target) return cart;
        target.quantity = nextQuantity;
        saveItems(cart);
        return cart;
    };

    const removeItem = (lineId) => {
        const cart = getItems().filter((row) => row.lineId !== lineId);
        saveItems(cart);
        return cart;
    };

    const clear = () => {
        localStorage.removeItem(STORAGE_KEY);
        window.dispatchEvent(new CustomEvent(CART_CHANGE_EVENT, {
            detail: {
                items: []
            }
        }));
    };

    const getTotals = (items = getItems()) => {
        const subtotal = items.reduce((sum, item) => sum + item.price * item.quantity, 0);
        const shipping = subtotal > 0 ? (subtotal >= 50 ? 0 : 5) : 0;
        const tax = subtotal * 0.2;
        const total = subtotal + shipping + tax;
        return { subtotal, shipping, tax, total };
    };

    const getItemCount = (items = getItems()) => items.reduce((sum, item) => sum + item.quantity, 0);

    window.CartState = {
        getItems,
        saveItems,
        addItem,
        updateQuantity,
        removeItem,
        clear,
        getTotals,
        getItemCount,
        events: {
            updated: CART_CHANGE_EVENT
        }
    };
})();
