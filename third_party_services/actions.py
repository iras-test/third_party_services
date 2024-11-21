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