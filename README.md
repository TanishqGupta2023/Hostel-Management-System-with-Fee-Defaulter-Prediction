# Hostel Management System with Fee Defaulter Prediction

A Django-based Hostel Management System integrated with a Machine Learning model to predict potential fee defaulters. The system provides separate panels for Admin and Students. Admin account is created manually by running a dedicated admin creation file.

---

## 🚀 Features

### 👨‍💼 Admin Panel

- **Manual admin creation using a separate admin setup file**
- Secure admin login
- Add, edit, and delete student records
- Add new hostel rooms and auto-assign rooms based on availability
- View and update student fee status
- Predict potential fee defaulters using ML (Random Forest Classifier)
- Send fee reminders to all fee defaulters at once
- View and manage student complaints
- Admin dashboard for full control

### 🎓 Student Panel
- Student login
- View profile and room details
- Submit complaints
- Pay hostel fees if marked unpaid

---

## 🤖 Machine Learning
- **Algorithm:** Random Forest Classifier
- **Libraries:** scikit-learn, joblib
- **Purpose:** Predict students likely to default on hostel fees

---

## 🛠 Technology Stack
- **Frontend:** HTML, CSS, Bootstrap
- **Backend:** Django (Python)
- **Machine Learning:** scikit-learn
- **Database:** SQLite3

---

## ⚙️ Installation & Setup

• Clone the repository using `git clone https://github.com/your-username/hostel-management-system.git` and move into the project folder using `cd hostel-management-system`  

• Create and activate a virtual environment using `python -m venv venv` and `venv\Scripts\activate`  

• Install required dependencies using `pip install -r requirements.txt`  

• Apply database migrations using `python manage.py migrate`  

• Run the admin creation file once to create the admin user (`python create_admin.py`)  

• Start the server using `python manage.py runserver` and open `http://127.0.0.1:8000/` in the browser

📊 Results

Efficient hostel management through centralized admin control

ML-based prediction helps identify high-risk fee defaulters early

Reduced manual workload for administrators

📌 Future Enhancements

Email/SMS notification system

Online payment gateway integration

Enhanced ML prediction features

👤 Author

Tanishq Gupta