# 💊 Pharmacy Management System

A **full-stack Pharmacy Management System** built with **FastAPI**, **SQLite/MongoDB**, and a modern interactive **HTML/JS frontend**.  
The system helps pharmacies manage medicines, sales, and inventory efficiently.

---

## 🚀 Features
- 📦 **Medicine Management** – Add, edit, delete medicines with stock tracking.  
- 🔍 **Advanced Search** – Filter by name, manufacturer, price, or expired status.  
- 🛒 **Sales & Billing** – Record sales with automatic stock deduction.  
- ⚡ **Dual Database Support** – Easily switch between **SQLite** and **MongoDB**.  
- 🎨 **Modern UI** – Responsive, interactive design with Bootstrap/JS.  
- 🔒 **Secure Config** – Environment variables for DB credentials.  

---

## 🛠️ Tech Stack
- **Backend:** FastAPI, Uvicorn  
- **Frontend:** HTML, Bootstrap, JavaScript  
- **Database:** SQLite (default) / MongoDB (switchable)  
- **ORM/Driver:** SQLAlchemy & PyMongo  

---

## 📂 Project Structure
```
pharmacy_system/
│── app/
│   ├── core/              # Configurations
│   ├── db/                # Database sessions (SQL & Mongo)
│   ├── models/            # SQLAlchemy models
│   ├── routers/           # FastAPI routers (medicines, sales, home)
│   ├── schemas/           # Pydantic schemas
│   ├── services/          # Business logic
│   ├── templates/         # HTML files (frontend)
│   ├── static/            # CSS, JS, Images
│── pharmacy.db            # SQLite DB (if using SQL)
│── .env                   # Environment config
│── requirements.txt       # Python dependencies
│── run.sh / run.ps1       # Start scripts
```

---

## ⚙️ Setup Instructions

### 1️⃣ Clone the repo
```bash
git clone https://github.com/aliendevit/pharmacy_system.git
cd pharmacy_system
```

### 2️⃣ Create a virtual environment
```bash
python -m venv .venv
source .venv/bin/activate   # Linux/Mac
.venv\Scripts\activate      # Windows
```

### 3️⃣ Install dependencies
```bash
pip install -r requirements.txt
```

### 4️⃣ Configure environment
Copy `.env.example` → `.env` and set your DB:
```env
DB_TYPE=sqlite   # or "mongo"
DATABASE_URL=sqlite:///./pharmacy.db
MONGO_URI=mongodb://localhost:27017
```

### 5️⃣ Run the app
```bash
uvicorn app.main:app --reload
```
App runs at 👉 `http://127.0.0.1:8000`

---

## 🔄 Switching Between SQLite & MongoDB
1. Open `.env`.  
2. Change:
   ```env
   DB_TYPE=sqlite   # for SQLite
   DB_TYPE=mongo    # for MongoDB
   ```
3. Restart the app.  

---

## 👨‍💻 Author
- **Ali Ali**  
  💼 AI & Software Developer | 🚑 Hospitalist | Future MBA Candidate  
  📧 ali.iteng@outlook.com  
  🌍 Damascus, Syria  
