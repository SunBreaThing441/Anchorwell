# 🎨 Frontend Architecture & Workflow Specification

This document details the complete frontend architecture, user interaction lifecycles, UI component hierarchy, and rendering workflows of the **PsychBuddy** platform.

---

## 1. 🏗️ High-Level Frontend Architecture

PsychBuddy utilizes server-side rendering powered by the **Django Template Language (DTL)** combined with semantic HTML5, modular CSS3 styling, and modern Vanilla JavaScript for rich client-side interactivity.

```mermaid
flowchart TD
    subgraph Browser["Client Browser"]
        DOM[DOM / UI View]
        JS[Vanilla JS Event Handlers]
        Media[HTML5 Audio/Video Players]
        Webcam[Webcam Video Capture]
    end

    subgraph StaticAssets["Static Asset Pipeline (/static/)"]
        CSS["style.css / style2.css"]
        Images["Poster Art, Avatars, Icons"]
        Audio["MP3 Audio Files"]
        Video["MP4 Video Therapy Tracks"]
        Fonts["Poppins Typography"]
    end

    subgraph DjangoFrontend["Django Template Engine (/templates/)"]
        BaseLayout["Base Layout & usersNav.html"]
        PageTemplates["Page Views (index, YM, books, relaxation...)"]
        AdminTemplates["Admin Management Templates"]
    end

    DOM <--> JS
    DOM <--> Media
    DOM <--> Webcam
    CSS --> DOM
    Images --> DOM
    Audio --> Media
    Video --> Media
    Fonts --> CSS
    DjangoFrontend --> DOM
```

---

## 2. 🗺️ End-to-End User Journey Workflow

The following state diagram depicts how users navigate through authentication, onboarding, self-care features, therapy resources, and clinical logging:

```mermaid
stateDiagram-v2
    [*] --> LandingPage: Visit /
    LandingPage --> SigninPage: Click 'Sign In' (/signin)
    LandingPage --> Registration: Click 'Sign Up' (/first)

    state Registration {
        EmailVerify: Enter Email & Mobile (/first)
        OTPValidation: Verify 6-digit OTP (/third)
        ProfileCreation: Complete User Profile (/signedUp)
        EmailVerify --> OTPValidation
        OTPValidation --> ProfileCreation
    }

    Registration --> SigninPage: Account Created
    SigninPage --> UserDashboard: Successful Auth (/homepage)

    state UserDashboard {
        [*] --> HomeOverview
        HomeOverview --> TherapySessions: Browse Video Sessions (/sessions)
        HomeOverview --> SoundTherapy: Listen to Calming Audio (/relaxation)
        HomeOverview --> ReadingLibrary: Browse Self-Help Books (/books)
        HomeOverview --> YogaMeditation: Practice Asanas & Meditation (/YM)
        HomeOverview --> WellnessJournal: Log Daily Emotions (/wellnessLog)
        HomeOverview --> FindTherapist: Search Psychiatrists (/psychiatrist)
        HomeOverview --> CommunityForum: Join Discussions (/myforum)
        HomeOverview --> LiveNews: Read Mental Health News (/news)
    }

    FindTherapist --> BookAppointment: Select Psychiatrist (/psychinfo)
    WellnessJournal --> ExportReport: Download DOCX Log (/wellnessLogFileCreator)
```

---

## 3. 🧩 Core Feature Workflows

### 3.1 🎧 Sound Therapy & Relaxation Player Workflow
Users can stream high-definition ambient nature sounds (ocean waves, rain, nightingale, river stream) without page interruptions:

```mermaid
sequenceDiagram
    autonumber
    actor User
    participant Browser as Browser UI (/relaxation)
    participant Django as Django Template Engine
    participant Static as Static File Server (/static/audio/)

    User->>Browser: Navigate to /relaxation
    Browser->>Django: GET /relaxation
    Django-->>Browser: Render relaxation.html with Sound Cards
    User->>Browser: Clicks 'Play' on Ocean Waves card
    Browser->>Static: Request audio/Ocean Wave Sound.mp3 (Range request)
    Static-->>Browser: Stream MP3 Audio Chunk
    Browser->>User: Playback ambient audio with loop controls
```

---

### 3.2 📚 Reading Resources & E-Book Library Workflow
Provides access to curated mental health literature, trauma healing guides, and relationship books:

```mermaid
sequenceDiagram
    autonumber
    actor User
    participant UI as Library UI (/books)
    participant Django as Django Backend
    participant Static as Static Storage (/static/books/)

    User->>UI: Open Reading Resources (/books)
    UI->>Django: GET /books
    Django-->>UI: Render books.html with titles, authors, and cover art
    User->>UI: Click 'Read Book' on "Hope and Help for Your Nerves"
    UI->>Static: Open /static/books/Hope and Help for Your Nerves.pdf
    Static-->>User: Embedded PDF Viewer in browser / Direct Download
```

---

### 3.3 🧘 Yoga & Meditation (YM) Workflow
Guides users through asana routines and mindfulness exercises tailored to stress reduction:

```mermaid
flowchart LR
    A["User visits /YM"] --> B{"Choose Practice"}
    B -->|Physical Self-Care| C["Yoga Postures Section"]
    B -->|Mental Calming| D["Meditation Guides Section"]

    C --> C1["View Asana Card (e.g., Balasana)"]
    C1 --> C2["Inspect Step-by-Step Instructions"]
    C2 --> C3["Review Physical & Mental Health Benefits"]

    D --> D1["Select Mindfulness Technique"]
    D1 --> D2["Read Guided Script (e.g., Box Breathing 4-4-4-4)"]
    D2 --> D3["Practice Routine"]
```

---

### 3.4 🎥 Video Therapy Sessions Workflow
Provides 6 specialized categories of guided psychological video sessions:

```mermaid
flowchart TD
    Catalog["Sessions Catalog (/sessions)"] --> Cat1["Individual Therapy (/individualtherapy)"]
    Catalog --> Cat2["Group Therapy (/grouptherapy)"]
    Catalog --> Cat3["Couples Therapy (/coupletherapy)"]
    Catalog --> Cat4["Family Therapy (/familytherapy)"]
    Catalog --> Cat5["Heartbreak Therapy (/heartbrokentherapy)"]
    Catalog --> Cat6["Trauma Therapy (/traumatherapy)"]

    Cat1 & Cat2 & Cat3 & Cat4 & Cat5 & Cat6 --> VideoView["Render sessionpage.html"]
    VideoView --> HTML5Player["HTML5 Video Player (Stream from /static/sessions/)"]
```

---

### 3.5 📝 Daily Mental Wellness Progress Log Workflow
Allows users to write daily reflective logs and export clinical summaries to Word documents for therapists:

```mermaid
sequenceDiagram
    autonumber
    actor User
    participant LogUI as Journal UI (/wellnessLog)
    participant View as views.wellnessLog
    participant DB as MySQL (wellnesslog table)
    participant Docx as Document Generator (/wellnessLogFileCreator)

    User->>LogUI: Enter daily mood, activities & stress triggers
    User->>LogUI: Click 'Store Reflection'
    LogUI->>View: POST /wellnessLog (tb1=text)
    View->>DB: INSERT INTO wellnesslog (email, log, time, date)
    DB-->>View: Confirmed
    View-->>LogUI: JavaScript alert('Data stored successfully!')

    User->>LogUI: Click 'Export to Therapist' (/wellnessLogFileCreator)
    LogUI->>Docx: GET /wellnessLogFileCreator
    Docx->>DB: SELECT logs JOIN users WHERE login_status=1
    Docx->>Docx: Generate structured Word file (userlogs/*.docx)
    Docx-->>User: File generated notification & direct download
```

---

## 4. 📁 Template Hierarchy & Component Map

```
templates/
├── Base & Navigation
│   ├── index.html                   # Public hero landing page
│   ├── homepage.html                # Authenticated user dashboard
│   ├── usersNav.html                # Reusable navigation bar component
│   └── aboutus.html                 # Mission, team, and contact info
│
├── Authentication & Onboarding
│   ├── emailVerify.html             # Step 1: Email and mobile input
│   ├── verifyOTP.html               # Step 2: 6-digit OTP code input
│   ├── signup.html                  # Step 3: Profile details form
│   └── signin.html                  # User login credentials form
│
├── Mental Wellness Features
│   ├── psychiatrist.html            # Verified doctors directory
│   ├── psychInfo.html               # Doctor bio & booking confirmation
│   ├── relaxation.html              # Sound therapy audio player
│   ├── books.html                   # Reading resources library
│   ├── YM.html                      # Yoga & Meditation routines
│   ├── sessions.html                # Video sessions directory
│   ├── sessionpage.html             # Video category streaming player
│   ├── MentalWellnessLog.html       # Daily emotional log entry form
│   ├── MentalWellnessLogDir.html    # Progress history & export options
│   ├── forum.html / myforum.html    # Peer community discussion board
│   ├── tips.html                    # Personalized emotion advice
│   ├── news.html                    # Real-time mental health news
│   └── feedback.html                # User reviews & suggestions
│
└── Admin Management Portal
    ├── adminlogin.html              # Secure administrator authentication
    ├── admindashboard.html          # Main administrator overview
    ├── manageResources.html         # Resource management center
    ├── videoResAdmin.html           # Video session uploader
    ├── audioResAdmin.html           # Audio therapy uploader
    ├── readingResAdmin.html         # Book & PDF uploader
    ├── yResAdmin.html               # Yoga pose uploader
    ├── mResAdmin.html               # Meditation guide uploader
    ├── delVideoRes.html             # Video session deleter
    ├── delAudioRes.html             # Audio resource deleter
    ├── delBookRes.html              # Book resource deleter
    ├── delYRes.html                 # Yoga pose deleter
    ├── delMRes.html                 # Meditation guide deleter
    ├── adminforum.html              # Community forum moderator
    ├── feedbackinfo.html            # Patient reviews list
    ├── appointmentmail.html         # Appointment confirmation dispatcher
    └── admintips.html               # Administrator daily tips editor
```
