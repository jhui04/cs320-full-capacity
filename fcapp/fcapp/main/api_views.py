from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListAPIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.http import Http404

from .mongo_models import Device, Status
from .serializers import DeviceSerializer, StatusSerializer

class DeviceDetail(RetrieveUpdateDestroyAPIView):
	"""
	View information about a device.
	"""

	#queryset = Device.objects.all()
	def get_queryset(self):
		return Device.for_user(self.request.user.id)

	serializer_class = DeviceSerializer
	permission_classes = (IsAuthenticated,)


class StatusDetail(RetrieveUpdateDestroyAPIView):
	"""
	View information about a device.
	"""

	#queryset = Status.objects.all()
	def get_queryset(self):
		return Status.for_user(self.request.user.id)
	serializer_class = StatusSerializer


@api_view(['GET', 'PATCH'])
def status_activate(request, pk):
	if request.method == 'PATCH':
		s = Status.for_user(request.user.id).get(id=pk)
		s.active = True
		s.save()
		return Response({"response": "Success"})

	return Response({"response": "Send a HTTP PATCH request to this endpoint."}, status=405)


@api_view(['GET', 'PATCH'])
def status_deactivate(request, pk):
	if request.method == 'PATCH':
		s = Status.for_user(request.user.id).get(id=pk)
		s.active = False
		s.save()
		return Response({"response": "Success"})

	return Response({"response": "Send a HTTP PATCH request to this endpoint."}, status=405)
