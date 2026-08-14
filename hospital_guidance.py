"""
STEP 9 - BALLARI HEALTHCARE DIRECTORY

This module provides local healthcare-directory guidance.

IMPORTANT:
- This module does NOT diagnose diseases.
- It does NOT prescribe medicines.
- Hospital information can change.
- Users should verify contact details and services before visiting.
"""

HOSPITALS = [

    # =========================================================
    # GENERAL / MULTISPECIALITY
    # =========================================================

    {
        "name": "Vijayanagara Institute of Medical Sciences (VIMS)",
        "type": "Government / Teaching Hospital",
        "specialties": [
            "General Medicine",
            "Cardiology",
            "Dermatology",
            "Neurology",
            "Orthopaedics",
            "ENT",
            "Ophthalmology",
            "Paediatrics",
            "Psychiatry",
            "Surgery",
            "Obstetrics & Gynaecology",
            "Dental",
            "Emergency / Trauma"
        ],
        "address": "Cantonment, Ballari - 583104",
        "phone": "08392-235201"
    },

    {
        "name": "District Hospital Ballari",
        "type": "Government Hospital",
        "specialties": [
            "General Medicine",
            "Orthopaedics",
            "Dermatology",
            "ENT",
            "Ophthalmology",
            "Paediatrics",
            "Psychiatry",
            "Surgery",
            "Obstetrics & Gynaecology",
            "Dental",
            "Emergency / Trauma"
        ],
        "address": "Anantapur Road, Ballari",
        "phone": "08392-275255"
    },

    {
        "name": "BKS Hospital",
        "type": "Private / Multispeciality",
        "specialties": [
            "General Medicine",
            "Multispeciality",
            "Cardiology",
            "Diagnostics"
        ],
        "address": "Gandhi Nagar, Ballari - 583103",
        "phone": "08392-256500"
    },

    {
        "name": "Danamma Super Speciality Hospital",
        "type": "Private / Multispeciality",
        "specialties": [
            "General Medicine",
            "Multispeciality",
            "Surgery"
        ],
        "address": "Kolachalam Compound, Royal Circle, Ballari",
        "phone": "08392-270361"
    },

    {
        "name": "Sanjeevini Hospital",
        "type": "Private Hospital",
        "specialties": [
            "General Medicine",
            "Multispeciality"
        ],
        "address": "KHB Colony, Gandhi Nagar, Ballari",
        "phone": "09449054636"
    },

    {
        "name": "Dwaraka Hospital",
        "type": "Private Hospital",
        "specialties": [
            "General Medicine",
            "Multispeciality"
        ],
        "address": "Moka Road, KHB Colony, Gandhi Nagar, Ballari",
        "phone": "08392-255911"
    },

    {
        "name": "Shree Navodaya Multi Speciality Hospital",
        "type": "Private / Multispeciality",
        "specialties": [
            "General Medicine",
            "Multispeciality"
        ],
        "address": "Nallacheruvu, Cowl Bazaar, Ballari",
        "phone": "09480874519"
    },

    {
        "name": "Saroja Hanumaiah Speciality Hospital",
        "type": "Private / Speciality Hospital",
        "specialties": [
            "General Medicine",
            "Multispeciality"
        ],
        "address": "Siruguppa Road, Ashok Nagar, Ballari",
        "phone": "08872523222"
    },

    {
        "name": "Royal City Hospital",
        "type": "Private Hospital",
        "specialties": [
            "General Medicine",
            "General Care"
        ],
        "address": "Dr Rajkumar Road, Ballari",
        "phone": "08392-275199"
    },

    {
        "name": "Ballari Lifeline Hospital",
        "type": "Private Hospital",
        "specialties": [
            "General Medicine",
            "Multispeciality",
            "Emergency Care"
        ],
        "address": "Double Road, Ballari",
        "phone": "08088849991"
    },

    {
        "name": "VOISE Multi-Speciality Hospital and Research Center",
        "type": "Private / Multispeciality",
        "specialties": [
            "General Medicine",
            "Multispeciality"
        ],
        "address": "Moka Road, KHB Colony, Gandhi Nagar, Ballari",
        "phone": "08392-256444"
    },

    {
        "name": "Nava Karnataka Multi-Speciality Hospital",
        "type": "Private / Multispeciality",
        "specialties": [
            "General Medicine",
            "Multispeciality"
        ],
        "address": "Anantapur Road, Ballari",
        "phone": "08392-358571"
    },

    {
        "name": "Shruti Super Speciality Hospital",
        "type": "Private / Multispeciality",
        "specialties": [
            "General Medicine",
            "Multispeciality"
        ],
        "address": "Sudha Cross, Tilak Nagar, Cantonment, Ballari",
        "phone": "09480383671"
    },

    {
        "name": "R K Hospital",
        "type": "Private Hospital",
        "specialties": [
            "General Medicine",
            "General Care"
        ],
        "address": "Satyanarayana Pet Main Road, Ballari",
        "phone": "08392-273793"
    },

    {
        "name": "Bellary Nursing Home",
        "type": "Private Hospital",
        "specialties": [
            "General Medicine",
            "General Care"
        ],
        "address": "Cowl Bazaar, Ballari",
        "phone": "Verify with hospital"
    },

    {
        "name": "St. Mary's Hospital",
        "type": "Hospital",
        "specialties": [
            "General Care",
            "General Medicine"
        ],
        "address": "Cantonment, Ballari",
        "phone": "Verify with hospital"
    },


    # =========================================================
    # CARDIOLOGY
    # =========================================================

    {
        "name": "Ballari Hrudayalaya",
        "type": "Speciality Hospital",
        "specialties": [
            "Cardiology",
            "Heart Care"
        ],
        "address": "Gandhi Nagar, Ballari",
        "phone": "Verify with hospital"
    },

    {
        "name": "Anuradha Heart Care Center",
        "type": "Speciality Clinic",
        "specialties": [
            "Cardiology",
            "Heart Care"
        ],
        "address": "Housing Board Colony, Indira Nagar, Ballari",
        "phone": "09035839179"
    },

    {
        "name": "Adarsh Heart Care Centre",
        "type": "Speciality Clinic",
        "specialties": [
            "Cardiology",
            "Heart Care"
        ],
        "address": "Kolachalam Compound, Ballari",
        "phone": "Verify with hospital"
    },


    # =========================================================
    # DERMATOLOGY
    # =========================================================

    {
        "name": "Dr Dani's Skin, Cosmetic and Laser Clinic",
        "type": "Dermatology Clinic",
        "specialties": [
            "Dermatology",
            "Skin Care",
            "Cosmetology",
            "Laser Treatment"
        ],
        "address": "Infantry Road, Sanjay Gandhi Nagar, Ballari",
        "phone": "08277606300"
    },

    {
        "name": "Dr Divya Skin, Cosmoderm and Laser Clinic",
        "type": "Dermatology Clinic",
        "specialties": [
            "Dermatology",
            "Skin Care",
            "Cosmetology",
            "Laser Treatment"
        ],
        "address": "Gandhi Nagar, Ballari",
        "phone": "09845350510"
    },

    {
        "name": "Dr Afshan Skin & Hair Clinic",
        "type": "Dermatology Clinic",
        "specialties": [
            "Dermatology",
            "Skin Care",
            "Hair Care"
        ],
        "address": "Cowl Bazaar, Ballari",
        "phone": "07795734781"
    },


    # =========================================================
    # ORTHOPAEDICS
    # =========================================================

    {
        "name": "Raghuveer Orthopaedics, Trauma & Multispeciality Centre",
        "type": "Orthopaedic / Trauma Centre",
        "specialties": [
            "Orthopaedics",
            "Trauma",
            "Fracture Care",
            "Joint Care"
        ],
        "address": "Anantapur Road, Ballari",
        "phone": "07353061610"
    },

    {
        "name": "Dr Lakshmi Narayana Reddy G Orthopaedic Hospital",
        "type": "Orthopaedic Hospital",
        "specialties": [
            "Orthopaedics",
            "Knee Care",
            "Hip Care",
            "Fracture Care",
            "Sports Injury"
        ],
        "address": "Double Road, Ballari",
        "phone": "09110475300"
    },

    {
        "name": "VasuDev Hospital",
        "type": "Private / Multispeciality",
        "specialties": [
            "Orthopaedics",
            "ENT",
            "General Medicine",
            "Plastic Surgery",
            "Surgical Oncology",
            "Physiotherapy"
        ],
        "address": "Dr Rajkumar Road, Ballari",
        "phone": "09482097637"
    },


    # =========================================================
    # OPHTHALMOLOGY
    # =========================================================

    {
        "name": "Vijay Nagaraj Super Speciality Eye Hospital",
        "type": "Eye Hospital",
        "specialties": [
            "Ophthalmology",
            "Retina Care",
            "Eye Surgery"
        ],
        "address": "Sudha Cross, Cantonment, Ballari",
        "phone": "Verify with hospital"
    },

    {
        "name": "Dr Kulkarni Eye Hospital",
        "type": "Eye Hospital",
        "specialties": [
            "Ophthalmology",
            "Eye Care"
        ],
        "address": "Gandhi Nagar, Ballari",
        "phone": "Verify with hospital"
    },

    {
        "name": "Mehta Eye Care",
        "type": "Eye Clinic",
        "specialties": [
            "Ophthalmology",
            "Eye Care"
        ],
        "address": "Kalamma Street, Ballari",
        "phone": "Verify with hospital"
    },

    {
        "name": "Lakshmi Priya Eye & Retina Care Centre",
        "type": "Eye / Retina Centre",
        "specialties": [
            "Ophthalmology",
            "Retina Care"
        ],
        "address": "Siruguppa Road, Ashok Nagar, Ballari",
        "phone": "08277808070"
    },

    {
        "name": "Vaishnavi Nethralaya",
        "type": "Eye Hospital",
        "specialties": [
            "Ophthalmology",
            "Eye Care"
        ],
        "address": "Satyanarayana Pet, Ballari",
        "phone": "08088826727"
    },


    # =========================================================
    # PAEDIATRICS
    # =========================================================

    {
        "name": "Sri Srinivasa Mother and Child Hospital",
        "type": "Mother & Child Hospital",
        "specialties": [
            "Paediatrics",
            "Maternity",
            "Obstetrics & Gynaecology",
            "Mother & Child Care"
        ],
        "address": "KC Road, Cowl Bazaar, Ballari",
        "phone": "08392-273666"
    },

    {
        "name": "RR Children's Clinic",
        "type": "Paediatric Clinic",
        "specialties": [
            "Paediatrics",
            "Child Health"
        ],
        "address": "Vidya Nagar, Ballari",
        "phone": "08147341528"
    },

    {
        "name": "Prithvi Children's Hospital",
        "type": "Children's Hospital",
        "specialties": [
            "Paediatrics",
            "Child Health"
        ],
        "address": "Gandhi Nagar, Ballari",
        "phone": "Verify with hospital"
    },

    {
        "name": "Chiranjeevi Child Health Centre",
        "type": "Paediatric Centre",
        "specialties": [
            "Paediatrics",
            "Child Health",
            "Newborn Care"
        ],
        "address": "Kalamma Street, Ballari",
        "phone": "08392-275112"
    },


    # =========================================================
    # DENTAL
    # =========================================================

    {
        "name": "Bellary Superspeciality Dental Hospital",
        "type": "Dental Hospital",
        "specialties": [
            "Dental",
            "Oral Health"
        ],
        "address": "Kappagal Road, Ballari",
        "phone": "09845861354"
    },


    # =========================================================
    # WOMEN'S HEALTH / MATERNITY
    # =========================================================

    {
        "name": "Mother's Hospital",
        "type": "Maternity Hospital",
        "specialties": [
            "Obstetrics & Gynaecology",
            "Maternity",
            "Women's Health"
        ],
        "address": "Cowl Bazaar, Ballari",
        "phone": "Verify with hospital"
    },


    # =========================================================
    # AYURVEDIC CARE
    # =========================================================

    {
        "name": "RJR Herbal Hospital",
        "type": "Ayurvedic / Traditional Care",
        "specialties": [
            "Ayurvedic Care",
            "Traditional Medicine"
        ],
        "address": "Cowl Bazaar, Ballari",
        "phone": "07826977711"
    },

    {
        "name": "Bille Ayurvedic Health Care",
        "type": "Ayurvedic Clinic",
        "specialties": [
            "Ayurvedic Care"
        ],
        "address": "Satyanarayana Pet, Ballari",
        "phone": "Verify with clinic"
    }
]


# ============================================================
# SEARCH FUNCTION
# ============================================================

def search_hospitals(specialty=None, hospital_type=None):
    """
    Search Ballari healthcare facilities.

    Returns a list of matching hospitals.
    """

    results = []

    for hospital in HOSPITALS:

        specialty_match = True
        type_match = True

        # Specialty filter
        if specialty:

            specialty_lower = specialty.lower()

            specialty_match = any(
                specialty_lower in item.lower()
                for item in hospital["specialties"]
            )

        # Type filter
        if hospital_type:

            type_match = (
                hospital_type.lower()
                in hospital["type"].lower()
            )

        if specialty_match and type_match:
            results.append(hospital)

    return results


# ============================================================
# REMOVE DUPLICATES
# ============================================================

def remove_duplicates(hospitals):
    """
    Remove duplicate hospitals based on hospital name.
    """

    unique = []
    seen = set()

    for hospital in hospitals:

        key = hospital["name"].strip().lower()

        if key not in seen:

            seen.add(key)
            unique.append(hospital)

    return unique


# ============================================================
# DISPLAY HOSPITALS
# ============================================================

def show_hospitals(specialty=None, hospital_type=None):

    hospitals = search_hospitals(
        specialty,
        hospital_type
    )

    hospitals = remove_duplicates(hospitals)

    title = specialty if specialty else "General"

    print(
        f"\n{title} - Ballari Healthcare Guidance"
    )

    print("=" * 60)

    if not hospitals:

        print(
            "\nNo matching healthcare facilities "
            "were found in the current database."
        )

        print(
            "Please try another specialty or "
            "consult a general hospital."
        )

        return

    print(
        f"\nFound {len(hospitals)} "
        f"healthcare options:\n"
    )

    for index, hospital in enumerate(
        hospitals,
        start=1
    ):

        print(
            f"{index}. {hospital['name']}"
        )

        print(
            f"   Type: {hospital['type']}"
        )

        print(
            f"   Address: {hospital['address']}"
        )

        print(
            f"   Phone: {hospital['phone']}"
        )

        print(
            "   Services: "
            + ", ".join(
                hospital["specialties"]
            )
        )

        print("-" * 60)

    print(
        "\nIMPORTANT:"
    )

    print(
        "This is local healthcare-directory "
        "guidance, not medical advice."
    )

    print(
        "Hospital services, doctors, timings and "
        "contact information may change."
    )

    print(
        "Please verify details before visiting."
    )

    print(
        "For emergencies, go to the nearest "
        "emergency department."
    )


# ============================================================
# SHOW ALL HOSPITALS
# ============================================================

def show_all_hospitals():

    hospitals = remove_duplicates(
        HOSPITALS
    )

    print(
        "\nBALLARI HEALTHCARE DIRECTORY"
    )

    print("=" * 60)

    print(
        f"\nTotal facilities in database: "
        f"{len(hospitals)}"
    )

    for index, hospital in enumerate(
        hospitals,
        start=1
    ):

        print(
            f"\n{index}. {hospital['name']}"
        )

        print(
            f"   Type: {hospital['type']}"
        )

        print(
            f"   Address: {hospital['address']}"
        )

        print(
            f"   Phone: {hospital['phone']}"
        )

        print(
            "   Services: "
            + ", ".join(
                hospital["specialties"]
            )
        )


# ============================================================
# TEST MODE
# ============================================================

if __name__ == "__main__":

    print(
        "BALLARI HEALTHCARE DIRECTORY"
    )

    print(
        "Type a specialty to search."
    )

    print(
        "Type 'all' to display all facilities."
    )

    print(
        "Type 'exit' to stop."
    )

    while True:

        user_input = input(
            "\nSearch: "
        ).strip()

        if user_input.lower() == "exit":
            print("Goodbye!")
            break

        if user_input.lower() == "all":
            show_all_hospitals()
            continue

        show_hospitals(user_input)