Here are your **concise notes**:

## **Full Flow of Architecture**

* User submits form (HTML)
  - JavaScript validates input on the frontend first
  - Instant feedback without waiting for a server response
  - Reduces unnecessary requests
  - Bad input gets stopped before it reaches the backend, reducing server load and network traffic
  - Catches common mistakes
  - Honey pots used for bots
* JS `fetch()` > POST to backend
* JS removed the data from the browser so that the information is gone from the frontend
* Backend (Python/Node):
  - Server side validation is vital 
    - The backend is the single source of truth and cannot be bypassed by users
    - Ensures all entries meet your constraints (types, ranges, lengths) so your application doesn’t break or store invalid data
    - If frontend validation fails, or if an attacker bypasses it, the backend still protects you
  - Validate/sanitize
  - Store in DB
  - Call Email API (Gmail/Outlook)
  - Honey pots used for bots
* Email sent + optional calendar booking

