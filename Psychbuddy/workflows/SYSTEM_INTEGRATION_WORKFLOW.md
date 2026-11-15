# 🔄 System Integration & End-to-End Operational Workflow

This document details the complete end-to-end operational architecture connecting the **Frontend (Client/Templates)**, **Backend (Django/Python)**, and **Database (MySQL/PyMySQL)** into a cohesive mental health companion platform.

---

## 1. 🏗️ Multi-Tier Architecture Overview

```mermaid
flowchart TD
    subgraph Tier1["1. Presentation Tier (Client / Frontend)"]
        Browser["User Browser (Desktop / Mobile)"]
        Templates["Django Templates (HTML5 + CSS3 + Vanilla JS)"]
        MediaPlayers["HTML5 Video / Audio Players"]
    end

    subgraph Tier2["2. Application Tier (Django Backend)"]
        WSGI["WSGI / ASGI Gateway"]
        Router["URL Routing Engine (psychbuddy.urls)"]
        Views["Business Logic & Views (psychbuddy.views)"]
        SessionStore["Session & Auth Engine"]
    end

    subgraph Tier3["3. Service & Integration Tier"]
        DotEnv[".env Configuration (python-dotenv)"]
        SMTPService["Gmail SMTP / Yagmail Mailer"]
        NewsAPIService["NewsAPI External Client"]
        DocxService["python-docx Report Generator"]
        EmotionService["Emotion Detection Module"]
    end

    subgraph Tier4["4. Persistence & File Storage Tier"]
        MySQL[("MySQL Database (psychbuddy)")]
        SQLite[("SQLite Session DB (db.sqlite3)")]
        StaticStorage["Static Media Storage (/static/)"]
        UserLogsStorage["Exported Document Storage (/userlogs/)"]
    end

    Browser <--> Templates
    Browser <--> MediaPlayers
    Templates <--> WSGI
    WSGI <--> Router
    Router <--> Views
    Views <--> SessionStore
    DotEnv -.-> Views
    Views <--> SMTPService
    Views <--> NewsAPIService
    Views <--> DocxService
    Views <--> EmotionService
    Views <--> MySQL
    SessionStore <--> SQLite
    MediaPlayers <--> StaticStorage
    DocxService --> UserLogsStorage
```

---

## 2. 🚀 System Startup & Initialization Sequence

The following diagram illustrates the proper order of operations to launch the entire stack:

```mermaid
sequenceDiagram
    autonumber
    actor Dev as Developer / Operator
    participant MySQL as MySQL Daemon (Port 3306)
    participant Migrator as Database Migrator (db_migrator.py)
    participant Django as Django Server (Port 8000)
    actor User as End User

    Dev->>MySQL: Start mysqld (C:\xampp\mysql\bin\mysqld.exe)
    MySQL-->>Dev: Port 3306 listening
    Dev->>Migrator: Execute `python manage.py seed_db` (or `python migrate_db.py`)
    Migrator->>MySQL: Verify database & create 14 tables
    Migrator->>MySQL: Seed sample psychiatrists, audio, books, yoga, sessions
    Migrator-->>Dev: Confirmation: All tables ready
    Dev->>Django: Run `python manage.py runserver 0.0.0.0:8000`
    Django-->>Dev: StatReloader active, Listening on http://0.0.0.0:8000/
    User->>Django: GET http://localhost:8000/
    Django->>MySQL: Fetch initial data
    Django-->>User: Render landing page (HTTP 200)
```

---

## 3. 🎯 Core End-to-End Operational Scenarios

### 3.1 Scenario A: Patient Finds a Psychiatrist and Books an Appointment

```mermaid
sequenceDiagram
    autonumber
    actor Patient
    participant Browser
    participant Django as Django Backend
    participant DB as MySQL Database
    participant SMTP as Yagmail SMTP
    actor Doctor as Psychiatrist

    Patient->>Browser: Opens /psychiatrist
    Browser->>Django: GET /psychiatrist
    Django->>DB: SELECT * FROM psychiatrist_dir
    DB-->>Django: Returns 10 doctor profiles
    Django-->>Browser: Renders doctor cards with photos & ratings
    Patient->>Browser: Selects "Dr. Harish Shetty" -> Clicks "Book Appointment"
    Browser->>Django: POST /psychinfo (psychname="Dr. Harish Shetty", date="2026-11-20", time="14:00")
    Django->>DB: SELECT email FROM psychiatrist_dir WHERE psychname="Dr. Harish Shetty"
    Django->>DB: SELECT * FROM users WHERE login_status = 1
    Django->>SMTP: Dispatches appointment booking notification
    SMTP-->>Doctor: Delivers email notification to dr.shetty@psychbuddy.com
    Django-->>Browser: Alert: "Appointment Request Submitted!"
```

---

### 3.2 Scenario B: Multimedia Streaming Workflow (Audio & Video)

```mermaid
flowchart TD
    User["User in Browser"] --> Choice{"Select Media Type"}

    Choice -->|Sound Therapy| AudioReq["Request /relaxation"]
    AudioReq --> AudioDB["SELECT * FROM sound_therapy"]
    AudioDB --> AudioCards["Render Audio Player Cards"]
    AudioCards --> AudioStream["Stream /static/audio/*.mp3 via HTTP 206 Partial Content"]
    AudioStream --> AudioPlay["Continuous ambient loop playback in browser"]

    Choice -->|Video Therapy| VideoReq["Request /sessions or category (e.g., /coupletherapy)"]
    VideoReq --> VideoDB["SELECT * FROM sessions WHERE sess_category = 'Couple Therapy'"]
    VideoDB --> VideoCards["Render sessionpage.html with Video Element"]
    VideoCards --> VideoStream["Stream /static/sessions/*/*.mp4 via HTML5 Video tag"]
    VideoStream --> VideoPlay["Play, pause, rewind, full-screen playback"]
```

---

### 3.3 Scenario C: Daily Journal Reflection & Clinical Report Export

```mermaid
flowchart LR
    A["Patient logs in"] --> B["Opens /wellnessLog"]
    B --> C["Enters daily reflection"]
    C --> D["POST /wellnessLog"]
    D --> E[("INSERT INTO wellnesslog")]
    E --> F["View reflection history on /wellnesslogdir"]
    F --> G["Click 'Export Log' (/wellnessLogFileCreator)"]
    G --> H["Backend joins wellnesslog with user profile"]
    H --> I["python-docx generates formatted .docx"]
    I --> J["Saved in /userlogs/ and downloaded by patient"]
```

---

## 4. 🌐 Production Deployment Architecture

For deploying PsychBuddy in production environments, the recommended industry topology is:

```mermaid
flowchart TD
    Internet["Public Internet / HTTPS Traffic"] --> Nginx["Nginx Reverse Proxy & Static Asset Server"]

    subgraph WebServer["Web Server Layer"]
        Nginx -->|Proxy HTTP Requests| Gunicorn["Gunicorn / Uvicorn WSGI Application Server"]
        Nginx -->|Serve Directly| StaticCache["Static Media Directory (/static/, /userlogs/)"]
    end

    subgraph AppServer["Application Layer"]
        Gunicorn --> Worker1["Django Worker Process 1"]
        Gunicorn --> Worker2["Django Worker Process 2"]
        Gunicorn --> Worker3["Django Worker Process 3"]
    end

    subgraph DatabaseLayer["Data Layer"]
        Worker1 & Worker2 & Worker3 --> MySQLMaster[("MySQL Database (Port 3306)")]
        Worker1 & Worker2 & Worker3 --> RedisCache[("Redis / SQLite (Sessions & Cache)")]
    end
```

---

## 5. 🛡️ Operational Checklist for Administrators

1. **Environment Secrets:** Never commit `.env` to Git. Ensure `.gitignore` contains `.env`.
2. **Database Backups:** Schedule regular mysqldump snapshots:
   ```powershell
   mysqldump -u root -p psychbuddy > backup_psychbuddy.sql
   ```
3. **Database Migration:** Always run migration on new deployments:
   ```powershell
   python manage.py seed_db
   ```
4. **App Service Monitoring:** Monitor the Django server and MySQL process via system services or task managers.
