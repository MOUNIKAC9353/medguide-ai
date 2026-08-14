"""
STEP 10 - SQLite Healthcare Database

Stores Ballari healthcare facilities in a local SQLite database.

This is a healthcare-directory module.
It does NOT diagnose diseases or prescribe medicines.
"""

import sqlite3
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "ballari_healthcare.db"


def create_database():
    """Create the healthcare database and table."""

    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS hospitals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            hospital_type TEXT,
            specialties TEXT,
            address TEXT,
            phone TEXT,
            source TEXT,
            verified_date TEXT
        )
    """)

    connection.commit()
    connection.close()


def add_hospital(
    name,
    hospital_type,
    specialties,
    address,
    phone,
    source,
    verified_date
):
    """Add a hospital to the database."""

    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO hospitals
        (
            name,
            hospital_type,
            specialties,
            address,
            phone,
            source,
            verified_date
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        name,
        hospital_type,
        specialties,
        address,
        phone,
        source,
        verified_date
    ))

    connection.commit()
    connection.close()


def search_hospitals(specialty=None):
    """Search hospitals by specialty."""

    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    if specialty:
        query = """
            SELECT
                name,
                hospital_type,
                specialties,
                address,
                phone,
                source,
                verified_date
            FROM hospitals
            WHERE LOWER(specialties) LIKE ?
            ORDER BY name
        """

        cursor.execute(
            query,
            (f"%{specialty.lower()}%",)
        )

    else:

        cursor.execute("""
            SELECT
                name,
                hospital_type,
                specialties,
                address,
                phone,
                source,
                verified_date
            FROM hospitals
            ORDER BY name
        """)

    results = cursor.fetchall()

    connection.close()

    return results


def display_hospitals(specialty=None):

    hospitals = search_hospitals(specialty)

    print("\n")
    print("=" * 65)

    if specialty:
        print(
            f"{specialty} - BALLARI HEALTHCARE DIRECTORY"
        )
    else:
        print("BALLARI HEALTHCARE DIRECTORY")

    print("=" * 65)

    if not hospitals:

        print("\nNo matching healthcare facilities found.")

        return

    print(
        f"\nFound {len(hospitals)} healthcare option(s).\n"
    )

    for index, hospital in enumerate(
        hospitals,
        start=1
    ):

        (
            name,
            hospital_type,
            specialties,
            address,
            phone,
            source,
            verified_date
        ) = hospital

        print(f"{index}. {name}")
        print(f"   Type: {hospital_type}")
        print(f"   Address: {address}")
        print(f"   Phone: {phone}")
        print(f"   Services: {specialties}")
        print(f"   Verified: {verified_date}")
        print("-" * 65)

    print("\nIMPORTANT:")
    print(
        "This is local healthcare-directory information, "
        "not medical advice."
    )
    print(
        "Please verify current hospital services and "
        "contact information before visiting."
    )


def count_hospitals():

    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    cursor.execute(
        "SELECT COUNT(*) FROM hospitals"
    )

    count = cursor.fetchone()[0]

    connection.close()

    return count


if __name__ == "__main__":

    create_database()

    # ---------------------------------------------------------
    # VERIFIED GOVERNMENT HEALTHCARE FACILITIES
    # ---------------------------------------------------------

    hospitals = [

        {
            "name": "Vijayanagara Institute of Medical Sciences (VIMS)",
            "type": "Government / Teaching Hospital",
            "specialties": (
                "General Medicine, Cardiology, Dermatology, "
                "Neurology, Orthopaedics, ENT, Ophthalmology, "
                "Paediatrics, Psychiatry, Surgery, "
                "Obstetrics & Gynaecology, Dental, "
                "Emergency / Trauma"
            ),
            "address": "Cantonment, Ballari - 583104",
            "phone": "08392-235201",
            "source": "Official Ballari District / VIMS",
            "verified_date": "2026-08-14"
        },

        {
            "name": "District Hospital Ballari",
            "type": "Government Hospital",
            "specialties": (
                "General Medicine, Orthopaedics, Dermatology, "
                "ENT, Ophthalmology, Paediatrics, Psychiatry, "
                "Surgery, Obstetrics & Gynaecology, Dental, "
                "Emergency / Trauma"
            ),
            "address": "Anantapur Road, Ballari",
            "phone": "08392-275255",
            "source": "Official Ballari District",
            "verified_date": "2026-08-14"
        },

        {
            "name": "Taluka General Hospital Sandur",
            "type": "Government Hospital",
            "specialties": (
                "General Medicine, General Surgery, "
                "Emergency Care, Maternal & Child Health"
            ),
            "address": "Sandur, Ballari District",
            "phone": "Verify with hospital",
            "source": "Official Ballari District",
            "verified_date": "2026-08-14"
        },

        {
            "name": "Government Hospital Siruguppa",
            "type": "Government Hospital",
            "specialties": (
                "General Medicine, General Care, "
                "Emergency Care, Maternal & Child Health"
            ),
            "address": "Siruguppa, Ballari District",
            "phone": "Verify with hospital",
            "source": "Official Ballari District",
            "verified_date": "2026-08-14"
        },

        {
            "name": "CHC Kampli",
            "type": "Government Community Health Centre",
            "specialties": (
                "General Medicine, General Care, "
                "Emergency Care, Maternal & Child Health"
            ),
            "address": "Kampli, Ballari District",
            "phone": "Verify with hospital",
            "source": "Official Ballari District",
            "verified_date": "2026-08-14"
        },

        {
            "name": "CHC Ujjini",
            "type": "Government Community Health Centre",
            "specialties": (
                "General Medicine, General Care, "
                "Emergency Care, Maternal & Child Health"
            ),
            "address": "Ujjini, Ballari District",
            "phone": "Verify with hospital",
            "source": "Official Ballari District",
            "verified_date": "2026-08-14"
        },

        {
            "name": "CHC Kurugodu",
            "type": "Government Community Health Centre",
            "specialties": (
                "General Medicine, General Care, "
                "Emergency Care, Maternal & Child Health"
            ),
            "address": "Kurugodu, Ballari District",
            "phone": "Verify with hospital",
            "source": "Official Ballari District",
            "verified_date": "2026-08-14"
        },

        {
            "name": "CHC Moka",
            "type": "Government Community Health Centre",
            "specialties": (
                "General Medicine, General Care, "
                "Emergency Care, Maternal & Child Health"
            ),
            "address": "Moka, Ballari District",
            "phone": "Verify with hospital",
            "source": "Official Ballari District",
            "verified_date": "2026-08-14"
        },

        {
            "name": "CHC Tekkalakote",
            "type": "Government Community Health Centre",
            "specialties": (
                "General Medicine, General Care, "
                "Emergency Care, Maternal & Child Health"
            ),
            "address": "Tekkalakote, Ballari District",
            "phone": "Verify with hospital",
            "source": "Official Ballari District",
            "verified_date": "2026-08-14"
        },

        {
            "name": "CHC Toranagallu",
            "type": "Government Community Health Centre",
            "specialties": (
                "General Medicine, General Care, "
                "Emergency Care, Maternal & Child Health"
            ),
            "address": "Toranagallu, Ballari District",
            "phone": "Verify with hospital",
            "source": "Official Ballari District",
            "verified_date": "2026-08-14"
        }
    ]

    # ---------------------------------------------------------
    # INSERT RECORDS
    # ---------------------------------------------------------

    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    for hospital in hospitals:

        cursor.execute("""
            SELECT id
            FROM hospitals
            WHERE LOWER(name) = LOWER(?)
        """, (hospital["name"],))

        existing = cursor.fetchone()

        if existing:
            continue

        cursor.execute("""
            INSERT INTO hospitals
            (
                name,
                hospital_type,
                specialties,
                address,
                phone,
                source,
                verified_date
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            hospital["name"],
            hospital["type"],
            hospital["specialties"],
            hospital["address"],
            hospital["phone"],
            hospital["source"],
            hospital["verified_date"]
        ))

    connection.commit()
    connection.close()

    print("=" * 65)
    print("STEP 10B - BALLARI HEALTHCARE DATABASE")
    print("=" * 65)

    print(
        f"\nDatabase location:\n{DB_PATH}"
    )

    print(
        f"\nTotal hospital/healthcare records: "
        f"{count_hospitals()}"
    )

    print(
        "\nDatabase population completed successfully."
    )

    print(
        "\nNext step: connect this database to chatbot.py."
    )