/* =========================================================================
   SCENTS BY SARA - PRODUCT PAGE LOGIC
   Handles:
   - Quantity Selector
   - Color Swatches (Large)
   - Pill Button Selectors (Shape, Scent)
   - Accordion Toggle
   - Gallery Thumbnail Swap
   ========================================================================= */

document.addEventListener('DOMContentLoaded', () => {
    const getSelectedColorName = (swatchEl) => {
        if (!swatchEl) return 'CARAMEL';
        if (swatchEl.classList.contains('swatch-tan')) return 'CARAMEL';
        if (swatchEl.classList.contains('swatch-white')) return 'IVORY';
        if (swatchEl.classList.contains('swatch-brown')) return 'MOCHA';
        return 'CARAMEL';
    };

    /* --- Gallery Thumbnail Logic --- */
    const thumbnails = document.querySelectorAll('.thumb-wrap');
    const mainImage = document.querySelector('.main-image-wrap img');

    thumbnails.forEach(thumb => {
        thumb.addEventListener('click', () => {
            thumbnails.forEach(t => t.classList.remove('active'));
            thumb.classList.add('active');
            const newSrc = thumb.querySelector('img').src;
            if (mainImage) mainImage.src = newSrc;
        });
    });

    /* --- Color Swatches --- */
    const lgSwatches = document.querySelectorAll('.swatch-lg');
    const colorLabel = document.querySelector('.product-details .selector-group .selector-label');

    lgSwatches.forEach(swatch => {
        swatch.addEventListener('click', () => {
            lgSwatches.forEach(s => s.classList.remove('selected'));
            swatch.classList.add('selected');

            // Update Label
            if (colorLabel) {
                colorLabel.textContent = `COLOUR : ${getSelectedColorName(swatch)}`;
            }
        });
    });

    /* --- Pill Selectors (Shape, Scent) --- */
    const pillGroups = document.querySelectorAll('.pill-group');
    pillGroups.forEach(group => {
        const pills = group.querySelectorAll('.pill-btn');
        const label = group.closest('.selector-group').querySelector('.selector-label');
        const labelPrefix = label ? label.textContent.split(':')[0] : '';

        pills.forEach(pill => {
            pill.addEventListener('click', () => {
                pills.forEach(p => p.classList.remove('selected'));
                pill.classList.add('selected');

                if (label) {
                    label.textContent = `${labelPrefix}: ${pill.textContent}`;
                }
            });
        });
    });

    /* --- Quantity Selector --- */
    const qtyInput = document.querySelector('.qty-input');
    const qtyBtns = document.querySelectorAll('.qty-btn');

    if (qtyInput && qtyBtns.length > 0) {
        qtyBtns.forEach(btn => {
            btn.addEventListener('click', () => {
                let currentVal = parseInt(qtyInput.value);
                if (btn.textContent === '+') {
                    qtyInput.value = currentVal + 1;
                } else if (currentVal > 1) {
                    qtyInput.value = currentVal - 1;
                }
                updateAddButtonText();
            });
        });
    }

    function updateAddButtonText() {
        const addBtn = document.querySelector('.btn-add-bag');
        if (addBtn && qtyInput) {
            const unitGbp = parseFloat(addBtn.getAttribute('data-unit-price-gbp')) || 20.26;
            const total = unitGbp * parseInt(qtyInput.value);
            if (window.CurrencyConverter) {
                addBtn.innerHTML = 'ADD TO BAG - ' + window.CurrencyConverter.formatPrice(total);
            } else {
                addBtn.textContent = `ADD TO BAG - £${total.toFixed(2)}`;
            }
        }
    }

    /* --- Accordions --- */
    const accordions = document.querySelectorAll('.accordion');
    accordions.forEach(acc => {
        const header = acc.querySelector('.accordion-header');
        header.addEventListener('click', () => {
            // Close others
            accordions.forEach(other => {
                if (other !== acc) other.classList.remove('active');
            });
            // Toggle current
            acc.classList.toggle('active');
        });
    });

    /* --- Add to Bag Interaction --- */
    const addBagBtn = document.querySelector('.btn-add-bag');
    if (addBagBtn) {
        addBagBtn.addEventListener('click', () => {
            const originalText = addBagBtn.textContent;
            const qtyValue = parseInt(qtyInput?.value || '1', 10) || 1;
            const detailLabels = document.querySelectorAll('.product-details .selector-group .selector-label');
            const selectedSwatch = document.querySelector('.swatch-lg.selected');
            const selectedColor = getSelectedColorName(selectedSwatch);
            const selectedSize = detailLabels[1]?.textContent.split(':')[1]?.trim() || 'PLUS-SIZE';
            const selectedScent = detailLabels[2]?.textContent.split(':')[1]?.trim() || 'VANILLA';
            const productName = document.querySelector('.product-header-block h1')?.textContent.trim() || 'SHE IS LUST';
            const mainImgSrc = document.querySelector('.main-image-wrap img')?.getAttribute('src') || 'assets/images/product-1.png';
            const priceEl = document.querySelector('.product-header-block .price');
            const unitPrice = parseFloat(priceEl?.getAttribute('data-price-gbp')) || 20.26;

            if (window.CartState) {
                window.CartState.addItem({
                    id: `${productName.toLowerCase().replace(/\s+/g, '-')}`,
                    name: productName,
                    price: unitPrice,
                    quantity: qtyValue,
                    color: selectedColor,
                    size: selectedSize,
                    scent: selectedScent,
                    image: mainImgSrc,
                    url: 'product.html'
                });
            }

            addBagBtn.textContent = 'ADDED TO BAG';
            addBagBtn.classList.add('success');

            setTimeout(() => {
                addBagBtn.textContent = originalText;
                addBagBtn.classList.remove('success');
            }, 2000);
        });
    }

    /* --- PDP Testimonials Dots --- */
    const pdpDots = document.querySelectorAll('.testimonials-section .slider-dots .dot');
    const testimonialText = document.querySelector('.testimonials-section .text-body');
    const testimonialAuthor = document.querySelector('.testimonials-section .text-micro');
    const testimonials = [
        {
            text: 'I knew the candles looked amazing, but I did not expect them to smell this good. It turns every evening into a ritual.',
            author: 'EUNICE YUMBA'
        },
        {
            text: 'The scent throw is beautiful even before lighting. It feels like a design object and a wellness tool in one.',
            author: 'NADIA IBRAHIM'
        },
        {
            text: 'I ordered it as a gift and ended up ordering one for myself. The craftsmanship and fragrance are genuinely premium.',
            author: 'PRIYA MEHTA'
        }
    ];

    if (pdpDots.length && testimonialText && testimonialAuthor) {
        const setTestimonial = (index) => {
            const safeIndex = index % testimonials.length;
            testimonialText.textContent = testimonials[safeIndex].text;
            testimonialAuthor.textContent = testimonials[safeIndex].author;
            pdpDots.forEach((dot, dotIndex) => {
                dot.classList.toggle('active', dotIndex === safeIndex);
            });
        };

        pdpDots.forEach((dot, index) => {
            dot.addEventListener('click', () => setTestimonial(index));
        });
    }

    if (window.CurrencyConverter) {
        window.CurrencyConverter.onChange(updateAddButtonText);
    }
});
