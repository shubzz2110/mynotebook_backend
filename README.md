# 📝 MyNotebook Backend  

A **Django + Django REST Framework (DRF)** powered backend for the **MyNotebook** application.  
This backend provides APIs for managing notes, including features like:  

- 🔐 User authentication (JWT)  
- 📝 Create, Read, Update, Delete (CRUD) notes  
- 📑 Filtering, searching, ordering, and pagination  
- 📌 Pin and favorite notes  
- 🤝 Shared notes support  
- ⚡ Production-ready with PostgreSQL, Gunicorn, and Whitenoise  

---

## 🚀 Tech Stack  

- **Backend Framework:** Django 5.x  
- **API Layer:** Django REST Framework  
- **Database:** PostgreSQL (default) / SQLite (for development)  
- **Authentication:** JWT (using `djangorestframework-simplejwt`)  
- **Filtering:** `django-filter`  
- **Static Files:** Whitenoise  

---

## 📂 Project Structure  

```
mynotebook_backend/
├── accounts/          # User accounts, authentication, permissions
├── notes/             # Notes app (CRUD, filters, favorites, pinned, etc.)
├── mynotebook_backend/ # Project settings and URLs
├── requirements.txt   # Dependencies
└── manage.py          # Django management CLI
```

---

## ⚙️ Prerequisites  

Make sure you have the following installed on your system:  

- [Python 3.10+](https://www.python.org/downloads/)  
- [pip](https://pip.pypa.io/en/stable/)  
- [PostgreSQL](https://www.postgresql.org/) (or use SQLite for development)  
- [Git](https://git-scm.com/)  

---

## 🛠️ Installation & Setup  

### 1️⃣ Clone the repository  
```bash
git clone https://github.com/your-username/mynotebook_backend.git
cd mynotebook_backend
```

### 2️⃣ Create and activate a virtual environment  
```bash
python -m venv venv
# On Linux / macOS
source venv/bin/activate
# On Windows
venv\Scripts\activate
```

### 3️⃣ Install dependencies  
```bash
pip install -r requirements.txt
```

### 4️⃣ Environment variables  
Create a `.env` file in the project root and configure it:  

```ini
DEBUG=True
SECRET_KEY=your-secret-key
ALLOWED_HOSTS=127.0.0.1,localhost

# Database (PostgreSQL)
DATABASE_URL=postgres://USER:PASSWORD@localhost:5432/mynotebook

# For SQLite (development only)
# DATABASE_URL=sqlite:///db.sqlite3

# JWT Settings
ACCESS_TOKEN_LIFETIME=3600
REFRESH_TOKEN_LIFETIME=86400
```

### 5️⃣ Apply migrations  
```bash
python manage.py migrate
```

### 6️⃣ Create a superuser  
```bash
python manage.py createsuperuser
```

### 7️⃣ Run the server  
```bash
python manage.py runserver
```

The backend API will be available at:  
👉 [http://127.0.0.1:8000/api/](http://127.0.0.1:8000/api/)  

---

## 📡 API Endpoints  

Some important endpoints:  

- **Authentication**
  - `POST /api/auth/login/` → Login with username/password  
  - `POST /api/auth/register/` → Register a new user  
  - `POST /api/auth/token/refresh/` → Refresh JWT token  

- **Notes**
  - `GET /api/notes/` → List notes (with pagination, search, filter)  
  - `POST /api/notes/` → Create a new note  
  - `GET /api/notes/{id}/` → Retrieve a note  
  - `PUT /api/notes/{id}/` → Update a note  
  - `DELETE /api/notes/{id}/` → Delete a note  

---

## 🧪 Running Tests  

```bash
pytest
```

or with Django’s test runner:  

```bash
python manage.py test
```

---

## 📦 Deployment  

For production:  

1. Set `DEBUG=False` in `.env`  
2. Configure `ALLOWED_HOSTS` properly  
3. Use **Gunicorn + Nginx** (recommended)  
4. Serve static files with **Whitenoise**  

Example (Gunicorn):  
```bash
gunicorn mynotebook_backend.wsgi:application --bind 0.0.0.0:8000
```

---

## 🤝 Contributing  

1. Fork the repository  
2. Create a feature branch (`git checkout -b feature/new-feature`)  
3. Commit changes (`git commit -m 'Add new feature'`)  
4. Push branch (`git push origin feature/new-feature`)  
5. Create a Pull Request  

---

## 📜 License  

This project is licensed under the **MIT License**.  
