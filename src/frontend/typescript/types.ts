/**
 * Adds static typing to JavaScript to catch errors during development.
 * Provides better tooling (autocomplete/refactoring) and enforces 
 * data structures to ensure code reliability before it ever runs.
 */

export interface QuoteFormData {
    username: string;
    email: string;
    phone: string;
    service: string;
}

export interface ValidationResult {
    valid: boolean;
    errors: Partial<Record<keyof QuoteFormData, string>>;
}