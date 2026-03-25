const selector = '[data-accordion][data-accordion-group]';
const desktopBreakpoint = window.matchMedia('(min-width: 990px)');

function closeOthers(activeDetails) {
  const groupName = activeDetails.dataset.accordionGroup;

  if (!groupName || !activeDetails.open) {
    return;
  }

  document.querySelectorAll(`${selector}[data-accordion-group="${groupName}"]`).forEach((details) => {
    if (details !== activeDetails) {
      details.open = false;
    }
  });
}

function syncAccordionState() {
  document.querySelectorAll(selector).forEach((details) => {
    details.open = desktopBreakpoint.matches;
  });
}

function initAccordion(details) {
  if (details.dataset.accordionInitialized === 'true') {
    return;
  }

  details.dataset.accordionInitialized = 'true';
  details.addEventListener('toggle', () => closeOthers(details));
}

document.querySelectorAll(selector).forEach(initAccordion);
syncAccordionState();

if (typeof desktopBreakpoint.addEventListener === 'function') {
  desktopBreakpoint.addEventListener('change', syncAccordionState);
} else {
  desktopBreakpoint.addListener(syncAccordionState);
}

export {};
