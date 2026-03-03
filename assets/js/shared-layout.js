/* =========================================================================
   SCENTS BY SARA - SHARED LAYOUT INJECTOR
   Injects shared header/footer/mobile menu partials before main.js bootstraps.
   ========================================================================= */

(function () {
    const placeholders = document.querySelectorAll('[data-shared-partial]');
    if (!placeholders.length) return;

    const partialCache = new Map();

    const loadPartial = (name) => {
        const path = `partials/${name}.html`;
        if (partialCache.has(path)) return partialCache.get(path);

        const request = new XMLHttpRequest();
        request.open('GET', path, false);
        request.send();

        if (request.status >= 200 && request.status < 300) {
            partialCache.set(path, request.responseText);
            return request.responseText;
        }

        partialCache.set(path, '');
        return '';
    };

    placeholders.forEach((placeholder) => {
        const partialName = placeholder.getAttribute('data-shared-partial');
        if (!partialName) return;

        const markup = loadPartial(partialName);
        if (!markup) return;

        const temp = document.createElement('div');
        temp.innerHTML = markup;

        const fragment = document.createDocumentFragment();
        while (temp.firstChild) {
            fragment.appendChild(temp.firstChild);
        }

        placeholder.replaceWith(fragment);
    });
})();
