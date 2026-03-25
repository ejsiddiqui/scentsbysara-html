/* =========================================================================
   Shared form validation for story/contact pages
   ========================================================================= */

document.addEventListener('DOMContentLoaded', () => {
    const forms = document.querySelectorAll('.js-validated-form');
    if (!forms.length) return;

    const messages = {
        required: 'This field is required.',
        name: 'Enter at least 2 characters for your name.',
        email: 'Enter a valid email address.',
        topic: 'Choose a topic.',
        story: 'Share at least 40 characters so we can understand your story.',
        contact: 'Please enter at least 20 characters.'
    };

    const isEmailValid = (value) => /^[^\\s@]+@[^\\s@]+\\.[^\\s@]+$/.test(value);

    const updateCounter = (textarea) => {
        const counter = document.querySelector(`[data-counter-for="${textarea.id}"]`);
        if (!counter) return;
        const maxLength = Number(textarea.getAttribute('maxlength')) || 1200;
        counter.textContent = `${textarea.value.length} / ${maxLength}`;
    };

    document.querySelectorAll('[data-counter-for]').forEach((counter) => {
        const textarea = document.getElementById(counter.getAttribute('data-counter-for'));
        if (textarea) {
            updateCounter(textarea);
            textarea.addEventListener('input', () => updateCounter(textarea));
        }
    });

    const clearErrors = (form) => {
        form.querySelectorAll('.field-error').forEach((errorNode) => {
            errorNode.textContent = '';
        });
        form.querySelectorAll('[aria-invalid="true"]').forEach((field) => {
            field.setAttribute('aria-invalid', 'false');
        });
    };

    const setError = (form, fieldName, field, message) => {
        const errorNode = form.querySelector(`.field-error[data-for="${fieldName}"]`);
        if (errorNode) errorNode.textContent = message;
        field.setAttribute('aria-invalid', 'true');
    };

    const validateForm = (form) => {
        const data = Object.fromEntries(new FormData(form).entries());
        const formType = form.getAttribute('data-form-type');
        let isValid = true;

        clearErrors(form);

        const nameField = form.querySelector('[name="name"]');
        const emailField = form.querySelector('[name="email"]');
        const topicField = form.querySelector('[name="topic"]');
        const messageField = form.querySelector('[name="message"]');

        if (nameField && (!data.name || data.name.trim().length < 2)) {
            setError(form, 'name', nameField, messages.name);
            isValid = false;
        }

        if (emailField && (!data.email || !isEmailValid(data.email.trim()))) {
            setError(form, 'email', emailField, messages.email);
            isValid = false;
        }

        if (topicField && !data.topic) {
            setError(form, 'topic', topicField, messages.topic);
            isValid = false;
        }

        if (messageField) {
            const minimum = formType === 'story' ? 40 : 20;
            if (!data.message || data.message.trim().length < minimum) {
                setError(form, 'message', messageField, formType === 'story' ? messages.story : messages.contact);
                isValid = false;
            }
        }

        return isValid;
    };

    forms.forEach((form) => {
        const status = form.querySelector('.form-status');

        form.addEventListener('submit', (event) => {
            event.preventDefault();
            if (status) {
                status.textContent = '';
                status.classList.remove('is-success', 'is-error');
            }

            const isValid = validateForm(form);
            if (!isValid) {
                if (status) {
                    status.textContent = 'Please correct the highlighted fields and try again.';
                    status.classList.add('is-error');
                }
                const firstInvalid = form.querySelector('[aria-invalid="true"]');
                if (firstInvalid) firstInvalid.focus();
                return;
            }

            form.reset();
            form.querySelectorAll('[data-counter-for]').forEach((counter) => {
                const targetId = counter.getAttribute('data-counter-for');
                const target = document.getElementById(targetId);
                if (target) updateCounter(target);
            });
            clearErrors(form);

            if (status) {
                status.textContent = 'Thank you. Your message has been received.';
                status.classList.add('is-success');
            }
        });
    });
});
