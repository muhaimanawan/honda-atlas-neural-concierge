<<<<<<< HEAD
# Honda Atlas Autonomous Neural Concierge & Voice Intelligence System

> **Enterprise-grade automotive web application engineered for Honda Atlas Cars (Pakistan) Limited.**  
> Featuring a Dual-Engine Neural Core (Google Gemini 2.0 / Autonomous Sales Director), Real-Time Bidirectional Web Speech Pipeline, Interactive Virtual Showroom Matrix, State Bank compliant auto-leasing calculator, and secure administrative CRM inventory controller.
>
> **Architected & Engineered by:** Engr. Muhaiman Awan

---

## 🏎️ 1. Official Honda Atlas Lineup & Ex-Factory Specifications Matrix

The relational database is pre-loaded with the exact current ex-factory retail specifications for Honda Atlas Pakistan:

| Category | Model Name | Ex-Factory Price | Live Stock | Available Colors | Powertrain Specs | Fuel Economy | Safety & Airbags |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **City** | **Honda City 1.2L CVT** | PKR 4,737,000 | 5 Units | Urban Titanium, Taffeta White | 88 HP @ 6000 RPM / 110 Nm | 15-18 KM/L | Dual SRS Airbags |
| **City** | **Honda City 1.5L Aspire CVT** | PKR 6,069,000 | 3 Units | Crystal Black Pearl, Carnelian Red | 119 HP @ 6600 RPM / 145 Nm | 14-17 KM/L | Dual SRS Airbags |
| **City** | **Honda City 1.5L Aspire S CVT** | PKR 6,149,000 | 2 Units | Lunar Silver Metallic | 119 HP (Paddle Shifters) | 14-17 KM/L | Dual SRS Airbags |
| **Civic** | **Honda Civic Standard** | PKR 8,499,000 | 2 Units | Morning Mist Blue, Taffeta White | 127 HP Turbo / 180 Nm | 12-14 KM/L | Dual SRS + EPB |
| **Civic** | **Honda Civic Oriel** | PKR 8,834,000 | 4 Units | Meteoroid Gray Metallic | 127 HP Turbo + Sunroof | 11-14 KM/L | Dual SRS + Hill Assist |
| **Civic** | **Honda Civic RS** | PKR 10,100,000 | 1 Unit | Obsidian Blue Pearl | 176 HP Turbo / 220 Nm | 11-13 KM/L | 6 Airbags + Honda SENSING |
| **HR-V** | **Honda HR-V VTi-S** | PKR 7,299,000 | 3 Units | Ignite Red Metallic | 119 HP Petrol / 145 Nm | 13-16 KM/L | 4 Airbags + Magic Seats |
| **HR-V** | **Honda HR-V e:HEV (Hybrid)** | PKR 9,299,000 | 2 Units | Platinum White Pearl | 129 HP Combined / 253 Nm | 22-26 KM/L | 6 Airbags + Honda SENSING |

---

## ⚡ 2. Core Architectural Pillars

### 🧠 A. Dual-Engine Neural Core (Google Gemini + Autonomous Sales Core)
- **Executive Persona:** System prompt configures the AI as Engr. Farhan Tariq, Senior Sales Director at Honda Atlas Head Office, 41-Km Multan Road, Lahore.
- **Multilingual Fluidity:** Automatic linguistic detection for:
  - **English:** High-level corporate automotive salesmanship.
  - **Roman Urdu:** Natural Pakistani automotive phrasing (e.g., *"Bhai Civic RS ka current stock kitna hai aur agar installment plan par leni ho toh down payment kya hogi?"*).
  - **Urdu Script (اردو):** Elegant Nastaliq-styled responses.
- **Zero-Failure Autonomous Fallback:** If `GEMINI_API_KEY` is not provided or network is offline, the embedded heuristic intelligence engine handles stock verification, vehicle comparisons, and financing calculations without dropping a single beat.

### 🎙️ B. Real-Time Bidirectional Voice Pipeline
- **Speech-to-Text (STT):** Browser-based Web Speech API with microphone pulsating animation and live transcript streaming.
- **Text-to-Speech (TTS):** Natural speech synthesis with dynamic voice detection, pitch/rate calibration, and mute toggle.
- **Audio Wave Visualizer:** Real-time HTML5 Canvas animation rendering dual sinusoidal frequencies in Honda Championship Red (`#E40521`) and Hybrid Electric Cyan (`#00E5FF`).

### 🏛️ C. Interactive Virtual Showroom & Financial Engine
- **Visual Car Configurator:** Dynamic high-resolution imagery, instant category pills (City, Civic, HR-V), real-time stock availability badges (In-Stock, Low Stock, Sold Out).
- **State Bank Compliant Auto-Financing Calculator:** Sliders for Down Payment (15%–50%), Tenure (1–7 Years), and KIBOR + Bank Spread markup. Calculates monthly installments in PKR and transfers custom plans directly into the chat concierge.
- **Side-by-Side Model Comparison Matrix:** Compare up to 3 vehicles across horsepower, torque, mileage, boot capacity, airbags, and pricing.

### 🛡️ D. Secure Admin Command Center & CRM Pipeline (`/admin`)
- **Credentials:** Protected by token authentication (`admin` / `honda_admin_2025`).
- **Live Inventory Controller:** Inline modification of stock counts and ex-factory prices with instant SQLite persistence.
- **Customer CRM Pipeline:** Manage VIP test drive requests with appointment date/time, dealership routing, and one-click direct WhatsApp integration (`wa.me`).
- **Export Facility:** One-click CSV export of all customer leads (`honda_atlas_customer_leads.csv`).

### 🏢 E. Corporate Footer & Watermark Constraints
- **Official Contact Matrix:** Embedded in global footer:
  - **UAN:** `042-111-111-243`
  - **Email:** `info@honda.com.pk`
  - **Head Office:** `41-Km, Multan Road, Lahore, Pakistan`
- **Minimalist Watermark:** Fixed pristine executive badge on the bottom-left corner of the UI:  
  **`Developed by Engr. Muhaiman Awan`**

---

## 📁 3. Modular Directory Structure

```text
honda-atlas-neural-concierge/
│
├── .env.example                     # Environment template
├── .env                             # Active configuration file
├── requirements.txt                 # Verified Python dependencies
├── run.bat                          # One-click Windows startup script
├── README.md                        # Enterprise documentation
├── app.py                           # FastAPI core application & REST API routes
├── database.py                      # SQLite ORM models, DB init & official seed data
├── ai_engine.py                     # Dual-Engine Neural Core (Gemini SDK & Fallback)
│
├── static/
│   ├── css/
│   │   └── custom.css               # Luxury dark-mode styling & canvas wave animations
│   └── js/
│       ├── app.js                   # Client speech STT/TTS, visualizer, showroom & chat
│       └── admin.js                 # Admin inventory controller & CRM lead manager
│
└── templates/
    ├── index.html                   # Master UI: Split-screen Showroom & Neural Concierge
    └── admin.html                   # Administrative Command Center & CRM Portal
```

---

## 🚀 4. Step-by-Step Local Execution Guide

### Prerequisites
- Python 3.10+ (Python 3.13 tested and verified)
- Modern Web Browser (Google Chrome, Microsoft Edge, Safari, or Firefox)

### Method 1: Instant Launch (Windows 1-Click)
Double-click `run.bat` located inside the root directory.  
The script automatically locates the Python virtual environment, initializes the database, and launches the server.

### Method 2: Manual Command Line Execution

1. **Navigate to the Project Directory:**
   ```bash
   cd "C:\Users\muhaiman awan\.gemini\antigravity\scratch\honda-atlas-neural-concierge"
   ```

2. **Activate the Virtual Environment (or create one):**
   ```bash
   # Windows PowerShell:
   .\venv\Scripts\Activate.ps1

   # Or standard Command Prompt:
   .\venv\Scripts\activate.bat
   ```

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment Variables (Optional):**
   To enable live Google Gemini 2.0 API intelligence, open `.env` and insert your Gemini API Key:
   ```env
   GEMINI_API_KEY=your_google_ai_studio_api_key_here
   GEMINI_MODEL=gemini-2.0-flash
   ```
   *(If left empty, the built-in Autonomous Sales Core functions offline with full capabilities!)*

5. **Start the FastAPI Server:**
   ```bash
   uvicorn app:app --host 127.0.0.1 --port 8000 --reload
   ```

6. **Access the Applications in Your Browser:**
   - **Public Master Showroom & Voice Concierge:** [http://127.0.0.1:8000](http://127.0.0.1:8000)
   - **Secure Admin Command Center:** [http://127.0.0.1:8000/admin](http://127.0.0.1:8000/admin)  
     *(Default Username: `admin` | Password: `honda_admin_2025`)*
   - **OpenAPI Interactive Documentation:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## 🔒 5. Administrative Credentials

- **Route:** `/admin`
- **Default Username:** `admin`
- **Default Password:** `honda_admin_2025`
- Configurable via `.env` variables `ADMIN_USERNAME` and `ADMIN_PASSWORD`.

---

## 🛠️ 6. REST API Endpoints Overview

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/` | Master Split-Screen UI |
| `GET` | `/admin` | Administrative Command Center |
| `GET` | `/api/inventory` | Live fleet matrix with real-time stock |
| `GET` | `/api/inventory/{id}` | Single vehicle specifications |
| `POST` | `/api/chat` | Multilingual Neural Core query handler |
| `POST` | `/api/leads` | Capture VIP test drive bookings into CRM |
| `POST` | `/api/admin/login` | Administrative credential validation |
| `GET` | `/api/admin/metrics` | Real-time KPIs (Fleet Valuation, Units, Leads) |
| `GET` | `/api/admin/leads` | Retrieve all customer CRM records |
| `PUT` | `/api/admin/leads/{id}/status`| Update customer workflow status |
| `PUT` | `/api/admin/inventory/{id}` | Update vehicle stock count & ex-factory price |
| `GET` | `/api/admin/export-leads` | Export customer leads as CSV |
| `GET` | `/health` | Server operational status check |

---
**Honda Atlas Cars (Pakistan) Limited • All Rights Reserved**  
*Autonomous Neural Concierge Engineered by Engr. Muhaiman Awan*
=======
# honda-atlas-neural-concierge
Enterprise AI web platform for Honda Atlas Pakistan. Features a Google Gemini + Roman Urdu voice intelligence pipeline, live audio wave visualizer, interactive virtual showroom, auto-leasing calculator, and secure administrative CRM inventory controller.
>>>>>>> 0e6745f4a2768f1a7f0fc98f721ad0bf7a855132
