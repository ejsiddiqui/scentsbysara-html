/* =========================================================================
   Currency Converter
   - Choices.js dropdown in announcement bar
   - Client-side price conversion with fixed + live rates
   ========================================================================= */

(function () {
    'use strict';

    const DEFAULT_RATES = { GBP: 1, AED: 4.9087, USD: 1.3366, EUR: 1.1531 };
    const AED_SVG = '<span class="currency-symbol-svg" aria-label="AED"></span>';
    const SYMBOLS = { AED: AED_SVG, GBP: '\u00A3', USD: '$', EUR: '\u20AC' };
    const CURRENCY_OPTIONS = ['AED', 'GBP', 'USD', 'EUR'];
    const STORAGE_CURRENCY = 'sbs_currency';
    const STORAGE_RATES = 'sbs_rates';
    const RATE_TTL = 12 * 60 * 60 * 1000; // 12 hours
    const API_URL = 'https://v6.exchangerate-api.com/v6/42b984d2ebcbe1021baee097/latest/GBP';
    const SELECTOR = '[data-currency-select]';

    /* --- Rates --- */

    function loadRates() {
        try {
            const stored = JSON.parse(localStorage.getItem(STORAGE_RATES));
            if (stored && stored.rates && stored.timestamp) return stored;
        } catch (_) { /* ignore */ }
        return { rates: DEFAULT_RATES, timestamp: 0 };
    }

    function saveRates(rates) {
        localStorage.setItem(STORAGE_RATES, JSON.stringify({ rates: rates, timestamp: Date.now() }));
    }

    function isStale(timestamp) {
        return Date.now() - timestamp > RATE_TTL;
    }

    function refreshRatesIfNeeded(state) {
        if (!isStale(state.timestamp)) return;
        fetch(API_URL)
            .then(function (r) { return r.json(); })
            .then(function (data) {
                if (data.result === 'success' && data.conversion_rates) {
                    var fresh = {};
                    CURRENCY_OPTIONS.forEach(function (c) {
                        fresh[c] = data.conversion_rates[c] || DEFAULT_RATES[c];
                    });
                    state.rates = fresh;
                    state.timestamp = Date.now();
                    saveRates(fresh);
                    convertAllPrices(state);
                }
            })
            .catch(function () { /* use existing rates silently */ });
    }

    /* --- Currency --- */

    function getSelectedCurrency() {
        return localStorage.getItem(STORAGE_CURRENCY) || 'AED';
    }

    function setSelectedCurrency(code) {
        localStorage.setItem(STORAGE_CURRENCY, code);
    }

    /* --- Formatting --- */

    function formatPrice(gbpValue, currency, rates) {
        var converted = gbpValue * (rates[currency] || 1);
        var amount = converted.toFixed(2);
        // AED uses SVG span — add a small space after it for readability
        return currency === 'AED' ? SYMBOLS['AED'] + ' ' + amount : SYMBOLS[currency] + amount;
    }

    /* --- DOM conversion --- */

    function convertAllPrices(state) {
        var currency = getSelectedCurrency();
        var els = document.querySelectorAll('[data-price-gbp]');
        els.forEach(function (el) {
            var gbp = parseFloat(el.getAttribute('data-price-gbp'));
            if (isNaN(gbp)) return;
            el.innerHTML = formatPrice(gbp, currency, state.rates);
        });

        // Update add-to-bag buttons that embed price
        var addBtns = document.querySelectorAll('.btn-add-bag[data-unit-price-gbp]');
        addBtns.forEach(function (btn) {
            var unitGbp = parseFloat(btn.getAttribute('data-unit-price-gbp'));
            var qtyInput = document.querySelector('.qty-input');
            var qty = qtyInput ? parseInt(qtyInput.value) || 1 : 1;
            var total = unitGbp * qty;
            var converted = total * (state.rates[currency] || 1);
            var formatted = currency === 'AED' ? SYMBOLS['AED'] + ' ' + converted.toFixed(2) : SYMBOLS[currency] + converted.toFixed(2);
            btn.innerHTML = 'ADD TO BAG - ' + formatted;
        });
    }

    /* --- Dropdown init --- */

    function createChoicesInstance(select) {
        if (!window.Choices) return null;

        return new window.Choices(select, {
            searchEnabled: false,
            itemSelectText: '',
            shouldSort: false,
            allowHTML: true,
            position: 'bottom',
            callbackOnCreateTemplates: function (template, _, getClassNames) {
                function buildClassName(classNameList) {
                    return getClassNames(classNameList).join(' ');
                }

                function buildStateClass(condition, classNameList) {
                    return condition ? ' ' + buildClassName(classNameList) : '';
                }

                return {
                    item: function (config, data) {
                        var classNames = config.classNames;
                        var label = data.value === 'AED'
                            ? data.label + ' ' + AED_SVG
                            : data.label;
                        var itemClassName = buildClassName(classNames.item)
                            + buildStateClass(data.highlighted, classNames.highlightedState)
                            + buildStateClass(!data.placeholder, classNames.itemSelectable);

                        return template('<div class="' + itemClassName + '" data-item data-id="' + data.id + '" data-value="' + data.value + '">' + label + '</div>');
                    },
                    choice: function (config, data) {
                        var classNames = config.classNames;
                        var label = data.value === 'AED'
                            ? data.label + ' ' + AED_SVG
                            : data.label;
                        var choiceClassName = buildClassName(classNames.item)
                            + ' '
                            + buildClassName(classNames.itemChoice)
                            + buildStateClass(data.disabled, classNames.itemDisabled)
                            + buildStateClass(!data.disabled, classNames.itemSelectable);

                        return template('<div class="' + choiceClassName + '" data-select-text="" data-choice ' + (data.disabled ? 'data-choice-disabled aria-disabled="true"' : 'data-choice-selectable') + ' data-id="' + data.id + '" data-value="' + data.value + '" role="option">' + label + '</div>');
                    }
                };
            }
        });
    }

    function syncSelectControl(select, instance, value) {
        select.value = value;

        if (instance) {
            instance.setChoiceByValue(value);
        }
    }

    function initDropdowns(state) {
        var selects = Array.prototype.slice.call(document.querySelectorAll(SELECTOR));
        if (!selects.length) return [];

        var saved = getSelectedCurrency();
        var isSyncing = false;
        var controls = selects.map(function (select) {
            return {
                select: select,
                instance: createChoicesInstance(select)
            };
        });

        controls.forEach(function (control) {
            syncSelectControl(control.select, control.instance, saved);
        });

        controls.forEach(function (control) {
            control.select.addEventListener('change', function () {
                if (isSyncing) return;

                isSyncing = true;
                setSelectedCurrency(control.select.value);

                controls.forEach(function (otherControl) {
                    if (otherControl.select !== control.select) {
                        syncSelectControl(otherControl.select, otherControl.instance, control.select.value);
                    }
                });

                convertAllPrices(state);
                isSyncing = false;
            });
        });

        return controls;
    }

    /* --- Expose global helper for cart/checkout/product JS --- */

    window.CurrencyConverter = {
        formatPrice: function (gbpValue) {
            var state = loadRates();
            var currency = getSelectedCurrency();
            return formatPrice(gbpValue, currency, state.rates);
        },
        getSymbol: function () {
            return SYMBOLS[getSelectedCurrency()];
        },
        convertValue: function (gbpValue) {
            var state = loadRates();
            var currency = getSelectedCurrency();
            return (gbpValue * (state.rates[currency] || 1)).toFixed(2);
        },
        onChange: function (callback) {
            document.querySelectorAll(SELECTOR).forEach(function (select) {
                select.addEventListener('change', callback);
            });
        }
    };

    /* --- Boot --- */

    document.addEventListener('DOMContentLoaded', function () {
        var state = loadRates();

        // If first visit (no rates saved yet), save defaults
        if (state.timestamp === 0) {
            state.rates = DEFAULT_RATES;
            state.timestamp = Date.now();
            saveRates(DEFAULT_RATES);
        }

        initDropdowns(state);
        convertAllPrices(state);
        refreshRatesIfNeeded(state);
    });
})();
