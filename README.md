# TaskForge - Premium Job Portal

A modern, high-performance web job application portal built with Django, SQLite, and Bootstrap 5. TaskForge features a scroll-driven SaaS landing page, dynamic search/filtering for listings, candidate application tracking, resume/cover letter uploads, and real-time external job imports via third-party API.

## Features

### For Job Seekers
*   **Registration & Profiles**: Create accounts dedicated to job seekers.
*   **Dynamic Search & Filtering**: Filter jobs by category, location, and keywords instantly.
*   **Direct Application**: Apply directly inside the portal with custom cover letters and resume uploads (PDF/DOCX).
*   **Modern Job Feed**: Browse local opportunities alongside imported external jobs.

### For Employers
*   **Job Listing Management**: Post, update, and manage job openings.
*   **Candidate Pipeline**: View incoming job applications, download candidate resumes, read cover letters, and track statuses from the employer dashboard.
*   **Clean Authorization**: Employers are automatically redirected to their dedicated dashboard.

### API Integration (Admins Only)
*   **External Sync**: Admin dashboard features a button to sync live English listings from **The Muse API**.
*   **Clean Database Sync**: Automatic cleanup of stale external records on sync, ensuring only active, deduplicated listings populate the system.

### Visual Architecture
*   **SaaS Landing Page**: Fully immersive, animated dark-mode landing page designed for premium aesthetics (visible to logged-out users).
*   **Instant Access**: Logged-in users bypass the landing page entirely and redirect straight to the main job feed or employer dashboard.

---

## Installation & Setup

1.  **Clone the Repository**:
    ```bash
    git clone <repository_url>
    cd TaskForge-Python
    ```

2.  **Set Up Virtual Environment**:
    ```bash
    python -m venv venv
    venv\Scripts\activate  # On Windows
    source venv/bin/activate  # On macOS/Linux
    ```

3.  **Install Dependencies**:
    ```bash
    pip install django requests
    ```

4.  **Run Migrations**:
    ```bash
    python manage.py migrate
    ```

5.  **Create a Superuser (Admin)**:
    ```bash
    python manage.py createsuperuser
    ```

6.  **Run Development Server**:
    ```bash
    python manage.py runserver
    ```

7.  **Access the Application**:
    *   Main App: `http://127.0.0.1:8000/`
    *   Django Admin Interface: `http://127.0.0.1:8000/admin/`

---

## Folder Structure

*   `job_portal/`: Project settings and routing configuration.
*   `jobs/`: Main application directory containing forms, views, models, and URLs.
*   `media/`: Media folder handling candidate resume uploads.
*   `templates/`: HTML5 responsive templates styled with vanilla CSS and Bootstrap 5.
