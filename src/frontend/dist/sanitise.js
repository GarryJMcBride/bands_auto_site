import DOMPurify from 'dompurify';
/**
 * Sanitises user input for safe frontend rendering.
 *
 * DOMPurify removes all HTML and prevents XSS attacks.
 * We avoid extra regex stripping because it can break valid input
 * (names like O'Connor, emails) and does not reliably stop attacks.
 *
 * Backend should handle real security (SQL, shell, etc.). Shared by every
 * form's submit handler (bookForm.ts, enquiryForm.ts) so sanitisation
 * rules can't drift between forms.
 *
 * @param value - Raw user input
 * @returns Cleaned, safe string
 */
export function sanitiseString(value) {
    // Strip all HTML tags and attributes, leaving only text content
    const cleaned = DOMPurify.sanitize(value, { ALLOWED_TAGS: [] });
    return cleaned.trim().replace(/\$\{.*?\}/g, ''); // remove template patterns
}
