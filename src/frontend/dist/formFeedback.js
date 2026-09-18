/**
 * Shared form-feedback UI helpers: per-field validation errors and a
 * top-level submit success/error message. Generic over the form's data shape
 * so both bookForm.ts and enquiryForm.ts (two independent forms on the same
 * page) reuse the exact same DOM behaviour instead of each re-implementing it.
 *
 * The submit-message element id is derived from `form.id` (not a fixed
 * constant) specifically because two forms live on one page at once — a
 * shared fixed id would mean one form's success message could stomp on the
 * other's error message.
 */
/**
 * Displays validation errors next to their corresponding input fields.
 * Add CSS class "form-error-message" to style error messages (e.g., red text, smaller font).
 *
 * @param errors - Field name -> error message, from a form's validate*FormData()
 * @param form - The form the errors belong to
 */
export function displayErrors(errors, form) {
    // Clear previous errors first
    clearErrors(form);
    // Display new errors next to the relevant input fields and mark them as invalid for accessibility
    for (const [field, message] of Object.entries(errors)) {
        // Find the input element by name
        const input = form.elements.namedItem(field);
        if (!input)
            continue;
        // Create an error message element and insert it after the input field
        const errorEl = document.createElement('span');
        errorEl.className = 'form-error-message';
        errorEl.textContent = message ?? '';
        errorEl.setAttribute('role', 'alert'); // Accessibility: Announce error messages to screen readers
        input.insertAdjacentElement('afterend', errorEl);
        input.setAttribute('aria-invalid', 'true'); // Accessibility: Mark the input as invalid
    }
}
/**
 * Removes all error messages and resets input states in the form.
 *
 * @param form
 */
export function clearErrors(form) {
    form.querySelectorAll('.form-error-message').forEach((el) => el.remove());
    form.querySelectorAll('[aria-invalid]').forEach((el) => el.removeAttribute('aria-invalid'));
}
function submitMessageId(form) {
    return `${form.id}-submit-message`;
}
/**
 * Shows a success/error message immediately above the form, replacing any
 * previous one for that same form. Uses the same "form-success-message"/
 * "form-error-message" classes and position (immediately before the <form>)
 * as the server-rendered no-JS fallback banner in index.html, so both paths
 * look the same regardless of how they were reached.
 */
export function showSubmitMessage(form, type, message) {
    clearSubmitMessage(form);
    const messageEl = document.createElement('p');
    messageEl.id = submitMessageId(form);
    messageEl.className = type === 'success' ? 'form-success-message' : 'form-error-message';
    messageEl.textContent = message;
    messageEl.setAttribute('role', 'status');
    form.insertAdjacentElement('beforebegin', messageEl);
}
export function clearSubmitMessage(form) {
    document.getElementById(submitMessageId(form))?.remove();
}
