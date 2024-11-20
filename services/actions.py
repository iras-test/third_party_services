from rest_framework.response import Response
from services.serializers import NinDetailsSerializer


def validate_nin(self, request, **kwargs):
    serializer = NinDetailsSerializer(data=request.query_params)
    serializer.is_valid(raise_exception=True)
    return Response(serializer.details())