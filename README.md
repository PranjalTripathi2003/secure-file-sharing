# Secure File Sharing System - Backend Assessment for EZ Works

This project demonstrates my backend development skills and understanding of Flask, focusing on building a secure file-sharing system. It serves as a **proof of work** for the backend engineer position at EZ Works and highlights the core functionalities required for such a system.

## Core Features

* **User Authentication:** Secure signup and login for two user types: Ops Users and Client Users.
* **File Upload (Ops Users):** Ops Users can upload files of specific types (pptx, docx, xlsx).
* **Secure File Download (Client Users):** Client Users can download files using encrypted, time-limited URLs.
* **File Listing (Client Users):** Client Users can view a list of available files with download links.
* **Email Verification (Client Users):** Client Users must verify their email addresses before accessing certain features.

## Technologies Used

* **Framework:** Flask (Python)
* **Database:** SQLite
* **Other Libraries:** Flask-SQLAlchemy, Flask-Mail, itsdangerous, werkzeug

## Project Status

This project is a **work in progress**, primarily focusing on demonstrating core backend functionalities.  

## Areas for Further Implementation

* **Robust Authentication:** Implement a more sophisticated authentication mechanism (e.g., JWTs or sessions) to manage user sessions and permissions effectively.
* **Comprehensive Error Handling:** Add more detailed error handling and informative error messages to improve the user experience and facilitate debugging.
* **Enhanced Input Validation:** Implement stricter input validation to prevent potential security vulnerabilities and ensure data integrity.
* **Thorough Testing:** Write unit tests and integration tests to verify the correctness and robustness of the application.
* **Production-Ready Deployment:** Explore deployment strategies for a production environment, considering scalability, security, and database choices.

## Setup and Running (for demonstration purposes)

1. **Clone the repository:** `git clone https://github.com/PranjalTripathi2003/secure-file-sharing`
2. **Install dependencies:** `pip install -r requirements.txt`
3. **Set up the database:** 
    * Create the SQLite database: `flask db init`
    * Generate the database tables: `flask db migrate`
    * Apply the migrations: `flask db upgrade`
4. **Run the application:** `flask run` (or `python main.py`)

## API Endpoints

* **`/signup` (POST):** Registers a new user.
* **`/confirm/<token>` (GET):** Confirms a user's email address.
* **`/login` (POST):** Authenticates a user and returns a token.
* **`/upload` (POST):** Allows Ops Users to upload files.
* **`/download/<token>` (GET):** Provides a secure download link for a file.
* **`/files` (GET):** Lists all uploaded files for Client Users.

## Disclaimer

This project was developed as a backend assessment for EZ Works. While it demonstrates core functionalities, it's not a fully production-ready application and would require further development and refinement before deployment.
