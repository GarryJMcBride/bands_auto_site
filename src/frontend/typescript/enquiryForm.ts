import type { EnquiryFormData, ValidationResult } from './types';
import { sanitiseString } from './sanitise.js';
import { displayErrors, clearErrors, showSubmitMessage } from './formFeedback.js';

// ---- Validation --------------------------------------------------

/**
 * Validates the enquiry form data against defined rules:
 * - Name: 2-64 chars, letters/spaces/hyphens/apostrophes only
 * - Email: standard format check
 * - Phone: digits, spaces, +, (), - only; 7–20 digits
 * - Subject: 2-128 characters
 * - Message: 2-2000 characters
 *
 * Mirrors bookForm.ts's validateBookFormData — kept as its own function
 * (not a shared generic validator) since the two forms' rules only overlap
 * on name/email/phone and diverge everywhere else (registration/service vs
 * subject/message), so a forced shared abstraction would buy little.
 *
 * @param data
 * @returns
 */
function validateEnquiryFormData(data: EnquiryFormData): ValidationResult<EnquiryFormData> {
  const errors: Partial<Record<keyof EnquiryFormData, string>> = {};

  // Name: Letters, spaces, hyphens, apostrophes only
  if (!data.username) {
    errors.username = 'Name is required.';
  } else if (!/^[a-zA-Z\s'\-]{2,64}$/.test(data.username)) {
    errors.username =
      'Name must be 2-64 characters and contain only letters, spaces, hyphens, or apostrophes.';
  }

  // Email: standard format check
  if (!data.email) {
    errors.email = 'Email address is required.';
  } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(data.email)) {
    errors.email = 'Please enter a valid email address.';
  }

  // Phone: digits, spaces, +, (), - only; 7–20 digits
  if (!data.phone) {
    errors.phone = 'Phone number is required.';
  } else if (!/^\+?[\d\s\-()]{7,20}$/.test(data.phone)) {
    errors.phone = 'Please enter a valid phone number.';
  }

  // Subject: short free text
  if (!data.subject) {
    errors.subject = 'Subject is required.';
  } else if (data.subject.length < 2 || data.subject.length > 128) {
    errors.subject = 'Subject must be 2-128 characters.';
  }

  // Message: longer free text
  if (!data.message) {
    errors.message = 'Message is required.';
  } else if (data.message.length < 2 || data.message.length > 2000) {
    errors.message = 'Message must be 2-2000 characters.';
  }

  return {
    valid: Object.keys(errors).length === 0,
    errors,
  };
}

// ---- Form Handler --------------------------------------------------

/**
 * Handles the submission of the enquiry form.
 * Prevents default form submission, sanitises and validates the input,
 * and calls display errors if not valid.
 *
 * @param event The submit event.
 */
function handleEnquiryFormSubmit(event: SubmitEvent): void {
  event.preventDefault(); // Prevent default POST / page reload

  const form = event.target as HTMLFormElement;

  // Read raw values - Assumes the element always exists, they will as user must fill them in to submit
  const rawData: EnquiryFormData = {
    username: (form.elements.namedItem('username') as HTMLInputElement).value,
    email: (form.elements.namedItem('email') as HTMLInputElement).value,
    phone: (form.elements.namedItem('phone') as HTMLInputElement).value,
    subject: (form.elements.namedItem('subject') as HTMLInputElement).value,
    message: (form.elements.namedItem('message') as HTMLTextAreaElement).value,
  };

  // Sanitise first, then validate the cleaned data
  const sanitisedData: EnquiryFormData = {
    username: sanitiseString(rawData.username),
    email: sanitiseString(rawData.email),
    phone: sanitiseString(rawData.phone),
    subject: sanitiseString(rawData.subject),
    message: sanitiseString(rawData.message),
  };

  // Validate the sanitised data
  const { valid, errors } = validateEnquiryFormData(sanitisedData);

  // If not valid, show errors and stop submission
  if (!valid) {
    displayErrors(errors, form);
    return;
  }

  // If valid, clear any previous errors and submit the data
  clearErrors(form);
  submitEnquiryData(sanitisedData, form);
}

// ---- Data Submission --------------------------------------------------

/**
 * Sends the validated enquiry data to the backend API using fetch.
 * Handles network errors and server responses, showing a message to the user either way.
 *
 * Note: The backend will also validate the data again for security, as frontend validation can be bypassed.
 *
 * @param data
 * @param form
 */
async function submitEnquiryData(data: EnquiryFormData, form: HTMLFormElement): Promise<void> {
  // Give immediate feedback that the click registered, rather than leaving the
  // form silent for the duration of the network round-trip.
  const submitButton = form.querySelector('button') as HTMLButtonElement | null;
  const buttonLabel = submitButton?.querySelector('.btn-title') ?? null;
  const originalLabel = buttonLabel?.textContent ?? null;

  if (submitButton) submitButton.disabled = true;
  if (buttonLabel) buttonLabel.textContent = 'Submitting…';

  try {
    const response = await fetch('/api/enquiry-javascript-pipeline', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    });

    if (!response.ok) {
      throw new Error(`Server error: ${response.status}`);
    }

    showSubmitMessage(form, 'success', 'Thanks! We will be in touch shortly.');
    form.reset(); // Data has served its purpose the moment the backend received it — don't linger.

    // Catch any network or server errors and log them. Show user a generic error message instead of details for security.
  } catch (err) {
    console.error('Error submitting enquiry:', err);
    showSubmitMessage(
      form,
      'error',
      'Sorry, something went wrong. Please check your details and try again.',
    );
  } finally {
    if (submitButton) submitButton.disabled = false;
    if (buttonLabel && originalLabel !== null) buttonLabel.textContent = originalLabel;
  }
}

// ---- Initialise --------------------------------------------------

/**
 * Initialises the form handling by adding an event listener to the form submit event.
 * Waits for the DOM to load before trying to access the form element.
 * If the form is not found, logs an error and does not add the event listener.
 */
document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('contact-form') as HTMLFormElement | null;

  if (!form) {
    console.error('Enquiry form not found in the DOM.');
    return;
  }

  form.addEventListener('submit', handleEnquiryFormSubmit);
});
