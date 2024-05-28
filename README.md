# Tutor-Ai - NLP Based Toolkit for Every Teacher

Welcome to Tutor-Ai, a production-ready SaaS platform designed to help teachers efficiently manage class quizzes and grade student submissions using advanced OCR technology. This Django-based application leverages prompt templating for quizzes and integrates Google Vision to automate the evaluation of handwritten submissions. Hosted on Google Cloud, Tutor-Ai is built to scale and deliver a seamless experience for educators.

## Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Installation](#installation)
  - [Prerequisites](#prerequisites)
  - [Clone the Repository](#clone-the-repository)
  - [Set up the Environment](#set-up-the-environment)
  - [Migrate the Database](#migrate-the-database)
  - [Run the Development Server](#run-the-development-server)
  - [Access the Application](#access-the-application)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## Features

- **Prompt Templating for Quizzes:** Create, customize, and manage quizzes effortlessly with our intuitive prompt templating system.
- **OCR Grading with Google Vision:** Utilize Google Vision's OCR capabilities to automatically grade handwritten submissions, saving time and ensuring accuracy.
- **Secure and Scalable:** Hosted on Google Cloud to provide a robust, scalable, and secure platform for your classroom needs.
- **Student Submission Management:** Easily track and manage quiz submissions from students, with organized storage and retrieval.
- **User-Friendly Interface:** Designed with a focus on simplicity and usability, making it easy for teachers to navigate and use all features effectively.

## Tech Stack

- **Backend:** Django
- **Frontend:** HTML, CSS, JavaScript, Bootstrap
- **OCR:** Google Vision API
- **Hosting:** Google Cloud
- **Database:** SQLite (for development), Google Cloud SQL (for production)

## Installation

### Prerequisites

- Python >= 3.8
- pip (Python package installer)
- Google Cloud account
- Google Vision API key

### Clone the Repository

```sh
git clone https://github.com/hadithedetonator/tutor-ai-llm-toolkit.git
cd tutor-ai-llm-toolkit
```


## Set up the Environment

1. **Create a virtual environment:**

   ```sh
   python -m venv venv
   source venv/bin/activate   # On Windows use `venv\Scripts\activate`
   ```
2. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```
   
## Migrate the Database
```
python manage.py migrate app
python manage.py migrate accounts
python manage.py migrate
```

## Run the Development Server
```sh
python manage.py runserver
```

## Access the Application
Open your browser and navigate to http://localhost:8000.

## Usage

- **Register/Login:** Teachers can register or log in to their accounts.
- **Create Quizzes, Assignments, Exams:** Use the prompt templating system to create and manage quizzes, exams, and even a Mid Term /Final Exam.
- **Student Submissions:** Students can submit their handwritten answers.
- **Automatic Grading:** Google Vision OCR processes and grades the submissions.
- **Review and Remark:** Teachers can review graded submissions AI report and provide final marks.

## Contributing

Contributions are welcome! Follow these steps to contribute:

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

For any questions or discussions, you can contact Haris Ali Baig at [harisalibaig11@gmail.com](mailto:harisalibaig11@gmail.com).

## License

Distributed under the MIT License. See [LICENSE](LICENSE) for more information.

## Contact

Abdul Hadi - [harisalibaig11@gmail.com](mailto:harisalibaig11@gmail.com)

