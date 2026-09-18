import type { BookFormData, ValidationResult, ValidService } from './types';
import { VALID_SERVICES } from './classes.js';
import { sanitiseString } from './sanitise.js';
import { displayErrors, clearErrors, showSubmitMessage } from './formFeedback.js';

// ---- Validation --------------------------------------------------

/**
 * Checks if the provided service is a valid service.
 * VALID_SERVICES is defined in classes.ts and contains the list of valid options.
 *
 * @param service - The service to validate.
 * @returns True if the service is valid, false otherwise.
 */
function isValidService(value: string): value is ValidService {
  return (VALID_SERVICES as readonly string[]).includes(value);
}

/**
 * Validates the form data against defined rules:
 * - Name: 2-64 chars, letters/spaces/hyphens/apostrophes only
 * - Email: standard format check
 * - Phone: digits, spaces, +, (), - only; 7–15 digits
 * - Service: must be one of the predefined options
 *
 * Signals to the user that they need to fill in these fields before
 * submission, and prevents invalid data from being sent to the backend.
 *
 * @param data
 * @returns
 */
function validateBookFormData(data: BookFormData): ValidationResult<BookFormData> {
  const errors: Partial<Record<keyof BookFormData, string>> = {};

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

  // Phone: digits, spaces, +, (), - only; 7–15 digits
  if (!data.phone) {
    errors.phone = 'Phone number is required.';
  } else if (!/^\+?[\d\s\-()]{7,20}$/.test(data.phone)) {
    errors.phone = 'Please enter a valid phone number.';
  }

  // Vehicle Registration: letters, digits, spaces, (), - only; 2–20 characters
  if (!data.registration) {
    errors.registration = 'Vehicle registration is required.';
  } else if (!/^[a-zA-Z0-9\s\-()]{2,20}$/.test(data.registration)) {
    errors.registration = 'Please enter a valid vehicle registration.';
  }

  // Service: must be one of the predefined options
  if (!data.service) {
    errors.service = 'Please select a service.';
  } else if (!isValidService(data.service)) {
    errors.service = 'Selected service is not valid.';
  }

  return {
    valid: Object.keys(errors).length === 0,
    errors,
  };
}

// ---- Form Handler --------------------------------------------------

/**
 * Handles the submission of the booking form.
 * Prevents default form submission, sanitises and validates the input,
 * and calls display errors if not valid.
 *
 * @param event The submit event.
 */
function handleBookFormSubmit(event: SubmitEvent): void {
  event.preventDefault(); // Prevent default POST / page reload

  // Get form data
  const form = event.target as HTMLFormElement;

  // Read raw values - Assumes the element always exists, they will as user must fill them in to submit
  const rawData: BookFormData = {
    username: (form.elements.namedItem('username') as HTMLInputElement).value,
    email: (form.elements.namedItem('email') as HTMLInputElement).value,
    phone: (form.elements.namedItem('phone') as HTMLInputElement).value,
    registration: (form.elements.namedItem('registration') as HTMLInputElement).value,
    service: (form.elements.namedItem('service') as HTMLSelectElement).value,
  };

  // Santise first, then validate the cleaned data
  const sanitisedData: BookFormData = {
    username: sanitiseString(rawData.username),
    email: sanitiseString(rawData.email),
    phone: sanitiseString(rawData.phone),
    registration: sanitiseString(rawData.registration),
    service: sanitiseString(rawData.service),
  };

  // Validate the sanitised data
  const { valid, errors } = validateBookFormData(sanitisedData);

  // If not valid, show errors and stop submission
  if (!valid) {
    displayErrors(errors, form);
    return;
  }

  // If valid, clear any previous errors and submit the data
  clearErrors(form);
  submitBookData(sanitisedData, form);
}

// ---- Data Submission --------------------------------------------------

/**
 * Sends the validated booking data to the backend API using fetch.
 * Handles network errors and server responses, showing a message to the user either way.
 *
 * Note: The backend will also validate the data again for security, as frontend validation can be bypassed.
 *
 * @param data
 * @param form
 */
async function submitBookData(data: BookFormData, form: HTMLFormElement): Promise<void> {
  // Give immediate feedback that the click registered, rather than leaving the
  // form silent for the duration of the network round-trip.
  const submitButton = form.querySelector('button') as HTMLButtonElement | null;
  const buttonLabel = submitButton?.querySelector('.btn-title') ?? null;
  const originalLabel = buttonLabel?.textContent ?? null;

  if (submitButton) submitButton.disabled = true;
  if (buttonLabel) buttonLabel.textContent = 'Submitting…';

  try {
    // fetch is used here to send the data to the backend API
    const response = await fetch('/api/book-javascript-pipeline', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    });

    // Check if the response is successful (status code 2xx)
    if (!response.ok) {
      throw new Error(`Server error: ${response.status}`);
    }

    showSubmitMessage(form, 'success', 'Thanks! We will be in touch shortly.');
    form.reset(); // Data has served its purpose the moment the backend received it — don't linger.

    // Catch any network or server errors and log them. Show user a generic error message instead of details for security.
  } catch (err) {
    console.error('Error submitting booking request:', err);
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
 *
 * This ensures that the form handling code only runs when the relevant elements are present in the DOM, preventing errors and improving user experience.
 */
document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('book-form') as HTMLFormElement | null;

  if (!form) {
    console.error('Booking form not found in the DOM.');
    return;
  }

  form.addEventListener('submit', handleBookFormSubmit);
});
