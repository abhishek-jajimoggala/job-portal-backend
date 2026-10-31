# 💼 Job Portal Application Using React.js and RESTful APIs

## 📌 Project Overview

The Job Portal Application is a full-stack web application developed using React.js, Python Flask, RESTful APIs, and MySQL. The main objective of this project is to connect job seekers with recruiters and simplify the recruitment process.

The application provides separate modules for Users and Administrators. Users can register, search for jobs, apply for suitable opportunities, and track their application status. Administrators can manage job postings, registered users, and candidate applications through an admin dashboard.

## 🚀 Key Features

### 👤 User Module
- User registration with Email OTP verification.
- Secure user login and logout.
- Forgot password and password reset using email OTP.
- User profile management.
- Upload profile pictures and resumes.
- Search jobs by title, skills, and company name.
- Filter jobs by location, job type, experience, work mode, and salary.
- Save jobs for future reference.
- Apply for available jobs.
- Track application status (Pending, Shortlisted, Rejected).

### 🛠️ Admin Module
- Admin login and authentication.
- Admin dashboard with application statistics.
- Add, update, and delete job postings.
- View registered users.
- Manage job applications.
- Shortlist or reject candidates.
- View shortlisted and rejected candidates.
- Manage jobs based on admin ownership.

### 📧 Email Notification Module
- Email OTP verification.
- Forgot password OTP notifications.
- New job posting notifications.
- Updated job notifications.
- Candidate shortlisted notifications.
- Candidate rejection notifications.
- Responsive HTML email templates.

## 💻 Technologies Used

### Frontend
- React.js
- JavaScript
- HTML5
- CSS3
- Bootstrap
- Bootstrap Icons
- Axios
- React Router
- React Toastify

### Backend
- Python
- Flask
- RESTful APIs
- Flask-Bcrypt
- Flask-CORS

### Database
- MySQL

### Tools
- Visual Studio Code
- Postman
- Git
- GitHub

## 🏗️ Project Architecture

The application follows a client-server architecture.

1. **Frontend:** React.js handles the user interface and user interactions.
2. **API Integration:** Axios sends HTTP requests to the backend.
3. **Backend:** Python Flask handles business logic and RESTful API requests.
4. **Database:** MySQL stores user details, job postings, and application information.
5. **Email Service:** Sends OTP verification and job-related email notifications.

## 🔄 Application Workflow

1. Users visit the Job Portal home page.
2. New users register and verify their email using OTP.
3. Users log in and complete their profiles.
4. Users search, filter, save, and apply for jobs.
5. Users track their applications through the My Applications section.
6. Administrators log in to the admin dashboard.
7. Administrators manage job postings and review applications.
8. Administrators shortlist or reject candidates.
9. Email notifications are sent to users based on relevant events.

## 📂 Project Structure

```text
JobPortal/
│
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── styles/
│   │   ├── App.jsx
│   │   └── main.jsx
│   ├── package.json
│   └── vite.config.js
│
├── backend/
│   ├── app.py
│   ├── routes/
│   ├── uploads/
│   ├── requirements.txt
│   └── config.py
│
└── README.md
```

*Note: Update the folder structure according to your actual repository.*

## ⚙️ Installation and Setup

### 1. Clone the Repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
```

### 2. Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

The frontend will run at:

```text
http://localhost:5173
```

### 3. Backend Setup

Open another terminal:

```bash
cd backend
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate the virtual environment on Windows:

```bash
venv\Scripts\activate
```

Install the required dependencies:

```bash
pip install -r requirements.txt
```

Start the Flask application:

```bash
python app.py
```

The backend will run at:

```text
http://localhost:5000
```

### 4. Database Configuration

1. Install and start MySQL.
2. Create a database named `jobportaldb`.
3. Configure the MySQL connection details in the backend configuration.
4. Create the required database tables.
5. Update the database credentials in your backend environment configuration.

### 5. Environment Configuration

Configure the required environment variables for:

- MySQL database credentials.
- Email SMTP settings.
- Email account credentials.
- Flask secret key.

**Important:** Never upload passwords, secret keys, database credentials, or email credentials to GitHub.

## 🔗 API Integration

The frontend communicates with the Flask backend using RESTful APIs.

Common HTTP methods used:

| Method | Purpose |
|---|---|
| GET | Retrieve jobs, users, and applications |
| POST | Register users, login, and apply for jobs |
| PUT | Update jobs and application statuses |
| DELETE | Delete job postings |

## 🎯 Project Objective

The main objective of this project is to provide a user-friendly platform where job seekers can easily find suitable job opportunities and recruiters can efficiently manage job postings and candidate applications.

## 👨‍💻 Author

**Abhishek**

Python Full Stack Trainee  
Codegnan IT Solutions

## ⭐ Conclusion

This project helped me gain practical experience in full-stack web development, React.js, Python Flask, RESTful API integration, MySQL database management, authentication, and email notification systems.
