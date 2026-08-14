"""
Step 9 - Symptom Guidance Layer

Educational guidance only.
This module does not diagnose diseases or prescribe medicines.
"""

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


def get_symptom_guidance(text):
    """
    Returns symptom guidance when a supported keyword is found.

    Returns:
        dictionary containing specialty and guidance,
        or None if no matching symptom is found.
    """

    normalized = text.lower().strip()

    for keyword, information in SYMPTOM_GUIDANCE.items():

        if keyword in normalized:

            return {
                "keyword": keyword,
                "specialty": information["specialty"],
                "guidance": information["guidance"]
            }

    return None


if __name__ == "__main__":

    print("Symptom Guidance Tester")
    print("Type 'exit' to stop.")

    while True:

        text = input("\nUser: ").strip()

        if text.lower() == "exit":
            break

        result = get_symptom_guidance(text)

        if result:

            print(
                f"\nSuggested specialty: "
                f"{result['specialty']}"
            )

            print(
                f"Guidance: "
                f"{result['guidance']}"
            )

        else:

            print(
                "\nNo symptom guidance found."
            )