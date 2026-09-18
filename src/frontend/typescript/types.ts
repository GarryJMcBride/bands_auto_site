/**
 * Adds static typing to JavaScript to catch errors during development.
 * Provides better tooling (autocomplete/refactoring) and enforces
 * data structures to ensure code reliability before it ever runs.
 */

import type { VALID_SERVICES } from './classes.js';

export type ValidService = (typeof VALID_SERVICES)[number];

export interface BookFormData {
  username: string;
  email: string;
  phone: string;
  registration: string;
  service: string;
}

export interface EnquiryFormData {
  username: string;
  email: string;
  phone: string;
  subject: string;
  message: string;
}

// Generic over the form's data shape so bookForm.ts and enquiryForm.ts share
// one type instead of each declaring its own near-identical result shape.
export interface ValidationResult<T> {
  valid: boolean;
  errors: Partial<Record<keyof T, string>>;
}
