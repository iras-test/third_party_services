OBRS_SERVICE_DENIED_MESSAGE_TEMPLATES = {
    "dormant": "{company} is currently dormant.",
    "struck off": "{company} has been struck off.",
    "ceased": "{company} has been dissolved/ceased operations.",
    "de registered": "{company} is deregistered.",
    "in provisional liquidation": "{company} is under provisional liquidation.",
    "in liquidation": "{company} is undergoing liquidation.",
}

def normalize_registration_status(value):
    normalized = str(value or "").strip().lower()
    for separator in ("_", "-", "/"):
        normalized = normalized.replace(separator, " ")
    return " ".join(normalized.split())


def service_eligibility_error(company):
    registration_status = company.get("registrationStatus")
    normalized_status = normalize_registration_status(registration_status)
    denied_template = OBRS_SERVICE_DENIED_MESSAGE_TEMPLATES.get(normalized_status)

    if denied_template:
        entity_name = str(company.get("entityName") or "").strip()
        denied_message = denied_template.format(company=entity_name or "This company")
        return {
            "error": "OBRS_SERVICE_NOT_ALLOWED",
            "message": denied_message,
            "detail": denied_message,
            "data": {
                "registrationStatus": registration_status,
                "legal_name": "",
            },
            "status": 400,
        }, 400

    return None
