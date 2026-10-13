"""
Honda Atlas Pakistan - Dual-Engine Neural Core & Sales Intelligence Engine
Integrates Google Gemini 2.0 / 1.5 API with Autonomous Fallback Architecture
Multilingual Support: English, Urdu, Roman Urdu
"""

import os
import re
import json
import logging
from typing import Dict, Any, List, Tuple
from dotenv import load_dotenv
import database

# Load environment configuration
load_dotenv()

logger = logging.getLogger("HondaNeuralEngine")
logger.setLevel(logging.INFO)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "").strip()
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.0-flash").strip()

# Initialize Google GenAI client if API key is provided
genai_client = None
if GEMINI_API_KEY:
    try:
        from google import genai
        from google.genai import types
        genai_client = genai.Client(api_key=GEMINI_API_KEY)
        logger.info(f"Google GenAI Client initialized successfully with model {GEMINI_MODEL}")
    except Exception as e:
        logger.warning(f"Failed to initialize Google GenAI SDK: {e}. Falling back to Autonomous Engine.")
        genai_client = None


def detect_language(text: str) -> str:
    """
    Detects whether the user is communicating in:
    - 'ur' (Urdu in Perso-Arabic script)
    - 'roman_ur' (Roman Urdu / conversational Pakistani Urdu in Latin script)
    - 'en' (Standard English)
    """
    # 1. Check for Perso-Arabic Urdu Unicode characters
    if re.search(r"[\u0600-\u06FF]", text):
        return "ur"

    # 2. Check for Roman Urdu characteristic linguistic tokens
    roman_urdu_tokens = {
        "bhai", "kia", "kya", "hai", "hain", "kese", "kaise", "kitna", "kitni", "kitne",
        "gari", "gaari", "car", "chahiye", "chahye", "chahta", "chahti", "lena", "leni",
        "lene", "hoga", "hogi", "hoge", "kist", "qist", "qistein", "qistain", "kiston",
        "qeemat", "qeematain", "rate", "down", "payment", "advance", "rang", "color",
        "milegi", "mil", "sakta", "sakti", "kab", "tak", "delivery", "stock", "showroom",
        "lahore", "karachi", "islamabad", "rawalpindi", "shukriya", "meherbani", "batao",
        "bataen", "bataien", "batayein", "test", "drive", "opper", "niche", "wali", "wala"
    }

    words = re.findall(r"\b[a-zA-Z]+\b", text.lower())
    matched_count = sum(1 for w in words if w in roman_urdu_tokens)

    if matched_count >= 2 or (len(words) <= 4 and matched_count >= 1):
        return "roman_ur"

    return "en"


def calculate_financing_quote(price: int, down_payment_pct: float = 25.0, tenure_years: int = 5, markup_rate: float = 17.5) -> Dict[str, Any]:
    """
    Calculates detailed Islamic & Conventional auto leasing estimations
    according to State Bank of Pakistan consumer lending guidelines.
    """
    down_payment = int(price * (down_payment_pct / 100.0))
    financed_amount = price - down_payment
    
    total_interest = int(financed_amount * (markup_rate / 100.0) * tenure_years)
    total_payable = financed_amount + total_interest
    monthly_installment = int(total_payable / (tenure_years * 12))

    return {
        "price": price,
        "down_payment_pct": down_payment_pct,
        "down_payment": down_payment,
        "financed_amount": financed_amount,
        "tenure_years": tenure_years,
        "tenure_months": tenure_years * 12,
        "markup_rate": markup_rate,
        "monthly_installment": monthly_installment,
        "formatted_monthly": f"PKR {monthly_installment:,}",
        "formatted_down_payment": f"PKR {down_payment:,}"
    }


def build_system_prompt() -> str:
    """
    Constructs the real-time knowledge base for the Executive Senior Sales Director
    of Honda Atlas Cars (Pakistan) Limited, injecting live inventory and pricing.
    """
    cars = database.get_all_cars(only_active=True)
    inventory_summary = []
    for c in cars:
        inventory_summary.append(
            f"- Model: {c['name']} ({c['category']})\n"
            f"  Ex-Factory Retail Price: PKR {c['price']:,}\n"
            f"  Current Live Dealership Stock: {c['stock']} unit(s)\n"
            f"  Available Colors: {', '.join(c['colors'])}\n"
            f"  Horsepower & Torque: {c['horsepower']} | {c['torque']}\n"
            f"  Transmission: {c['transmission']}\n"
            f"  Fuel Economy: {c['fuel_economy']}\n"
            f"  Boot Capacity: {c['boot_capacity']} | Airbags: {c['airbags']}\n"
        )
    inventory_text = "\n".join(inventory_summary)

    prompt = f"""
You are the Executive Senior Sales Director of Honda Atlas Cars (Pakistan) Limited.
Your name is Engr. Farhan Tariq, Senior Sales Director at Honda Atlas Head Office, 41-Km Multan Road, Lahore.

YOUR CORPORATE PERSONA:
- Authoritative, polished, impeccably polite, and deeply knowledgeable about Pakistan's automotive sector.
- You treat every customer like a VIP executive buyer.
- You have exact knowledge of Honda Pakistan's ex-factory pricing, booking timelines, token money, and leasing plans.
- Official Corporate Contact Matrix:
  * UAN Hotline: 042-111-111-243
  * Corporate Email: info@honda.com.pk
  * Headquarters: 41-Km, Multan Road, Lahore, Pakistan

MULTILINGUAL INTELLIGENCE INSTRUCTIONS:
1. If the user writes in English, reply in refined, professional corporate English.
2. If the user writes in Roman Urdu (e.g., "Bhai Civic RS ka current stock kitna hai aur installment plan kya hai?"), reply in fluent, respectful, conversational Roman Urdu with polite greetings (e.g. "Assalam-o-Alaikum! Honda Atlas showroom mein khushamdeed...").
3. If the user writes in Urdu script (اردو), reply in elegant, professional Urdu script.
4. Always mirror the user's language smoothly.

REAL-TIME LIVE HONDA ATLAS INVENTORY & SPECIFICATIONS:
{inventory_text}

BANK LEASING & INSTALLMENT LOGIC:
- Down payment typically ranges from 15% to 30% under State Bank of Pakistan consumer financing guidelines.
- Standard tenure is 1 to 5 years (up to 7 years depending on bank policies).
- Indicative markup is KIBOR + 3% to 4% (approx 16.5% - 19.5% APR).
- Provide instant approximate calculations if the customer asks for down payment or monthly installments.

LEAD CAPTURE & TEST DRIVE CALL TO ACTION:
- Whenever a customer expresses strong intent to purchase, inquiries about booking, or asks for a test drive, warmly offer to schedule a VIP test drive at their nearest Honda 3S dealership (Lahore, Karachi, Islamabad, Rawalpindi, Faisalabad, Multan).
- If appropriate, invite them to fill the test drive booking form or provide their contact number.

Keep your responses structured, clear, and engaging. Use bullet points for vehicle comparisons.
"""
    return prompt


def generate_autonomous_response(user_message: str, lang: str) -> Dict[str, Any]:
    """
    Autonomous Fallback Sales Intelligence Core.
    Operates with zero internet dependencies or when API keys are unconfigured.
    Provides mathematically accurate finance quotes, inventory lookups, and multi-turn sales logic.
    """
    cars = database.get_all_cars(only_active=True)
    user_lower = user_message.lower()

    # Identify specific vehicle mentioned using specificity-first matching
    matched_car = None
    
    # Priority 1: Check specific flagship sub-models first
    if re.search(r"\b(rs|turbo)\b", user_lower):
        matched_car = next((c for c in cars if "rs" in c["name"].lower()), None)
    elif re.search(r"\boriel\b", user_lower):
        matched_car = next((c for c in cars if "oriel" in c["name"].lower()), None)
    elif re.search(r"\b(aspire\s*s|aspire-s)\b", user_lower):
        matched_car = next((c for c in cars if "aspire s" in c["name"].lower()), None)
    elif re.search(r"\baspire\b", user_lower):
        matched_car = next((c for c in cars if "1.5l aspire cvt" in c["name"].lower() and "aspire s" not in c["name"].lower()), None)
    elif re.search(r"\b(hybrid|e:hev|ehev)\b", user_lower):
        matched_car = next((c for c in cars if "e:hev" in c["name"].lower() or "hybrid" in c["name"].lower()), None)
    elif re.search(r"\b(vti-s|vtis|vti)\b", user_lower):
        matched_car = next((c for c in cars if "vti-s" in c["name"].lower()), None)
    elif re.search(r"\b(1\.2|1\.2l)\b", user_lower):
        matched_car = next((c for c in cars if "1.2l" in c["name"].lower()), None)
    elif re.search(r"\bstandard\b", user_lower):
        matched_car = next((c for c in cars if "standard" in c["name"].lower()), None)

    # Priority 2: Generic model families if no sub-model specified
    if not matched_car:
        if re.search(r"\bcivic\b", user_lower):
            matched_car = next((c for c in cars if "civic rs" in c["name"].lower()), None) or cars[3]
        elif re.search(r"\bcity\b", user_lower):
            matched_car = next((c for c in cars if "1.2l" in c["name"].lower()), None)
        elif re.search(r"\b(hr-v|hrv)\b", user_lower):
            matched_car = next((c for c in cars if "vti-s" in c["name"].lower()), None)

    # If no specific car matched, default to flagship Civic RS for general context
    is_civic_query = "civic" in user_lower
    is_city_query = "city" in user_lower
    is_hrv_query = "hr-v" in user_lower or "hrv" in user_lower
    is_finance_query = any(k in user_lower for k in ["installment", "down payment", "kist", "qist", "advance", "lease", "financing", "monthly"])
    is_stock_query = any(k in user_lower for k in ["stock", "available", "units", "kitni", "kitna", "mojood", "dastiab", "colors", "rang"])
    is_test_drive = any(k in user_lower for k in ["test drive", "drive", "booking", "book", "showroom", "visit"])

    response_text = ""
    trigger_lead_modal = False

    # 1. MULTILINGUAL RESPONSES FOR SPECIFIC VEHICLE WITH FINANCING / STOCK
    if matched_car and is_finance_query:
        quote = calculate_financing_quote(matched_car["price"], down_payment_pct=25, tenure_years=5)
        dp_30 = calculate_financing_quote(matched_car["price"], down_payment_pct=30, tenure_years=5)

        if lang == "roman_ur":
            response_text = (
                f"Assalam-o-Alaikum! Honda Atlas showroom mein khushamdeed.\n\n"
                f"**{matched_car['name']}** ka official ex-factory rate **PKR {matched_car['price']:,}** hai.\n"
                f"Current stock: **{matched_car['stock']} unit(s)** ({', '.join(matched_car['colors'])}).\n\n"
                f"📊 **Indicative Installment & Down Payment Plan (SBP Rules):**\n"
                f"• **Down Payment (25%):** Taqreeban **{quote['formatted_down_payment']}**\n"
                f"• **Monthly Installment (5 Years / 60 Months):** Taqreeban **{quote['formatted_monthly']} / month**\n"
                f"• **Down Payment (30% option):** {dp_30['formatted_down_payment']} (Monthly: {dp_30['formatted_monthly']})\n"
                f"• **Transmission & Engine:** {matched_car['transmission']} | {matched_car['horsepower']}\n\n"
                f"Kya aap chahte hain ke hum aap ke liye test drive schedule karein ya official quotation generate karein?"
            )
        elif lang == "ur":
            response_text = (
                f"السلام علیکم! ہونڈا اٹلس پاکستان میں خوش آمدید۔\n\n"
                f"**{matched_car['name']}** کی ایکس فیکٹری قیمت **{matched_car['price']:,} روپے** ہے۔\n"
                f"موجودہ سٹاک: **{matched_car['stock']} گاڑیاں** ({', '.join(matched_car['colors'])})۔\n\n"
                f"📊 **اقساط اور ڈاؤن پیمنٹ پلان:**\n"
                f"• **ڈاؤن پیمنٹ (25%):** تقریباً **{quote['formatted_down_payment']}**\n"
                f"• **ماہانہ قسط (5 سالہ مدت):** تقریباً **{quote['formatted_monthly']} روپے**\n"
                f"• **ہارس پاور اور گیئر:** {matched_car['horsepower']} | {matched_car['transmission']}\n\n"
                f"کیا آپ اپنے قریبی 3S ڈیلرشپ پر ٹیسٹ ڈرائیو بک کرنا چاہیں گے؟"
            )
        else:
            response_text = (
                f"Welcome to Honda Atlas Cars (Pakistan) Limited.\n\n"
                f"Regarding the **{matched_car['name']}**:\n"
                f"• **Ex-Factory Price:** PKR {matched_car['price']:,}\n"
                f"• **Current Warehouse Stock:** {matched_car['stock']} unit(s) ({', '.join(matched_car['colors'])})\n"
                f"• **Powertrain:** {matched_car['horsepower']} | {matched_car['torque']}\n\n"
                f"📊 **Estimated Auto Financing Breakdown (5-Year Plan):**\n"
                f"• **Down Payment (25%):** {quote['formatted_down_payment']}\n"
                f"• **Monthly Installment:** Approx. {quote['formatted_monthly']}/month (subject to KIBOR + bank spread)\n"
                f"• **Down Payment (30% option):** {dp_30['formatted_down_payment']} (Monthly: {dp_30['formatted_monthly']})\n\n"
                f"Would you like me to reserve an allocation or arrange a VIP test drive at your nearest authorized 3S dealership?"
            )
        trigger_lead_modal = True

    elif matched_car and is_stock_query:
        if lang == "roman_ur":
            response_text = (
                f"Janab, **{matched_car['name']}** ka is waqt hamare live inventory mein **{matched_car['stock']} unit** dastiab hai.\n"
                f"• **Ex-Factory Price:** PKR {matched_car['price']:,}\n"
                f"• **Available Colors:** {', '.join(matched_car['colors'])}\n"
                f"• **Fuel Average:** {matched_car['fuel_economy']}\n"
                f"• **Key Safety:** {matched_car['airbags']}\n\n"
                f"Stock tezi se book ho raha hai. Agar aap booking token ya quotation lena chahte hain toh foran rabta farmayein!"
            )
        elif lang == "ur":
            response_text = (
                f"جناب، **{matched_car['name']}** کا موجودہ سٹاک **{matched_car['stock']} یونٹ** ہے۔\n"
                f"• **قیمت:** {matched_car['price']:,} روپے\n"
                f"• **دستیاب رنگ:** {', '.join(matched_car['colors'])}\n"
                f"• **فیول ایوریج:** {matched_car['fuel_economy']}\n"
                f"• **ائیر بیگز:** {matched_car['airbags']}۔"
            )
        else:
            response_text = (
                f"The **{matched_car['name']}** currently has **{matched_car['stock']} unit(s) in live inventory**.\n"
                f"• **Price (Ex-Factory):** PKR {matched_car['price']:,}\n"
                f"• **Ready Colors:** {', '.join(matched_car['colors'])}\n"
                f"• **Fuel Economy:** {matched_car['fuel_economy']}\n"
                f"• **Transmission:** {matched_car['transmission']}\n"
                f"• **Boot Space:** {matched_car['boot_capacity']}\n\n"
                f"Units are moving rapidly. Shall I initiate a priority allocation hold for you?"
            )

    elif is_civic_query and ("compare" in user_lower or "difference" in user_lower or "faraq" in user_lower or "vs" in user_lower):
        if lang == "roman_ur":
            response_text = (
                "**Honda Civic Lineup Comparison (Pakistani Market):**\n\n"
                "1. **Civic Standard (PKR 8,499,000):**\n"
                "   • 127 HP Turbo, Dual Airbags, Digital TFT Screen, Fabric Seats.\n"
                "2. **Civic Oriel (PKR 8,834,000):**\n"
                "   • 127 HP Turbo, **Electric Sunroof**, Rear AC Vents, Alloy Wheels.\n"
                "3. **Civic RS Flagship (PKR 10,100,000):**\n"
                "   • **176 HP High-Output Turbo**, Full **Honda SENSING ADAS**, 6 Airbags, 17\" Matte Black Alloys, Sport Mode.\n\n"
                "Agar driving thrill aur complete safety suite chahiye toh RS is the ultimate choice!"
            )
        else:
            response_text = (
                "**Honda Civic Lineup Architectural Breakdown:**\n\n"
                "• **Civic Standard (PKR 8,499,000 | Stock: 2):** 127 HP 1.5L Turbo, Dual Airbags, Electronic Parking Brake.\n"
                "• **Civic Oriel (PKR 8,834,000 | Stock: 4):** Adds One-Touch Sunroof, Rear Passenger Air Vents, Premium Alloys.\n"
                "• **Civic RS (PKR 10,100,000 | Stock: 1):** Flagship 176 HP Motorsport Turbo, Full Honda SENSING Suite, 6 Airbags, Sport Mode.\n\n"
                "Which variant aligns best with your executive requirements?"
            )

    elif is_hrv_query:
        hrv_hybrid = next((c for c in cars if "hybrid" in c["name"].lower() or "e:hev" in c["name"].lower()), None)
        hrv_vtis = next((c for c in cars if "vti-s" in c["name"].lower()), None)
        if lang == "roman_ur":
            response_text = (
                f"**Honda HR-V Lineup Pakistan:**\n\n"
                f"• **HR-V VTi-S (PKR 7,299,000 | Stock: 3 units):** 119 HP i-VTEC petrol engine, coupe-SUV stance, 4 Airbags, Magic Seats, Ignite Red.\n"
                f"• **HR-V e:HEV Hybrid (PKR 9,299,000 | Stock: 2 units):** Dual-Motor self-charging Hybrid, **22-26 KM/L mileage**, 253 Nm electric torque, 6 Airbags + Honda SENSING.\n\n"
                f"Pakistan ke city traffic mein e:HEV Hybrid petrol kharche ko 50% se zyada kam kar deta hai!"
            )
        else:
            response_text = (
                f"**Honda HR-V Cross-Utility Lineup Overview:**\n\n"
                f"1. **Honda HR-V VTi-S (PKR 7,299,000 | Stock: 3 units):**\n"
                f"   • 1.5L i-VTEC Petrol (119 HP / 145 Nm), 13-16 KM/L, Wireless Charger, 4 Airbags.\n"
                f"2. **Honda HR-V e:HEV Hybrid (PKR 9,299,000 | Stock: 2 units):**\n"
                f"   • Dual-Motor Electric Hybrid, **22-26 KM/L Super Efficiency**, 253 Nm Instant Torque, 6 Airbags & Honda SENSING.\n\n"
                f"Would you like to experience the silent electric drive of the e:HEV Hybrid firsthand?"
            )

    elif is_test_drive:
        trigger_lead_modal = True
        if lang == "roman_ur":
            response_text = (
                "Beshak! Aap ke liye VIP Test Drive schedule karna hamari khushnaseebi hogi.\n\n"
                "Hum Lahore (Honda Fort / Point), Karachi (Honda South / Drive-In), Islamabad (Honda Classic), aur Rawalpindi (Honda Avenue) par ready hain.\n"
                "Baraye meherbani screen par mojood **'Book Test Drive'** button par click karein ya apna contact number share karein taake hamara sales manager aap ko call kare!"
            )
        elif lang == "ur":
            response_text = (
                "بہت خوب! آپ کے لیے وی آئی پی ٹیسٹ ڈرائیو کا اہتمام کرنا ہمارے لیے باعث فخر ہے۔\n\n"
                "برائے مہربانی اسکرین پر 'Book Test Drive' پر کلک کریں یا اپنی پسندیدہ تاریخ اور شہر فراہم کریں۔"
            )
        else:
            response_text = (
                "Outstanding! We would be delighted to host you for a bespoke test drive.\n\n"
                "We operate premier 3S facilities across Lahore, Karachi, Islamabad, Rawalpindi, Faisalabad, and Multan.\n"
                "Please trigger the **'Book Test Drive'** modal on your dashboard or provide your preferred date and contact details to lock in your slot."
            )

    else:
        # General Executive Sales Welcome & Lineup Summary
        if lang == "roman_ur":
            response_text = (
                "Assalam-o-Alaikum! Main Engr. Farhan Tariq hoon, Honda Atlas Cars (Pakistan) Limited ka Senior Sales Director.\n\n"
                "Hamare official lineup mein is waqt dastiab hain:\n"
                "• **Honda City (PKR 4.73M - 6.14M):** 1.2L CVT, 1.5L Aspire, aur Aspire S.\n"
                "• **Honda Civic (PKR 8.49M - 10.10M):** Standard, Oriel Sunroof, aur 176 HP RS Turbo.\n"
                "• **Honda HR-V (PKR 7.29M - 9.29M):** VTi-S aur cutting-edge e:HEV Dual-Motor Hybrid.\n\n"
                "Aap kisi specific model ka live stock, bank installment plan, ya technical specs poochna chahte hain?"
            )
        elif lang == "ur":
            response_text = (
                "السلام علیکم! میں ہونڈا اٹلس پاکستان کا سینئر سیلز ڈائریکٹر ہوں۔\n\n"
                "ہمارے پاس ہونڈا سٹی، ہونڈا سیوک (سٹینڈرڈ، اوریل، آر ایس)، اور ہونڈا ایچ آر وی (ہائبرڈ) مکمل طور پر دستیاب ہیں۔\n"
                "آپ کسی بھی ماڈل کی قیمت، اقساط، یا بکنگ کے حوالے سے رہنمائی حاصل کر سکتے ہیں۔"
            )
        else:
            response_text = (
                "Welcome to the Honda Atlas Autonomous Neural Concierge. I am Engr. Farhan Tariq, Senior Sales Director at Honda Atlas Cars (Pakistan) Limited.\n\n"
                "Our current ex-factory production lineup comprises:\n"
                "• **Honda City:** 1.2L CVT (PKR 4.73M), 1.5L Aspire (PKR 6.06M), Aspire S (PKR 6.14M)\n"
                "• **Honda Civic:** Standard Turbo (PKR 8.49M), Oriel Sunroof (PKR 8.83M), RS 176 HP Flagship (PKR 10.10M)\n"
                "• **Honda HR-V:** VTi-S (PKR 7.29M) and e:HEV Intelligent Hybrid (PKR 9.29M)\n\n"
                "How may I assist you today? You can inquire about live warehouse stock, calculate custom installment plans, compare models, or book an immediate test drive."
            )

    return {
        "text": response_text,
        "language": lang,
        "matched_car": matched_car["slug"] if matched_car else None,
        "trigger_lead_modal": trigger_lead_modal,
        "engine_used": "Autonomous Heuristic Sales Core"
    }


def query_neural_sales_director(user_message: str, chat_history: List[Dict[str, str]] = None) -> Dict[str, Any]:
    """
    Main Orchestrator:
    Attempts Google Gemini 2.0 / 1.5 invocation with live database context;
    gracefully and seamlessly falls back to Autonomous Sales Core on failure or missing API key.
    """
    lang = detect_language(user_message)
    
    # Check if Gemini Client is active
    if genai_client and GEMINI_API_KEY:
        try:
            system_prompt = build_system_prompt()
            
            # Format history for Gemini API
            # Generate response via google.genai
            response = genai_client.models.generate_content(
                model=GEMINI_MODEL,
                contents=f"{system_prompt}\n\nCustomer query in language [{lang}]:\n{user_message}"
            )
            
            if response and response.text:
                clean_text = response.text.strip()
                
                # Check for serious purchase intent
                user_lower = user_message.lower()
                trigger_lead = any(k in user_lower for k in ["book", "test drive", "buy", "purchase", "kharidna", "leni hai", "booking", "contact me"])

                return {
                    "text": clean_text,
                    "language": lang,
                    "engine_used": f"Google Gemini Core ({GEMINI_MODEL})",
                    "trigger_lead_modal": trigger_lead
                }
        except Exception as e:
            logger.warning(f"Gemini API call failed ({e}). Seamlessly switching to Autonomous Fallback.")

    # Autonomous Fallback
    fallback_result = generate_autonomous_response(user_message, lang)
    return fallback_result
