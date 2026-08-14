"""
SELF-RELIANT MEDICAL CHATBOT - ADVANCED FINAL VERSION

Features:
- ML intent classification
- ML condition classification
- Confidence scoring
- Emergency safety layer
- Built-in symptom guidance
- Medical specialty detection
- Ballari healthcare directory
- Specialty-based hospital search
- Hospital address
- Hospital phone
- Emergency phone
- Emergency availability
- Hospital timings
- Hospital services
- Doctor information
- Doctor specialty
- Doctor OPD days
- Doctor OPD timings
- Appointment phone
- SQLite database
- Session history
- Help commands

Educational / final-year engineering project prototype.
This system does not diagnose diseases or prescribe medicines.
"""

from pathlib import Path
from datetime import datetime
import sqlite3
import joblib

from severity_checker import check_severity


# ============================================================
# PROJECT PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent

MODEL_DIR = BASE_DIR / "model"

INTENT_MODEL = MODEL_DIR / "intent_classifier.joblib"

CONDITION_MODEL = MODEL_DIR / "condition_classifier.joblib"

DATABASE_PATH = BASE_DIR / "ballari_healthcare.db"


# ============================================================
# SETTINGS
# ============================================================

CONFIDENCE_THRESHOLD = 0.55

MAX_HISTORY = 20

conversation_history = []


# ============================================================
# BUILT-IN SYMPTOM GUIDANCE
# ============================================================

SYMPTOM_GUIDANCE = {

    "fever": {
        "specialty": "General Medicine",
        "guidance": (
            "Fever can occur with many different conditions. "
            "A healthcare professional can evaluate the duration, "
            "temperature and other associated symptoms."
        )
    },

    "cough": {
        "specialty": "General Medicine",
        "guidance": (
            "Cough can have many causes. "
            "A clinician can assess how long it has been present "
            "and whether other symptoms are present."
        )
    },

    "cold": {
        "specialty": "General Medicine",
        "guidance": (
            "Cold-like symptoms are commonly evaluated by "
            "a general physician, especially when symptoms persist "
            "or become severe."
        )
    },

    "skin": {
        "specialty": "Dermatology",
        "guidance": (
            "Skin symptoms such as rashes, itching, acne or changes "
            "in the skin can have different causes. "
            "A dermatologist can examine the affected area."
        )
    },

    "rash": {
        "specialty": "Dermatology",
        "guidance": (
            "A rash can have several possible causes. "
            "A dermatologist can evaluate its appearance, location "
            "and duration."
        )
    },

    "itching": {
        "specialty": "Dermatology",
        "guidance": (
            "Persistent or unexplained itching should be evaluated "
            "by a qualified healthcare professional."
        )
    },

    "headache": {
        "specialty": "General Medicine",
        "guidance": (
            "Headaches can have many causes. "
            "A clinician can assess the pattern, duration and "
            "associated symptoms."
        )
    },

    "eye": {
        "specialty": "Ophthalmology",
        "guidance": (
            "Eye symptoms or changes in vision should be evaluated "
            "by an eye-care professional, particularly when symptoms "
            "are persistent or sudden."
        )
    },

    "vision": {
        "specialty": "Ophthalmology",
        "guidance": (
            "Changes in vision can have different causes. "
            "An ophthalmologist can perform an appropriate eye examination."
        )
    },

    "ear": {
        "specialty": "ENT",
        "guidance": (
            "Persistent ear symptoms, hearing changes or ear pain "
            "can be evaluated by an ENT specialist."
        )
    },

    "throat": {
        "specialty": "ENT",
        "guidance": (
            "Persistent throat symptoms can be evaluated by a "
            "general physician or ENT specialist."
        )
    },

    "joint": {
        "specialty": "Orthopaedics",
        "guidance": (
            "Persistent joint pain or movement problems can be "
            "evaluated by an orthopaedic specialist."
        )
    },

    "bone": {
        "specialty": "Orthopaedics",
        "guidance": (
            "Bone or musculoskeletal problems should be evaluated "
            "by a qualified healthcare professional."
        )
    },

    "tooth": {
        "specialty": "Dental",
        "guidance": (
            "Tooth or gum problems can be evaluated by a dentist."
        )
    },

    "teeth": {
        "specialty": "Dental",
        "guidance": (
            "Dental symptoms should be evaluated by a qualified dentist."
        )
    },

    "pregnancy": {
        "specialty": "Obstetrics & Gynaecology",
        "guidance": (
            "Pregnancy-related concerns should be discussed with "
            "a qualified obstetrician or gynaecologist."
        )
    }
}


# ============================================================
# SYMPTOM GUIDANCE FUNCTION
# ============================================================

def get_symptom_guidance(text):

    normalized = text.lower().strip()

    for keyword, information in SYMPTOM_GUIDANCE.items():

        if keyword in normalized:

            return {
                "keyword": keyword,
                "specialty": information["specialty"],
                "guidance": information["guidance"]
            }

    return None


# ============================================================
# LOAD MODEL
# ============================================================

def load_model(path):

    if not path.exists():

        raise FileNotFoundError(
            f"Model not found:\n{path}"
        )

    return joblib.load(path)


# ============================================================
# PREDICTION WITH CONFIDENCE
# ============================================================

def predict_with_confidence(model, text):

    label = model.predict([text])[0]

    confidence = None

    if hasattr(model, "predict_proba"):

        probabilities = model.predict_proba([text])[0]

        if len(probabilities) > 0:

            confidence = float(
                max(probabilities)
            )

    return str(label), confidence


# ============================================================
# SPECIALTY DETECTION
# ============================================================

def detect_specialty(text):

    text = text.lower().strip()

    specialty_keywords = {

        "Dermatology": [
            "skin",
            "dermatology",
            "rash",
            "acne",
            "pimple",
            "itching",
            "itchy",
            "skin allergy",
            "hair problem",
            "hair loss"
        ],

        "Cardiology": [
            "heart",
            "cardiac",
            "cardiology",
            "heart hospital",
            "blood pressure",
            "hypertension",
            "chest pain",
            "palpitation",
            "palpitations",
            "heart problem"
        ],

        "Ophthalmology": [
            "eye",
            "eyes",
            "ophthalmology",
            "vision",
            "sight",
            "eye hospital",
            "cataract",
            "eye problem"
        ],

        "Orthopaedics": [
            "bone",
            "bones",
            "joint",
            "joints",
            "fracture",
            "orthopedic",
            "orthopaedic",
            "knee",
            "shoulder",
            "back pain"
        ],

        "ENT": [
            "ear",
            "ears",
            "nose",
            "throat",
            "ent",
            "hearing",
            "sinus"
        ],

        "Paediatrics": [
            "child",
            "children",
            "baby",
            "paediatric",
            "pediatric",
            "kids"
        ],

        "Neurology": [
            "brain",
            "neurology",
            "migraine",
            "seizure",
            "nerve",
            "nerves"
        ],

        "Psychiatry": [
            "mental health",
            "psychiatry",
            "anxiety",
            "depression",
            "stress"
        ],

        "Dental": [
            "tooth",
            "teeth",
            "dental",
            "dentist",
            "gum",
            "gums"
        ],

        "Obstetrics & Gynaecology": [
            "pregnancy",
            "pregnant",
            "gynaecology",
            "gynecology",
            "maternity",
            "women's health"
        ],

        "General Medicine": [
            "fever",
            "cold",
            "cough",
            "headache",
            "general physician",
            "general medicine"
        ]
    }

    for specialty, keywords in specialty_keywords.items():

        for keyword in keywords:

            if keyword in text:

                return specialty

    return None


# ============================================================
# DATABASE CONNECTION
# ============================================================

def get_connection():

    if not DATABASE_PATH.exists():

        return None

    try:

        return sqlite3.connect(
            DATABASE_PATH
        )

    except sqlite3.Error as error:

        print(
            f"\nDatabase connection error: {error}"
        )

        return None


# ============================================================
# SEARCH HOSPITALS
# ============================================================

def search_hospitals(specialty=None):

    connection = get_connection()

    if connection is None:

        return []

    try:

        cursor = connection.cursor()

        if specialty:

            cursor.execute(
                """
                SELECT
                    id,
                    name,
                    hospital_type,
                    specialties,
                    address,
                    phone,
                    source,
                    verified_date,
                    emergency_phone,
                    emergency_available,
                    hospital_timings,
                    services_detail,
                    website
                FROM hospitals
                WHERE LOWER(specialties) LIKE ?
                   OR LOWER(name) LIKE ?
                ORDER BY name
                """,
                (
                    f"%{specialty.lower()}%",
                    f"%{specialty.lower()}%"
                )
            )

        else:

            cursor.execute(
                """
                SELECT
                    id,
                    name,
                    hospital_type,
                    specialties,
                    address,
                    phone,
                    source,
                    verified_date,
                    emergency_phone,
                    emergency_available,
                    hospital_timings,
                    services_detail,
                    website
                FROM hospitals
                ORDER BY name
                """
            )

        return cursor.fetchall()

    except sqlite3.Error as error:

        print(
            f"\nDatabase error: {error}"
        )

        return []

    finally:

        connection.close()


# ============================================================
# SEARCH DOCTORS
# ============================================================

def search_doctors(
    hospital_name=None,
    specialty=None
):

    connection = get_connection()

    if connection is None:

        return []

    try:

        cursor = connection.cursor()

        if hospital_name and specialty:

            cursor.execute(
                """
                SELECT
                    hospital_name,
                    doctor_name,
                    specialty,
                    qualification,
                    opd_days,
                    opd_start_time,
                    opd_end_time,
                    appointment_phone,
                    availability_status,
                    source,
                    verified_date
                FROM doctors
                WHERE LOWER(hospital_name) = LOWER(?)
                  AND LOWER(specialty) LIKE ?
                ORDER BY doctor_name
                """,
                (
                    hospital_name,
                    f"%{specialty.lower()}%"
                )
            )

        elif hospital_name:

            cursor.execute(
                """
                SELECT
                    hospital_name,
                    doctor_name,
                    specialty,
                    qualification,
                    opd_days,
                    opd_start_time,
                    opd_end_time,
                    appointment_phone,
                    availability_status,
                    source,
                    verified_date
                FROM doctors
                WHERE LOWER(hospital_name) = LOWER(?)
                ORDER BY doctor_name
                """,
                (hospital_name,)
            )

        elif specialty:

            cursor.execute(
                """
                SELECT
                    hospital_name,
                    doctor_name,
                    specialty,
                    qualification,
                    opd_days,
                    opd_start_time,
                    opd_end_time,
                    appointment_phone,
                    availability_status,
                    source,
                    verified_date
                FROM doctors
                WHERE LOWER(specialty) LIKE ?
                ORDER BY hospital_name, doctor_name
                """,
                (f"%{specialty.lower()}%",)
            )

        else:

            cursor.execute(
                """
                SELECT
                    hospital_name,
                    doctor_name,
                    specialty,
                    qualification,
                    opd_days,
                    opd_start_time,
                    opd_end_time,
                    appointment_phone,
                    availability_status,
                    source,
                    verified_date
                FROM doctors
                ORDER BY hospital_name, doctor_name
                """
            )

        return cursor.fetchall()

    except sqlite3.Error as error:

        print(
            f"\nDoctor database error: {error}"
        )

        return []

    finally:

        connection.close()


# ============================================================
# DISPLAY DOCTOR INFORMATION
# ============================================================

def display_doctors(doctors):

    if not doctors:

        print(
            "   Doctor Information: "
            "No doctor records available in database."
        )

        return

    print(
        "\n   DOCTOR INFORMATION"
    )

    for doctor in doctors:

        (
            hospital_name,
            doctor_name,
            specialty,
            qualification,
            opd_days,
            opd_start_time,
            opd_end_time,
            appointment_phone,
            availability_status,
            source,
            verified_date
        ) = doctor

        print(
            f"\n   Doctor: {doctor_name}"
        )

        print(
            f"   Specialty: {specialty}"
        )

        print(
            f"   Qualification: {qualification}"
        )

        print(
            f"   OPD Days: {opd_days}"
        )

        print(
            f"   OPD Time: "
            f"{opd_start_time} - {opd_end_time}"
        )

        print(
            f"   Appointment Phone: "
            f"{appointment_phone}"
        )

        print(
            f"   Availability: "
            f"{availability_status}"
        )


# ============================================================
# DISPLAY HOSPITAL INFORMATION
# ============================================================

def display_hospitals(
    hospitals,
    specialty=None
):

    print("\n")

    print("=" * 70)

    if specialty:

        print(
            f"{specialty.upper()} "
            f"HEALTHCARE OPTIONS - BALLARI"
        )

    else:

        print(
            "BALLARI HEALTHCARE DIRECTORY"
        )

    print("=" * 70)

    if not hospitals:

        print(
            "\nNo matching healthcare facilities "
            "were found in the database."
        )

        return

    print(
        f"\nFound {len(hospitals)} healthcare option(s):"
    )

    for index, hospital in enumerate(
        hospitals,
        start=1
    ):

        (
            hospital_id,
            name,
            hospital_type,
            specialties,
            address,
            phone,
            source,
            verified_date,
            emergency_phone,
            emergency_available,
            hospital_timings,
            services_detail,
            website
        ) = hospital

        print("\n")

        print(
            f"{index}. {name}"
        )

        print(
            f"   Type: {hospital_type}"
        )

        if specialty:

            print(
                f"   Recommended Specialty: "
                f"{specialty}"
            )

        print(
            f"   Specialties: {specialties}"
        )

        print(
            f"   Address: {address}"
        )

        print(
            f"   Hospital Phone: {phone}"
        )

        print(
            f"   Emergency Phone: "
            f"{emergency_phone}"
        )

        print(
            f"   Emergency Availability: "
            f"{emergency_available}"
        )

        print(
            f"   Hospital Timings: "
            f"{hospital_timings}"
        )

        print(
            f"   Services: "
            f"{services_detail}"
        )

        if website:

            print(
                f"   Website: {website}"
            )

        doctors = search_doctors(
            hospital_name=name,
            specialty=specialty
        )

        if not doctors:

            doctors = search_doctors(
                hospital_name=name
            )

        display_doctors(
            doctors
        )

        print(
            f"\n   Information Source: "
            f"{source}"
        )

        print(
            f"   Information Updated: "
            f"{verified_date}"
        )

        print(
            "-" * 70
        )


# ============================================================
# SHOW ALL HOSPITALS
# ============================================================

def show_all_hospitals():

    hospitals = search_hospitals()

    display_hospitals(
        hospitals
    )


# ============================================================
# SHOW EMERGENCY HOSPITALS
# ============================================================

def show_emergency_hospitals():

    hospitals = search_hospitals()

    emergency_hospitals = []

    for hospital in hospitals:

        emergency_available = hospital[9]

        if emergency_available:

            emergency_hospitals.append(
                hospital
            )

    display_hospitals(
        emergency_hospitals
    )


# ============================================================
# HISTORY
# ============================================================

def add_history(
    user_text,
    response
):

    conversation_history.append(
        {
            "time":
                datetime.now().strftime(
                    "%H:%M:%S"
                ),

            "user":
                user_text,

            "response":
                response
        }
    )

    if len(
        conversation_history
    ) > MAX_HISTORY:

        conversation_history.pop(0)


def show_history():

    print("\n")

    print("=" * 70)

    print(
        "CURRENT SESSION HISTORY"
    )

    print("=" * 70)

    if not conversation_history:

        print(
            "\nNo conversation history."
        )

        return

    for index, item in enumerate(
        conversation_history,
        start=1
    ):

        print(
            f"\n{index}. "
            f"[{item['time']}]"
        )

        print(
            f"   User: "
            f"{item['user']}"
        )

        print(
            f"   System: "
            f"{item['response']}"
        )


# ============================================================
# HELP
# ============================================================

def show_help():

    print("\n")

    print("=" * 70)

    print(
        "CHATBOT COMMANDS"
    )

    print("=" * 70)

    print(
        "\nYou can enter:"
    )

    print(
        "  Symptoms or health questions"
    )

    print(
        "  Hospital requests"
    )

    print(
        "  hospitals  -> Show all hospitals"
    )

    print(
        "  emergency  -> Show emergency facilities"
    )

    print(
        "  history    -> Show conversation history"
    )

    print(
        "  help       -> Show commands"
    )

    print(
        "  exit       -> Exit chatbot"
    )


# ============================================================
# EMERGENCY HANDLER
# ============================================================

def handle_emergency(matched):

    print("\n")

    print("=" * 70)

    print(
        "URGENT MEDICAL ALERT"
    )

    print("=" * 70)

    if matched:

        print(
            f"\nMatched warning sign: "
            f"{matched}"
        )

    print(
        "\nThe message may indicate "
        "a potentially urgent situation."
    )

    print(
        "\nEmergency healthcare facilities "
        "available in Ballari:"
    )

    hospitals = search_hospitals()

    emergency_hospitals = []

    for hospital in hospitals:

        if hospital[9]:

            emergency_hospitals.append(
                hospital
            )

    display_hospitals(
        emergency_hospitals
    )


# ============================================================
# HOSPITAL REQUEST HANDLER
# ============================================================

def handle_hospital_request(text):

    specialty = detect_specialty(
        text
    )

    if specialty:

        print(
            f"\nDetected Specialty: "
            f"{specialty}"
        )

        print(
            "\nSearching Ballari healthcare database..."
        )

        hospitals = search_hospitals(
            specialty
        )

        display_hospitals(
            hospitals,
            specialty
        )

        return

    print(
        "\nSpecific specialty was not detected."
    )

    print(
        "Showing all available healthcare facilities."
    )

    show_all_hospitals()


# ============================================================
# SHOW SYMPTOM INFORMATION
# ============================================================

def show_symptom_information(text):

    result = get_symptom_guidance(
        text
    )

    if not result:

        return None

    print("\n")

    print("=" * 70)

    print(
        "SYMPTOM INFORMATION"
    )

    print("=" * 70)

    print(
        f"\nDetected Symptom: "
        f"{result['keyword']}"
    )

    print(
        f"Suggested Specialty: "
        f"{result['specialty']}"
    )

    print(
        "\nEducational Guidance:"
    )

    print(
        result["guidance"]
    )

    return result


# ============================================================
# MAIN MESSAGE HANDLER
# ============================================================

def handle_message(
    text,
    intent_model,
    condition_model
):

    severity, matched = check_severity(
        text
    )

    if severity == "urgent":

        handle_emergency(
            matched
        )

        add_history(
            text,
            "Emergency healthcare information displayed"
        )

        return

    intent, confidence = predict_with_confidence(
        intent_model,
        text
    )

    print(
        f"\nDetected intent: "
        f"{intent}"
    )

    if confidence is not None:

        print(
            f"Intent confidence: "
            f"{confidence * 100:.2f}%"
        )

    # --------------------------------------------------------
    # HOSPITAL REQUEST
    # --------------------------------------------------------

    if intent == "hospital_request":

        handle_hospital_request(
            text
        )

        add_history(
            text,
            "Hospital and doctor information displayed"
        )

        return

    # --------------------------------------------------------
    # GREETING
    # --------------------------------------------------------

    if intent == "greeting":

        print(
            "\nHello!"
        )

        print(
            "I can help you with symptoms, "
            "medical specialties, hospitals, "
            "doctors and emergency healthcare facilities "
            "in Ballari."
        )

        add_history(
            text,
            "Greeting response"
        )

        return

    # --------------------------------------------------------
    # GENERAL HEALTH
    # --------------------------------------------------------

    if intent == "general_health":

        print(
            "\nGeneral Health Information:"
        )

        print(
            "I can provide general educational "
            "health information."
        )

        print(
            "For personal medical evaluation, "
            "consult a qualified healthcare professional."
        )

        add_history(
            text,
            "General health guidance"
        )

        return

    # --------------------------------------------------------
    # UNKNOWN INTENT
    # --------------------------------------------------------

    if intent == "unknown":

        guidance = show_symptom_information(
            text
        )

        specialty = detect_specialty(
            text
        )

        if guidance:

            specialty = guidance[
                "specialty"
            ]

        if specialty:

            hospitals = search_hospitals(
                specialty
            )

            if hospitals:

                print(
                    f"\nHealthcare facilities "
                    f"for {specialty} in Ballari:"
                )

                display_hospitals(
                    hospitals,
                    specialty
                )

                add_history(
                    text,
                    "Symptom and hospital information displayed"
                )

                return

        print(
            "\nI couldn't confidently "
            "identify your request."
        )

        print(
            "Please describe your symptom "
            "or ask for a hospital."
        )

        add_history(
            text,
            "Unknown intent response"
        )

        return

    # --------------------------------------------------------
    # SYMPTOM CHECK
    # --------------------------------------------------------

    if intent == "symptom_check":

        guidance = show_symptom_information(
            text
        )

        specialty = detect_specialty(
            text
        )

        if guidance:

            specialty = guidance[
                "specialty"
            ]

        if specialty:

            print(
                f"\nSuggested Specialty: "
                f"{specialty}"
            )

            hospitals = search_hospitals(
                specialty
            )

            if hospitals:

                print(
                    f"\nHealthcare facilities "
                    f"for {specialty} in Ballari:"
                )

                display_hospitals(
                    hospitals,
                    specialty
                )

        # ----------------------------------------------------
        # LOW CONFIDENCE
        # ----------------------------------------------------

        if (
            confidence is not None
            and confidence < CONFIDENCE_THRESHOLD
        ):

            print(
                "\nThe chatbot is not confident "
                "enough for condition classification."
            )

            print(
                "Symptom guidance and relevant "
                "healthcare facilities have been displayed."
            )

            add_history(
                text,
                "Symptom guidance and hospital information displayed"
            )

            return

        # ----------------------------------------------------
        # CONDITION CLASSIFICATION
        # ----------------------------------------------------

        condition, condition_confidence = (
            predict_with_confidence(
                condition_model,
                text
            )
        )

        print(
            f"\nCondition model output: "
            f"{condition}"
        )

        if condition_confidence is not None:

            print(
                f"Condition-model confidence: "
                f"{condition_confidence * 100:.2f}%"
            )

        print(
            "\nThis ML classification is "
            "educational information only "
            "and is not a medical diagnosis."
        )

        add_history(
            text,
            "Symptom classification and hospital information displayed"
        )

        return

    # --------------------------------------------------------
    # FALLBACK
    # --------------------------------------------------------

    print(
        "\nNo response rule is configured "
        "for this intent yet."
    )

    add_history(
        text,
        "Fallback response"
    )


# ============================================================
# PROJECT VALIDATION
# ============================================================

def validate_project():

    errors = []

    if not INTENT_MODEL.exists():

        errors.append(
            f"Missing intent model: "
            f"{INTENT_MODEL}"
        )

    if not CONDITION_MODEL.exists():

        errors.append(
            f"Missing condition model: "
            f"{CONDITION_MODEL}"
        )

    if not DATABASE_PATH.exists():

        errors.append(
            f"Missing healthcare database: "
            f"{DATABASE_PATH}"
        )

    return errors


# ============================================================
# MAIN
# ============================================================

def main():

    print("=" * 70)

    print(
        "SELF-RELIANT MEDICAL CHATBOT - "
        "ADVANCED FINAL VERSION"
    )

    print("=" * 70)

    print(
        "Type 'help' to see available commands."
    )

    print(
        "Type 'exit' to stop."
    )

    print(
        "Prototype: educational healthcare guidance only."
    )

    print("=" * 70)

    errors = validate_project()

    if errors:

        print(
            "\nPROJECT VALIDATION ERROR:"
        )

        for error in errors:

            print(
                f"- {error}"
            )

        print(
            "\nPlease make sure the required "
            "files are present."
        )

        return

    try:

        print(
            "\nLoading ML models..."
        )

        intent_model = load_model(
            INTENT_MODEL
        )

        condition_model = load_model(
            CONDITION_MODEL
        )

        print(
            "ML models loaded successfully."
        )

    except Exception as error:

        print(
            "\nCould not load ML models:"
        )

        print(
            error
        )

        return

    print(
        "Ballari healthcare database detected."
    )

    print(
        f"Database: "
        f"{DATABASE_PATH.name}"
    )

    print(
        "Built-in symptom guidance loaded."
    )

    print(
        "\nSystem ready."
    )

    while True:

        try:

            text = input(
                "\nUser: "
            ).strip()

        except (
            KeyboardInterrupt,
            EOFError
        ):

            print(
                "\nGoodbye!"
            )

            break

        if not text:

            print(
                "Please enter a message."
            )

            continue

        command = text.lower()

        if command in {
            "exit",
            "quit",
            "bye"
        }:

            print(
                "Goodbye!"
            )

            break

        if command == "help":

            show_help()

            continue

        if command == "history":

            show_history()

            continue

        if command in {
            "hospitals",
            "show hospitals",
            "list hospitals",
            "all hospitals"
        }:

            show_all_hospitals()

            continue

        if command in {
            "emergency",
            "emergency hospitals",
            "emergency hospital",
            "emergency facilities"
        }:

            show_emergency_hospitals()

            continue

        try:

            handle_message(
                text,
                intent_model,
                condition_model
            )

        except Exception as error:

            print(
                "\nProcessing error:"
            )

            print(
                error
            )

            print(
                "\nThe chatbot could not "
                "process this message."
            )


# ============================================================
# PROGRAM ENTRY
# ============================================================

if __name__ == "__main__":
    main()