OBRS_SERVICE_DENIED_MESSAGES = {
    "dormant": (
        "This company is currently dormant."
    ),
    "struck off": (
        "This company has been struck off."
    ),
    "dissolved ceased": (
        "This company has been dissolved or ceased operations."
    ),
    "de registered": (
        "This company is deregistered ."
    ),
    "in provisional liquidation": (
        "This company is under provisional liquidation"
    ),
    "in liquidation": (
        "This company is undergoing liquidation."
    ),
}

def normalize_registration_status(value):
    normalized = str(value or "").strip().lower()
    for separator in ("_", "-", "/"):
        normalized = normalized.replace(separator, " ")
    return " ".join(normalized.split())


def service_eligibility_error(company):
    registration_status = company.get("registrationStatus")
    normalized_status = normalize_registration_status(registration_status)
    denied_message = OBRS_SERVICE_DENIED_MESSAGES.get(normalized_status)

    if denied_message:
        return {
            "error": "OBRS_SERVICE_NOT_ALLOWED",
            "message": denied_message,
            "detail": denied_message,
            "data": {"registrationStatus": registration_status},
            "status": 400,
        }, 400

    return None
