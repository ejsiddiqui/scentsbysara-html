/* =========================================================================
   SCENTS BY SARA - V2 MAIN SCRIPT
   Handles:
   - Header Scroll Logic (Hide down, show up)
   - Mobile Hamburger Menu Toggle
   ========================================================================= */

const MOBILE_MENU_TEMPLATE = `
    <div class="mobile-menu-content container">
        <div class="mobile-menu-top">
            <a href="index.html" class="mobile-menu-brand" aria-label="Scents by Sara">
                <img src="assets/images/logo-long.svg" alt="Scents by Sara Logo">
            </a>
            <div class="mobile-menu-actions">
                <button class="icon-btn mobile-menu-cart" aria-label="Cart" onclick="window.location.href='cart.html'">
                    <img src="assets/icons/handbag 1.svg" alt="" aria-hidden="true">
                </button>
                <button class="icon-btn mobile-menu-search search-toggle" aria-label="Search">
                    <img src="assets/icons/search 1.svg" alt="" aria-hidden="true">
                </button>
                <button class="icon-btn close-mobile-menu" aria-label="Close Menu">
                    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.2"
                        stroke-linecap="round" stroke-linejoin="round">
                        <line x1="3" y1="12" x2="21" y2="12"></line>
                        <line x1="3" y1="6" x2="21" y2="6"></line>
                        <line x1="3" y1="18" x2="21" y2="18"></line>
                    </svg>
                </button>
            </div>
        </div>

        <div class="mobile-menu-body">
            <nav class="mobile-nav-links mobile-nav-primary" role="navigation" aria-label="Mobile Navigation">
                <div class="mobile-nav-item mobile-nav-item-shop">
                    <button class="mobile-shop-toggle" type="button" aria-expanded="false" aria-controls="mobile-shop-panel">
                        <span>SHOP</span>
                        <svg class="mobile-shop-toggle-icon" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.2"
                            stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
                            <polyline points="9 6 15 12 9 18"></polyline>
                        </svg>
                    </button>
                    <div class="mobile-shop-panel" id="mobile-shop-panel" hidden>
                        <div class="mobile-shop-group">
                            <h3>POPULAR</h3>
                            <a href="shop.html">Shop All</a>
                            <a href="shop.html">Bestsellers</a>
                        </div>
                        <div class="mobile-shop-group">
                            <h3>BODY CANDLES</h3>
                            <a href="body-candles.html">All Body Candles</a>
                            <a href="product.html">She is You</a>
                            <a href="product.html">She is Strength</a>
                            <a href="product.html">She is Real</a>
                            <a href="product.html">She is Power</a>
                            <a href="product.html">She is Timeless</a>
                            <a href="product.html">She is Beauty</a>
                        </div>
                        <div class="mobile-shop-group">
                            <h3>SHOP BY SIZE</h3>
                            <a href="shop.html">Slim</a>
                            <a href="shop.html">Curvy</a>
                            <a href="shop.html">Plus Size</a>
                        </div>
                        <div class="mobile-shop-group">
                            <h3>SHOP BY COLLECTION</h3>
                            <a href="scar-collection.html">Scar Collection</a>
                            <a href="sculpted-collection.html">Sculpted Collection</a>
                        </div>
                    </div>
                </div>
                <a href="gifts.html">GIFTS</a>
                <a href="our-story.html">OUR STORY</a>
                <a href="your-story.html">YOUR STORY</a>
                <a href="shop.html">WISHLIST</a>
                <a href="contact.html">CONTACT</a>
            </nav>

            <div class="mobile-menu-footer">
                <a href="contact.html" class="btn-outline full-width-btn mobile-menu-cta">LOG IN</a>
                <a href="contact.html" class="btn-outline full-width-btn mobile-menu-cta">JOIN OUR NEWSLETTER</a>
                <div class="mobile-menu-meta">
                    <div class="mobile-menu-social">
                        <a href="https://instagram.com" target="_blank" rel="noopener noreferrer" aria-label="Instagram">
                            <img src="assets/icons/instagram.svg" alt="" aria-hidden="true">
                        </a>
                        <a href="https://facebook.com" target="_blank" rel="noopener noreferrer" aria-label="Facebook">
                            <img src="assets/icons/facebook.svg" alt="" aria-hidden="true">
                        </a>
                        <a href="https://tiktok.com" target="_blank" rel="noopener noreferrer" aria-label="TikTok">
                            <img src="assets/icons/tiktok.svg" alt="" aria-hidden="true">
                        </a>
                        <a href="https://pinterest.com" target="_blank" rel="noopener noreferrer" aria-label="Pinterest">
                            <img src="assets/icons/pinterest.svg" alt="" aria-hidden="true">
                        </a>
                    </div>
                    <div class="mobile-menu-currency">
                        <select data-currency-select aria-label="Mobile currency">
                            <option value="AED">AED</option>
                            <option value="GBP">GBP £</option>
                            <option value="USD">USD $</option>
                            <option value="EUR">EUR €</option>
                        </select>
                    </div>
                </div>
            </div>
        </div>
    </div>
`;

(function ensureMobileMenuIntegrity() {
    const mobileMenu = document.querySelector('.mobile-menu-overlay');
    if (!mobileMenu) return;

    const primaryNav = mobileMenu.querySelector('.mobile-nav-primary');
    const primaryLinkCount = primaryNav ? primaryNav.querySelectorAll(':scope > a').length : 0;
    const socialLinkCount = mobileMenu.querySelectorAll('.mobile-menu-social a').length;
    const hasCurrency = !!mobileMenu.querySelector('.mobile-menu-currency select');
    const hasFooter = !!mobileMenu.querySelector('.mobile-menu-footer');
    const hasShopToggle = !!mobileMenu.querySelector('.mobile-shop-toggle');

    const isIncomplete = !primaryNav
        || primaryLinkCount < 5
        || socialLinkCount < 4
        || !hasCurrency
        || !hasFooter
        || !hasShopToggle;

    if (isIncomplete) {
        mobileMenu.innerHTML = MOBILE_MENU_TEMPLATE;
    }
})();

document.addEventListener('DOMContentLoaded', () => {
    const cartCountBadges = document.querySelectorAll('[data-cart-count]');

    const updateCartCountBadges = (items = null) => {
        if (!cartCountBadges.length || !window.CartState) return;

        const count = window.CartState.getItemCount(items || window.CartState.getItems());
        cartCountBadges.forEach((badge) => {
            badge.textContent = String(count);
            badge.hidden = count < 1;
        });
    };

    if (cartCountBadges.length && window.CartState) {
        updateCartCountBadges();
        window.addEventListener(window.CartState.events.updated, (event) => {
            updateCartCountBadges(event.detail?.items || null);
        });

        window.addEventListener('storage', (event) => {
            if (event.key === 'scentsbysara-cart-v1') {
                updateCartCountBadges();
            }
        });
    }

    /* --- Header Scroll Logic --- */
    const header = document.querySelector('.site-header');
    let lastScrollY = window.scrollY;
    const SCROLL_THRESHOLD = 8;
    let headerScrollTicking = false;

    if (header) {
        window.addEventListener('scroll', () => {
            if (headerScrollTicking) return;
            headerScrollTicking = true;

            window.requestAnimationFrame(() => {
                const currentScrollY = window.scrollY;
                const delta = currentScrollY - lastScrollY;

                // At the very top
                if (currentScrollY <= 0) {
                    header.classList.remove('header-scrolled', 'header-hidden');
                }
                // Scrolling Down -> Hide Menu
                else if (delta > SCROLL_THRESHOLD) {
                    header.classList.add('header-hidden');
                    header.classList.remove('header-scrolled');
                }
                // Scrolling Up -> Show Sticky Menu
                else if (delta < -SCROLL_THRESHOLD) {
                    header.classList.remove('header-hidden');
                    header.classList.add('header-scrolled');
                }

                lastScrollY = currentScrollY;
                headerScrollTicking = false;
            });
        }, { passive: true });
    }

    /* --- Mobile Navigation Toggle --- */
    const hamburgerBtn = document.querySelector('.hamburger-btn');
    const mobileMenu = document.querySelector('.mobile-menu-overlay');
    const closeMenuBtn = document.querySelector('.close-mobile-menu');
    const mobileMenuLinks = document.querySelectorAll('.mobile-nav-links a');
    const mobileShopItem = document.querySelector('.mobile-nav-item-shop');
    const mobileShopToggle = document.querySelector('.mobile-shop-toggle');
    const mobileShopPanel = document.querySelector('.mobile-shop-panel');
    const MENU_CLOSE_DURATION_MS = 450;
    const SHOP_PANEL_DURATION_MS = 180;
    let closeMenuTimeoutId = null;
    let closeTransitionHandler = null;
    let pageScrollY = 0;
    let shopPanelTimeoutId = null;

    const setShopMenuExpanded = (isExpanded) => {
        if (!mobileShopItem || !mobileShopToggle || !mobileShopPanel) return;

        if (shopPanelTimeoutId) {
            window.clearTimeout(shopPanelTimeoutId);
            shopPanelTimeoutId = null;
        }

        mobileShopItem.classList.toggle('expanded', isExpanded);
        mobileShopToggle.setAttribute('aria-expanded', String(isExpanded));

        if (isExpanded) {
            mobileShopPanel.removeAttribute('hidden');
            mobileShopPanel.style.maxHeight = '0px';
            mobileShopPanel.style.opacity = '0';

            window.requestAnimationFrame(() => {
                mobileShopPanel.style.maxHeight = `${mobileShopPanel.scrollHeight}px`;
                mobileShopPanel.style.opacity = '1';
            });

            mobileShopPanel.removeAttribute('hidden');
            return;
        }

        const currentHeight = mobileShopPanel.scrollHeight;
        mobileShopPanel.style.maxHeight = `${currentHeight}px`;
        mobileShopPanel.style.opacity = '1';

        window.requestAnimationFrame(() => {
            mobileShopPanel.style.maxHeight = '0px';
            mobileShopPanel.style.opacity = '0';
        });

        shopPanelTimeoutId = window.setTimeout(() => {
            mobileShopPanel.setAttribute('hidden', '');
        }, SHOP_PANEL_DURATION_MS);
    };

    const lockPageScroll = () => {
        pageScrollY = window.scrollY;
        document.documentElement.style.overflow = 'hidden';
        document.body.style.overflow = 'hidden';
        document.body.style.position = 'fixed';
        document.body.style.top = `-${pageScrollY}px`;
        document.body.style.width = '100%';
    };

    const unlockPageScroll = () => {
        document.documentElement.style.overflow = '';
        document.body.style.overflow = '';
        document.body.style.position = '';
        document.body.style.top = '';
        document.body.style.width = '';
        window.scrollTo(0, pageScrollY);
    };

    const clearCloseAnimation = () => {
        if (!mobileMenu) return;

        if (closeMenuTimeoutId) {
            window.clearTimeout(closeMenuTimeoutId);
            closeMenuTimeoutId = null;
        }

        if (closeTransitionHandler) {
            mobileMenu.removeEventListener('transitionend', closeTransitionHandler);
            closeTransitionHandler = null;
        }
    };

    const applyClosedState = () => {
        if (!hamburgerBtn || !mobileMenu) return;

        hamburgerBtn.setAttribute('aria-expanded', 'false');
        mobileMenu.classList.remove('active', 'closing');
        mobileMenu.setAttribute('aria-hidden', 'true');
        mobileMenu.setAttribute('inert', '');
        unlockPageScroll();
        setShopMenuExpanded(false);
    };

    const openMenu = () => {
        if (!hamburgerBtn || !mobileMenu) return;
        clearCloseAnimation();
        setShopMenuExpanded(false);

        hamburgerBtn.setAttribute('aria-expanded', 'true');
        mobileMenu.classList.remove('closing');
        mobileMenu.classList.add('active');
        mobileMenu.setAttribute('aria-hidden', 'false');
        mobileMenu.removeAttribute('inert');
        lockPageScroll();
    };

    const closeMenu = (animate = true) => {
        if (!hamburgerBtn || !mobileMenu) return;
        clearCloseAnimation();

        if (!animate) {
            applyClosedState();
            return;
        }

        const isActive = mobileMenu.classList.contains('active');
        const isClosing = mobileMenu.classList.contains('closing');

        if (!isActive && !isClosing) {
            applyClosedState();
            return;
        }

        hamburgerBtn.setAttribute('aria-expanded', 'false');
        mobileMenu.classList.remove('active');
        mobileMenu.classList.add('closing');
        mobileMenu.setAttribute('aria-hidden', 'false');
        mobileMenu.removeAttribute('inert');
        unlockPageScroll();

        closeTransitionHandler = (event) => {
            if (event.target !== mobileMenu || event.propertyName !== 'right') return;
            clearCloseAnimation();
            applyClosedState();
        };

        mobileMenu.addEventListener('transitionend', closeTransitionHandler);
        closeMenuTimeoutId = window.setTimeout(() => {
            clearCloseAnimation();
            applyClosedState();
        }, MENU_CLOSE_DURATION_MS);
    };

    const setMenuState = (isOpen, options = {}) => {
        if (isOpen) {
            openMenu();
            return;
        }

        closeMenu(options.animateClose ?? true);
    };

    const toggleMenu = (e) => {
        if (e) e.preventDefault();
        const isOpen = hamburgerBtn.getAttribute('aria-expanded') === 'true';
        setMenuState(!isOpen);
    };

    if (hamburgerBtn && mobileMenu) {
        setMenuState(false, { animateClose: false });
        hamburgerBtn.addEventListener('click', toggleMenu);
    }

    if (closeMenuBtn && mobileMenu) {
        closeMenuBtn.addEventListener('click', (event) => {
            event.preventDefault();
            setMenuState(false);
        });
    }

    if (mobileMenuLinks.length > 0) {
        mobileMenuLinks.forEach((link) => {
            link.addEventListener('click', () => setMenuState(false));
        });
    }

        if (mobileShopToggle) {
            setShopMenuExpanded(false);
            mobileShopToggle.addEventListener('click', () => {
                const isExpanded = mobileShopToggle.getAttribute('aria-expanded') === 'true';
                setShopMenuExpanded(!isExpanded);
        });
    }

    document.addEventListener('keydown', (event) => {
        if (event.key === 'Escape' && mobileMenu && mobileMenu.classList.contains('active')) {
            setMenuState(false);
        }
    });

    /* --- Footer Mobile Accordion --- */
    const footerAccordionQuery = window.matchMedia('(max-width: 480px)');
    const footerAccordionItems = Array.from(document.querySelectorAll('.footer-links-col')).map((section) => ({
        section,
        trigger: section.querySelector('.footer-accordion-trigger'),
        icon: section.querySelector('.footer-accordion-icon'),
    })).filter((item) => item.trigger && item.icon);

    const setFooterAccordionExpanded = (item, isExpanded) => {
        item.section.classList.toggle('expanded', isExpanded);
        item.trigger.setAttribute('aria-expanded', String(isExpanded));
        item.icon.textContent = isExpanded ? '-' : '+';
    };

    const syncFooterAccordionState = () => {
        if (!footerAccordionItems.length) return;

        footerAccordionItems.forEach((item) => {
            setFooterAccordionExpanded(item, !footerAccordionQuery.matches);
        });
    };

    if (footerAccordionItems.length) {
        syncFooterAccordionState();

        footerAccordionItems.forEach((item) => {
            item.trigger.addEventListener('click', () => {
                if (!footerAccordionQuery.matches) return;

                const isExpanded = item.trigger.getAttribute('aria-expanded') === 'true';
                setFooterAccordionExpanded(item, !isExpanded);
            });
        });

        if (typeof footerAccordionQuery.addEventListener === 'function') {
            footerAccordionQuery.addEventListener('change', syncFooterAccordionState);
        } else if (typeof footerAccordionQuery.addListener === 'function') {
            footerAccordionQuery.addListener(syncFooterAccordionState);
        }
    }

    /* --- Search Toggle Logic --- */
    const searchToggleBtns = document.querySelectorAll('.search-toggle');
    const searchCloseBtn = document.querySelector('.search-close');
    const searchOverlay = document.querySelector('.search-overlay');
    const searchInput = document.querySelector('.search-input');

    if (searchToggleBtns && searchOverlay) {
        searchToggleBtns.forEach(btn => {
            btn.addEventListener('click', (e) => {
                e.preventDefault();
                searchOverlay.classList.toggle('active');
                if (searchOverlay.classList.contains('active')) {
                    setTimeout(() => searchInput.focus(), 100);
                }
            });
        });
    }

    if (searchCloseBtn && searchOverlay) {
        searchCloseBtn.addEventListener('click', (e) => {
            e.preventDefault();
            searchOverlay.classList.remove('active');
        });
    }

    /* --- Hero Image Slider Logic --- */
    const heroSection = document.querySelector('.home-hero');
    const heroSlider = document.querySelector('.hero-slider');
    const heroDots = document.querySelectorAll('.home-hero .slider-dots .dot');

    if (heroSection && heroSlider && heroDots.length > 0) {
        const totalSlides = heroDots.length;
        const HERO_DRAG_THRESHOLD_PX = 56;
        const HERO_DRAG_THRESHOLD_RATIO = 0.12;
        let currentSlide = 0;
        let autoSlideInterval;
        let activePointerId = null;
        let dragStartX = 0;
        let dragStartY = 0;
        let dragDistanceX = 0;
        let isDraggingHero = false;

        const getHeroSlideWidth = () => heroSection.getBoundingClientRect().width || heroSlider.offsetWidth;

        const setHeroSliderOffsetPx = (offsetPx) => {
            heroSlider.style.transform = `translate3d(${offsetPx}px, 0, 0)`;
        };

        const updateSlider = (index) => {
            heroSection.classList.remove('is-dragging');
            heroSlider.classList.remove('is-dragging');
            heroSlider.style.transform = `translate3d(-${index * 100}%, 0, 0)`;
            heroDots.forEach((dot) => dot.classList.remove('active'));
            heroDots[index].classList.add('active');
            currentSlide = index;
        };

        const nextSlide = () => {
            let next = currentSlide + 1;
            if (next >= totalSlides) next = 0;
            updateSlider(next);
        };

        const prevSlide = () => {
            let prev = currentSlide - 1;
            if (prev < 0) prev = totalSlides - 1;
            updateSlider(prev);
        }

        // Dots click
        heroDots.forEach((dot, index) => {
            dot.addEventListener('click', () => {
                updateSlider(index);
                resetAutoSlide();
            });
        });

        const resetHeroDragState = () => {
            activePointerId = null;
            dragDistanceX = 0;
            isDraggingHero = false;
            heroSection.classList.remove('is-dragging');
            heroSlider.classList.remove('is-dragging');
        };

        const commitHeroSwipe = () => {
            if (activePointerId === null) return;

            const slideWidth = getHeroSlideWidth();
            const swipeThreshold = Math.max(HERO_DRAG_THRESHOLD_PX, slideWidth * HERO_DRAG_THRESHOLD_RATIO);
            let targetSlide = currentSlide;

            if (isDraggingHero && Math.abs(dragDistanceX) >= swipeThreshold) {
                targetSlide = dragDistanceX < 0 ? (currentSlide + 1) % totalSlides : (currentSlide - 1 + totalSlides) % totalSlides;
            }

            updateSlider(targetSlide);

            if (isDraggingHero || Math.abs(dragDistanceX) > 0) {
                resetAutoSlide();
            }

            resetHeroDragState();
        };

        const handleHeroPointerDown = (event) => {
            if (activePointerId !== null) return;
            if (event.pointerType === 'mouse' && event.button !== 0) return;
            if (event.target.closest('a, button, input, select, textarea, label, .slider-dots, .dot')) return;

            activePointerId = event.pointerId;
            dragStartX = event.clientX;
            dragStartY = event.clientY;
            dragDistanceX = 0;
            isDraggingHero = false;
            heroSection.classList.add('is-dragging');
            heroSlider.classList.add('is-dragging');

            if (typeof heroSection.setPointerCapture === 'function') {
                heroSection.setPointerCapture(activePointerId);
            }
        };

        const handleHeroPointerMove = (event) => {
            if (event.pointerId !== activePointerId) return;

            const deltaX = event.clientX - dragStartX;
            const deltaY = event.clientY - dragStartY;

            if (!isDraggingHero) {
                if (Math.abs(deltaX) < 6 || Math.abs(deltaX) < Math.abs(deltaY)) {
                    return;
                }

                isDraggingHero = true;
            }

            dragDistanceX = deltaX;

            const atFirstSlide = currentSlide === 0 && dragDistanceX > 0;
            const atLastSlide = currentSlide === totalSlides - 1 && dragDistanceX < 0;
            const dragResistance = atFirstSlide || atLastSlide ? 0.35 : 1;
            const baseOffsetPx = -currentSlide * getHeroSlideWidth();

            setHeroSliderOffsetPx(baseOffsetPx + (dragDistanceX * dragResistance));
            event.preventDefault();
        };

        const handleHeroPointerEnd = (event) => {
            if (event.pointerId !== activePointerId) return;

            if (typeof heroSection.releasePointerCapture === 'function' && heroSection.hasPointerCapture(event.pointerId)) {
                heroSection.releasePointerCapture(event.pointerId);
            }

            commitHeroSwipe();
        };

        const startAutoSlide = () => {
            autoSlideInterval = setInterval(nextSlide, 5000); // 5s
        };

        const resetAutoSlide = () => {
            clearInterval(autoSlideInterval);
            startAutoSlide();
        };

        heroSection.addEventListener('pointerdown', handleHeroPointerDown);
        heroSection.addEventListener('pointermove', handleHeroPointerMove);
        heroSection.addEventListener('pointerup', handleHeroPointerEnd);
        heroSection.addEventListener('pointercancel', handleHeroPointerEnd);
        heroSection.addEventListener('lostpointercapture', () => {
            if (activePointerId !== null) {
                commitHeroSwipe();
            }
        });
        heroSection.addEventListener('dragstart', (event) => {
            event.preventDefault();
        });

        // Init
        updateSlider(0);
        startAutoSlide();
    }

    /* --- Testimonials Slider Logic --- */
    const testSlider = document.querySelector('.testimonials-slider');
    const testDots = document.querySelectorAll('.testimonials-section .slider-dots .dot');
    const testSlides = document.querySelectorAll('.testimonial-slide');

    if (testSlider && testDots.length > 0 && testSlides.length > 0) {
        const totalSlides = testDots.length;
        let currentSlide = 0;
        let autoSlideInterval;

        const updateSlider = (index) => {
            testSlides.forEach(slide => slide.classList.remove('active'));
            testDots.forEach(dot => dot.classList.remove('active'));

            testSlides[index].classList.add('active');
            testDots[index].classList.add('active');
            currentSlide = index;
        };

        const nextSlide = () => {
            let next = currentSlide + 1;
            if (next >= totalSlides) next = 0;
            updateSlider(next);
        };

        // Dots click
        testDots.forEach((dot, index) => {
            dot.addEventListener('click', () => {
                updateSlider(index);
                resetAutoSlide();
            });
        });

        const startAutoSlide = () => {
            autoSlideInterval = setInterval(nextSlide, 6000); // 6s
        };

        const resetAutoSlide = () => {
            clearInterval(autoSlideInterval);
            startAutoSlide();
        };

        // Init
        startAutoSlide();
    }

});
