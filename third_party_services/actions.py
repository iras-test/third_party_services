import requests
from django.conf import settings
from rest_framework import status
from rest_framework.response import Response
from third_party_services.serializers import (
    BrnDetailsSerializer,
    NinDetailsSerializer,
    ObrsBrnSerializer,
    TinDetailsSerializer,
    VehicleDetailsSerializer,
)


def validate_nin(self, request, **kwargs):
    """Validate the NIN by calling the external service."""
    serializer = NinDetailsSerializer(data=request.query_params)
    serializer.is_valid(raise_exception=True)
    return Response(serializer.details())


def validate_tin(self, request, **kwargs):
    """Validate the TIN by calling the external service."""
    serializer = TinDetailsSerializer(data=request.query_params)
    serializer.is_valid(raise_exception=True)
    return Response(serializer.details())

def validate_brn(self, request, **kwargs):
    """Validate the BRN by calling the external service."""
    serializer = BrnDetailsSerializer(data=request.query_params)
    serializer.is_valid(raise_exception=True)
    return Response(serializer.details())


def validate_obrs_brn(self, request, **kwargs):
    """Validate a BRN using the OBRS service."""
    serializer = ObrsBrnSerializer(data=request.query_params)
    serializer.is_valid(raise_exception=True)

    timeout = getattr(settings, "EXTERNAL_SERVICE_TIMEOUT", 30) or 30
    url = f"{settings.SERVICE_URL.rstrip('/')}/ura/services/validate-obrs-brn/"

    try:
        response = requests.get(
            url,
            params={"brn": serializer.validated_data["brn"]},
            timeout=timeout,
        )
    except requests.exceptions.Timeout:
        return Response(
            {
                "error": "OBRS_TIMEOUT",
                "message": "The OBRS validation service timed out.",
                "data": None,
                "status": status.HTTP_504_GATEWAY_TIMEOUT,
            },
            status=status.HTTP_504_GATEWAY_TIMEOUT,
        )
    except requests.exceptions.RequestException:
        return Response(
            {
                "error": "OBRS_UNAVAILABLE",
                "message": "The OBRS validation service is unavailable.",
                "data": None,
                "status": status.HTTP_502_BAD_GATEWAY,
            },
            status=status.HTTP_502_BAD_GATEWAY,
        )

    try:
        payload = response.json()
    except ValueError:
        error_data = {
            "upstreamStatus": response.status_code,
            "contentType": response.headers.get("Content-Type", ""),
        }
        if getattr(settings, "DEBUG", False):
            error_data["rawResponse"] = response.text

        return Response(
            {
                "error": "OBRS_INVALID_RESPONSE",
                "message": "The OBRS validation service returned invalid JSON.",
                "data": error_data,
                "status": status.HTTP_502_BAD_GATEWAY,
            },
            status=status.HTTP_502_BAD_GATEWAY,
        )

    if not response.ok:
        return Response(payload, status=response.status_code)

    company = payload.get("data") if isinstance(payload, dict) else None
    if not isinstance(company, dict):
        return Response(
            {
                "error": "OBRS_INVALID_RESPONSE",
                "message": "The OBRS validation service returned no company data.",
                "data": None,
                "status": status.HTTP_502_BAD_GATEWAY,
            },
            status=status.HTTP_502_BAD_GATEWAY,
        )

    return Response(
        {
            "entityName": company.get("entityName") or "",
            "incorporationDate": company.get("incorporationDate") or "",
            "isValid": True,
        },
        status=status.HTTP_200_OK,
    )


def validate_vehicle(self, request, **kwargs):
    """Validate the vehicle by calling the external service."""
    serializer = VehicleDetailsSerializer(data=request.query_params)
    serializer.is_valid(raise_exception=True)
    return Response(serializer.details())

def get_vehicle_details(number_plate):
    vehicle_serializer = VehicleDetailsSerializer(data={'number_plate': number_plate})
    vehicle_details = vehicle_serializer.details(unmasked=True)

    tin = vehicle_details.get('tin', None)
    email = vehicle_details.get('email', None)
    mobile_number = vehicle_details.get('mobile_number', None)
    owner_name = vehicle_details.get('tax_payer_name', "")

    make_year =  vehicle_details.get('make_year', "")
    model = vehicle_details.get('model', "")
    engine_number = vehicle_details.get('engine_number', "")
    chasis_number = vehicle_details.get('chasis_number', "")
    color = vehicle_details.get('color', "")
    is_individual = vehicle_details.get('is_individual', "")
    seat_capacity =  vehicle_details.get('seat_capacity', "")
    category_name =  vehicle_details.get('category_name', "")
    purpose =  vehicle_details.get('purpose', "")
    
    return owner_name, f"256{mobile_number}", email, tin, make_year , model, engine_number ,chasis_number ,color ,is_individual ,seat_capacity ,category_name, purpose


def get_vehicle_details_dict(number_plate):
    """Retrieve vehicle details and return them as a dictionary."""
    vehicle_serializer = VehicleDetailsSerializer(data={'number_plate': number_plate})
    vehicle_serializer.is_valid(raise_exception=True)
    vehicle_details = vehicle_serializer.details(unmasked=True)

    return {
        "owner_name": vehicle_details.get("tax_payer_name", ""),
        "mobile_number": f"256{vehicle_details.get('mobile_number', '')}",
        "email": vehicle_details.get("email", None),
        "tin": vehicle_details.get("tin", None),
        "make_year": vehicle_details.get("make_year", ""),
        "model": vehicle_details.get("model", ""),
        "engine_number": vehicle_details.get("engine_number", ""),
        "chasis_number": vehicle_details.get("chasis_number", ""),
        "color": vehicle_details.get("color", ""),
        "is_individual": vehicle_details.get("is_individual", ""),
        "seat_capacity": vehicle_details.get("seat_capacity", ""),
        "category_name": vehicle_details.get("category_name", ""),
        "purpose": vehicle_details.get("purpose", ""),
        "gross_weight": vehicle_details.get("grossWeight", ""),
        "net_weight": vehicle_details.get("netWeight", ""),
        "tonnage": vehicle_details.get("tonnage", "")
    }
