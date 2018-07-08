from rest_framework_mongoengine import serializers
from rest_framework import serializers as rest_serializers
from .mongo_models import (
    System, Capacity, Performance, PerformanceBandwidth,
    PerformanceSummary, DisksByType, Disks, Authorized,
    Device, Tenant, StatusCriteria, DefaultStatus, Status)

from django.contrib.auth.models import User


class SystemSerializer(serializers.DocumentSerializer):
    class Meta:
        model = System
        fields = '__all__'


class CapacitySerializer(serializers.DocumentSerializer):
    class Meta:
        model = Capacity
        fields = '__all__'


class PerformanceSerializer(serializers.DocumentSerializer):
    class Meta:
        model = Performance
        fields = '__all__'


class PerformanceBandwidthSerializer(serializers.DocumentSerializer):
    class Meta:
        model = PerformanceBandwidth
        fields = '__all__'


class PerformanceSummarySerializer(serializers.DocumentSerializer):
    class Meta:
        model = PerformanceSummary
        fields = '__all__'


class DisksByTypeSerializer(serializers.DocumentSerializer):
    class Meta:
        model = DisksByType
        fields = '__all__'


class DisksSerializer(serializers.DocumentSerializer):
    class Meta:
        model = Disks
        fields = '__all__'


class AuthorizedSerializer(serializers.DocumentSerializer):
    class Meta:
        model = Authorized
        fields = '__all__'


class DeviceSerializer(serializers.DocumentSerializer):
    name = rest_serializers.SerializerMethodField()
    has_triggered = rest_serializers.SerializerMethodField()

    def get_name(self, obj):
        return obj.system.fullModel

    def get_has_triggered(self, obj):
        return obj.has_triggered()
    
    class Meta:
        model = Device
        fields = '__all__'


class DeviceMinimalSerializer(serializers.DocumentSerializer):
    """ UNUSED """
    url = rest_serializers.HyperlinkedIdentityField(view_name='device-detail', read_only=True)
    name = rest_serializers.SerializerMethodField()

    def get_name(self, obj):
        return obj.system.fullModel

    class Meta:
        model = Device
        fields = ('id', 'serialNumberInserv', 'authorized', 'url', 'name')


class UserSerializer(rest_serializers.Serializer):
    is_active = rest_serializers.BooleanField()
    first_name = rest_serializers.CharField()
    last_name = rest_serializers.CharField()
    email = rest_serializers.CharField()
    date_joined = rest_serializers.DateTimeField()
    last_login = rest_serializers.DateTimeField()
    username = rest_serializers.CharField()
    is_staff = rest_serializers.BooleanField()
    is_superuser = rest_serializers.BooleanField()
    id = rest_serializers.IntegerField()
    
    
    class Meta:
        model = User
        fields = ('is_active', 'first_name', 'last_name', 'email', 'date_joined',
                  'last_login', 'username', 'is_staff', 'is_superuser', 'id')

class TenantSerializer(serializers.DocumentSerializer):
    user = rest_serializers.SerializerMethodField()

    def get_user(self, obj):
        return UserSerializer(User.objects.get(id=obj.user_id)).data

    class Meta:
        model = Tenant
        fields = '__all__'

class StatusCriteriaSerializer(serializers.EmbeddedDocumentSerializer):
    operation_symbol = rest_serializers.SerializerMethodField()
    metric_pretty = rest_serializers.SerializerMethodField()
    metric_str = rest_serializers.SerializerMethodField()

    def get_operation_symbol(self, obj):
        return obj.operation_symbol

    def get_metric_pretty(self, obj):
        return obj.metric_pretty()

    def get_metric_str(self, obj):
        return ','.join(obj.metric)

    class Meta:
        model = StatusCriteria
        fields = '__all__'


class DefaultStatusSerializer(serializers.DocumentSerializer):
    criteria = StatusCriteriaSerializer(many=False)
    class Meta:
        model = DefaultStatus
        fields = '__all__'


class StatusSerializer(serializers.DocumentSerializer):
    url = rest_serializers.HyperlinkedIdentityField(view_name='status-detail', read_only=True)
    current_value = rest_serializers.SerializerMethodField()
    current_check = rest_serializers.SerializerMethodField()
    criteria = StatusCriteriaSerializer(many=False)

    device_name = rest_serializers.SerializerMethodField()

    def get_current_value(self, obj):
        return obj.current_value()

    def get_current_check(self, obj):
        return obj.current_check()

    def get_device_name(self, obj):
        dev = Device.objects.get(id=str(obj.device_id))
        return str(dev)

    class Meta:
        model = Status
        fields = '__all__'