 Budget Tracker – ALX Capstone Project

A personal finance management API built with Django REST Framework (DRF).
This project is my ALX Backend Engineering Capstone, designed to demonstrate skills in building secure, scalable, and well-documented backend systems.


Project Overview

Budget Tracker helps users:

* Register and authenticate securely
* Create budgets across categories (e.g., Rent, Food, Savings)
* Record transactions (income & expenses)
* View reports and summaries to understand spending habits
* Ensure data privacy → each user only sees their own budgets and expenses

 Tech Stack

* Framework: Django, Django REST Framework
* Database: SQLite 
* Authentication: DRF Token Authentication
* Version Control: Git and GitHub


 Installation and Setup

1. Clone repository

```bash
git clone https://github.com/Mulkah-dev/budget_tracker.git
cd budget_tracker

 2. Create and activate virtual environment

bash
python -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate      # Windows
```

3. Install dependencies
bash
pip install -r requirements.txt


 4. Run migrations

bash
python manage.py migrate


 5. Create superuser (admin)

```bash
python manage.py createsuperuser
```

### 6. Run development server

```bash
python manage.py runserver
```

API will be live at:
[http://127.0.0.1:8000/](http://127.0.0.1:8000/)

---

## 📌 API Endpoints

### Authentication

* POST /register/ → Register a new user
* POST /login/ → Obtain token for authentication

### Budgets

* GET /budgets/ → List user’s budgets
* POST /budgets/ → Create a budget
* GET /budgets/<id>/ → Retrieve budget
* PUT /budgets/<id>/ → Update budget
* DELETE /budgets/<id>/ → Delete budget

### Categories

* GET /categories/ → List categories
* POST /categories/ → Create category

### Transactions

* GET /transactions/ → List transactions
* POST /transactions/ → Create transaction

---

## 🧪 Running Tests

```bash
python manage.py test
```

---

## 📂 Project Structure

```
budget_tracker/
│
├── accounts/         # Handles user authentication
├── budgets/          # Budget creation and management
├── categories/       # Budget categories
├── transactions/     # Income and expenses
├── budget_tracker/   # Project-level settings
└── README.md
```

