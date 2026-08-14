from flask import Flask, render_template, request, jsonify
from pathlib import Path
import sqlite3
import sys


# ============================================================
# APPLICATION SETUP
# ============================================================

BASE_DIR = Path(__file__).resolve().parent

if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))


# ============================================================
# EXISTING CHATBOT MODULES
# ============================================================

from chatbot import (
    load_model,
    predict_with_confidence,
    detect_specialty,
    search_hospitals,
    DATABASE_PATH,
    INTENT_MODEL,
    CONDITION_MODEL,
    CONFIDENCE_THRESHOLD
)

from severity_checker import check_severity


app = Flask(__name__)


# ============================================================
# APPLICATION INFORMATION
# ============================================================

APP_NAME = "Ballari Medical Assistant"
APP_VERSION = "2.0"


# ============================================================
# SYMPTOM GUIDANCE
#
# NOTE:
# This application provides educational information only.
# It does not diagnose diseases or prescribe medicines.
# ============================================================

SYMPTOM_GUIDANCE = {

    "fever": {
        "specialty": "General Medicine",
        "category": "general",
        "guidance": (
            "Fever can have many causes. Rest, drink adequate fluids "
            "and monitor your temperature. If the fever is persistent, "
            "very high, worsening, or accompanied by concerning symptoms, "
            "please consult a qualified healthcare professional."
        )
    },

    "temperature": {
        "specialty": "General Medicine",
        "category": "general",
        "guidance": (
            "An elevated temperature can occur for many reasons. "
            "Monitor your temperature and other symptoms. "
            "Seek medical advice if it persists, becomes severe, "
            "or is associated with concerning symptoms."
        )
    },

    "cough": {
        "specialty": "General Medicine",
        "category": "general",
        "guidance": (
            "Cough can have many causes. A general physician can "
            "assess how long it has been present and whether other "
            "symptoms are occurring."
        )
    },

    "cold": {
        "specialty": "General Medicine",
        "category": "general",
        "guidance": (
            "Cold-like symptoms are commonly evaluated by a general "
            "physician, especially when symptoms persist or become severe."
        )
    },

    "skin": {
        "specialty": "Dermatology",
        "category": "skin",
        "guidance": (
            "Skin symptoms such as rashes, itching, acne, swelling "
            "or changes in the skin can have different causes. "
            "A dermatologist can examine the affected area."
        )
    },

    "rash": {
        "specialty": "Dermatology",
        "category": "skin",
        "guidance": (
            "A rash can have several possible causes. A dermatologist "
            "can evaluate its appearance, location and duration."
        )
    },

    "itching": {
        "specialty": "Dermatology",
        "category": "skin",
        "guidance": (
            "Persistent or unexplained itching should be evaluated "
            "by a qualified healthcare professional, particularly "
            "if it is spreading or associated with other symptoms."
        )
    },

    "acne": {
        "specialty": "Dermatology",
        "category": "skin",
        "guidance": (
            "Acne can have several contributing factors. A dermatologist "
            "can recommend an appropriate evaluation and treatment plan."
        )
    },

    "skin infection": {
        "specialty": "Dermatology",
        "category": "skin",
        "guidance": (
            "Possible skin infections should be assessed by a qualified "
            "healthcare professional, especially when there is increasing "
            "redness, swelling, pain, discharge or fever."
        )
    },

    "eye": {
        "specialty": "Ophthalmology",
        "category": "eye",
        "guidance": (
            "Eye symptoms or changes in vision should be evaluated by "
            "an eye-care professional, particularly when symptoms are "
            "persistent or sudden."
        )
    },

    "vision": {
        "specialty": "Ophthalmology",
        "category": "eye",
        "guidance": (
            "Changes in vision can have different causes. An ophthalmologist "
            "can perform an appropriate eye examination."
        )
    },

    "blurred vision": {
        "specialty": "Ophthalmology",
        "category": "eye",
        "guidance": (
            "Blurred vision should be evaluated by an eye-care professional. "
            "Sudden changes in vision require prompt medical assessment."
        )
    },

    "eye pain": {
        "specialty": "Ophthalmology",
        "category": "eye",
        "guidance": (
            "Eye pain can have several causes and should be evaluated by "
            "an eye-care professional, particularly when severe or sudden."
        )
    },

    "ear": {
        "specialty": "ENT",
        "category": "ent",
        "guidance": (
            "Persistent ear symptoms, hearing changes or ear pain "
            "can be evaluated by an ENT specialist."
        )
    },

    "throat": {
        "specialty": "ENT",
        "category": "ent",
        "guidance": (
            "Persistent throat symptoms can be evaluated by a general "
            "physician or ENT specialist."
        )
    },

    "joint": {
        "specialty": "Orthopaedics",
        "category": "orthopaedics",
        "guidance": (
            "Persistent joint pain or movement problems can be "
            "evaluated by an orthopaedic specialist."
        )
    },

    "bone": {
        "specialty": "Orthopaedics",
        "category": "orthopaedics",
        "guidance": (
            "Bone or musculoskeletal problems should be evaluated "
            "by a qualified healthcare professional."
        )
    },

    "tooth": {
        "specialty": "Dental",
        "category": "dental",
        "guidance": (
            "Tooth or gum problems can be evaluated by a dentist."
        )
    },

    "teeth": {
        "specialty": "Dental",
        "category": "dental",
        "guidance": (
            "Dental symptoms should be evaluated by a qualified dentist."
        )
    },

    "pregnancy": {
        "specialty": "Obstetrics & Gynaecology",
        "category": "obstetrics",
        "guidance": (
            "Pregnancy-related concerns should be discussed with "
            "a qualified obstetrician or gynaecologist."
        )
    },

    "chest pain": {
        "specialty": "Cardiology",
        "category": "heart",
        "guidance": (
            "Chest pain can have many causes. If it is severe, sudden, "
            "persistent, or associated with breathing difficulty, sweating, "
            "fainting or pain spreading to the arm, jaw or back, seek "
            "urgent medical attention."
        )
    },

    "heart": {
        "specialty": "Cardiology",
        "category": "heart",
        "guidance": (
            "Heart-related symptoms should be evaluated by a qualified "
            "medical professional. A cardiologist can perform appropriate "
            "cardiac evaluation."
        )
    },

    "palpitations": {
        "specialty": "Cardiology",
        "category": "heart",
        "guidance": (
            "Palpitations can have different causes. A healthcare "
            "professional can assess your symptoms and determine "
            "whether cardiac evaluation is appropriate."
        )
    }
}


# ============================================================
# SPECIALTY ALIASES
#
# These allow the frontend buttons and user messages to use
# different names while the database search uses consistent names.
# ============================================================

SPECIALTY_ALIASES = {

    "skin": "Dermatology",
    "skin problem": "Dermatology",
    "skin problems": "Dermatology",
    "dermatology": "Dermatology",
    "dermatologist": "Dermatology",

    "eye": "Ophthalmology",
    "eye problem": "Ophthalmology",
    "eye problems": "Ophthalmology",
    "eyes": "Ophthalmology",
    "ophthalmology": "Ophthalmology",
    "ophthalmologist": "Ophthalmology",
    "eye specialist": "Ophthalmology",

    "heart": "Cardiology",
    "heart problem": "Cardiology",
    "heart problems": "Cardiology",
    "cardiology": "Cardiology",
    "cardiologist": "Cardiology",
    "heart hospital": "Cardiology",

    "fever": "General Medicine",
    "general": "General Medicine",
    "general medicine": "General Medicine",
    "general physician": "General Medicine",

    "ent": "ENT",
    "ear": "ENT",
    "throat": "ENT",

    "bone": "Orthopaedics",
    "bones": "Orthopaedics",
    "orthopaedics": "Orthopaedics",
    "orthopedics": "Orthopaedics",

    "dental": "Dental",
    "dentist": "Dental",
    "tooth": "Dental",
    "teeth": "Dental",

    "pregnancy": "Obstetrics & Gynaecology",
    "gynaecology": "Obstetrics & Gynaecology",
    "gynecology": "Obstetrics & Gynaecology"
}


# ============================================================
# FEATURES
#
# Used by the Features section in the frontend.
# ============================================================

FEATURES = [

    {
        "icon": "🤖",
        "title": "AI Medical Assistant",
        "description": (
            "Describe symptoms or ask general healthcare questions "
            "and receive educational guidance."
        )
    },

    {
        "icon": "🏥",
        "title": "Ballari Hospital Finder",
        "description": (
            "Browse healthcare facilities available in Ballari "
            "and view hospital contact and service information."
        )
    },

    {
        "icon": "🩺",
        "title": "Specialty Matching",
        "description": (
            "Skin, eye, heart and other health concerns can be "
            "connected with the relevant medical specialty."
        )
    },

    {
        "icon": "🚨",
        "title": "Emergency Awareness",
        "description": (
            "Potential emergency messages can be flagged so that "
            "the user is encouraged to seek immediate medical attention."
        )
    },

    {
        "icon": "👨‍⚕️",
        "title": "Doctor Information",
        "description": (
            "Where available in the project database, hospital "
            "doctor and OPD information can be displayed."
        )
    },

    {
        "icon": "📞",
        "title": "Hospital Contact Details",
        "description": (
            "Hospital phone numbers, emergency contacts, addresses "
            "and timings can be displayed."
        )
    },

    {
        "icon": "🔎",
        "title": "Specialized Hospital Search",
        "description": (
            "Search specifically for Dermatology, Ophthalmology, "
            "Cardiology, General Medicine and other specialties."
        )
    },

    {
        "icon": "🔒",
        "title": "Educational Healthcare Support",
        "description": (
            "The assistant is designed to provide general educational "
            "information and is not a replacement for a doctor."
        )
    }
]


# ============================================================
# GET SYMPTOM GUIDANCE
# ============================================================

def get_symptom_guidance(text):

    normalized = str(text).lower().strip()

    # Check longer phrases first.
    # Example: "chest pain" should be checked before "heart".
    sorted_keywords = sorted(
        SYMPTOM_GUIDANCE.keys(),
        key=len,
        reverse=True
    )

    for keyword in sorted_keywords:

        if keyword in normalized:

            information = SYMPTOM_GUIDANCE[keyword]

            return {
                "keyword": keyword,
                "specialty": information["specialty"],
                "category": information["category"],
                "guidance": information["guidance"]
            }

    return None


# ============================================================
# NORMALIZE SPECIALTY
# ============================================================

def normalize_specialty(specialty):

    if not specialty:
        return None

    value = str(specialty).strip()

    if not value:
        return None

    lower_value = value.lower()

    if lower_value in SPECIALTY_ALIASES:
        return SPECIALTY_ALIASES[lower_value]

    # Handle partial matches.
    for alias, normalized in SPECIALTY_ALIASES.items():

        if alias in lower_value:
            return normalized

    return value


# ============================================================
# DETECT SPECIALTY FROM USER MESSAGE
# ============================================================

def detect_requested_specialty(text):

    normalized = str(text).lower().strip()

    # Strong explicit mappings first.
    keyword_order = [
        "skin problem",
        "skin problems",
        "skin",
        "dermatology",
        "dermatologist",

        "eye problem",
        "eye problems",
        "eye specialist",
        "eye",
        "eyes",
        "ophthalmology",
        "ophthalmologist",

        "heart hospital",
        "heart problem",
        "heart problems",
        "heart",
        "cardiology",
        "cardiologist",

        "fever",
        "general medicine",
        "general physician",

        "ent",
        "ear",
        "throat",

        "orthopaedics",
        "orthopedics",
        "bone",
        "bones",

        "dental",
        "dentist",
        "tooth",
        "teeth",

        "pregnancy",
        "gynaecology",
        "gynecology"
    ]

    for keyword in keyword_order:

        if keyword in normalized:

            return normalize_specialty(keyword)

    # Fall back to your existing chatbot specialty detector.
    try:

        detected = detect_specialty(text)

        if detected:
            return normalize_specialty(detected)

    except Exception:

        pass

    return None


# ============================================================
# LOAD ML MODELS
# ============================================================

MODELS_LOADED = False
MODEL_ERROR = None

try:

    intent_model = load_model(INTENT_MODEL)

    condition_model = load_model(CONDITION_MODEL)

    MODELS_LOADED = True

except Exception as error:

    intent_model = None

    condition_model = None

    MODELS_LOADED = False

    MODEL_ERROR = str(error)


# ============================================================
# DATABASE CONNECTION
# ============================================================

def get_database_connection():

    connection = sqlite3.connect(
        DATABASE_PATH
    )

    connection.row_factory = sqlite3.Row

    return connection


# ============================================================
# CHECK DATABASE
# ============================================================

def database_table_exists(table_name):

    if not DATABASE_PATH.exists():
        return False

    try:

        connection = get_database_connection()

        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT name
            FROM sqlite_master
            WHERE type='table'
            AND name=?
            """,
            (table_name,)
        )

        result = cursor.fetchone()

        connection.close()

        return result is not None

    except sqlite3.Error:

        return False


# ============================================================
# DOCTOR SEARCH
# ============================================================

def get_doctors_for_hospital(hospital_name):

    doctors = []

    if not DATABASE_PATH.exists():
        return doctors

    if not database_table_exists("doctors"):
        return doctors

    try:

        connection = get_database_connection()

        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT
                doctor_name,
                specialty,
                qualification,
                opd_days,
                opd_start_time,
                opd_end_time,
                appointment_phone,
                availability_status
            FROM doctors
            WHERE LOWER(hospital_name) = LOWER(?)
            ORDER BY doctor_name
            """,
            (hospital_name,)
        )

        rows = cursor.fetchall()

        connection.close()

        for row in rows:

            doctors.append({

                "doctor_name":
                    row["doctor_name"],

                "specialty":
                    row["specialty"],

                "qualification":
                    row["qualification"],

                "opd_days":
                    row["opd_days"],

                "opd_start_time":
                    row["opd_start_time"],

                "opd_end_time":
                    row["opd_end_time"],

                "appointment_phone":
                    row["appointment_phone"],

                "availability_status":
                    row["availability_status"]

            })

    except sqlite3.Error as error:

        print(
            "Doctor database error:",
            error
        )

    return doctors


# ============================================================
# HOSPITAL INFORMATION
# ============================================================

def get_hospital_information(specialty=None):

    normalized_specialty = normalize_specialty(
        specialty
    )

    hospitals = []

    try:

        hospitals = search_hospitals(
            normalized_specialty
        )

    except Exception as error:

        print(
            "Hospital search error:",
            error
        )

        hospitals = []

    result = []

    for hospital in hospitals:

        # Your existing search_hospitals() returns:
        #
        # name
        # hospital_type
        # specialties
        # address
        # phone
        # source
        # verified_date

        try:

            name = hospital[0]

            hospital_type = hospital[1]

            specialties = hospital[2]

            address = hospital[3]

            phone = hospital[4]

            source = hospital[5]

            verified_date = hospital[6]

        except (IndexError, TypeError):

            continue


        emergency_phone = ""

        emergency_available = ""

        hospital_timings = ""

        services_detail = ""

        website = ""

        image_url = ""


        # ----------------------------------------------------
        # Get additional information from hospitals table.
        # ----------------------------------------------------

        try:

            if database_table_exists("hospitals"):

                connection = get_database_connection()

                cursor = connection.cursor()

                cursor.execute(
                    """
                    SELECT
                        emergency_phone,
                        emergency_available,
                        hospital_timings,
                        services_detail,
                        website
                    FROM hospitals
                    WHERE LOWER(name) = LOWER(?)
                    LIMIT 1
                    """,
                    (name,)
                )

                advanced_data = cursor.fetchone()

                connection.close()

                if advanced_data:

                    emergency_phone = (
                        advanced_data["emergency_phone"]
                        or ""
                    )

                    emergency_available = (
                        advanced_data["emergency_available"]
                        or ""
                    )

                    hospital_timings = (
                        advanced_data["hospital_timings"]
                        or ""
                    )

                    services_detail = (
                        advanced_data["services_detail"]
                        or ""
                    )

                    website = (
                        advanced_data["website"]
                        or ""
                    )

        except sqlite3.Error as error:

            print(
                "Hospital detail error:",
                error
            )


        # ----------------------------------------------------
        # Doctor information.
        # ----------------------------------------------------

        doctors = get_doctors_for_hospital(
            name
        )


        # ----------------------------------------------------
        # Hospital category.
        # ----------------------------------------------------

        category = get_hospital_category(
            specialties,
            normalized_specialty
        )


        result.append({

            "name":
                name,

            "hospital_type":
                hospital_type,

            "specialties":
                specialties,

            "address":
                address,

            "phone":
                phone,

            "source":
                source,

            "verified_date":
                verified_date,

            "emergency_phone":
                emergency_phone,

            "emergency_available":
                emergency_available,

            "hospital_timings":
                hospital_timings,

            "services_detail":
                services_detail,

            "website":
                website,

            "image_url":
                image_url,

            "category":
                category,

            "doctors":
                doctors

        })

    return result


# ============================================================
# DETERMINE HOSPITAL CATEGORY
# ============================================================

def get_hospital_category(
    specialties,
    requested_specialty=None
):

    text = (
        str(specialties or "")
        .lower()
    )

    specialty = (
        str(requested_specialty or "")
        .lower()
    )

    combined = text + " " + specialty

    if "dermat" in combined:
        return "Dermatology"

    if (
        "ophthalm" in combined
        or "eye" in combined
    ):
        return "Ophthalmology"

    if (
        "cardio" in combined
        or "heart" in combined
    ):
        return "Cardiology"

    if (
        "general medicine" in combined
        or "general physician" in combined
    ):
        return "General Medicine"

    if "ent" in combined:
        return "ENT"

    if (
        "orthop" in combined
        or "bone" in combined
    ):
        return "Orthopaedics"

    if (
        "dental" in combined
        or "dentist" in combined
    ):
        return "Dental"

    return requested_specialty or "Multi-Specialty"


# ============================================================
# HOME PAGE
# ============================================================

@app.route("/")
def home():

    return render_template(
        "index.html"
    )


# ============================================================
# SYSTEM STATUS
# ============================================================

@app.route("/api/status")
def status():

    return jsonify({

        "success":
            True,

        "application":
            APP_NAME,

        "version":
            APP_VERSION,

        "models_loaded":
            MODELS_LOADED,

        "database_available":
            DATABASE_PATH.exists(),

        "hospitals_table":
            database_table_exists(
                "hospitals"
            ),

        "doctors_table":
            database_table_exists(
                "doctors"
            ),

        "message":
            "Medical chatbot backend is running."

    })


# ============================================================
# FEATURES API
# ============================================================

@app.route("/api/features")
def features():

    return jsonify({

        "success":
            True,

        "application":
            APP_NAME,

        "features":
            FEATURES

    })


# ============================================================
# ALL HOSPITALS API
#
# GET:
# /api/hospitals
#
# Returns all hospitals.
# ============================================================

@app.route("/api/hospitals")
def hospitals_api():

    specialty = request.args.get(
        "specialty",
        default=None,
        type=str
    )

    specialty = normalize_specialty(
        specialty
    )

    hospitals = get_hospital_information(
        specialty
    )

    return jsonify({

        "success":
            True,

        "specialty":
            specialty,

        "count":
            len(hospitals),

        "hospitals":
            hospitals

    })


# ============================================================
# SPECIALTY HOSPITAL API
#
# Examples:
#
# /api/hospitals?specialty=Dermatology
# /api/hospitals?specialty=Ophthalmology
# /api/hospitals?specialty=Cardiology
# ============================================================

@app.route("/api/hospitals/specialty")
def specialty_hospitals_api():

    specialty = request.args.get(
        "specialty",
        default="",
        type=str
    )

    specialty = normalize_specialty(
        specialty
    )

    if not specialty:

        return jsonify({

            "success":
                False,

            "message":
                "Please provide a medical specialty."

        }), 400


    hospitals = get_hospital_information(
        specialty
    )


    return jsonify({

        "success":
            True,

        "specialty":
            specialty,

        "count":
            len(hospitals),

        "hospitals":
            hospitals

    })


# ============================================================
# CHAT API
# ============================================================

@app.route(
    "/api/chat",
    methods=["POST"]
)
def chat():

    try:

        data = request.get_json(
            silent=True
        )


        if not data:

            return jsonify({

                "success":
                    False,

                "message":
                    "Invalid request."

            }), 400


        user_message = str(
            data.get(
                "message",
                ""
            )
        ).strip()


        if not user_message:

            return jsonify({

                "success":
                    False,

                "message":
                    "Please enter a message."

            }), 400


        text_lower = (
            user_message
            .lower()
            .strip()
        )


        # ====================================================
        # EXIT
        # ====================================================

        if text_lower in {
            "exit",
            "quit",
            "bye"
        }:

            return jsonify({

                "success":
                    True,

                "type":
                    "text",

                "message":
                    "Thank you for using the Ballari Medical Assistant."

            })


        # ====================================================
        # EMERGENCY CHECK
        # ====================================================

        severity, matched = check_severity(
            user_message
        )


        if severity == "urgent":

            hospitals = (
                get_hospital_information()
            )


            return jsonify({

                "success":
                    True,

                "type":
                    "emergency",

                "emergency":
                    True,

                "message":
                    (
                        "Your message may indicate a situation "
                        "that needs immediate medical attention."
                    ),

                "matched_warning":
                    matched,

                "action":
                    (
                        "Please seek immediate medical attention "
                        "at the nearest emergency department. "
                        "Do not rely on the chatbot for emergency care."
                    ),

                "hospitals":
                    hospitals

            })


        # ====================================================
        # EXPLICIT SPECIALTY REQUEST
        # ====================================================

        requested_specialty = (
            detect_requested_specialty(
                user_message
            )
        )


        # ====================================================
        # HOSPITAL REQUEST
        # ====================================================

        hospital_words = {

            "hospital",
            "hospitals",
            "clinic",
            "clinics",
            "doctor",
            "doctors",
            "specialist",
            "specialists",
            "medical center",
            "medical centre"

        }


        asks_for_hospital = any(
            word in text_lower
            for word in hospital_words
        )


        if asks_for_hospital:

            hospitals = (
                get_hospital_information(
                    requested_specialty
                )
            )


            return jsonify({

                "success":
                    True,

                "type":
                    "hospital",

                "message":
                    (
                        "Here are the healthcare facilities "
                        "available for your request."
                    ),

                "specialty":
                    requested_specialty,

                "hospitals":
                    hospitals

            })


        # ====================================================
        # MODEL VALIDATION
        # ====================================================

        if not MODELS_LOADED:

            return jsonify({

                "success":
                    False,

                "message":
                    (
                        "The ML models could not be loaded."
                    ),

                "error":
                    MODEL_ERROR

            }), 500


        # ====================================================
        # INTENT PREDICTION
        # ====================================================

        intent, intent_confidence = (
            predict_with_confidence(
                intent_model,
                user_message
            )
        )


        # ====================================================
        # SYMPTOM GUIDANCE
        # ====================================================

        guidance = (
            get_symptom_guidance(
                user_message
            )
        )


        if guidance:

            specialty = (
                guidance["specialty"]
            )


            # ------------------------------------------------
            # Condition prediction
            # ------------------------------------------------

            condition = None

            condition_confidence = None


            if (

                intent == "symptom_check"

                and

                intent_confidence is not None

                and

                intent_confidence >=
                    CONFIDENCE_THRESHOLD

            ):

                try:

                    (
                        condition,
                        condition_confidence
                    ) = predict_with_confidence(
                        condition_model,
                        user_message
                    )

                except Exception:

                    condition = None

                    condition_confidence = None


            # ------------------------------------------------
            # Relevant hospitals
            # ------------------------------------------------

            hospitals = (
                get_hospital_information(
                    specialty
                )
            )


            return jsonify({

                "success":
                    True,

                "type":
                    "symptom",

                "message":
                    (
                        "I found symptom-related educational "
                        "information for your message."
                    ),

                "intent":
                    intent,

                "intent_confidence":
                    (
                        round(
                            intent_confidence * 100,
                            2
                        )
                        if intent_confidence is not None
                        else None
                    ),

                "keyword":
                    guidance["keyword"],

                "symptom":
                    guidance["keyword"],

                "category":
                    guidance["category"],

                "specialty":
                    specialty,

                "guidance":
                    guidance["guidance"],

                "condition":
                    condition,

                "condition_confidence":
                    (
                        round(
                            condition_confidence * 100,
                            2
                        )
                        if condition_confidence is not None
                        else None
                    ),

                "hospitals":
                    hospitals

            })


        # ====================================================
        # GREETING
        # ====================================================

        if intent == "greeting":

            return jsonify({

                "success":
                    True,

                "type":
                    "greeting",

                "message":
                    (
                        "Hello! I am your Ballari Medical Assistant. "
                        "You can describe symptoms, find hospitals, "
                        "or search for medical specialties."
                    )

            })


        # ====================================================
        # GENERAL HEALTH
        # ====================================================

        if intent == "general_health":

            return jsonify({

                "success":
                    True,

                "type":
                    "general",

                "message":
                    (
                        "I can provide general educational healthcare "
                        "information. Please describe your question "
                        "or symptoms clearly."
                    )

            })


        # ====================================================
        # UNKNOWN
        # ====================================================

        return jsonify({

            "success":
                True,

            "type":
                "unknown",

            "message":
                (
                    "I could not confidently understand your request. "
                    "Try describing your symptom or asking for a "
                    "hospital or medical specialty."
                ),

            "intent":
                intent,

            "intent_confidence":
                (
                    round(
                        intent_confidence * 100,
                        2
                    )
                    if intent_confidence is not None
                    else None
                )

        })


    except Exception as error:

        print(
            "CHAT ERROR:",
            error
        )


        return jsonify({

            "success":
                False,

            "message":
                (
                    "The chatbot encountered an error "
                    "while processing your request."
                ),

            "error":
                str(error)

        }), 500


# ============================================================
# HEALTH INFORMATION ENDPOINT
#
# This can be used by the frontend for the four quick buttons.
# ============================================================

@app.route("/api/health-topics")
def health_topics():

    topics = {

        "fever": {

            "title":
                "Fever",

            "icon":
                "🤒",

            "specialty":
                "General Medicine",

            "guidance":
                SYMPTOM_GUIDANCE["fever"]["guidance"]

        },

        "skin": {

            "title":
                "Skin Problem",

            "icon":
                "🩹",

            "specialty":
                "Dermatology",

            "guidance":
                SYMPTOM_GUIDANCE["skin"]["guidance"]

        },

        "eye": {

            "title":
                "Eye Problem",

            "icon":
                "👁️",

            "specialty":
                "Ophthalmology",

            "guidance":
                SYMPTOM_GUIDANCE["eye"]["guidance"]

        },

        "heart": {

            "title":
                "Heart Problem",

            "icon":
                "❤️",

            "specialty":
                "Cardiology",

            "guidance":
                SYMPTOM_GUIDANCE["heart"]["guidance"]

        }

    }


    return jsonify({

        "success":
            True,

        "topics":
            topics

    })


# ============================================================
# DATABASE INFORMATION
#
# Useful while developing/debugging.
# ============================================================

@app.route("/api/database-info")
def database_info():

    hospitals_count = 0

    doctors_count = 0


    try:

        if database_table_exists(
            "hospitals"
        ):

            connection = (
                get_database_connection()
            )

            cursor = (
                connection.cursor()
            )

            cursor.execute(
                "SELECT COUNT(*) AS count FROM hospitals"
            )

            row = cursor.fetchone()

            hospitals_count = (
                row["count"]
                if row
                else 0
            )

            connection.close()


        if database_table_exists(
            "doctors"
        ):

            connection = (
                get_database_connection()
            )

            cursor = (
                connection.cursor()
            )

            cursor.execute(
                "SELECT COUNT(*) AS count FROM doctors"
            )

            row = cursor.fetchone()

            doctors_count = (
                row["count"]
                if row
                else 0
            )

            connection.close()

    except sqlite3.Error as error:

        return jsonify({

            "success":
                False,

            "error":
                str(error)

        }), 500


    return jsonify({

        "success":
            True,

        "database":
            str(DATABASE_PATH),

        "hospitals":
            hospitals_count,

        "doctors":
            doctors_count

    })


# ============================================================
# ERROR HANDLERS
# ============================================================

@app.errorhandler(404)
def page_not_found(error):

    # API requests receive JSON.
    if request.path.startswith("/api/"):

        return jsonify({

            "success":
                False,

            "message":
                "API endpoint not found."

        }), 404


    return (
        "Page not found.",
        404
    )


@app.errorhandler(500)
def internal_server_error(error):

    if request.path.startswith("/api/"):

        return jsonify({

            "success":
                False,

            "message":
                "Internal server error."

        }), 500


    return (
        "Internal server error.",
        500
    )


# ============================================================
# RUN APPLICATION
# ============================================================

if __name__ == "__main__":

    print()
    print("=" * 70)

    print(
        "BALLARI MEDICAL CHATBOT - WEB APPLICATION"
    )

    print("=" * 70)

    print(
        "Application:",
        APP_NAME
    )

    print(
        "Version:",
        APP_VERSION
    )

    print(
        "Backend:",
        "Flask"
    )

    print(
        "ML models:",
        (
            "Loaded"
            if MODELS_LOADED
            else "ERROR"
        )
    )

    print(
        "Database:",
        DATABASE_PATH
    )

    print(
        "Database available:",
        DATABASE_PATH.exists()
    )

    print(
        "Hospitals table:",
        database_table_exists(
            "hospitals"
        )
    )

    print(
        "Doctors table:",
        database_table_exists(
            "doctors"
        )
    )

    if MODEL_ERROR:

        print(
            "Model error:",
            MODEL_ERROR
        )

    print()

    print(
        "Open in browser:"
    )

    print(
        "http://127.0.0.1:5000"
    )

    print()

    print(
        "API endpoints:"
    )

    print(
        "  /api/status"
    )

    print(
        "  /api/features"
    )

    print(
        "  /api/hospitals"
    )

    print(
        "  /api/hospitals?specialty=Dermatology"
    )

    print(
        "  /api/hospitals?specialty=Ophthalmology"
    )

    print(
        "  /api/hospitals?specialty=Cardiology"
    )

    print(
        "  /api/health-topics"
    )

    print(
        "  /api/database-info"
    )

    print("=" * 70)
    print()


    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )