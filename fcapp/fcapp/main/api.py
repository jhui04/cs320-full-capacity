from rest_framework import generics
from .serializers import DeviceMinimalSerializer

class ListDevices(generics.ListCreateAPIView):
	serializer_class = DeviceMinimalSerializer
