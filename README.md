# AnchorWell: UNESCO Mental Support Grid

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Framework: Django](https://img.shields.io/badge/Framework-Django-092E20?logo=django)](https://www.djangoproject.com/)
[![Database: MySQL](https://img.shields.io/badge/Database-MySQL%20%2F%20PyMySQL-4479A1?logo=mysql)](https://www.mysql.com/)
[![UI: AnchorWell Design System](https://img.shields.io/badge/UI-Futuristic%20Glassmorphism-2DD4BF)](#design-system)
[![Status: Production Ready](https://img.shields.io/badge/Status-Production%20Ready-10B981)](#)

> **AnchorWell** is a decentralized, evidence-based psychosocial support platform built in alignment with multilateral cognitive health frameworks. Formerly *PsychBuddy*, the platform has been completely overhauled with a futuristic presentation tier, persistent sound sanctuary streaming, and role-based clinical security guards.

---

## Architecture Overview

AnchorWell utilizes a decoupled architecture where an intelligent Single Page Application (SPA) runtime interfaces with Django's native session engine on Port 8000 and a high-throughput MySQL persistence tier on Port 3306.

```
                    +------------------------------------------+
                    |    AnchorWell Client Presentation Tier   |
                    |   (SPA DOM Morphing & Audio Sanctuary)   |
                    +--------------------+---------------------+
                                         | HTTP/AJAX (withCredentials)
                                         v
                    +--------------------+---------------------+
                    |       Django WSGI Application Core       |
                    |   (Session Engine, Auth, REST Relay)     |
                    +--------------------+---------------------+
                                         | PyMySQL Connection Pool
                                         v
                    +--------------------+---------------------+
                    |    MySQL Persistence Tier ("psychbuddy") |
                    | (users, sessions, wellnesslog, admintips)|
                    +------------------------------------------+
```

---

## Core Feature Modules

### 1. Neuro-Acoustic Sound Sanctuary (`/relaxation`)
* **Persistent Audio Dock (`#awAudioDock`):** Global floating audio console mounted to `document.body` that streams psychoacoustic audio (`/static/audio/*.mp3`) continuously across page navigations without interruption.
* **Harmonic Presets:** Oceanic restoration, deep forest nightingales, theta brainwave calibration, and peaceful rain frequencies.

### 2. Clinical Video Therapy Hub (`/sessions`, `/sessionpage`)
* **HTTP 206 Byte-Range Streaming:** Smooth playback for high-definition clinical guidance tracks (`/static/sessions/*/*.mp4`).
* **Therapy Vectors:** Individual, Couples, Family, Trauma-Informed, and Heartbreak Recovery modules.

### 3. Mind-Body Calibration (`/YM`)
* **Somatic Asanas:** Anatomically guided yoga postures with step-by-step breath synchronization.
* **Guided Meditation:** Evidence-based mindfulness and parasympathetic down-regulation protocols.

### 4. Somatic Reflection Journal (`/wellnessLog`, `/wellnesslogdir`)
* **Live Longitudinal Journaling:** Real-time character/word telemetry counter submitting encrypted reflections to MySQL.
* **Clinical Telemetry Compiler (`/wellnessLogFileCreator`):** Multi-stage progress HUD compiling historical reflection entries into authenticated DOCX clinical dossiers.

### 5. Specialist Directory & Booking (`/psychiatrist`, `/psychInfo`)
* **Specialist Dossiers:** Responsive, data-dense cards featuring UNESCO-verified psychiatric specialists.
* **Modal Appointment Dispatch:** Real-time booking dialog sending appointment parameters and historical logs via SMTP relay.

### 6. UNESCO Peer Mesh & Global Intelligence (`/forum`, `/news`)
* **Psychosocial Chat Mesh:** Decentralized peer discussion forum with live DOM message append.
* **NewsAPI Intelligence Feed:** Global mental health telemetry and psychiatric research articles.

### 7. Administrative Command Console (`/adminlogin`, `/admin/`)
* **Level 4 Clearance Security:** Complete isolation between patient and administrative contexts with 15-minute auto-locking timers.
* **Resource Pipelines:** Multipart upload HUDs with progress indicators for audio, video, literature, and yoga assets.

---

## Design System & Color Psychology

The AnchorWell UI replaces legacy styling with a high-tech glassmorphic design system:

| Token | Hex | Psychological Intention |
| :--- | :--- | :--- |
| **Deep Grounding Indigo** | `#030611` / `#0A0F26` | Fosters neurological stability and reduces visual fatigue. |
| **Bioluminescent Teal** | `#2DD4BF` / `#0D9488` | Promotes mental clarity, calm focus, and positive reinforcement. |
| **Sterile Clinical White** | `#FFFFFF` / `#F8FAFC` | Delivers unambiguous clinical readability and contrast. |
| **Distress / Crisis Accent** | `#F43F5E` | Immediate visual alerting for urgent somatic and deletion triggers. |
| **Administrative Amber** | `#F59E0B` | Visual hierarchy for Level 4 clearance administrative controls. |

---

## Technology Stack

* **Frontend:** AnchorWell SPA Runtime (`anchorwell.js`), Custom Glassmorphic CSS3 System (`anchorwell.css`), HTML5 Media APIs
* **Backend:** Python 3.10+, Django 4.2 / 5.x WSGI Router
* **Database:** MySQL 8.0 / MariaDB 10.4+ (`psychbuddy` schema) via PyMySQL connection pool
* **Document Processing:** `python-docx` for automated clinical report compilation
* **Email & Notifications:** `yagmail` / SMTP relay

---

## Quick Start & Installation

### 1. Prerequisites
* **Python 3.10+**
* **MySQL / MariaDB** (e.g., via XAMPP or native service on Port 3306)
* Database named `psychbuddy` imported with platform tables.

### 2. Clone the Repository
```bash
git clone https://github.com/SunBreaThing441/Anchorwell.git
cd Anchorwell
```

### 3. Environment Configuration
Copy `.env.example` to `.env` and verify database credentials:
```ini
DB_NAME=psychbuddy
DB_USER=root
DB_PASSWORD=
DB_HOST=localhost
DB_PORT=3306
```

### 4. Launch the Platform
Double-click [`start_anchorwell.bat`](start_anchorwell.bat) or execute via terminal:

```powershell
# Verify MySQL on port 3306 is running, then:
cd Psychbuddy
python manage.py runserver 127.0.0.1:8000
```

Navigate to `http://127.0.0.1:8000/` in any modern web browser.

---

## Route Directory

| Route | View Name | Access Clearance | Description |
| :--- | :--- | :--- | :--- |
| `/` | `index` | Public | AnchorWell landing portal & telemetry |
| `/aboutus` | `aboutus` | Public | UNESCO Accord charter & node latency |
| `/signin` | `signin` | Public | Patient authentication gateway |
| `/first` | `emailVerify` | Public | Registration Step 1: E.164 & Email verification |
| `/second` | `otpVerify` | Public | Registration Step 2: 6-Digit PIN validation |
| `/third` | `signup` | Public | Registration Step 3: Profile creation |
| `/homepage` | `home` | Patient | Authenticated patient command console |
| `/relaxation` | `audio_therapy` | Patient | Sound Sanctuary persistent audio hub |
| `/sessions` | `sessions` | Patient | Clinical Video Therapy catalog |
| `/wellnessLog`| `wellness_log` | Patient | Longitudinal reflection journal |
| `/psychiatrist`| `psychiatrist`| Patient | Verified specialist registry |
| `/adminlogin` | `adminlogin` | Admin | Administrative gateway |
| `/admin/` | `admin` | Level 4 Admin | Isolated administrative console |

---

## License & Accords

Distributed under the MIT License. Developed in adherence to multilateral psychosocial guidelines.
