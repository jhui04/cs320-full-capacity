from rest_framework_mongoengine import viewsets
from rest_framework.permissions import IsAuthenticated
from .serializers import DeviceSerializer, DeviceMinimalSerializer, DefaultStatusSerializer, StatusSerializer, TenantSerializer
from .mongo_models import Device, System, Tenant, Status, DefaultStatus

MAX_DEVICE_LIMIT = 20

class DeviceViewSet(viewsets.ModelViewSet):
    lookup_field = 'id'
    #serializer_class = DeviceMinimalSerializer
    serializer_class = DeviceSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = None

    def get_queryset(self):
        return Device.for_user(self.request.user.id).limit(MAX_DEVICE_LIMIT)


class AllDeviceViewSet(viewsets.ModelViewSet):
    lookup_field = 'id'
    serializer_class = DeviceMinimalSerializer

    def get_queryset(self):
        return Device.objects.all()


class TenantViewSet(viewsets.ModelViewSet):
    lookup_field = 'id'
    serializer_class = TenantSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = None

    def get_queryset(self):
        return Tenant.for_user(self.request.user.id)


class AllTenantViewSet(viewsets.ModelViewSet):
    lookup_field = 'id'
    serializer_class = TenantSerializer

    def get_queryset(self):
        return Tenant.objects.all()


class DefaultStatusViewSet(viewsets.ModelViewSet):
    lookup_field = 'id'
    serializer_class = DefaultStatusSerializer

    def get_queryset(self):
        return DefaultStatus.objects.all()


class StatusViewSet(viewsets.ModelViewSet):
    lookup_field = 'id'
    serializer_class = StatusSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user_id = self.request.user.id
        return Status.for_user(user_id)


class TriggeredStatusViewSet(viewsets.ModelViewSet):
    lookup_field = 'id'
    serializer_class = StatusSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user_id = self.request.user.id
        return Status.only_triggered_for(user_id)


class AllStatusViewSet(viewsets.ModelViewSet):
    lookup_field = 'id'
    serializer_class = StatusSerializer

    def get_queryset(self):
        return Status.objects.all()