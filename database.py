"""
Honda Atlas Pakistan - Autonomous Neural Concierge & Voice Intelligence System
Database & Relational State Management Module
Engineered for Honda Atlas Cars (Pakistan) Limited Official Lineup
"""

import sqlite3
import json
import os
from datetime import datetime
from typing import List, Dict, Any, Optional

DB_PATH = os.path.join(os.path.dirname(__file__), "honda_atlas.db")


def get_db_connection() -> sqlite3.Connection:
    """Creates a connection to the SQLite database with dictionary cursor row support."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Initializes tables and seeds the core Honda Atlas Pakistan lineup."""
    conn = get_db_connection()
    cursor = conn.cursor()

    # 1. Vehicles Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS cars (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        slug TEXT UNIQUE NOT NULL,
        name TEXT NOT NULL,
        category TEXT NOT NULL,
        price INTEGER NOT NULL,
        stock INTEGER NOT NULL DEFAULT 0,
        colors TEXT NOT NULL,
        horsepower TEXT NOT NULL,
        torque TEXT NOT NULL,
        transmission TEXT NOT NULL,
        fuel_economy TEXT NOT NULL,
        boot_capacity TEXT NOT NULL,
        airbags TEXT NOT NULL,
        image_url TEXT NOT NULL,
        tagline TEXT,
        description TEXT,
        features TEXT,
        is_active INTEGER NOT NULL DEFAULT 1,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    # 2. Leads & Test-Drive Bookings CRM Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS leads (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        phone TEXT NOT NULL,
        email TEXT,
        city TEXT NOT NULL,
        car_model TEXT NOT NULL,
        dealership TEXT,
        preferred_date TEXT,
        preferred_time TEXT,
        source TEXT DEFAULT 'Web Concierge',
        status TEXT DEFAULT 'New',
        notes TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    # 3. Chat Session Logs Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS chat_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        session_id TEXT NOT NULL,
        role TEXT NOT NULL,
        message TEXT NOT NULL,
        language TEXT,
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    conn.commit()

    # Verify if cars need seeding
    cursor.execute("SELECT COUNT(*) as count FROM cars")
    count = cursor.fetchone()["count"]

    if count == 0:
        seed_honda_inventory(cursor)
        conn.commit()

    conn.close()


def seed_honda_inventory(cursor: sqlite3.Cursor):
    """
    Seeds the exact current lineup and official ex-factory specifications
    of Honda Atlas Cars (Pakistan) Limited as required by enterprise specifications.
    """
    official_cars = [
        # --- 1. HONDA CITY LINEUP ---
        {
            "slug": "honda-city-12l-cvt",
            "name": "Honda City 1.2L CVT",
            "category": "Honda City",
            "price": 4737000,
            "stock": 5,
            "colors": json.dumps(["Urban Titanium", "Taffeta White"]),
            "horsepower": "88 HP @ 6,000 RPM",
            "torque": "110 Nm @ 4,800 RPM",
            "transmission": "Continuous Variable Transmission (CVT)",
            "fuel_economy": "15-18 KM/L",
            "boot_capacity": "506 Liters",
            "airbags": "Dual SRS Airbags (Driver & Front Passenger)",
            "image_url": "/static/images/honda_city_12.jpg",
            "tagline": "Urban Sophistication Meets Unmatched Daily Fuel Efficiency",
            "description": "The Honda City 1.2L CVT redefines urban commuting in Pakistan with high fuel economy, ultra-smooth CVT transmission, and class-leading 506-liter boot capacity.",
            "features": json.dumps([
                "1.2L SOHC 16-Valve i-VTEC Engine",
                "CVT Transmission with Earth Dreams Tech",
                "ABS with EBD & Brake Assist",
                "Shark Fin Antenna & Steering Audio Switches",
                "Eco Assist & ECON Driving Mode"
            ]),
            "is_active": 1
        },
        {
            "slug": "honda-city-15l-aspire-cvt",
            "name": "Honda City 1.5L Aspire CVT",
            "category": "Honda City",
            "price": 6069000,
            "stock": 3,
            "colors": json.dumps(["Crystal Black Pearl", "Carnelian Red"]),
            "horsepower": "119 HP @ 6,600 RPM",
            "torque": "145 Nm @ 4,300 RPM",
            "transmission": "Continuous Variable Transmission (CVT)",
            "fuel_economy": "14-17 KM/L",
            "boot_capacity": "506 Liters",
            "airbags": "Dual SRS Airbags",
            "image_url": "/static/images/honda_city_aspire.jpg",
            "tagline": "The Executive Pinnacle of the City Lineup",
            "description": "Equipped with a powerful 1.5L i-VTEC engine, premium leather upholstery, 9-inch capacitive touchscreen, and chrome accents designed for discerning Pakistani executives.",
            "features": json.dumps([
                "1.5L i-VTEC High Output Engine",
                "Premium Leather Upholstery & Armrest",
                "9-inch Advanced Infotainment with Screen Mirroring",
                "Cruise Control & Smart Keyless Entry",
                "Automatic Climate Control"
            ]),
            "is_active": 1
        },
        {
            "slug": "honda-city-15l-aspire-s-cvt",
            "name": "Honda City 1.5L Aspire S CVT",
            "category": "Honda City",
            "price": 6149000,
            "stock": 2,
            "colors": json.dumps(["Lunar Silver Metallic"]),
            "horsepower": "119 HP @ 6,600 RPM",
            "torque": "145 Nm @ 4,300 RPM",
            "transmission": "Continuous Variable Transmission (CVT) with Paddle Shifters",
            "fuel_economy": "14-17 KM/L",
            "boot_capacity": "506 Liters",
            "airbags": "Dual SRS Airbags",
            "image_url": "/static/images/honda_city_aspire_s.jpg",
            "tagline": "Sport-Inspired Executive Luxury with Paddle Controls",
            "description": "The Special Edition Aspire S delivers aggressive styling cues, steering paddle shifters for spirited driving, and exclusive Lunar Silver metallic finishing.",
            "features": json.dumps([
                "Steering-Mounted Paddle Shifters",
                "15-inch Diamond Cut Alloy Wheels",
                "Push Start with Smart Keyless Entry",
                "Reverse Camera with Dynamic Guidelines",
                "Vehicle Stability Assist (VSA)"
            ]),
            "is_active": 1
        },

        # --- 2. HONDA CIVIC LINEUP ---
        {
            "slug": "honda-civic-standard",
            "name": "Honda Civic Standard",
            "category": "Honda Civic",
            "price": 8499000,
            "stock": 2,
            "colors": json.dumps(["Morning Mist Blue", "Taffeta White"]),
            "horsepower": "127 HP @ 5,500 - 6,000 RPM",
            "torque": "180 Nm @ 1,700 - 4,500 RPM",
            "transmission": "M-CVT (Continuously Variable Transmission)",
            "fuel_economy": "12-14 KM/L",
            "boot_capacity": "409 Liters",
            "airbags": "Dual SRS Airbags + ABS/EBD/VSA",
            "image_url": "/static/images/honda_civic_standard.jpg",
            "tagline": "Pure Dynamic Sophistication & Iconic Engineering",
            "description": "11th Generation Honda Civic Standard chassis with rigid laser brazing, refined ergonomics, and turbocharged responsiveness for an effortless drive across Pakistani motorways.",
            "features": json.dumps([
                "1.5L Turbocharged DOHC VTEC Engine",
                "Electronic Parking Brake (EPB) with Auto Brake Hold",
                "Full Digital 7-inch TFT Multi-Information Display",
                "Hill Start Assist & Emergency Stop Signal",
                "Agile Handling Assist (AHA)"
            ]),
            "is_active": 1
        },
        {
            "slug": "honda-civic-oriel",
            "name": "Honda Civic Oriel",
            "category": "Honda Civic",
            "price": 8834000,
            "stock": 4,
            "colors": json.dumps(["Meteoroid Gray Metallic"]),
            "horsepower": "127 HP @ 5,500 - 6,000 RPM",
            "torque": "180 Nm @ 1,700 - 4,500 RPM",
            "transmission": "M-CVT with Electronic Sunroof Integration",
            "fuel_economy": "11-14 KM/L",
            "boot_capacity": "409 Liters",
            "airbags": "Dual SRS Airbags + Hill Start Assist",
            "image_url": "/static/images/honda_civic_oriel.jpg",
            "tagline": "The Premier Choice with Panoramic Sunroof & Refinement",
            "description": "Pakistan's undisputed executive sedan flagship with one-touch electric sunroof, rear A/C vents, ambient cabin illumination, and Meteoroid Gray prestige.",
            "features": json.dumps([
                "One-Touch Electric Sunroof",
                "Rear Passenger AC Air Vents",
                "Dual-Zone Automatic Climate Control",
                "Dual Exhaust Pipes with Chrome Finishers",
                "16-inch Premium Aluminum Alloy Wheels"
            ]),
            "is_active": 1
        },
        {
            "slug": "honda-civic-rs",
            "name": "Honda Civic RS",
            "category": "Honda Civic",
            "price": 10100000,
            "stock": 1,
            "colors": json.dumps(["Obsidian Blue Pearl"]),
            "horsepower": "176 HP @ 6,000 RPM (High-Output Turbo)",
            "torque": "220 Nm @ 1,700 - 4,500 RPM",
            "transmission": "LL-CVT with Paddle Shifters & Sport Drive Mode",
            "fuel_economy": "11-13 KM/L",
            "boot_capacity": "409 Liters",
            "airbags": "6 Airbags (Dual Front, Side & Full-Length Curtain)",
            "image_url": "/static/images/honda_civic_rs.jpg",
            "tagline": "176 HP Motorsport Breed with Full Honda SENSING Suite",
            "description": "The apex predator of Pakistan's sedan sector: 176 HP Turbo, full autonomous Honda SENSING ADAS suite, 17-inch Matte Black alloys, RS aero kit, and 6 safety airbags.",
            "features": json.dumps([
                "Honda SENSING Suite (CMBS, LKAS, RDM, ACC with LSF, AHB)",
                "176 HP High-Output 1.5L VTEC Turbo Engine",
                "6 Full SRS Airbags",
                "17-inch Matte Black RS Alloy Wheels & Dual Exhaust",
                "Sport Mode Drive Selector & Black Suede Leather Interior"
            ]),
            "is_active": 1
        },

        # --- 3. HONDA HR-V LINEUP ---
        {
            "slug": "honda-hr-v-vti-s",
            "name": "Honda HR-V VTi-S",
            "category": "Honda HR-V",
            "price": 7299000,
            "stock": 3,
            "colors": json.dumps(["Ignite Red Metallic"]),
            "horsepower": "119 HP @ 6,600 RPM",
            "torque": "145 Nm @ 4,300 RPM",
            "transmission": "CVT (Continuous Variable Transmission)",
            "fuel_economy": "13-16 KM/L",
            "boot_capacity": "319 Liters",
            "airbags": "4 Airbags (Dual Front + Side Airbags)",
            "image_url": "/static/images/honda_hrv_vtis.jpg",
            "tagline": "Modern High-Riding Urban Crossover Architecture",
            "description": "The HR-V VTi-S marries crossover ground clearance with coupe silhouette design, wireless mobile charging, and versatile Honda Magic Seats.",
            "features": json.dumps([
                "Coupe-Inspired High Ground Clearance Crossover",
                "Versatile Honda Ultra / Magic Seats (Utility, Tall, Long modes)",
                "Full LED Headlights with LED Fog Lamps",
                "Wireless Smartphone Charger",
                "Hill Descent Control (HDC)"
            ]),
            "is_active": 1
        },
        {
            "slug": "honda-hr-v-ehev-hybrid",
            "name": "Honda HR-V e:HEV (Hybrid)",
            "category": "Honda HR-V",
            "price": 9299000,
            "stock": 2,
            "colors": json.dumps(["Platinum White Pearl"]),
            "horsepower": "129 HP Combined (105 HP Atkinson + 131 HP Motor)",
            "torque": "253 Nm (Instant Electric Drive Motor)",
            "transmission": "E-CVT (Dual-Motor Electric Variable Drive)",
            "fuel_economy": "22-26 KM/L (Self-Charging Hybrid)",
            "boot_capacity": "304 Liters",
            "airbags": "6 Airbags + Honda SENSING Suite",
            "image_url": "/static/images/honda_hrv_hybrid.jpg",
            "tagline": "Ultra-Efficient Dual-Motor Hybrid with 253 Nm Instant Torque",
            "description": "Pakistan's leading Japanese hybrid crossover: 22-26 KM/L real-world fuel economy, instant electric acceleration with 253 Nm torque, and complete Honda SENSING safety shield.",
            "features": json.dumps([
                "e:HEV Dual-Motor Intelligent Self-Charging Hybrid System",
                "Real-World 22-26 KM/L Super Mileage in City Traffic",
                "253 Nm Instant Electric Torque",
                "Honda SENSING Suite + Deceleration Paddle Selectors",
                "Hands-Free Power Tailgate with Walk-Away Close"
            ]),
            "is_active": 1
        }
    ]

    for car in official_cars:
        cursor.execute("""
        INSERT INTO cars (
            slug, name, category, price, stock, colors,
            horsepower, torque, transmission, fuel_economy,
            boot_capacity, airbags, image_url, tagline,
            description, features, is_active
        ) VALUES (
            :slug, :name, :category, :price, :stock, :colors,
            :horsepower, :torque, :transmission, :fuel_economy,
            :boot_capacity, :airbags, :image_url, :tagline,
            :description, :features, :is_active
        )
        """, car)


# ---------------- DATA ACCESS HELPERS ----------------

def get_all_cars(only_active: bool = False) -> List[Dict[str, Any]]:
    """Retrieves all vehicles with parsed JSON attributes and real-time status labels."""
    conn = get_db_connection()
    cursor = conn.cursor()
    query = "SELECT * FROM cars"
    if only_active:
        query += " WHERE is_active = 1"
    query += " ORDER BY price ASC"
    cursor.execute(query)
    rows = cursor.fetchall()
    conn.close()

    cars = []
    for r in rows:
        car = dict(r)
        car["colors"] = json.loads(car["colors"]) if isinstance(car["colors"], str) else car["colors"]
        car["features"] = json.loads(car["features"]) if isinstance(car["features"], str) else car["features"]
        
        # Real-time stock status badge logic
        if car["stock"] >= 3:
            car["stock_status"] = "In-Stock"
            car["stock_class"] = "emerald"
        elif car["stock"] > 0:
            car["stock_status"] = f"Low Stock ({car['stock']} left)"
            car["stock_class"] = "amber"
        else:
            car["stock_status"] = "Sold Out"
            car["stock_class"] = "rose"

        # Formatted price
        car["formatted_price"] = f"PKR {car['price']:,}"
        cars.append(car)
    return cars


def get_car_by_slug(slug: str) -> Optional[Dict[str, Any]]:
    """Finds a vehicle by its unique slug."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM cars WHERE slug = ?", (slug,))
    row = cursor.fetchone()
    conn.close()
    if not row:
        return None
    car = dict(row)
    car["colors"] = json.loads(car["colors"])
    car["features"] = json.loads(car["features"])
    car["formatted_price"] = f"PKR {car['price']:,}"
    return car


def get_car_by_id(car_id: int) -> Optional[Dict[str, Any]]:
    """Finds a vehicle by its primary key."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM cars WHERE id = ?", (car_id,))
    row = cursor.fetchone()
    conn.close()
    if not row:
        return None
    car = dict(row)
    car["colors"] = json.loads(car["colors"])
    car["features"] = json.loads(car["features"])
    car["formatted_price"] = f"PKR {car['price']:,}"
    return car


def update_car_inventory(car_id: int, stock: int, price: Optional[int] = None, is_active: Optional[int] = None) -> bool:
    """Updates stock, price, and active status for administrative controller."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    fields = ["stock = ?", "updated_at = CURRENT_TIMESTAMP"]
    params = [stock]

    if price is not None:
        fields.append("price = ?")
        params.append(price)

    if is_active is not None:
        fields.append("is_active = ?")
        params.append(is_active)

    params.append(car_id)
    query = f"UPDATE cars SET {', '.join(fields)} WHERE id = ?"
    cursor.execute(query, params)
    conn.commit()
    rows_affected = cursor.rowcount
    conn.close()
    return rows_affected > 0


def create_lead(lead_data: Dict[str, Any]) -> int:
    """Stores a qualified customer lead or test drive booking in the CRM database."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO leads (
        name, phone, email, city, car_model, dealership,
        preferred_date, preferred_time, source, status, notes
    ) VALUES (
        :name, :phone, :email, :city, :car_model, :dealership,
        :preferred_date, :preferred_time, :source, :status, :notes
    )
    """, {
        "name": lead_data.get("name", "Valued Customer"),
        "phone": lead_data.get("phone", ""),
        "email": lead_data.get("email", ""),
        "city": lead_data.get("city", "Lahore"),
        "car_model": lead_data.get("car_model", "Honda Civic"),
        "dealership": lead_data.get("dealership", "Honda Fort Lahore"),
        "preferred_date": lead_data.get("preferred_date", ""),
        "preferred_time": lead_data.get("preferred_time", ""),
        "source": lead_data.get("source", "Web Concierge"),
        "status": lead_data.get("status", "New"),
        "notes": lead_data.get("notes", "")
    })
    lead_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return lead_id


def get_all_leads() -> List[Dict[str, Any]]:
    """Retrieves all customer leads sorted by most recent."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM leads ORDER BY created_at DESC")
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]


def update_lead_status(lead_id: int, status: str) -> bool:
    """Updates CRM lead workflow status."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE leads SET status = ? WHERE id = ?", (status, lead_id))
    conn.commit()
    affected = cursor.rowcount
    conn.close()
    return affected > 0


def get_dashboard_metrics() -> Dict[str, Any]:
    """Computes real-time executive inventory valuation and CRM pipeline statistics."""
    conn = get_db_connection()
    cursor = conn.cursor()

    # Total inventory units & valuation
    cursor.execute("SELECT SUM(stock) as total_units, SUM(stock * price) as fleet_valuation, COUNT(*) as model_count FROM cars")
    inv_data = cursor.fetchone()

    # Total leads count & status breakdown
    cursor.execute("SELECT COUNT(*) as total_leads FROM leads")
    total_leads = cursor.fetchone()["total_leads"]

    cursor.execute("SELECT status, COUNT(*) as count FROM leads GROUP BY status")
    lead_status_breakdown = {row["status"]: row["count"] for row in cursor.fetchall()}

    # Low stock count
    cursor.execute("SELECT COUNT(*) as low_stock_count FROM cars WHERE stock <= 2 AND stock > 0")
    low_stock_count = cursor.fetchone()["low_stock_count"]

    conn.close()

    total_units = inv_data["total_units"] or 0
    fleet_valuation = inv_data["fleet_valuation"] or 0

    return {
        "total_units": total_units,
        "fleet_valuation": fleet_valuation,
        "formatted_valuation": f"PKR {fleet_valuation:,}",
        "model_count": inv_data["model_count"],
        "total_leads": total_leads,
        "low_stock_count": low_stock_count,
        "lead_status_breakdown": lead_status_breakdown
    }


def log_chat_interaction(session_id: str, role: str, message: str, language: str = "en"):
    """Persists chat transcripts for behavioral analytics and lead conversion tracking."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO chat_logs (session_id, role, message, language)
    VALUES (?, ?, ?, ?)
    """, (session_id, role, message, language))
    conn.commit()
    conn.close()


# Initialize database automatically when imported
init_db()
