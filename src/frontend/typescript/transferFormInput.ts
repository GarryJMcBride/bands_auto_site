import DOMPurify from "dompurify";

import type { QuoteFormData } from "./types";
import type { ValidationResult } from "./types";
import { VALID_SERVICES } from "./classes";

// ---- Sanitisation --------------------------------------------------

/**
 * Sanitises user input for safe frontend rendering.
 *
 * DOMPurify removes all HTML and prevents XSS attacks.
 * We avoid extra regex stripping because it can break valid input
 * (names like O'Connor, emails) and does not reliably stop attacks.
 *
 * Backend should handle real security (SQL, shell, etc.).
 *
 * @param value - Raw user input
 * @returns Cleaned, safe string
 */
function sanitiseString(value: string): string {
  // Strip all HTML tags and attributes, leaving only text content
  const cleaned = DOMPurify.sanitize(value, { ALLOWED_TAGS: [] });
  return cleaned
    .trim()
    .replace(/\$\{.*?\}/g, ""); // remove template patterns
}

// ---- Validation --------------------------------------------------

type ValidService = (typeof VALID_SERVICES)[number];

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
function validateFormData(data: QuoteFormData): ValidationResult {
  const errors: Partial<Record<keyof QuoteFormData, string>> = {};

  // Name: Letters, spaces, hyphens, apostrophes only
  if (!data.username) {
    errors.username = "Name is required.";
  } else if (!/^[a-zA-Z\s'\-]{2,64}$/.test(data.username)) {
    errors.username = "Name must be 2-64 characters and contain only letters, spaces, hyphens, or apostrophes.";
  }

  // Email: standard format check
  if (!data.email) {
    errors.email = "Email address is required.";
  } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(data.email)) {
    errors.email = "Please enter a valid email address.";
  }

   // Phone: digits, spaces, +, (), - only; 7–15 digits
   if (!data.phone) {
    errors.phone = "Phone number is required.";
  } else if (!/^\+?[\d\s\-()]{7,20}$/.test(data.phone)) {
    errors.phone = "Please enter a valid phone number.";
  }

  // Service: must be one of the predefined options
  if (!data.service) {
    errors.service = "Please select a service.";
  } else if (!isValidService(data.service)) {
    errors.service = "Selected service is not valid.";
  }

  return {
    valid: Object.keys(errors).length === 0, errors };
}

// ---- Form Handler --------------------------------------------------

/**
 * Handles the submission of the quote form.
 * Prevents default form submission, sanitises and validates the input,
 * and calls display errors if not valid.
 * 
 * @param event The submit event.
 */
function handleQuoteFormSubmit(event: SubmitEvent): void {
  event.preventDefault(); // Prevent default POST / page reload

  // Get form data
  const form = event.target as HTMLFormElement;

  // Read raw values - Assumes the element always exists, they will as user must fill them in to submit
  const rawData: QuoteFormData = {
    username: (form.elements.namedItem("username") as HTMLInputElement).value,
    email: (form.elements.namedItem("email") as HTMLInputElement).value,
    phone: (form.elements.namedItem("phone") as HTMLInputElement).value,
    service: (form.elements.namedItem("service") as HTMLSelectElement).value,
  }

  // Santise first, then validate the cleaned data
  const sanitisedData: QuoteFormData = {
    username: sanitiseString(rawData.username),
    email: sanitiseString(rawData.email),
    phone: sanitiseString(rawData.phone),
    service: sanitiseString(rawData.service),
  };

  // Validate the sanitised data
  const { valid, errors } = validateFormData(sanitisedData);
  
  // If not valid, show errors and stop submission
  if (!valid) {
    displayErrors(errors, form);
    return;
  }

  // If valid, clear any previous errors and submit the data
  clearErrors(form);
  submitQuoteData(sanitisedData);
}

// ---- Error Display --------------------------------------------------

/**
 * Clears all existing error messages from the form and resets input states.
 * This is called before displaying new errors to ensure the user sees only current issues.
 * Add CSS class "form-error-message" to style error messages (e.g., red text, smaller font).
 * 
 * @param errors 
 * @param form 
 */
function displayErrors(errors: Partial<Record<keyof QuoteFormData, string>>, form: HTMLFormElement): void {
  // Clear previous errors first
  clearErrors(form);

  // Display new errors next to the relevant input fields and mark them as invalid for accessibility
  for (const [field, message] of Object.entries(errors)) {
    // Find the input element by name
    const input = form.elements.namedItem(field) as HTMLElement | null;
    if (!input) continue;

    // Create an error message element and insert it after the input field
    const errorEL = document.createElement("span");
    errorEL.className = "form-error-message";
    errorEL.textContent = message ?? "";
    errorEL.setAttribute("role", "alert"); // Accessibility: Announce error messages to screen readers
    input.insertAdjacentElement("afterend", errorEL);
    input.setAttribute("aria-invalid", "true"); // Accessibility: Mark the input as invalid
  }
}

/**
 * Removes all error messages and resets input states in the form.
 * This is called before displaying new errors to ensure the user sees only current issues.
 * 
 * 
 * @param form 
 */
function clearErrors(form: HTMLFormElement): void {
  form.querySelectorAll(".form-error-message").forEach((el) => el.remove());
  form.querySelectorAll("[aria-invalid]").forEach((el) => el.removeAttribute("aria-invalid"));
}

// ---- Data Submission --------------------------------------------------

/**
 * Sends the validated quote data to the backend API using fetch.
 * Handles network errors and server responses, logging them for now.
 * In a real application, you would show success/error messages to the user instead of logging.
 * 
 * Note: The backend will also validate the data again for security, as frontend validation can be bypassed.
 * 
 * @param data 
 */
async function submitQuoteData(data: QuoteFormData): Promise<void> {
  try {
    // fetch is used here to send the data to the backend API
    const response = await fetch("/api/quote", { // TODO: FASTAPI endpoint here
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data),
    });

    // Check if the response is successful (status code 2xx)
    if (!response.ok) {
      throw new Error(`Server error: ${response.status}`);
    }

    // For demonstration, we log the response, show user a message instead
    console.log("Quote request submitted successfully:", await response.json());
    // TODO: Show success message to user, reset form, etc.

  // Catch any network or server errors and log them. Show user a generic error message instead of details for security.  
  } catch (err) {
    console.error("Error submitting quote request:", err);
    // TODO: Show generic error message to user
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
document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("quote-form") as HTMLFormElement | null;

  if (!form) {
    console.error("Quote form not found in the DOM.");
    return;
  }

  form.addEventListener("submit", handleQuoteFormSubmit);
});