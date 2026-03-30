Here are your **concise notes**:

## **Full Flow of Architecture**

* User submits form (HTML)
* JS `fetch()` > POST to backend
* Backend (Python/Node):
  * Validate/sanitize
  * Store in DB
  * Call Email API (Gmail/Outlook)
* Email sent + optional calendar booking

