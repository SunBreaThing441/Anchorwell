# ⚙️ Backend Architecture & Workflow Specification

This document details the backend architecture, HTTP request-response lifecycle, authentication mechanics, external integrations, view handlers, and admin operations of the **PsychBuddy** web application.

---

## 1. 🏗️ High-Level Backend Architecture

PsychBuddy's backend is implemented using **Python 3.10+** and the **Django Framework**. It decouples Django's built-in session engine from application-specific data access using **PyMySQL**, interacting directly with the **MySQL / MariaDB** database.

```mermaid
flowchart TD
    subgraph ClientLayer["Client Layer"]
        HTTPReq["HTTP Request (GET/POST)"]
    end

    subgraph DjangoCore["Django Server Architecture"]
        WSGI["WSGI / ASGI Handler"]
        MW["Middleware Pipeline\n(Security, Sessions, Common, CSRF, Auth, Messages)"]
        Router["URL Dispatcher (psychbuddy.urls)"]
        Views["View Handlers (psychbuddy.views)"]
        Templates["Template Engine (psychbuddy.templates)"]
    end

    subgraph ServiceLayer["External Services & Modules"]
        Env[".env Configuration (python-dotenv)"]
        SMTP["Yagmail / Gmail SMTP Service"]
        NewsAPI["NewsAPI.org Mental Health Feed"]
        DocxGen["python-docx Report Generator"]
        EmotionAI["Emotion Detector Fallback Engine"]
    end

    subgraph DataLayer["Persistence Layer"]
        SQLite["SQLite (db.sqlite3 - Django Sessions)"]
        MySQL[("MySQL Database (psychbuddy)")]
    end

    HTTPReq --> WSGI
    WSGI --> MW
    MW --> Router
    Router --> Views
    Env -.-> Views
    Views <--> MySQL
    Views <--> SQLite
    Views <--> SMTP
    Views <--> NewsAPI
    Views <--> DocxGen
    Views <--> EmotionAI
    Views --> Templates
    Templates --> HTTPReq
```

---

## 2. 🔄 Request-Response Processing Lifecycle

Every HTTP request received by PsychBuddy undergoes the following deterministic sequence:

```mermaid
sequenceDiagram
    autonumber
    actor Client as User / Browser
    participant MW as Django Middleware Stack
    participant URL as URL Dispatcher (urls.py)
    participant View as View Function (views.py)
    participant DB as MySQL Connection Pool
    participant DTL as Django Template Engine

    Client->>MW: HTTP Request (Method, Headers, Body, Cookies)
    MW->>MW: Process Session Cookie & CSRF Token Validation
    MW->>URL: Route Request URL
    URL->>View: Dispatch to matched handler function
    View->>DB: Open pymysql.connect() & execute parameterized query
    DB-->>View: Return cursor dataset (DictCursor)
    View->>View: Business logic, session updating, data transformations
    View->>DTL: Call render(request, 'template.html', context_dict)
    DTL-->>View: Compiled HTML with dynamic values
    View-->>MW: Return HttpResponse object
    MW-->>Client: HTTP 200 OK Response (HTML / JSON stream)
```

---

## 3. 🔐 Authentication & Email OTP Workflow

User registration employs a multi-step verification protocol to ensure verified email addresses:

```mermaid
sequenceDiagram
    autonumber
    actor User as Prospective User
    participant V as views.OTP
    participant SMTP as Gmail SMTP / Yagmail
    participant DB as MySQL (otp_verification & users)
    participant Sess as Django Session Store

    User->>V: POST /second (mobile, email)
    V->>Sess: Store emailSess, mobileSess
    V->>V: Generate random 6-digit OTP (e.g. 849201)
    V->>SMTP: Send email with subject 'Psychbuddy Email Verification'
    V->>DB: INSERT INTO otp_verification (mobileno, email, otp, date, time)
    V-->>User: Render verifyOTP.html with countdown

    User->>V: POST /third (entered_otp)
    V->>DB: SELECT otp FROM otp_verification WHERE otp = %s
    alt OTP Matches
        V-->>User: Render signup.html
        User->>V: POST /signedUp (fullname, dob, age, password, address)
        V->>DB: INSERT INTO users (fullname, gender, dob, age, mobileno, email, address, password, login_status=0)
        V-->>User: Alert: 'Account Created Successfully!' -> Redirect /signin
    else OTP Invalid / Expired
        V-->>User: Alert: 'Incorrect OTP. Try Again!' -> Redirect /first
    end
```

---

## 4. 🌐 External Service Integrations

### 4.1 📰 NewsAPI Mental Health Feed (`views.news_view`)
Fetches up-to-the-minute clinical studies, news, and mental health advancements:

```mermaid
flowchart LR
    A["User requests /news"] --> B{"check_connection()"}
    B -->|Offline| C["Display Connection Error Notice"]
    B -->|Online| D["Read NEWS_API_KEY from .env"]
    D --> E["Call https://newsapi.org/v2/everything?q=mental%20health"]
    E --> F["Parse JSON Response (articles array)"]
    F --> G["Extract title, author, description, url, urlToImage"]
    G --> H["Render news.html with dynamic news cards"]
```

---

### 4.2 📑 Clinical Docx Report Generator (`views.wellnessLogFileCreator`)
Constructs formatted Microsoft Word documents summarizing patient wellness journals for therapists:

```mermaid
flowchart TD
    Trigger["User triggers /wellnessLogFileCreator"] --> Query["SELECT wellnesslog.*, users.fullname, users.age\nFROM wellnesslog JOIN users\nWHERE users.login_status = 1"]
    Query --> Docx["Initialize docx.Document()"]
    Docx --> Header["Add Patient Header (Name, Age, DOB, Mobile, Email)"]
    Header --> Table["Add Structured Table (No, Reflection Log, Time, Date)"]
    Table --> Save["Save to userlogs/{Patient_Name} Log.docx"]
    Save --> Notify["Alert: 'Log file generated successfully!'"]
```

---

### 4.3 📅 Doctor Appointment Notification Dispatcher (`views.psych_info`)
Notifies psychiatrists immediately via automated email when patients request consultations:

```mermaid
sequenceDiagram
    autonumber
    actor Patient
    participant View as views.psych_info
    participant DB as MySQL (psychiatrist_dir & users)
    participant SMTP as Yagmail SMTP Service
    actor Doctor as Psychiatrist

    Patient->>View: POST /psychinfo (psychname, appointment_date, time)
    View->>DB: SELECT email FROM psychiatrist_dir WHERE psychname = %s
    View->>DB: SELECT * FROM users WHERE login_status = 1
    View->>SMTP: Dispatch formatted consultation request
    Note over SMTP,Doctor: Email contains patient name, age, contact, requested slot
    SMTP-->>Doctor: Delivers notification to doctor's inbox
    View-->>Patient: Alert: 'Appointment Request Submitted!'
```

---

## 5. 🛡️ Admin Operations Workflow

The admin dashboard provides authenticated operators with complete content publishing and moderation capabilities:

```mermaid
stateDiagram-v2
    [*] --> AdminLogin: GET /adminlogin
    AdminLogin --> Authenticate: POST adminname + pass (Hex-encoded check)

    state AdminDashboard {
        [*] --> Overview: GET /admin/
        Overview --> ManageResources: /admin/manageResources
        Overview --> UserDirectory: /admin/usersNav
        Overview --> ForumModeration: /admin/adminforum
        Overview --> PatientFeedback: /admin/feedbackinfo
        Overview --> DailyTips: /admin/admintips
        Overview --> AppointmentConfirmations: /admin/appointmentmail

        state ManageResources {
            UploadVideo: /admin/videoRes
            UploadAudio: /admin/audioRes
            UploadBooks: /admin/bookRes
            UploadYoga: /admin/yRes
            UploadMeditation: /admin/mRes
            DeleteResources: /admin/del*
        }
    }

    AdminDashboard --> LoggedOut: GET /admin/adminlogout
```

---

## 6. 📋 Complete Backend Routing Directory

| URL Pattern | HTTP Method | Handler Function | Purpose |
| :--- | :--- | :--- | :--- |
| `/` | `GET` | `views.index` | Public landing page |
| `/first` | `GET/POST` | `views.email` | Registration start / email input |
| `/second` | `POST` | `views.OTP` | Generates & sends OTP via SMTP |
| `/third` | `POST` | `views.otpVerify` | Verifies submitted 6-digit OTP |
| `/signedUp` | `POST` | `views.signupUser` | Inserts new user record into database |
| `/signin` | `GET/POST` | `views.signin` | Authenticates user & activates session |
| `/homepage` | `GET` | `views.homePage` | Authenticated dashboard |
| `/psychiatrist` | `GET` | `views.psychiatrist` | Doctor directory |
| `/psychinfo` | `POST` | `views.psych_info` | Doctor details & booking mailer |
| `/relaxation` | `GET` | `views.audio_therapy` | Audio therapy tracks |
| `/books` | `GET` | `views.books` | Reading resources & e-books |
| `/YM` | `GET` | `views.YandM` | Yoga postures & meditation guides |
| `/sessions` | `GET` | `views.sessions` | Video sessions landing catalog |
| `/individualtherapy` | `GET` | `views.individual_therapy`| Individual video therapy player |
| `/grouptherapy` | `GET` | `views.group_therapy` | Group video therapy player |
| `/coupletherapy` | `GET` | `views.couple_therapy` | Couples therapy player |
| `/familytherapy` | `GET` | `views.family_therapy` | Family therapy player |
| `/heartbrokentherapy`| `GET` | `views.heartbroken_therapy`| Heartbreak therapy player |
| `/traumatherapy` | `GET` | `views.trauma_therapy` | Trauma recovery video player |
| `/wellnessLog` | `GET/POST` | `views.wellnessLog` | Log daily emotional reflection |
| `/wellnesslogdir` | `GET` | `views.wellnessLogDir` | Display emotional history timeline |
| `/wellnessLogFileCreator`|`GET`| `views.wellnessLogFileCreator`| Export Word report for therapist |
| `/myforum` / `/forum` | `GET/POST` | `views.chatForum` | Community forum messaging |
| `/news` | `GET` | `views.news_view` | NewsAPI mental health feed |
| `/tips` | `GET` | `views.tips` | Emotion-based advice |
| `/feedback` | `GET/POST` | `views.feedback` | Submit patient reviews |
| `/adminlogin` | `GET/POST` | `views.adminLogin` | Administrator authentication |
| `/admin/` | `GET` | `views.admindashboard` | Admin control panel |
| `/admin/manageResources`|`GET` | `views.manageResources` | Resource management navigation |
| `/admin/videoRes` | `GET/POST` | `views.videoResourcesUpload` | Upload video session files |
| `/admin/audioRes` | `GET/POST` | `views.audioResourcesUpload` | Upload audio therapy MP3s |
| `/admin/bookRes` | `GET/POST` | `views.bookResourcesUpload` | Upload books (PDF & cover art) |
| `/admin/yRes` | `GET/POST` | `views.yResourcesUpload` | Upload yoga postures & images |
| `/admin/mRes` | `GET/POST` | `views.mResourcesUpload` | Upload meditation guides |
| `/admin/del*` | `GET/POST` | `views.delete*` | Deletion endpoints for resources |
| `/admin/usersNav` | `GET` | `views.usersNav` | View registered user directory |
| `/admin/adminforum` | `GET/POST` | `views.chatAdminForum` | Forum moderation & announcements |
| `/admin/feedbackinfo` | `GET` | `views.feedbackinfo` | Patient feedback inspection |
| `/admin/appointmentmail`|`GET/POST`|`views.fixappointmentmail`| Send appointment confirmation |
| `/admin/admintips` | `GET/POST` | `views.admintips` | Update daily admin announcements |
| `/admin/adminlogout`| `GET` | `views.adminlogout` | Admin session termination |
