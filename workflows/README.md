# 📚 PsychBuddy Architecture & Workflow Documentation

Welcome to the comprehensive technical documentation and workflow specifications for **PsychBuddy**.

---

## 📑 Workflow Index & Navigation

| Document | Purpose | Key Contents |
| :--- | :--- | :--- |
| 🎨 **[Frontend Workflow](file:///D:/PROJECT_S/PsychBuddy/workflows/FRONTEND_WORKFLOW.md)** | User Interface, Templates & Client Interaction | DTL rendering pipeline, user navigation journeys, sound & video streaming, yoga & meditation, wellness progress journal, template directory map |
| ⚙️ **[Backend Workflow](file:///D:/PROJECT_S/PsychBuddy/workflows/BACKEND_WORKFLOW.md)** | Application Logic, APIs & Services | Request-response lifecycle, URL routing, email OTP protocol, NewsAPI, python-docx report generation, admin management, full routing directory |
| 🗄️ **[Database Workflow](file:///D:/PROJECT_S/PsychBuddy/workflows/DATABASE_WORKFLOW.md)** | Schema, Relational Models & Storage | Complete Mermaid ER diagram, table schemas, migration & seeding pipeline, safe parameterized SQL queries, relational joins |
| 🔄 **[System Integration Workflow](file:///D:/PROJECT_S/PsychBuddy/workflows/SYSTEM_INTEGRATION_WORKFLOW.md)** | End-to-End Orchestration & Operations | Multi-tier architectural topology, startup sequences, core operational scenarios, production deployment checklist |

---

## ⚡ Quick Operational Commands

### 1. Run Database Migration & Seeding
```powershell
# From the project directory:
python manage.py seed_db

# Or with complete reset:
python manage.py seed_db --reset
```

### 2. Start Application Server
```powershell
python manage.py runserver 0.0.0.0:8000
```

### 3. Access Live Application
- **Frontend / Homepage:** [http://localhost:8000/](http://localhost:8000/)
- **Admin Control Panel:** [http://localhost:8000/adminlogin](http://localhost:8000/adminlogin) *(Default: `admin` / `admin`)*
