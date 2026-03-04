/* =========================================================================
   Checkout behavior: summary mapping + validation
   ========================================================================= */

document.addEventListener('DOMContentLoaded', () => {
    if (!window.CartState) return;

    const summaryItems = document.getElementById('checkout-summary-items');
    const emptySummary = document.getElementById('checkout-summary-empty');
    const subtotalEl = document.getElementById('checkout-subtotal');
    const shippingEl = document.getElementById('checkout-shipping');
    const taxEl = document.getElementById('checkout-tax');
    const totalEl = document.getElementById('checkout-total');
    const form = document.getElementById('checkout-form');
    const formStatus = document.getElementById('checkout-form-status');

    const formatGBP = (value) => `£${value.toFixed(2)}`;

    const renderSummary = () => {
        if (!summaryItems || !emptySummary || !subtotalEl || !shippingEl || !taxEl || !totalEl) return;
        const items = window.CartState.getItems();
        const totals = window.CartState.getTotals(items);

        summaryItems.innerHTML = '';
        emptySummary.style.display = items.length ? 'none' : 'block';

        items.forEach((item) => {
            const line = document.createElement('div');
            line.className = 'summary-item';
            line.innerHTML = `
                <div class="summary-product">
                    <span class="qty-badge">${item.quantity}</span>
                    <div class="summary-img-wrap">
                        <img src="${item.image}" alt="${item.name}">
                    </div>
                    <div class="summary-details">
                        <h4 class="font-sans">${item.name}</h4>
                        <p>${item.color} · ${item.size} · ${item.scent}</p>
                        <span class="summary-price mt-2 block font-sans">${formatGBP(item.price * item.quantity)}</span>
                    </div>
                </div>
            `;
            summaryItems.appendChild(line);
        });

        subtotalEl.textContent = formatGBP(totals.subtotal);
        shippingEl.textContent = formatGBP(totals.shipping);
        taxEl.textContent = formatGBP(totals.tax);
        totalEl.textContent = formatGBP(totals.total);
    };

    const setError = (fieldName, message) => {
        const field = form?.querySelector(`[name="${fieldName}"]`);
        const error = form?.querySelector(`.field-error[data-for="${fieldName}"]`);
        if (field) field.setAttribute('aria-invalid', 'true');
        if (error) error.textContent = message;
    };

    const clearErrors = () => {
        if (!form) return;
        form.querySelectorAll('.field-error').forEach((node) => {
            node.textContent = '';
        });
        form.querySelectorAll('[aria-invalid="true"]').forEach((field) => {
            field.setAttribute('aria-invalid', 'false');
        });
    };

    const parseCardDigits = (value) => value.replace(/\D/g, '').slice(0, 16);
    const formatCardNumber = (value) => parseCardDigits(value).replace(/(\d{4})(?=\d)/g, '$1 ').trim();
    const parseExpiry = (value) => value.replace(/\D/g, '').slice(0, 4);
    const formatExpiry = (value) => {
        const digits = parseExpiry(value);
        if (digits.length <= 2) return digits;
        return `${digits.slice(0, 2)} / ${digits.slice(2)}`;
    };
    const parseCvc = (value) => value.replace(/\D/g, '').slice(0, 4);

    const validateCheckout = () => {
        if (!form) return false;
        const values = Object.fromEntries(new FormData(form).entries());
        let valid = true;

        clearErrors();

        const requiredFields = ['email', 'country', 'firstname', 'lastname', 'address', 'city', 'postcode', 'cardnumber', 'expiry', 'cvc'];
        requiredFields.forEach((fieldName) => {
            const value = String(values[fieldName] || '').trim();
            if (!value) {
                setError(fieldName, 'This field is required.');
                valid = false;
            }
        });

        if (values.email && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(String(values.email).trim())) {
            setError('email', 'Enter a valid email address.');
            valid = false;
        }

        const cardDigits = parseCardDigits(String(values.cardnumber || ''));
        if (cardDigits.length !== 16) {
            setError('cardnumber', 'Card number must be 16 digits.');
            valid = false;
        }

        const expiryDigits = parseExpiry(String(values.expiry || ''));
        if (expiryDigits.length !== 4) {
            setError('expiry', 'Use MM / YY format.');
            valid = false;
        } else {
            const month = Number(expiryDigits.slice(0, 2));
            const year = Number(expiryDigits.slice(2));
            const currentDate = new Date();
            const currentYear = currentDate.getFullYear() % 100;
            const currentMonth = currentDate.getMonth() + 1;
            const expired = year < currentYear || (year === currentYear && month < currentMonth);
            if (month < 1 || month > 12 || expired) {
                setError('expiry', 'Card expiry is invalid or expired.');
                valid = false;
            }
        }

        const cvcDigits = parseCvc(String(values.cvc || ''));
        if (cvcDigits.length < 3 || cvcDigits.length > 4) {
            setError('cvc', 'CVC must be 3 or 4 digits.');
            valid = false;
        }

        return valid;
    };

    const bindPaymentFormatting = () => {
        const cardNumberInput = document.getElementById('cardnumber');
        const expiryInput = document.getElementById('expiry');
        const cvcInput = document.getElementById('cvc');

        if (cardNumberInput) {
            cardNumberInput.addEventListener('input', () => {
                cardNumberInput.value = formatCardNumber(cardNumberInput.value);
            });
        }

        if (expiryInput) {
            expiryInput.addEventListener('input', () => {
                expiryInput.value = formatExpiry(expiryInput.value);
            });
        }

        if (cvcInput) {
            cvcInput.addEventListener('input', () => {
                cvcInput.value = parseCvc(cvcInput.value);
            });
        }
    };

    if (form) {
        bindPaymentFormatting();

        form.addEventListener('submit', (event) => {
            event.preventDefault();
            if (formStatus) {
                formStatus.textContent = '';
                formStatus.classList.remove('is-success', 'is-error');
            }

            if (!window.CartState.getItems().length) {
                if (formStatus) {
                    formStatus.textContent = 'Your bag is empty. Add products before checkout.';
                    formStatus.classList.add('is-error');
                }
                return;
            }

            const valid = validateCheckout();
            if (!valid) {
                if (formStatus) {
                    formStatus.textContent = 'Please fix the highlighted fields.';
                    formStatus.classList.add('is-error');
                }
                const firstInvalid = form.querySelector('[aria-invalid="true"]');
                if (firstInvalid instanceof HTMLElement) firstInvalid.focus();
                return;
            }

            if (formStatus) {
                formStatus.textContent = 'Order placed successfully.';
                formStatus.classList.add('is-success');
            }
            window.CartState.clear();
            renderSummary();
            form.reset();
        });
    }

    renderSummary();
});
