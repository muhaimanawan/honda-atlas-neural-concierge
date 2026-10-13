"""
Honda Atlas Pakistan - Autonomous Neural Concierge & Voice Intelligence System
Main Application Core (FastAPI Enterprise Server)
"""

import os
import csv
import io
from typing import Dict, Any, List, Optional
from fastapi import FastAPI, Request, HTTPException, Depends, Form, status
from fastapi.responses import HTMLResponse, JSONResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv

import database
import ai_engine

# Load environment configuration
load_dotenv()

ADMIN_USERNAME = os.getenv("ADMIN_USERNAME", "admin")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "honda_admin_2025")
SECRET_KEY = os.getenv("SECRET_KEY", "honda_atlas_secret_token_2025")

# Initialize FastAPI Enterprise Application
app = FastAPI(
    title="Honda Atlas Autonomous Neural Concierge & Voice Intelligence System",
    description="Enterprise-grade AI automotive showroom, voice conversational pipeline & inventory management system.",
    version="2.5.0"
)

# Enable CORS for cross-origin integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount Static Assets and Templates
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
templates = Jinja2Templates(directory=TEMPLATES_DIR)


# ---------------- PYDANTIC DATA SCHEMAS ----------------

class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = "default-session"
    history: Optional[List[Dict[str, str]]] = []

class LeadRequest(BaseModel):
    name: str
    phone: str
    email: Optional[str] = ""
    city: str
    car_model: str
    dealership: Optional[str] = "Honda Fort (Lahore)"
    preferred_date: Optional[str] = ""
    preferred_time: Optional[str] = ""
    source: Optional[str] = "Web Concierge"
    notes: Optional[str] = ""

class InventoryUpdateRequest(BaseModel):
    stock: int
    price: Optional[int] = None
    is_active: Optional[int] = 1

class LeadStatusUpdateRequest(BaseModel):
    status: str

class AdminLoginRequest(BaseModel):
    username: str
    password: str


# ---------------- FRONTEND HTML ROUTES ----------------

@app.get("/", response_class=HTMLResponse)
async def index_view(request: Request):
    """
    Renders the flagship Master UI:
    Split-screen Virtual Showroom & Autonomous Neural Voice Concierge.
    """
    cars = database.get_all_cars(only_active=True)
    metrics = database.get_dashboard_metrics()
    
    dealerships = [
        {"name": "Honda Fort", "city": "Lahore", "address": "Main Gulberg III, Lahore"},
        {"name": "Honda Point", "city": "Lahore", "address": "Defense Main Boulevard, Lahore"},
        {"name": "Honda Drive-In", "city": "Karachi", "address": "Main Rashid Minhas Road, Karachi"},
        {"name": "Honda South", "city": "Karachi", "address": "Korangi Industrial Area, Karachi"},
        {"name": "Honda Classic", "city": "Islamabad", "address": "I-9 Industrial Area, Islamabad"},
        {"name": "Honda Avenue", "city": "Rawalpindi", "address": "Main Peshawar Road, Rawalpindi"},
        {"name": "Honda Faisalabad", "city": "Faisalabad", "address": "Canal Road, Faisalabad"},
        {"name": "Honda Multan", "city": "Multan", "address": "Bosan Road, Multan"}
    ]

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "cars": cars,
            "metrics": metrics,
            "dealerships": dealerships,
            "corporate_uan": "042-111-111-243",
            "corporate_email": "info@honda.com.pk",
            "corporate_hq": "41-Km, Multan Road, Lahore, Pakistan",
            "watermark": "Developed by Engr. Muhaiman Awan"
        }
    )


@app.get("/admin", response_class=HTMLResponse)
async def admin_view(request: Request):
    """
    Renders the Secure Enterprise Admin Command Center & Inventory Controller.
    """
    cars = database.get_all_cars(only_active=False)
    leads = database.get_all_leads()
    metrics = database.get_dashboard_metrics()

    return templates.TemplateResponse(
        request=request,
        name="admin.html",
        context={
            "cars": cars,
            "leads": leads,
            "metrics": metrics,
            "watermark": "Developed by Engr. Muhaiman Awan"
        }
    )


# ---------------- API ENDPOINTS ----------------

@app.get("/api/inventory")
async def get_inventory_api():
    """Returns the live fleet inventory matrix with ex-factory pricing and real-time stock."""
    cars = database.get_all_cars(only_active=False)
    return JSONResponse(content={"status": "success", "cars": cars})


@app.get("/api/inventory/{car_id}")
async def get_car_api(car_id: int):
    """Retrieves full technical specifications and availability for a single vehicle."""
    car = database.get_car_by_id(car_id)
    if not car:
        raise HTTPException(status_code=404, detail="Vehicle model not found")
    return JSONResponse(content={"status": "success", "car": car})


@app.post("/api/chat")
async def chat_api(payload: ChatRequest):
    """
    Executes real-time conversational intelligence through the Dual-Engine Neural Core.
    Detects language (English / Urdu / Roman Urdu) and extracts intent.
    """
    user_msg = payload.message.strip()
    if not user_msg:
        raise HTTPException(status_code=400, detail="Message cannot be empty")

    # Invoke Neural Sales Director
    result = ai_engine.query_neural_sales_director(user_msg, payload.history)

    # Persist transcript in SQLite
    try:
        database.log_chat_interaction(
            session_id=payload.session_id or "default",
            role="user",
            message=user_msg,
            language=result.get("language", "en")
        )
        database.log_chat_interaction(
            session_id=payload.session_id or "default",
            role="assistant",
            message=result["text"],
            language=result.get("language", "en")
        )
    except Exception as e:
        # Non-blocking logging failure
        pass

    return JSONResponse(content={
        "status": "success",
        "response": result["text"],
        "language": result.get("language", "en"),
        "matched_car": result.get("matched_car"),
        "trigger_lead_modal": result.get("trigger_lead_modal", False),
        "engine_used": result.get("engine_used", "Autonomous Heuristic Core")
    })


@app.post("/api/leads")
async def create_lead_api(lead: LeadRequest):
    """
    CRM Hook: Captures qualified buyer leads & VIP test-drive reservations into SQLite.
    """
    if not lead.name or not lead.phone:
        raise HTTPException(status_code=400, detail="Customer Name and Phone Number are required")

    lead_data = {
        "name": lead.name,
        "phone": lead.phone,
        "email": lead.email or "",
        "city": lead.city,
        "car_model": lead.car_model,
        "dealership": lead.dealership or "Honda Fort (Lahore)",
        "preferred_date": lead.preferred_date or "",
        "preferred_time": lead.preferred_time or "",
        "source": lead.source or "Web Concierge",
        "status": "New",
        "notes": lead.notes or ""
    }

    lead_id = database.create_lead(lead_data)
    return JSONResponse(content={
        "status": "success",
        "lead_id": lead_id,
        "message": f"Test drive reservation successfully logged for {lead.name}."
    })


@app.post("/api/admin/login")
async def admin_login_api(login: AdminLoginRequest):
    """Validates administrative credentials."""
    if login.username == ADMIN_USERNAME and login.password == ADMIN_PASSWORD:
        return JSONResponse(content={
            "status": "success",
            "token": SECRET_KEY,
            "message": "Authentication successful"
        })
    raise HTTPException(status_code=401, detail="Invalid administrator credentials")


@app.get("/api/admin/metrics")
async def admin_metrics_api():
    """Returns executive dashboard KPIs: fleet valuation, stock count, leads breakdown."""
    metrics = database.get_dashboard_metrics()
    return JSONResponse(content={"status": "success", "metrics": metrics})


@app.get("/api/admin/leads")
async def admin_leads_api():
    """Returns all CRM customer leads."""
    leads = database.get_all_leads()
    return JSONResponse(content={"status": "success", "leads": leads})


@app.put("/api/admin/leads/{lead_id}/status")
async def update_lead_status_api(lead_id: int, payload: LeadStatusUpdateRequest):
    """Updates lead workflow status (e.g. New -> Contacted -> Test Drive Scheduled -> Converted)."""
    success = database.update_lead_status(lead_id, payload.status)
    if not success:
        raise HTTPException(status_code=404, detail="Lead not found")
    return JSONResponse(content={"status": "success", "message": f"Lead status updated to {payload.status}"})


@app.put("/api/admin/inventory/{car_id}")
async def update_inventory_api(car_id: int, payload: InventoryUpdateRequest):
    """
    Live Inventory Controller: updates warehouse stock count, ex-factory price, or active status.
    """
    success = database.update_car_inventory(
        car_id=car_id,
        stock=payload.stock,
        price=payload.price,
        is_active=payload.is_active
    )
    if not success:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    return JSONResponse(content={"status": "success", "message": "Inventory successfully updated"})


@app.get("/api/admin/export-leads")
async def export_leads_csv():
    """Exports all CRM test-drive bookings and customer leads to CSV spreadsheet."""
    leads = database.get_all_leads()

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow([
        "Lead ID", "Customer Name", "Phone", "Email", "City",
        "Vehicle of Interest", "Dealership", "Preferred Date",
        "Preferred Time", "Source", "Status", "Notes", "Created At"
    ])

    for l in leads:
        writer.writerow([
            l.get("id"), l.get("name"), l.get("phone"), l.get("email"),
            l.get("city"), l.get("car_model"), l.get("dealership"),
            l.get("preferred_date"), l.get("preferred_time"),
            l.get("source"), l.get("status"), l.get("notes"), l.get("created_at")
        ])

    output.seek(0)
    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=honda_atlas_customer_leads.csv"}
    )


@app.get("/health")
async def health_check():
    """System health check endpoint."""
    return {"status": "operational", "system": "Honda Atlas Autonomous Neural Concierge", "version": "2.5.0"}


if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    host = os.environ.get("HOST", "0.0.0.0")
    uvicorn.run("app:app", host=host, port=port, reload=False)

