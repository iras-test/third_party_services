from rest_framework.response import Response
from third_party_services.serializers import BrnDetailsSerializer, NinDetailsSerializer, TinDetailsSerializer, VehicleDetailsSerializer


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
